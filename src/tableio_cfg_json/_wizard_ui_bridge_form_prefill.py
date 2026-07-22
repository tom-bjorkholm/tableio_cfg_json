#! /usr/local/bin/python3
"""Apply a partial validator's prefills to a Textual form's widgets.

The Textual form bridge asks the partial validator after every change and
then places the prefill values it returns into the matching field widgets,
exactly as if the user had typed them. This module holds that write-back,
kept apart from the large Textual bridge module.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Sequence
from textual.dom import DOMNode
from textual.widgets import Checkbox, Input, Select, SelectionList
from tableio_cfg_json.wizard_ui_bridge_form_defs import AskField, \
    AskTextField, AskIntField, AskPathField, AskYesNoField, AskChoiceField, \
    AskMultiChoiceField, PrefillValues, PrefillValueType
from tableio_cfg_json._wizard_ui_bridge_form import valid_prefills
from tableio_cfg_json._wizard_ui_bridge_parse import NEW_FIELD_TYPES, \
    format_new_value


def apply_prefills(form: DOMNode, fields: Sequence[AskField], changed: int,
                   prefill_values: PrefillValues) -> None:
    """Write each valid prefill into its row's widget in form.

    A disabled row is written too, so the value shows greyed and takes
    effect if the row is later enabled. Writing a value equal to the one
    already there is a no-op, so a stable validator does not loop.
    """
    for index, value in valid_prefills(fields, changed, prefill_values):
        _set_field(form, fields[index], index, value)


def _set_field(form: DOMNode, field: AskField, index: int,
               value: PrefillValueType) -> None:
    """Write a prefill value into one field's widget, by field type.

    Setting the widget value raises the framework's change event, so the
    answer, the disabled set and any own-field error refresh as if the
    user had typed it, exactly like the directory picker write-back.
    """
    widget_id = f'#field_{index}'
    if isinstance(field, NEW_FIELD_TYPES):
        form.query_one(widget_id, Input).value = format_new_value(value)
    elif isinstance(field, AskTextField):
        assert isinstance(value, str)
        form.query_one(widget_id, Input).value = value
    elif isinstance(field, AskIntField):
        assert isinstance(value, int)
        form.query_one(widget_id, Input).value = str(value)
    elif isinstance(field, AskPathField):
        assert isinstance(value, Path)
        form.query_one(widget_id, Input).value = str(value)
    elif isinstance(field, AskYesNoField):
        assert isinstance(value, bool)
        form.query_one(widget_id, Checkbox).value = value
    elif isinstance(field, AskChoiceField):
        assert isinstance(value, str)
        form.query_one(widget_id, Select).value = value
    else:
        assert isinstance(field, AskMultiChoiceField)
        assert isinstance(value, list)
        _set_multi(form, index, field, value)


def _set_multi(form: DOMNode, index: int, field: AskMultiChoiceField,
               members: Sequence[str]) -> None:
    """Select exactly the given members in a multi-choice widget."""
    selection = form.query_one(f'#field_{index}', SelectionList)
    wanted = {field.choices.index(member) for member in members}
    current = set(selection.selected)
    for value in wanted - current:
        selection.select(value)
    for value in current - wanted:
        selection.deselect(value)
