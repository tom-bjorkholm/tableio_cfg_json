#! /usr/local/bin/python3
"""Helpers shared by the WizardUiBridge form question."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from collections.abc import Sequence
from dataclasses import replace
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Iterator, NoReturn, Optional
from tableio_cfg_json.wizard_ui_bridge_form_defs import AskField, \
    AnswerField, AskTextField, AskIntField, AskPathField, AskYesNoField, \
    AskChoiceField, AskMultiChoiceField, AskFloatField, AskDateField, \
    AskTimeField, AskDateTimeField, AskDurationField, AnswerTextField, \
    AnswerIntField, AnswerPathField, AnswerYesNoField, AnswerChoiceField, \
    AnswerMultiChoiceField, AnswerFloatField, AnswerDateField, \
    AnswerTimeField, AnswerDateTimeField, AnswerDurationField, \
    PrefillValueType, PrefillValues
_ORDERED_FIELDS = (AskIntField, AskFloatField, AskDateField, AskTimeField,
                   AskDateTimeField, AskDurationField)


def initial_answer(field: AskField) -> AnswerField:
    """Return the starting answer for a field before the user edits it.

    The value is the field's default, or the empty or not-yet-answered
    state when the field has no default. A choice field with no default
    starts as None, which tells a partial validator the choice is not
    answered yet; a bridge must not leave that None in a submitted form.
    """
    return _new_initial(field) or _basic_initial(field)


def _new_initial(field: AskField) -> Optional[AnswerField]:
    """Return the starting answer for a typed field, else None."""
    if isinstance(field, AskFloatField):
        return AnswerFloatField(field, field.default)
    if isinstance(field, AskDateField):
        return AnswerDateField(field, field.default)
    if isinstance(field, AskTimeField):
        return AnswerTimeField(field, field.default)
    if isinstance(field, AskDateTimeField):
        return AnswerDateTimeField(field, field.default)
    if isinstance(field, AskDurationField):
        return AnswerDurationField(field, field.default)
    return None


def _basic_initial(field: AskField) -> AnswerField:
    """Return the starting answer for one of the original field kinds."""
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
    if isinstance(field, _ORDERED_FIELDS):
        return _ordered_prefill(field, value, index)
    if isinstance(field, AskTextField):
        _need(value, index, str)
        return None if field.sensitive else value
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


def _ordered_prefill(field: AskField, value: PrefillValueType,
                     index: int) -> PrefillValueType:
    """Return an ordered field's prefill, or raise TypeError for it.

    An integer or float field takes a number, and a date field takes a
    date that is not a datetime, so a datetime is never mistaken for a
    plain date. Each temporal field takes exactly its own type.
    """
    if isinstance(field, AskIntField):
        if isinstance(value, bool) or not isinstance(value, int):
            _bad_type(index)
        return value
    if isinstance(field, AskFloatField):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            _bad_type(index)
        return value
    if isinstance(field, AskDateField):
        if not isinstance(value, date) or isinstance(value, datetime):
            _bad_type(index)
        return value
    if isinstance(field, AskTimeField):
        if not isinstance(value, time):
            _bad_type(index)
        return value
    if isinstance(field, AskDateTimeField):
        if not isinstance(value, datetime):
            _bad_type(index)
        return value
    assert isinstance(field, AskDurationField)
    if not isinstance(value, timedelta):
        _bad_type(index)
    return value


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
    integer or date outside the field's bounds, is ignored so the field
    keeps its own default. The prefill has already been checked against
    the field type by valid_prefills().
    """
    try:
        result = _default_a(field, prefill)
        return result if result is not None else _default_b(field, prefill)
    except ValueError:
        return field


def _default_a(field: AskField,
               prefill: PrefillValueType) -> Optional[AskField]:
    """Return field with prefill as default for the first field group."""
    if isinstance(field, AskPathField):
        assert isinstance(prefill, Path)
        options = replace(field.path_options, default=prefill)
        return replace(field, path_options=options)
    if isinstance(field, AskIntField):
        assert isinstance(prefill, int)
        return replace(field, default=prefill)
    if isinstance(field, AskFloatField):
        assert isinstance(prefill, (int, float))
        return replace(field, default=prefill)
    if isinstance(field, AskDateField):
        assert isinstance(prefill, date)
        return replace(field, default=prefill)
    if isinstance(field, AskTimeField):
        assert isinstance(prefill, time)
        return replace(field, default=prefill)
    return None


def _default_b(field: AskField, prefill: PrefillValueType) -> AskField:
    """Return field with prefill as default for the second field group."""
    if isinstance(field, AskDateTimeField):
        assert isinstance(prefill, datetime)
        return replace(field, default=prefill)
    if isinstance(field, AskDurationField):
        assert isinstance(prefill, timedelta)
        return replace(field, default=prefill)
    if isinstance(field, AskYesNoField):
        assert isinstance(prefill, bool)
        return replace(field, default=prefill)
    if isinstance(field, AskChoiceField):
        assert isinstance(prefill, str)
        return replace(field, default=prefill)
    if isinstance(field, AskTextField):
        assert isinstance(prefill, str)
        return replace(field, default=prefill)
    assert isinstance(field, AskMultiChoiceField)
    assert isinstance(prefill, list)
    return replace(field, default=prefill)
