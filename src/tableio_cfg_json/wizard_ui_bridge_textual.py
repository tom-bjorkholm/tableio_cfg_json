#! /usr/local/bin/python3
"""Textual full-screen user interface bridge for the wizard.

This module provides the concrete Textual bridge used when the wizard
talks to a user through a real terminal. Each ask method runs a short
lived Textual application for one question and returns its result, which
keeps the one-question-at-a-time contract of WizardUiBridge while giving
the user a full-screen interface with selectable lists, check boxes and
editable tables.

Navigation keys exit a screen with no value and record which
WizardNavigation request to raise, so the bridge re-raises it after the
screen closes. Messages passed to show() and diagnostics written to
error_file() are buffered and rendered in the header of the next
screen, so nothing is written straight to the terminal where it would
corrupt the Textual display.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from __future__ import annotations
from datetime import date
from functools import partial
from io import StringIO
from pathlib import Path
from typing import ClassVar, Iterator, Optional, Sequence, TypeVar
from textual import on
from textual.app import App, ComposeResult
from textual.binding import BindingType
from textual.containers import Grid, VerticalScroll
from textual.widget import Widget
from textual.widgets import Button, Checkbox, Footer, Input, \
    OptionList, Select, SelectionList, Static
from textual.widgets.selection_list import Selection
from tableio_cfg_json.wizard_ui_bridge import WizardUiBridge
from tableio_cfg_json._wizard_ui_bridge_helpers import check_text_args, \
    int_text, multi_count_error, out_of_range, path_answer, range_error, \
    text_answer
from tableio_cfg_json._wizard_ui_bridge_form import initial_answer
from tableio_cfg_json._wizard_ui_bridge_form_prefill import apply_prefills
from tableio_cfg_json._wizard_ui_bridge_parse import NEW_FIELD_TYPES, \
    value_from_text, error_from_text, new_answer
from tableio_cfg_json._wizard_ui_bridge_calendar import _CalendarScreen
from tableio_cfg_json._wizard_ui_bridge_textual_widgets import \
    _header_widgets, _default_index, _preselected, _parse_cell_id, \
    _make_select, _make_field_widget, _field_index, _browse_index, \
    _pick_index, _multi_error, _calendar_setup, _combined_text
from tableio_cfg_json._wizard_ui_bridge_path import _PathPick, \
    _PickerScreen, _start_dir, _start_value
from tableio_cfg_json.wizard_ui_bridge_arg_types import PartialCheck, \
    WizardNavigation, WizardBack, WizardCancelLevel, \
    WizardAbort, PathAskOptions, TableColumn, TableCell
from tableio_cfg_json.wizard_ui_bridge_form_defs import AskField, AskFields, \
    ALL_ASK_FIELD_TYPES, AnswerField, AnswerFields, PartialFormValidator, \
    AskTextField, AskIntField, AskPathField, AskYesNoField, AskChoiceField, \
    AskMultiChoiceField, AskDateField, AskDateTimeField, AnswerTextField, \
    AnswerIntField, AnswerPathField, AnswerYesNoField, AnswerChoiceField, \
    AnswerMultiChoiceField
from tableio_cfg_json.wizard_ui_bridge_table import _new_row_template

_CAL_TOKEN = '?'

_T = TypeVar('_T')
_INT_ERROR = 'Please enter an integer.'
_CHOICE_REQUIRED = 'Please choose a value.'


class _NavApp(App[_T]):
    """Base screen translating navigation keys into wizard requests.

    A subclass lays out one question. ctrl+b records a request to go
    back and ctrl+o a request to cancel the current level; the mnemonic
    for ctrl+o is "out one level". Both exit the screen with no value so
    the bridge can raise the matching request. The built-in ctrl+q quit
    also exits with no value, which the bridge treats as an abort. These
    keys avoid the editing shortcuts that the text input widget binds,
    so they work on every screen.
    """

    BINDINGS: ClassVar[list[BindingType]] = [
        ('ctrl+b', 'nav_back', 'Back'),
        ('ctrl+o', 'nav_cancel', 'Out one level')]

    def __init__(self) -> None:
        """Initialize with no pending navigation request."""
        super().__init__()
        self.nav: Optional[type[WizardNavigation]] = None

    def action_nav_back(self) -> None:
        """Record a request to return to the previous question.

        The name avoids App.action_back, the built-in screen-history
        action, so this records a wizard back request instead.
        """
        self.nav = WizardBack
        self.exit()

    def action_nav_cancel(self) -> None:
        """Record a request to cancel the current level."""
        self.nav = WizardCancelLevel
        self.exit()


class _TextApp(_NavApp[str]):
    """Free-text screen returning the string the user typed."""

    def __init__(self, question: str, messages: list[str], value: str = '',
                 password: bool = False) -> None:
        """Store the prompt, buffered messages and input settings."""
        super().__init__()
        self._question = question
        self._messages = messages
        self._value = value
        self._password = password

    def compose(self) -> ComposeResult:
        """Lay out the header, the input field and the footer."""
        yield from _header_widgets(self._messages, self._question)
        yield Input(value=self._value, password=self._password)
        yield Footer()

    @on(Input.Submitted)
    def _entered(self, event: Input.Submitted) -> None:
        """Exit returning the entered text, empty when nothing typed."""
        self.exit(event.value)


class _PathApp(_PathPick, _NavApp[str]):
    """Path screen with a filesystem tree and editable path input."""

    BINDINGS: ClassVar[list[BindingType]] = [('ctrl+s', 'submit', 'Submit')]

    def __init__(self, question: str, messages: list[str],
                 options: PathAskOptions, value: Optional[str]) -> None:
        """Store prompt, path options and initial input state."""
        super().__init__()
        self._question = question
        self._messages = messages
        self._kind = options.kind
        self._start = _start_dir(options.default)
        self._value = _start_value(value, options.default)

    def compose(self) -> ComposeResult:
        """Lay out the header, directory tree, path input and footer."""
        yield from _header_widgets(self._messages, self._question)
        yield from self.pick_widgets(self._start, self._value)
        yield Button('Submit', id='submit')
        yield Footer()

    @on(Button.Pressed, '#submit')
    def _submit_clicked(self, _event: Button.Pressed) -> None:
        """Submit the current input when the button is pressed."""
        self.action_submit()

    def _confirm(self, value: str) -> None:
        """Exit returning the confirmed path input."""
        self.exit(value)


class _ChoiceApp(_NavApp[int]):
    """Single-choice screen returning the chosen 0-based index."""

    def __init__(self, question: str, choices: list[str],
                 default_index: Optional[int], messages: list[str]) -> None:
        """Store the prompt, choices and the index to highlight."""
        super().__init__()
        self._question = question
        self._choices = choices
        self._default_index = default_index
        self._messages = messages

    def compose(self) -> ComposeResult:
        """Lay out the header, the option list and the footer."""
        yield from _header_widgets(self._messages, self._question)
        yield OptionList(*self._choices)
        yield Footer()

    def on_mount(self) -> None:
        """Highlight the default option when one is given."""
        if self._default_index is not None:
            self.query_one(OptionList).highlighted = self._default_index

    @on(OptionList.OptionSelected)
    def _picked(self, event: OptionList.OptionSelected) -> None:
        """Exit returning the index of the selected option."""
        self.exit(event.option_index)


class _MultiApp(_NavApp[list[int]]):
    """Multi-choice screen returning the chosen 0-based indexes."""

    BINDINGS: ClassVar[list[BindingType]] = [('ctrl+s', 'submit', 'Submit')]
    _list: SelectionList[int]

    # pylint: disable-next=too-many-arguments,too-many-positional-arguments
    def __init__(self, question: str, choices: list[str],
                 preselected: list[int], min_select: int,
                 max_select: Optional[int], messages: list[str]) -> None:
        """Store the prompt, choices, preselection and count limits."""
        super().__init__()
        self._question = question
        self._choices = choices
        self._preselected = set(preselected)
        self._min_select = min_select
        self._max_select = max_select
        self._messages = messages

    def compose(self) -> ComposeResult:
        """Lay out the header, the check-box list, submit and footer."""
        yield from _header_widgets(self._messages, self._question)
        self._list = SelectionList[int](*self._selections())
        yield self._list
        yield Button('Submit', id='submit')
        yield Static('', id='multi_error')
        yield Footer()

    def _selections(self) -> list[Selection[int]]:
        """Return one selection per choice, preselected as requested."""
        return [Selection(choice, index, index in self._preselected)
                for index, choice in enumerate(self._choices)]

    @on(Button.Pressed)
    def _clicked(self, _event: Button.Pressed) -> None:
        """Treat a click on the submit button like the submit action."""
        self.action_submit()

    def action_submit(self) -> None:
        """Exit with the selection, or show why the count is wrong."""
        chosen = list(self._list.selected)
        if self._count_ok(len(chosen)):
            self.exit(chosen)
            return
        message = multi_count_error(self._min_select, self._max_select)
        self.query_one('#multi_error', Static).update(message)

    def _count_ok(self, count: int) -> bool:
        """Return whether count is within the allowed selection range."""
        if count < self._min_select:
            return False
        return self._max_select is None or count <= self._max_select


# pylint: disable-next=too-many-instance-attributes
class _TableApp(_NavApp[list[list[Optional[str]]]]):
    """Editable grid returning every cell the user left.

    Read-only columns show fixed text in the template rows. Editable
    cells are a text input, or a drop-down when the cell offers choices.
    An empty editable cell is reported as None when the cell is nullable
    and as an empty string for a free-text cell, while a drop-down is
    blank only when the cell is nullable.

    When min_rows and max_rows are both given the table has a variable
    number of rows: an Add row and a Remove row button grow the table up
    to max_rows and shrink it down to min_rows. Every cell in an added
    row is editable, even in a read-only column, and its descriptor comes
    from _new_row_template().
    """

    BINDINGS: ClassVar[list[BindingType]] = [('ctrl+s', 'submit', 'Submit')]
    CSS = '#grid { height: auto; }'

    # pylint: disable-next=too-many-arguments,too-many-positional-arguments
    def __init__(self, columns: Sequence[TableColumn],
                 cells: list[list[TableCell]], question: str,
                 messages: list[str], partial_check: Optional[PartialCheck],
                 min_rows: Optional[int] = None,
                 max_rows: Optional[int] = None) -> None:
        """Store the columns, starting rows, prompt, check and bounds."""
        super().__init__()
        self._columns = columns
        self._question = question
        self._messages = messages
        self._partial_check = partial_check
        self._variable = min_rows is not None and max_rows is not None
        self._min_rows = len(cells) if min_rows is None else min_rows
        self._max_rows = len(cells) if max_rows is None else max_rows
        self._new_row = _new_row_template(columns, cells)
        self._rows = [list(row) for row in cells]
        self._added = [False] * len(cells)
        self._table: list[list[Optional[str]]] = [
            [cell.value for cell in row] for row in cells]

    def compose(self) -> ComposeResult:
        """Lay out the header, the editable grid, the buttons and footer."""
        yield from _header_widgets(self._messages, self._question)
        with VerticalScroll(id='scroll'), Grid(id='grid'):
            yield from self._grid_cells()
        if self._variable:
            yield Button('Add row', id='add_row')
            yield Button('Remove row', id='remove_row')
        yield Button('Submit', id='submit')
        yield Static('', id='table_status')
        yield Footer()

    def on_mount(self) -> None:
        """Size the grid, keep the scroll unfocused, focus a cell."""
        self.query_one('#scroll').can_focus = False
        grid = self.query_one('#grid', Grid)
        grid.styles.grid_size_columns = len(self._columns)
        self._focus_first_cell()

    def _focus_first_cell(self) -> None:
        """Move focus to the first editable cell of the first row."""
        if not self._rows:
            return
        for col in range(len(self._columns)):
            if not self._is_readonly(0, col):
                self.query_one(f'#cell_0_{col}').focus()
                return

    def _grid_cells(self) -> Iterator[Widget]:
        """Yield the header labels and then the rows, top to bottom."""
        for column in self._columns:
            yield Static(column.header)
        for row in range(len(self._rows)):
            yield from self._row_widgets(row)

    def _row_widgets(self, row: int) -> Iterator[Widget]:
        """Yield the widgets of one data row, left to right."""
        for col in range(len(self._columns)):
            yield self._cell_widget(row, col)

    def _is_readonly(self, row: int, col: int) -> bool:
        """Return whether a cell shows fixed text instead of a widget.

        Cells in added rows are always editable, even in a column that is
        read-only in the template rows.
        """
        return not self._added[row] and self._columns[col].read_only

    def _cell_widget(self, row: int, col: int) -> Widget:
        """Return the widget shown for one cell of the grid."""
        cell = self._rows[row][col]
        widget_id = f'cell_{row}_{col}'
        if self._is_readonly(row, col):
            return Static(cell.value or '', id=widget_id)
        if cell.choices is None:
            return Input(value=cell.value or '', id=widget_id)
        return _make_select(cell, widget_id)

    @on(Input.Changed)
    def _on_input(self, event: Input.Changed) -> None:
        """Re-check the table after a text cell changes."""
        self._recheck(_parse_cell_id(event.input.id))

    @on(Select.Changed)
    def _on_select(self, event: Select.Changed) -> None:
        """Re-check the table after a drop-down cell changes."""
        self._recheck(_parse_cell_id(event.select.id))

    def _recheck(self, position: Optional[tuple[int, int]]) -> None:
        """Update the changed cell and show any partial-check message."""
        if position is None:
            return
        row, col = position
        self._table[row][col] = self._read_cell(row, col)
        if self._partial_check is None:
            return
        accepted, message = self._partial_check(self._table, position)
        self._set_status('' if accepted else message)

    def action_submit(self) -> None:
        """Exit returning every cell, including the read-only columns."""
        result = [[self._read_cell(row, col)
                   for col in range(len(self._columns))]
                  for row in range(len(self._rows))]
        self.exit(result)

    @on(Button.Pressed, '#submit')
    def _submit_clicked(self, _event: Button.Pressed) -> None:
        """Submit the table when the submit button is pressed."""
        self.action_submit()

    @on(Button.Pressed, '#add_row')
    def _add_clicked(self, _event: Button.Pressed) -> None:
        """Add a row when the add-row button is pressed."""
        self._add_row()

    @on(Button.Pressed, '#remove_row')
    def _remove_clicked(self, _event: Button.Pressed) -> None:
        """Remove the last row when the remove-row button is pressed."""
        self._remove_row()

    def _add_row(self) -> None:
        """Append one editable row, up to max_rows."""
        if len(self._rows) >= self._max_rows:
            self._set_status(f'At most {self._max_rows} rows allowed.')
            return
        row = len(self._rows)
        self._rows.append(list(self._new_row))
        self._added.append(True)
        self._table.append([cell.value for cell in self._new_row])
        self.query_one('#grid', Grid).mount(*self._row_widgets(row))
        self._set_status('')

    def _remove_row(self) -> None:
        """Remove the last row, down to min_rows."""
        if len(self._rows) <= self._min_rows:
            self._set_status(f'At least {self._min_rows} rows required.')
            return
        row = len(self._rows) - 1
        for col in range(len(self._columns)):
            self.query_one(f'#cell_{row}_{col}').remove()
        self._rows.pop()
        self._added.pop()
        self._table.pop()
        self._set_status('')

    def _set_status(self, message: str) -> None:
        """Show a status message below the table."""
        self.query_one('#table_status', Static).update(message)

    def _read_cell(self, row: int, col: int) -> Optional[str]:
        """Return the current value of one cell for the result table."""
        cell = self._rows[row][col]
        if self._is_readonly(row, col):
            return cell.value
        widget_id = f'#cell_{row}_{col}'
        if cell.choices is not None:
            select = self.query_one(widget_id, Select)
            return None if select.is_blank() else str(select.value)
        text = self.query_one(widget_id, Input).value
        if text == '':
            return None if cell.nullable else ''
        return text


# pylint: disable-next=too-many-instance-attributes
class _FormApp(_NavApp[list[AnswerField]]):
    """One screen showing every form field in a two-column grid.

    The left column of each row is a label with the field's short
    question and the right column an input widget chosen by the field
    type: a text input, a spin-free integer input, a path input, a
    check box, a drop-down or a check-box list. A partial validator, when
    given, runs after each change to show advisory feedback and to enable
    or disable rows. On submit each enabled field is validated, so the
    returned answers are complete and a choice with no default is always
    answered.
    """

    BINDINGS: ClassVar[list[BindingType]] = [('ctrl+s', 'submit', 'Submit')]
    CSS = '''
    #form_grid { height: auto; }
    #form_grid Horizontal { height: auto; width: 1fr; }
    #form_grid Horizontal Input { width: 1fr; }
    #form_grid Horizontal Button { width: auto; margin-left: 1; }
    /* A definite max-height lets the auto-height grid size this row;
       the inherited 100% is parent-relative and collapses it to a
       sliver. A longer list scrolls inside these rows. */
    #form_grid SelectionList { max-height: 10; }
    '''

    def __init__(self, question: str, fields: list[AskField],
                 messages: list[str],
                 validator: Optional[PartialFormValidator]) -> None:
        """Store the prompt, fields, buffered messages and validator."""
        super().__init__()
        self._question = question
        self._fields = fields
        self._messages = messages
        self._validator = validator
        self._answers = [initial_answer(field) for field in fields]
        self._disabled: set[int] = set()
        self._last_changed = 0
        self._form_ready = False

    def compose(self) -> ComposeResult:
        """Lay out the header, the field grid, submit and footer."""
        yield from _header_widgets(self._messages, self._question)
        with VerticalScroll(id='form_scroll'), Grid(id='form_grid'):
            yield from self._field_widgets()
        yield Button('Submit', id='submit')
        yield Static('', id='form_status')
        yield Footer()

    def _field_widgets(self) -> Iterator[Widget]:
        """Yield a label and an input widget for each field."""
        for index, field in enumerate(self._fields):
            label = Static(field.short_question, id=f'label_{index}')
            widget = _make_field_widget(field, index)
            if field.help_text is not None:
                label.tooltip = field.help_text
                widget.tooltip = field.help_text
            yield label
            yield widget

    def on_mount(self) -> None:
        """Size the grid, keep the scroll unfocused, focus the first field."""
        self.query_one('#form_scroll').can_focus = False
        self.query_one('#form_grid', Grid).styles.grid_size_columns = 2
        if self._fields:
            self.query_one('#field_0').focus()
        self._form_ready = True

    @on(Input.Changed)
    def _input_changed(self, event: Input.Changed) -> None:
        """React to a text, integer or path field change."""
        self._changed(event.input.id)

    @on(Select.Changed)
    def _select_changed(self, event: Select.Changed) -> None:
        """React to a choice drop-down change."""
        self._changed(event.select.id)

    @on(Checkbox.Changed)
    def _checkbox_changed(self, event: Checkbox.Changed) -> None:
        """React to a yes/no check-box change."""
        self._changed(event.checkbox.id)

    @on(SelectionList.SelectedChanged)
    def _multi_changed(self, event: SelectionList.SelectedChanged[int]
                       ) -> None:
        """React to a multi-choice selection change."""
        self._changed(event.control.id)

    def _changed(self, widget_id: Optional[str]) -> None:
        """Update the changed answer and refresh the shown feedback."""
        if not self._form_ready:
            return
        index = _field_index(widget_id)
        if index is None:
            return
        if self._maybe_open_calendar(index):
            return
        self._last_changed = index
        self._answers[index] = self._read_field(index)
        validator_message = self._apply_validator(index)
        self._set_status(self._live_message(index, validator_message))

    def _maybe_open_calendar(self, index: int) -> bool:
        """Open the calendar when a date field holds the pick token.

        Typing the '?' token into a date or date-time input is an
        alternative to pressing the Pick button. The token is left in the
        input until the calendar closes, when it is replaced by the picked
        date or cleared on cancel.
        """
        field = self._fields[index]
        if not isinstance(field, (AskDateField, AskDateTimeField)):
            return False
        if self.query_one(f'#field_{index}', Input).value != _CAL_TOKEN:
            return False
        self._open_calendar(index)
        return True

    def _apply_validator(self, index: int) -> str:
        """Apply the validator's disabled rows and prefills, return message."""
        if self._validator is None:
            return ''
        result = self._validator(self._answers, index)
        self._apply_disabled(result.disable_row_idxs)
        apply_prefills(self, self._fields, index, result.prefill_values)
        return '' if result.is_valid else result.message

    def _live_message(self, index: int, validator_message: str) -> str:
        """Return the changed field's own error, else the validator's.

        A field disabled by the validator is skipped, as on submit, so an
        irrelevant field never blocks the user with its own error. This
        gives a path, integer, choice or multi-choice field the same
        immediate feedback while editing that the console bridge gives by
        re-asking, instead of waiting for submit.
        """
        if index in self._disabled:
            return validator_message
        error = self._field_error(index, self._fields[index])
        return validator_message if error is None else error

    def _apply_disabled(self, disable_row_idxs: tuple[int, ...]) -> None:
        """Enable or disable each row to match the validator result."""
        self._disabled = set(disable_row_idxs)
        for index in range(len(self._fields)):
            off = index in self._disabled
            self.query_one(f'#field_{index}').disabled = off
            self.query_one(f'#label_{index}').disabled = off
            for button in self.query(f'#browse_{index}'):
                button.disabled = off
            for button in self.query(f'#pick_{index}'):
                button.disabled = off

    @on(Button.Pressed, '#submit')
    def _submit_clicked(self, _event: Button.Pressed) -> None:
        """Submit the form when the submit button is pressed."""
        self.action_submit()

    @on(Button.Pressed, '.browse')
    def _browse_clicked(self, event: Button.Pressed) -> None:
        """Open the directory picker for the clicked path field."""
        index = _browse_index(event.button.id)
        if index is not None:
            self._open_picker(index)

    @on(Button.Pressed, '.pick')
    def _pick_clicked(self, event: Button.Pressed) -> None:
        """Open the calendar for the clicked date field."""
        index = _pick_index(event.button.id)
        if index is not None:
            self._open_calendar(index)

    def _open_picker(self, index: int) -> None:
        """Push the picker seeded with the field's current text."""
        field = self._fields[index]
        assert isinstance(field, AskPathField)
        text = self.query_one(f'#field_{index}', Input).value
        self.push_screen(_PickerScreen(field.path_options, text),
                         partial(self._path_picked, index))

    def _open_calendar(self, index: int) -> None:
        """Push the calendar seeded from the date field's current text."""
        field = self._fields[index]
        assert isinstance(field, (AskDateField, AskDateTimeField))
        text = self.query_one(f'#field_{index}', Input).value
        seed, minimum, maximum = _calendar_setup(field, text)
        self.push_screen(_CalendarScreen(seed, minimum, maximum),
                         partial(self._date_picked, index))

    def _path_picked(self, index: int, result: Optional[str]) -> None:
        """Fill the path input with the picked path, if any.

        Setting the input value raises Input.Changed, so the answer and
        the partial validator update as if the user had typed the path.
        """
        if result is not None:
            self.query_one(f'#field_{index}', Input).value = result

    def _date_picked(self, index: int, result: Optional[date]) -> None:
        """Fill the date input with the picked date, if any.

        A cancelled calendar clears a lingering pick token; a picked date
        replaces the input, keeping any time part of a date-time field.
        Setting the value raises Input.Changed, so the answer refreshes.
        """
        field = self._fields[index]
        assert isinstance(field, (AskDateField, AskDateTimeField))
        widget = self.query_one(f'#field_{index}', Input)
        if result is None:
            if widget.value == _CAL_TOKEN:
                widget.value = ''
            return
        widget.value = _combined_text(field, result, widget.value)

    def action_submit(self) -> None:
        """Validate every enabled field and exit with the answers."""
        for index in range(len(self._fields)):
            self._answers[index] = self._read_field(index)
        error = self._first_error()
        if error is not None:
            self._set_status(error)
            return
        if not self._validator_accepts():
            return
        self.exit(list(self._answers))

    def _validator_accepts(self) -> bool:
        """Return whether the partial validator accepts the whole form."""
        if self._validator is None:
            return True
        result = self._validator(self._answers, self._last_changed)
        self._apply_disabled(result.disable_row_idxs)
        if not result.is_valid:
            self._set_status(result.message)
        return result.is_valid

    def _first_error(self) -> Optional[str]:
        """Return the first enabled field's validation error, or None."""
        for index, field in enumerate(self._fields):
            if index in self._disabled:
                continue
            error = self._field_error(index, field)
            if error is not None:
                return error
        return None

    def _set_status(self, message: str) -> None:
        """Show a status message below the form."""
        self.query_one('#form_status', Static).update(message)

    def _read_field(self, index: int) -> AnswerField:
        """Return the current answer of one field read from its widget."""
        field = self._fields[index]
        answer = self._read_new_field(index, field)
        return answer if answer is not None \
            else self._read_basic_field(index, field)

    def _read_new_field(self, index: int,
                        field: AskField) -> Optional[AnswerField]:
        """Return a typed field's answer from its text input, else None."""
        if not isinstance(field, NEW_FIELD_TYPES):
            return None
        text = self.query_one(f'#field_{index}', Input).value
        return new_answer(field, value_from_text(field, text))

    def _read_basic_field(self, index: int, field: AskField) -> AnswerField:
        """Return one original field kind's answer read from its widget."""
        widget_id = f'#field_{index}'
        if isinstance(field, AskTextField):
            text = self.query_one(widget_id, Input).value
            answer = text_answer(text, field.nullable, field.default)
            return AnswerTextField(field, answer)
        if isinstance(field, AskIntField):
            return AnswerIntField(field, self._int_value(widget_id, field))
        if isinstance(field, AskPathField):
            text = self.query_one(widget_id, Input).value
            _, path, _ = path_answer(text, field.path_options)
            return AnswerPathField(field, path)
        if isinstance(field, AskYesNoField):
            checked = self.query_one(widget_id, Checkbox).value
            return AnswerYesNoField(field, bool(checked))
        if isinstance(field, AskChoiceField):
            select = self.query_one(widget_id, Select)
            value = None if select.is_blank() else str(select.value)
            return AnswerChoiceField(field, value)
        assert isinstance(field, AskMultiChoiceField)
        selection = self.query_one(widget_id, SelectionList)
        chosen = sorted(selection.selected)
        values = [field.choices[i] for i in chosen]
        return AnswerMultiChoiceField(field, values)

    def _int_value(self, widget_id: str, field: AskIntField) -> Optional[int]:
        """Return the integer value of a field, or None when unparsed."""
        text = self.query_one(widget_id, Input).value
        if text == '':
            return field.default
        return int_text(text)

    def _field_error(self, index: int, field: AskField) -> Optional[str]:
        """Return one field's own validation error, or None when valid."""
        widget_id = f'#field_{index}'
        if isinstance(field, NEW_FIELD_TYPES):
            text = self.query_one(widget_id, Input).value
            return error_from_text(field, text)
        if isinstance(field, AskIntField):
            return self._int_error(widget_id, field)
        if isinstance(field, AskPathField):
            text = self.query_one(widget_id, Input).value
            done, _, reason = path_answer(text, field.path_options)
            return None if done else reason
        if isinstance(field, AskChoiceField):
            blank = self.query_one(widget_id, Select).is_blank()
            return _CHOICE_REQUIRED if blank else None
        if isinstance(field, AskMultiChoiceField):
            count = len(self.query_one(widget_id, SelectionList).selected)
            return _multi_error(count, field)
        return None

    def _int_error(self, widget_id: str, field: AskIntField) -> Optional[str]:
        """Return the integer field's validation error, or None."""
        text = self.query_one(widget_id, Input).value
        if text == '':
            if field.nullable or field.default is not None:
                return None
            return _INT_ERROR
        value = int_text(text)
        if value is None:
            return _INT_ERROR
        if out_of_range(value, field.min_value, field.max_value):
            return range_error(field.min_value, field.max_value)
        return None


