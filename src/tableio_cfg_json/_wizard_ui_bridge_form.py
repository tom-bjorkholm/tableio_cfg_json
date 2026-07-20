#! /usr/local/bin/python3
"""Helpers shared by the WizardUiBridge form question."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Sequence
from dataclasses import replace
from pathlib import Path
from typing import Iterator, NoReturn, Optional
from tableio_cfg_json.wizard_ui_bridge_form_defs import AskField, \
    AnswerField, AskTextField, AskIntField, AskPathField, AskYesNoField, \
    AskChoiceField, AskMultiChoiceField, AnswerTextField, AnswerIntField, \
    AnswerPathField, AnswerYesNoField, AnswerChoiceField, \
    AnswerMultiChoiceField, PrefillValueType, PrefillValues


def initial_answer(field: AskField) -> AnswerField:
    """Return the starting answer for a field before the user edits it.

    The value is the field's default, or the empty or not-yet-answered
    state when the field has no default. A choice field with no default
    starts as None, which tells a partial validator the choice is not
    answered yet; a bridge must not leave that None in a submitted form.
    """
    if isinstance(field, AskTextField):
        return AnswerTextField(field, field.default)
    if isinstance(field, AskIntField):
        return AnswerIntField(field, field.default)
    if isinstance(field, AskPathField):
        return AnswerPathField(field, field.path_options.default)
    if isinstance(field, AskYesNoField):
        return AnswerYesNoField(field, field.default)
    if isinstance(field, AskChoiceField):
        return AnswerChoiceField(field, field.default)
    assert isinstance(field, AskMultiChoiceField)
    values = [] if field.default is None else list(field.default)
    return AnswerMultiChoiceField(field, values)


def valid_prefills(fields: Sequence[AskField], changed: int,
                   prefill_values: PrefillValues
                   ) -> Iterator[tuple[int, PrefillValueType]]:
    """Yield the prefill requests a bridge should apply, validated.

    Each yielded (index, value) pair is ready to place into the row's
    input. A prefill aimed at the changed row is skipped, so writing back
    never fights the user's current edit. A row index outside the form
    raises IndexError and a value whose Python type does not match the
    field raises TypeError, since both are validator bugs. A choice value
    not among the field's choices, any prefill of a sensitive text field,
    and a multi-choice value with no valid member, are dropped instead, so
    a portable validator stays safe. A multi-choice value keeps only its
    members that are valid choices.
    """
    for index, value in prefill_values:
        _check_row(fields, index)
        if index == changed:
            continue
        usable = _prefill_value(fields[index], value, index)
        if usable is not None:
            yield index, usable


def _check_row(fields: Sequence[AskField], index: int) -> None:
    """Raise when a prefill row index lies outside the form."""
    if not 0 <= index < len(fields):
        raise IndexError(f'prefill row index {index} is out of range')


def _prefill_value(field: AskField, value: PrefillValueType,
                   index: int) -> Optional[PrefillValueType]:
    """Return the value to apply for a prefill, or None to drop it.

    Raises TypeError when value's Python type does not match field.
    """
    if isinstance(field, AskTextField):
        _need(value, index, str)
        return None if field.sensitive else value
    if isinstance(field, AskIntField):
        if isinstance(value, bool) or not isinstance(value, int):
            _bad_type(index)
        return value
    if isinstance(field, AskPathField):
        _need(value, index, Path)
        return value
    if isinstance(field, AskYesNoField):
        if not isinstance(value, bool):
            _bad_type(index)
        return value
    if isinstance(field, AskChoiceField):
        _need(value, index, str)
        return value if value in field.choices else None
    assert isinstance(field, AskMultiChoiceField)
    return _multi_prefill(field, value, index)


def _multi_prefill(field: AskMultiChoiceField, value: PrefillValueType,
                   index: int) -> Optional[list[str]]:
    """Return the valid members of a multi-choice prefill, or None."""
    if isinstance(value, str) or not isinstance(value, Sequence):
        _bad_type(index)
    if not all(isinstance(member, str) for member in value):
        _bad_type(index)
    members = [member for member in value if member in field.choices]
    return members if members else None


def _need(value: PrefillValueType, index: int, wanted: type) -> None:
    """Raise TypeError when value is not an instance of wanted."""
    if not isinstance(value, wanted):
        _bad_type(index)


def _bad_type(index: int) -> NoReturn:
    """Raise a TypeError for a prefill value of the wrong type."""
    raise TypeError(f'prefill value for row {index} has the wrong type')


def prefilled_field(field: AskField, prefill: PrefillValueType) -> AskField:
    """Return field with prefill as its default.

    The console bridge offers a prefill as the row's default when the row
    is asked. A prefill that cannot serve as a valid default, such as an
    integer outside the field's bounds, is ignored so the field keeps its
    own default.
    """
    if isinstance(field, AskTextField):
        assert isinstance(prefill, str)
        return replace(field, default=prefill)
    if isinstance(field, AskIntField):
        assert isinstance(prefill, int)
        return _int_prefilled(field, prefill)
    if isinstance(field, AskPathField):
        assert isinstance(prefill, Path)
        options = replace(field.path_options, default=prefill)
        return replace(field, path_options=options)
    if isinstance(field, AskYesNoField):
        assert isinstance(prefill, bool)
        return replace(field, default=prefill)
    if isinstance(field, AskChoiceField):
        assert isinstance(prefill, str)
        return replace(field, default=prefill)
    assert isinstance(field, AskMultiChoiceField)
    assert isinstance(prefill, list)
    return replace(field, default=prefill)


def _int_prefilled(field: AskIntField, value: int) -> AskIntField:
    """Return field with value as default, or field if out of range."""
    try:
        return replace(field, default=value)
    except ValueError:
        return field
