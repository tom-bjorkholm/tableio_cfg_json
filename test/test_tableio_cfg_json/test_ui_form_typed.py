#! /usr/bin/env python3
"""Tests for the typed fields in the form helpers and prefills.

This covers the starting answers, the prefill type checks, the prefilled
default, and a console prefill seeding a typed field's offered default,
for the float, date, time, date-time and duration fields.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from datetime import date, datetime, time, timedelta
from io import StringIO
from pathlib import Path
from typing import Sequence

import pytest

from tableio_cfg_json import AskField, AskFloatField, AskDateField, \
    AskTimeField, AskDateTimeField, AskDurationField, AskTextField, \
    AskIntField, AskPathField, AskYesNoField, AskChoiceField, \
    AskMultiChoiceField, AnswerField, AnswerFloatField, AnswerDateField, \
    AnswerTimeField, AnswerDateTimeField, AnswerDurationField, \
    PartFormValidationResult, PrefillValues, PrefillValueType, \
    PathAskOptions, WizardUiBridgeConsole
from tableio_cfg_json._wizard_ui_bridge_form import initial_answer, \
    valid_prefills, prefilled_field


def test_initial_typed() -> None:
    """initial_answer returns each typed field's default as start value."""
    number = AskFloatField('R', None, default=2.0)
    day = AskDateField('D', None, default=date(2024, 1, 2))
    clock = AskTimeField('T', None, default=time(9))
    moment = AskDateTimeField('W', None, default=datetime(2024, 1, 2, 9))
    span = AskDurationField('L', None, default=timedelta(hours=1))
    assert initial_answer(number) == AnswerFloatField(number, 2.0)
    assert initial_answer(day) == AnswerDateField(day, date(2024, 1, 2))
    assert initial_answer(clock) == AnswerTimeField(clock, time(9))
    assert initial_answer(moment) == \
        AnswerDateTimeField(moment, datetime(2024, 1, 2, 9))
    assert initial_answer(span) == \
        AnswerDurationField(span, timedelta(hours=1))


@pytest.mark.parametrize('field, value', [
    (AskFloatField('R', None), 3.5),
    (AskFloatField('R', None), 3),
    (AskDateField('D', None), date(2024, 1, 1)),
    (AskTimeField('T', None), time(9)),
    (AskDateTimeField('W', None), datetime(2024, 1, 1, 9)),
    (AskDurationField('L', None), timedelta(hours=1))])
def test_prefill_typed_ok(field: AskField, value: object) -> None:
    """valid_prefills accepts a well-typed prefill for each typed field."""
    fields: list[AskField] = [field]
    prefills: PrefillValues = ((0, value),)  # type: ignore[assignment]
    assert list(valid_prefills(fields, -1, prefills)) == [(0, value)]


@pytest.mark.parametrize('field, value', [
    (AskFloatField('R', None), 'x'),
    (AskFloatField('R', None), True),
    (AskDateField('D', None), datetime(2024, 1, 1)),
    (AskDateField('D', None), 'x'),
    (AskTimeField('T', None), date(2024, 1, 1)),
    (AskDateTimeField('W', None), date(2024, 1, 1)),
    (AskDurationField('L', None), 5)])
def test_prefill_typed_bad(field: AskField, value: object) -> None:
    """valid_prefills rejects a prefill whose type does not match."""
    fields: list[AskField] = [field]
    prefills: PrefillValues = ((0, value),)  # type: ignore[assignment]
    with pytest.raises(TypeError):
        list(valid_prefills(fields, -1, prefills))


@pytest.mark.parametrize('field, value', [
    (AskTextField('S', None), 'hi'),
    (AskIntField('N', None), 7),
    (AskPathField('P', None, PathAskOptions()), Path('/tmp/x')),
    (AskYesNoField('B', None, False), True),
    (AskChoiceField('C', None, choices=('x', 'y')), 'y'),
    (AskMultiChoiceField('M', None, choices=('a', 'b')), ['a', 'b']),
    (AskFloatField('R', None), 4.0),
    (AskDateField('D', None), date(2024, 5, 6)),
    (AskTimeField('T', None), time(9, 30)),
    (AskDateTimeField('W', None), datetime(2024, 5, 6, 9, 30)),
    (AskDurationField('L', None), timedelta(hours=2))])
def test_prefilled_all(field: AskField, value: PrefillValueType) -> None:
    """prefilled_field seeds every field kind's offered default."""
    assert initial_answer(prefilled_field(field, value)).value == value


def test_prefilled_float_ok() -> None:
    """An in-range float prefill becomes the field's offered default."""
    field = AskFloatField('R', None, min_value=0.0, max_value=5.0)
    result = prefilled_field(field, 4.0)
    assert isinstance(result, AskFloatField)
    assert result.default == 4.0


def test_prefill_float_oob() -> None:
    """An out-of-range float prefill leaves the field default alone."""
    field = AskFloatField('R', None, min_value=0.0, max_value=5.0, default=3.0)
    result = prefilled_field(field, 9.0)
    assert isinstance(result, AskFloatField)
    assert result.default == 3.0


def test_prefilled_date_range() -> None:
    """An out-of-range date prefill leaves the field default alone."""
    field = AskDateField('D', None, min_value=date(2024, 1, 1),
                         max_value=date(2024, 12, 31),
                         default=date(2024, 6, 1))
    result = prefilled_field(field, date(2025, 1, 1))
    assert isinstance(result, AskDateField)
    assert result.default == date(2024, 6, 1)


def test_console_prefill_date() -> None:
    """A validator prefill seeds a console date field's offered default."""
    fields: list[AskField] = [AskTextField('A', None),
                              AskDateField('D', None)]

    def rule(answers: Sequence[AnswerField],
             changed: int) -> PartFormValidationResult:
        _ = answers
        prefill: PrefillValues = ((1, date(2024, 5, 6)),) if changed == 0 \
            else ()
        return PartFormValidationResult(True, '', (), prefill)
    out = StringIO()
    bridge = WizardUiBridgeConsole(out, StringIO('key\n\n'), StringIO())
    answers = bridge.ask_form('Q', fields, partial_validator=rule)
    assert answers[1].value == date(2024, 5, 6)
    assert '[2024-05-06]' in out.getvalue()