class WizardUiBridgeTextual(WizardUiBridge):
    """Bridge between the wizard and a Textual terminal interface.

    Each ask method runs a short-lived Textual application for one
    question and returns its result. Validation diagnostics written to
    error_file() and messages passed to show() are buffered and rendered
    in the header of the next question's screen, so nothing reaches the
    terminal directly where it would corrupt the Textual display.

    This bridge draws on the controlling terminal itself, so it takes no
    streams. Use make_text_ui_bridge() to obtain this bridge when a
    terminal is available and a console bridge otherwise.
    """

    def __init__(self) -> None:
        """Start with an empty diagnostics buffer and message list."""
        self._error_buffer = StringIO()
        self._pending: list[str] = []

    # pylint: disable-next=too-many-arguments
    def ask_text(self, question: str, re_ask_reason: Optional[str] = None,
                 nullable: bool = False, *, default: Optional[str] = None,
                 sensitive: bool = False) -> Optional[str]:
        """Ask for free text; see WizardUiBridge.ask_text."""
        check_text_args(default, sensitive)
        messages = self._collect(re_ask_reason)
        value = '' if default is None else default
        text = self._run(_TextApp(question, messages, value, sensitive))
        return text_answer(text, nullable, default)

    def ask_path(self, question: str, re_ask_reason: Optional[str] = None, *,
                 options: Optional[PathAskOptions] = None) -> Optional[Path]:
        """Ask for a path with a directory tree and editable path input."""
        path_options = PathAskOptions() if options is None else options
        reason = re_ask_reason
        value: Optional[str] = None
        while True:
            messages = self._collect(reason)
            text = self._run(_PathApp(question, messages, path_options, value))
            done, path, reason = path_answer(text, path_options)
            if done:
                return path
            value = text

    def ask_yes_no(self, question: str, default: bool,
                   re_ask_reason: Optional[str] = None) -> bool:
        """Ask a yes/no question; see WizardUiBridge.ask_yes_no."""
        messages = self._collect(re_ask_reason)
        default_index = 0 if default else 1
        chosen = self._run(_ChoiceApp(question, ['yes', 'no'], default_index,
                                      messages))
        return chosen == 0

    def ask_choice(self, question: str, *, choices: Sequence[str],
                   default: Optional[str] = None,
                   re_ask_reason: Optional[str] = None) -> str:
        """Ask the user to pick one choice; see ask_choice."""
        messages = self._collect(re_ask_reason)
        index = self._run(_ChoiceApp(question, list(choices),
                                     _default_index(choices, default),
                                     messages))
        return choices[index]

    # pylint: disable-next=too-many-arguments
    def ask_multi(self, question: str, *, choices: Sequence[str],
                  default: Optional[Sequence[str]] = None, min_select: int = 0,
                  max_select: Optional[int] = None,
                  re_ask_reason: Optional[str] = None) -> list[str]:
        """Ask the user to pick several choices; see ask_multi."""
        messages = self._collect(re_ask_reason)
        chosen = self._run(_MultiApp(question, list(choices),
                                     _preselected(choices, default),
                                     min_select, max_select, messages))
        return [choices[index] for index in sorted(chosen)]

    # pylint: disable-next=too-many-arguments
    def ask_table(self, columns: Sequence[TableColumn],
                  cells: list[list[TableCell]], question: str, *,
                  re_ask_reason: Optional[str] = None,
                  partial_check: Optional[PartialCheck] = None,
                  min_rows: Optional[int] = None,
                  max_rows: Optional[int] = None) -> list[list[Optional[str]]]:
        """Ask the user to fill a table; see WizardUiBridge.ask_table."""
        messages = self._collect(re_ask_reason)
        return self._run(_TableApp(columns, cells, question, messages,
                                   partial_check, min_rows, max_rows))

    def ask_form(self, long_question: str, ask_fields: AskFields, *,
                 re_ask_reason: Optional[str] = None,
                 partial_validator: Optional[PartialFormValidator] = None) \
            -> AnswerFields:
        """Ask the user to fill a whole form on one screen; see ask_form."""
        messages = self._collect(re_ask_reason)
        return self._run(_FormApp(long_question, list(ask_fields), messages,
                                  partial_validator))

    def supports_form_field(self, field: AskField) -> bool:
        """Show every form field type; see WizardUiBridge.

        The Textual form has a widget for each field type, including a
        text input for float, time and duration fields and a text input
        with a calendar Pick button for date and date-time fields.
        """
        return isinstance(field, ALL_ASK_FIELD_TYPES)

    def _run(self, app: _NavApp[_T]) -> _T:
        """Run one screen and translate its outcome.

        A recorded navigation request is re-raised. A screen that ends
        with no value, such as the built-in quit, is treated as an
        abort.
        """
        result = self._launch(app)
        if app.nav is not None:
            raise app.nav()
        if result is None:
            raise WizardAbort()
        return result

    def _launch(self, app: _NavApp[_T]) -> Optional[_T]:
        """Run the app and return its result.

        This is the only place that drives the terminal, so tests
        override it to exercise the bridge without a real terminal.
        """
        return app.run()  # pragma: no cover

    def _collect(self, re_ask_reason: Optional[str]) -> list[str]:
        """Drain buffered messages and append any re-ask reason."""
        lines = self._drain_messages()
        if re_ask_reason is not None:
            lines.append(re_ask_reason)
        return lines

    def _drain_messages(self) -> list[str]:
        """Return and clear buffered show() and diagnostic lines."""
        text = self._error_buffer.getvalue()
        self._error_buffer.seek(0)
        self._error_buffer.truncate(0)
        diagnostics = [line for line in text.splitlines() if line]
        lines = self._pending + diagnostics
        self._pending = []
        return lines

    def error_file(self) -> StringIO:
        """Return the in-memory stream shown on the next screen."""
        return self._error_buffer

    def show(self, message: str) -> None:
        """Buffer a message for the next question's screen.

        A message shown when no further question follows is not
        displayed, because only a Textual screen renders it.
        """
        self._pending.append(message)
