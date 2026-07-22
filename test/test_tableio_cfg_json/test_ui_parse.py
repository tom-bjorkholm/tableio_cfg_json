#! /usr/bin/env python3
"""Tests for parsing and formatting the typed form field values.

This covers the float, date, time, date-time and duration text parsers,
the duration formatter, the range messages, the resolve/read helpers used
by the forms, the faked text field, and the bounds validation the typed
field dataclasses perform when they are built.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from datetime import date, datetime, time, timedelta
from typing import Callable, Optional

import pytest

from tableio_cfg_json import AskField, AskFloatField, AskDateField, \
    AskTimeField, AskDateTimeField, AskDurationField, AnswerFloatField, \
    AnswerDateField, AnswerDateTimeField
from tableio_cfg_json._wizard_ui_bridge_parse import parse_float, parse_date, \
    parse_time, parse_datetime, parse_duration, format_duration, \
    format_new_value, ordered_range_error, resolve_new, value_from_text, \
    error_from_text, fake_field, new_answer, ask_typed, field_hint, \
    FLOAT_HINT, DATE_HINT


@pytest.mark.parametrize('text, expected', [
    ('3.5', 3.5), ('  -2 ', -2.0), ('0', 0.0), ('1e3', 1000.0),
    ('abc', None), ('', None), ('inf', None), ('nan', None)])
def test_parse_float(text: str, expected: Optional[float]) -> None:
    """parse_float reads finite floats and rejects other text."""
    assert parse_float(text) == expected


@pytest.mark.parametrize('text, expected', [
    ('2024-01-02', date(2024, 1, 2)), (' 2024-12-31 ', date(2024, 12, 31)),
    ('2024-01-02T10:00', None), ('not a date', None), ('', None)])
def test_parse_date(text: str, expected: Optional[date]) -> None:
    """parse_date reads an ISO date and rejects times or bad text."""
    assert parse_date(text) == expected


@pytest.mark.parametrize('text, expected', [
    ('13:30', time(13, 30)), ('13:30:05', time(13, 30, 5)),
    ('25:00', None), ('noon', None), ('', None)])
def test_parse_time(text: str, expected: Optional[time]) -> None:
    """parse_time reads an ISO time and rejects bad text."""
    assert parse_time(text) == expected


@pytest.mark.parametrize('text, expected', [
    ('2024-01-02 09:15', datetime(2024, 1, 2, 9, 15)),
    ('2024-01-02', datetime(2024, 1, 2, 0, 0)),
    ('2024-13-02 09:15', None), ('', None)])
def test_parse_datetime(text: str, expected: Optional[datetime]) -> None:
    """parse_datetime reads an ISO date-time and rejects bad text."""
    assert parse_datetime(text) == expected


@pytest.mark.parametrize('text, expected', [
    ('2 d 03:30:00', timedelta(days=2, hours=3, minutes=30)),
    ('03:30:00', timedelta(hours=3, minutes=30)),
    ('0 d 00:01:30', timedelta(minutes=1, seconds=30)),
    ('00:90:00', timedelta(minutes=90)),
    ('90', timedelta(seconds=90)),
    ('00:00:01.5', timedelta(seconds=1, milliseconds=500)),
    ('1.5', timedelta(seconds=1, milliseconds=500)),
    ('-5', None), ('1:2', None), ('x', None), ('', None),
    ('1e20', None),
    ('999999999999999 d 00:00:00', None)])
def test_parse_duration(text: str, expected: Optional[timedelta]) -> None:
    """parse_duration reads clock text and bare seconds, else None."""
    assert parse_duration(text) == expected


@pytest.mark.parametrize('value, expected', [
    (timedelta(days=2, hours=3, minutes=30), '2 d 03:30:00'),
    (timedelta(), '0 d 00:00:00'),
    (timedelta(seconds=1, milliseconds=500), '0 d 00:00:01.5'),
    (timedelta(hours=1), '0 d 01:00:00')])
def test_format_duration(value: timedelta, expected: str) -> None:
    """format_duration shows days, a clock part and any fraction."""
    assert format_duration(value) == expected


def test_duration_round_trip() -> None:
    """A formatted duration parses back to the same value."""
    value = timedelta(days=3, hours=1, minutes=2, seconds=3)
    assert parse_duration(format_duration(value)) == value


@pytest.mark.parametrize('value, expected', [
    (3.5, '3.5'), (date(2024, 1, 2), '2024-01-02'),
    (time(9, 5), '09:05:00'), (timedelta(hours=1), '0 d 01:00:00')])
def test_format_new_value(value: object, expected: str) -> None:
    """format_new_value renders each typed value as round-trip text."""
    assert format_new_value(value) == expected


@pytest.mark.parametrize('low, high, expected', [
    (0.0, 10.0, 'between 0.0 and 10.0'), (None, 5.0, 'at most 5.0'),
    (1.0, None, 'at least 1.0')])
def test_ordered_range_error(low: Optional[float], high: Optional[float],
                             expected: str) -> None:
    """ordered_range_error names the present bounds."""
    assert expected in ordered_range_error(low, high)


def test_resolve_new_ok() -> None:
    """resolve_new returns the value and no error for good text."""
    field = AskFloatField('R', None, min_value=0.0, max_value=10.0)
    assert resolve_new(field, '3.5') == (3.5, None)


def test_resolve_none_text() -> None:
    """resolve_new treats None text as an empty nullable answer."""
    assert resolve_new(AskFloatField('R', None), None) == (None, None)


def test_resolve_new_bad() -> None:
    """resolve_new reports the format hint for unparsable text."""
    value, error = resolve_new(AskDateField('D', None), 'nope')
    assert value is None
    assert error is not None and DATE_HINT in error


def test_resolve_new_range() -> None:
    """resolve_new reports a range error and drops the value."""
    field = AskFloatField('R', None, min_value=0.0, max_value=5.0)
    value, error = resolve_new(field, '9')
    assert value is None
    assert error == 'Please enter a value between 0.0 and 5.0.'


def test_value_empty_default() -> None:
    """value_from_text returns the field default for empty text."""
    field = AskFloatField('R', None, default=2.0)
    assert value_from_text(field, '') == 2.0


def test_error_required() -> None:
    """error_from_text reports a required value for empty text."""
    field = AskDateField('D', None)
    assert error_from_text(field, '') == f'Please enter {DATE_HINT}.'


def test_error_nullable() -> None:
    """error_from_text accepts empty text when the field is nullable."""
    assert error_from_text(AskDateField('D', None, nullable=True), '') is None


def test_fake_field() -> None:
    """fake_field turns a typed field into a text field with a hint."""
    field = AskDurationField('For', 'How long', default=timedelta(hours=1))
    faked = fake_field(field)
    assert faked.short_question == 'For'
    assert faked.help_text is not None and 'How long' in faked.help_text
    assert faked.default == '0 d 01:00:00'


def test_fake_field_nullable() -> None:
    """fake_field carries the nullable flag and shows the hint only."""
    faked = fake_field(AskFloatField('R', None, nullable=True))
    assert faked.nullable is True
    assert faked.help_text == f'Enter {FLOAT_HINT}.'


def test_new_answer_types() -> None:
    """new_answer wraps a value in the answer matching the field."""
    field = AskFloatField('R', None)
    assert new_answer(field, 3.5) == AnswerFloatField(field, 3.5)


def test_new_answer_none() -> None:
    """new_answer accepts None for an empty nullable typed field."""
    field = AskDateField('D', None, nullable=True)
    assert new_answer(field, None) == AnswerDateField(field, None)


def test_new_answer_datetime() -> None:
    """new_answer keeps a datetime value for a date-time field."""
    field = AskDateTimeField('W', None)
    moment = datetime(2024, 1, 2, 9, 0)
    assert new_answer(field, moment) == AnswerDateTimeField(field, moment)


def test_field_hint() -> None:
    """field_hint returns the format hint of each typed field."""
    assert field_hint(AskFloatField('R', None)) == FLOAT_HINT


def _reader(answers: list[Optional[str]]) -> Callable[..., Optional[str]]:
    """Return an ask_text stand-in yielding the scripted answers."""
    remaining = list(answers)

    def ask_text(question: str, re_ask_reason: Optional[str] = None,
                 nullable: bool = False, *,
                 default: Optional[str] = None) -> Optional[str]:
        _ = (question, re_ask_reason, nullable, default)
        return remaining.pop(0)
    return ask_text


def test_ask_typed_reask() -> None:
    """ask_typed re-asks until the entered text parses in range."""
    field = AskFloatField('R', None, min_value=0.0, max_value=10.0)
    reader = _reader(['abc', '99', '3.5'])
    assert ask_typed(reader, field, parse_float, FLOAT_HINT) == 3.5


def test_ask_typed_nullable() -> None:
    """ask_typed returns None for an empty nullable answer."""
    field = AskFloatField('R', None, nullable=True)
    assert ask_typed(_reader([None]), field, parse_float, FLOAT_HINT) is None


@pytest.mark.parametrize('field_class, low, high', [
    (AskFloatField, 5.0, 1.0),
    (AskDateField, date(2024, 2, 1), date(2024, 1, 1)),
    (AskTimeField, time(10), time(9)),
    (AskDateTimeField, datetime(2024, 2, 1), datetime(2024, 1, 1)),
    (AskDurationField, timedelta(days=2), timedelta(days=1))])
def test_bounds_reversed(field_class: type, low: object, high: object) -> None:
    """A typed field with min greater than max is rejected."""
    with pytest.raises(ValueError, match='min_value'):
        field_class('Q', None, min_value=low, max_value=high)


@pytest.mark.parametrize('field_class, low, high, bad', [
    (AskFloatField, 0.0, 5.0, 9.0),
    (AskDateField, date(2024, 1, 1), date(2024, 2, 1), date(2024, 3, 1)),
    (AskTimeField, time(9), time(17), time(20)),
    (AskDateTimeField, datetime(2024, 1, 1), datetime(2024, 2, 1),
     datetime(2024, 3, 1)),
    (AskDurationField, timedelta(0), timedelta(days=1), timedelta(days=2))])
def test_bounds_default_out(field_class: type, low: object, high: object,
                            bad: object) -> None:
    """A typed field default outside the bounds is rejected."""
    with pytest.raises(ValueError, match='range'):
        field_class('Q', None, min_value=low, max_value=high, default=bad)


def test_bounds_default_ok() -> None:
    """A typed field default within the bounds is accepted."""
    field = AskFloatField('R', None, min_value=0.0, max_value=10.0,
                          default=5.0)
    assert field.default == 5.0


def _ordered_fields() -> list[AskField]:
    """Return one typed field of each kind for shared checks."""
    return [AskFloatField('R', None), AskDateField('D', None),
            AskTimeField('T', None), AskDateTimeField('W', None),
            AskDurationField('L', None)]


def test_field_hint_all() -> None:
    """Every typed field reports a non-empty format hint."""
    assert all(field_hint(field) for field in _ordered_fields())
