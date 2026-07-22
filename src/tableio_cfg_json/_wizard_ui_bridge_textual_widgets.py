#! /usr/local/bin/python3
"""Widget builders and id helpers for the Textual wizard bridge.

The Textual bridge builds one input widget per form field and per menu,
and it maps widget ids back to field indexes and table positions. These
pure builders and id helpers are kept apart from the screen classes so
the main bridge module stays small; they hold no screen state and only
turn field descriptions into widgets and widget ids into indexes.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from datetime import date, datetime, time
from typing import Iterator, Optional, Sequence
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Button, Checkbox, Input, Select, SelectionList, \
    Static
from textual.widgets.selection_list import Selection
from tableio_cfg_json._wizard_ui_bridge_helpers import multi_count_error
from tableio_cfg_json._wizard_ui_bridge_parse import format_new_value, \
    parse_date, parse_datetime
from tableio_cfg_json.wizard_ui_bridge_arg_types import TableCell
from tableio_cfg_json.wizard_ui_bridge_form_defs import AskField, \
    AskTextField, AskIntField, AskPathField, AskYesNoField, AskChoiceField, \
    AskMultiChoiceField, AskFloatField, AskDateField, AskTimeField, \
    AskDateTimeField, AskDurationField


def _header_widgets(messages: list[str], question: str) -> Iterator[Static]:
    """Yield one static line per message and one for the question."""
    for line in messages:
        yield Static(line)
    yield Static(question)


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


def _choice_select(field: AskChoiceField, widget_id: str) -> Select[str]:
    """Return a drop-down for a choice field, blank when no default."""
    options = [(choice, choice) for choice in field.choices]
    if field.default is not None and field.default in field.choices:
        return Select(options, value=field.default, allow_blank=False,
                      id=widget_id)
    return Select(options, allow_blank=True, id=widget_id)


def _multi_selection(field: AskMultiChoiceField,
                     widget_id: str) -> SelectionList[int]:
    """Return a check-box list for a multi-choice field."""
    chosen = set(_preselected(field.choices, field.default))
    selections = [Selection(choice, index, index in chosen)
                  for index, choice in enumerate(field.choices)]
    return SelectionList[int](*selections, id=widget_id)


def _path_field_row(value: str, index: int) -> Horizontal:
    """Return a path input paired with a Browse button.

    The input keeps the plain field id so the form reads and validates
    it like any other field, while the button carries a browse class so
    the form can open the directory picker for this row.
    """
    return Horizontal(Input(value=value, id=f'field_{index}'),
                      Button('Browse', id=f'browse_{index}', classes='browse'),
                      id=f'pathrow_{index}')


def _pick_field_row(value: str, index: int) -> Horizontal:
    """Return a text input paired with a calendar Pick button.

    The input keeps the plain field id so the form reads and validates it
    like any other text field, while the button carries a pick class so
    the form can open the calendar for this row.
    """
    return Horizontal(Input(value=value, id=f'field_{index}'),
                      Button('Pick', id=f'pick_{index}', classes='pick'),
                      id=f'pickrow_{index}')


def _make_field_widget(field: AskField, index: int) -> Widget:
    """Return the input widget shown for one form field."""
    widget = _new_field_widget(field, index)
    return widget if widget is not None else _basic_field_widget(field, index)


def _new_field_widget(field: AskField, index: int) -> Optional[Widget]:
    """Return the widget for a typed field, or None for the basic kinds.

    A date or date-time field shows a text input with a Pick button that
    opens the calendar; a float, time or duration field shows a plain
    text input parsed on change. Each starts from its formatted default.
    """
    if isinstance(field, (AskDateField, AskDateTimeField)):
        text = '' if field.default is None else format_new_value(field.default)
        return _pick_field_row(text, index)
    if isinstance(field, (AskFloatField, AskTimeField, AskDurationField)):
        text = '' if field.default is None else format_new_value(field.default)
        return Input(value=text, id=f'field_{index}')
    return None


def _basic_field_widget(field: AskField, index: int) -> Widget:
    """Return the input widget for one of the original field kinds."""
    widget_id = f'field_{index}'
    if isinstance(field, AskTextField):
        value = '' if field.default is None else field.default
        return Input(value=value, password=field.sensitive, id=widget_id)
    if isinstance(field, AskIntField):
        value = '' if field.default is None else str(field.default)
        return Input(value=value, id=widget_id)
    if isinstance(field, AskPathField):
        default = field.path_options.default
        text = '' if default is None else str(default)
        return _path_field_row(text, index)
    if isinstance(field, AskYesNoField):
        return Checkbox(value=field.default, id=widget_id)
    if isinstance(field, AskChoiceField):
        return _choice_select(field, widget_id)
    assert isinstance(field, AskMultiChoiceField)
    return _multi_selection(field, widget_id)


def _id_index(widget_id: Optional[str], prefix: str) -> Optional[int]:
    """Return the integer index following prefix in a widget id."""
    if widget_id is None or not widget_id.startswith(prefix):
        return None
    return int(widget_id.split('_')[1])


def _field_index(widget_id: Optional[str]) -> Optional[int]:
    """Return the field index encoded in a field widget id."""
    return _id_index(widget_id, 'field_')


def _browse_index(widget_id: Optional[str]) -> Optional[int]:
    """Return the field index encoded in a browse button id."""
    return _id_index(widget_id, 'browse_')


def _pick_index(widget_id: Optional[str]) -> Optional[int]:
    """Return the field index encoded in a calendar Pick button id."""
    return _id_index(widget_id, 'pick_')


def _multi_error(count: int, field: AskMultiChoiceField) -> Optional[str]:
    """Return the multi-choice count error, or None when acceptable."""
    too_few = count < field.min_select
    too_many = field.max_select is not None and count > field.max_select
    if too_few or too_many:
        return multi_count_error(field.min_select, field.max_select)
    return None


def _date_of(value: Optional[date]) -> Optional[date]:
    """Return the date part of a date or datetime, or None."""
    if isinstance(value, datetime):
        return value.date()
    return value


def _calendar_setup(field: AskField, text: str
                    ) -> tuple[date, Optional[date], Optional[date]]:
    """Return the calendar seed date and its inclusive day bounds.

    A date-time field's bounds are its date parts, so the calendar offers
    the acceptable days and the field validates the exact date-time.
    """
    if isinstance(field, AskDateField):
        parsed = parse_date(text)
        minimum, maximum = field.min_value, field.max_value
    else:
        assert isinstance(field, AskDateTimeField)
        parsed = _date_of(parse_datetime(text))
        minimum = _date_of(field.min_value)
        maximum = _date_of(field.max_value)
    seed = parsed or _date_of(field.default) or date.today()
    return (seed, minimum, maximum)


def _combined_text(field: AskField, picked: date, current: str) -> str:
    """Return the input text for a picked date, keeping any typed time."""
    if isinstance(field, AskDateField):
        return picked.isoformat()
    assert isinstance(field, AskDateTimeField)
    existing = parse_datetime(current)
    clock = existing.time() if existing is not None else time()
    return datetime.combine(picked, clock).isoformat(sep=' ')
