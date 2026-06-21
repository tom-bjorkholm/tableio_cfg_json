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
from io import StringIO
from typing import ClassVar, Iterator, Optional, Sequence, TypeVar
from textual import on
from textual.app import App, ComposeResult
from textual.binding import BindingType
from textual.containers import Grid, VerticalScroll
from textual.widget import Widget
from textual.widgets import Button, Footer, Input, OptionList, Select, \
    SelectionList, Static
from textual.widgets.selection_list import Selection
from tableio_cfg_json.wizard_ui_bridge import PartialCheck, TableCell, \
    TableColumn, WizardAbort, WizardBack, WizardCancelLevel, \
    WizardNavigation, WizardUiBridge, _multi_count_error

_T = TypeVar('_T')
_V = TypeVar('_V')


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


def _header_widgets(messages: list[str], question: str) -> Iterator[Static]:
    """Yield one static line per message and one for the question."""
    for line in messages:
        yield Static(line)
    yield Static(question)


class _TextApp(_NavApp[str]):
    """Free-text screen returning the string the user typed."""

    def __init__(self, question: str, messages: list[str]) -> None:
        """Store the prompt and any buffered messages."""
        super().__init__()
        self._question = question
        self._messages = messages

    def compose(self) -> ComposeResult:
        """Lay out the header, the input field and the footer."""
        yield from _header_widgets(self._messages, self._question)
        yield Input()
        yield Footer()

    @on(Input.Submitted)
    def _entered(self, event: Input.Submitted) -> None:
        """Exit returning the entered text, empty when nothing typed."""
        self.exit(event.value)


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
        message = _multi_count_error(self._min_select, self._max_select)
        self.query_one('#multi_error', Static).update(message)

    def _count_ok(self, count: int) -> bool:
        """Return whether count is within the allowed selection range."""
        if count < self._min_select:
            return False
        return self._max_select is None or count <= self._max_select


def _default_index(choices: Sequence[str],
                   default: Optional[str]) -> Optional[int]:
    """Return the index of default within choices, or None."""
    if default is not None and default in choices:
        return list(choices).index(default)
    return None


def _preselected(choices: Sequence[str],
                 default: Optional[Sequence[str]]) -> list[int]:
    """Return the indexes of the default values within choices."""
    if default is None:
        return []
    wanted = set(default)
    return [index for index, choice in enumerate(choices)
            if choice in wanted]


def _parse_cell_id(widget_id: Optional[str]) -> Optional[tuple[int, int]]:
    """Return the (row, column) encoded in an editable cell id."""
    if widget_id is None or not widget_id.startswith('cell_'):
        return None
    _, row, col = widget_id.split('_')
    return (int(row), int(col))


def _make_select(cell: TableCell, widget_id: str) -> Select[str]:
    """Return a drop-down for one cell, blank only when nullable."""
    assert cell.choices is not None
    options = [(choice, choice) for choice in cell.choices]
    value = cell.value
    if value is not None and value in cell.choices:
        return Select(options, value=value, allow_blank=cell.nullable,
                      id=widget_id)
    if cell.nullable:
        return Select(options, allow_blank=True, id=widget_id)
    return Select(options, value=cell.choices[0], allow_blank=False,
                  id=widget_id)


def _uniform(values: list[_V], default: _V) -> _V:
    """Return the value shared by every entry, or the default."""
    if values and all(value == values[0] for value in values):
        return values[0]
    return default


def _new_row_template(columns: Sequence[TableColumn],
                      cells: list[list[TableCell]]) -> list[TableCell]:
    """Return the cell descriptors used for rows added to the table.

    For each column, a member of the new cell keeps the value shared by
    every template cell in that column, or falls back to a default when
    they differ: an empty string for value, None for choices and False
    for nullable.
    """
    new_row: list[TableCell] = []
    for col in range(len(columns)):
        column = [row[col] for row in cells]
        new_row.append(TableCell(
            value=_uniform([cell.value for cell in column], ''),
            choices=_uniform([cell.choices for cell in column], None),
            nullable=_uniform([cell.nullable for cell in column], False)))
    return new_row


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

    def ask(self, question: str, re_ask_reason: Optional[str] = None,
            choices: Optional[Sequence[str]] = None) -> str | int:
        """Ask one question; see WizardUiBridge.ask."""
        messages = self._collect(re_ask_reason)
        if choices is None:
            return self._run(_TextApp(question, messages))
        return self._run(_ChoiceApp(question, list(choices), None, messages))

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
