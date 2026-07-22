#! /usr/bin/env python3
"""Tests for the console form of the typed float and date-like fields.

The base ask_form() drives the console bridge, so these tests check that
a float, date, time, date-time or duration field is asked through
ask_text(), parsed, range-checked and re-asked on the console. The prompt
appears on stdout and a re-ask reason on stderr.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from datetime import date, datetime, time, timedelta
from io import StringIO
from typing import Optional

import pytest

from tableio_cfg_json import AskField, AskFloatField, AskDateField, \
    AskTimeField, AskDateTimeField, AskDurationField, WizardUiBridgeConsole
from .form_field_support import all_ask_fields, unknown_field


def _run(lines: str, fields: list[AskField]) -> tuple[list[object], str, str]:
    """Ask a console form with scripted input; return values, out, err."""
    out_file = StringIO()
    err_file = StringIO()
    bridge = WizardUiBridgeConsole(out_file, StringIO(lines), err_file)
    answers = bridge.ask_form('Fill this', fields)
    return ([answer.value for answer in answers],
            out_file.getvalue(), err_file.getvalue())


def _all_typed() -> list[AskField]:
    """Return one field of each typed kind, in a fixed order."""
    return [AskFloatField('Rate', None),
            AskDateField('Day', None),
            AskTimeField('At', None),
            AskDateTimeField('When', None),
            AskDurationField('For', None)]


def test_all_typed_fields() -> None:
    """The console form parses each typed field from its text answer."""
    answers = '3.5\n2024-01-02\n13:30\n2024-01-02 09:00\n1 d 02:00:00\n'
    values, _, _ = _run(answers, _all_typed())
    assert values == [3.5, date(2024, 1, 2), time(13, 30),
                      datetime(2024, 1, 2, 9, 0), timedelta(days=1, hours=2)]


def test_float_default() -> None:
    """An empty float answer selects the shown default."""
    values, out, _ = _run('\n', [AskFloatField('R', None, default=2.5)])
    assert values == [2.5]
    assert '[2.5]' in out


def test_float_nullable() -> None:
    """An empty nullable float answer returns None."""
    values, _, _ = _run('\n', [AskFloatField('R', None, nullable=True)])
    assert values == [None]


def test_float_range_reask() -> None:
    """An out-of-range float is re-asked until it is within bounds."""
    field = AskFloatField('R', None, min_value=0.0, max_value=10.0)
    values, _, err = _run('99\n5\n', [field])
    assert values == [5.0]
    assert 'between 0.0 and 10.0' in err


def test_float_bad_reask() -> None:
    """A non-numeric float answer is re-asked with the hint."""
    values, _, err = _run('abc\n3\n', [AskFloatField('R', None)])
    assert values == [3.0]
    assert 'a number' in err


def test_date_reask() -> None:
    """A bad date answer is re-asked with the date format hint."""
    values, _, err = _run('nope\n2024-05-06\n', [AskDateField('D', None)])
    assert values == [date(2024, 5, 6)]
    assert 'YYYY-MM-DD' in err


@pytest.mark.parametrize('text, expected', [
    ('90', timedelta(seconds=90)),
    ('2 d 03:30:00', timedelta(days=2, hours=3, minutes=30)),
    ('00:00:01.5', timedelta(seconds=1, milliseconds=500))])
def test_duration_forms(text: str, expected: Optional[timedelta]) -> None:
    """The console duration field accepts each accepted text form."""
    values, _, _ = _run(text + '\n', [AskDurationField('L', None)])
    assert values == [expected]


def test_duration_default() -> None:
    """A duration field shows its default in the console prompt."""
    field = AskDurationField('L', None, default=timedelta(hours=1))
    values, out, _ = _run('\n', [field])
    assert values == [timedelta(hours=1)]
    assert '[0 d 01:00:00]' in out


def test_hint_in_question() -> None:
    """The console question repeats the format hint for the field."""
    _, out, _ = _run('3\n', [AskFloatField('Rate', None)])
    assert 'Rate (a number)' in out


def test_supports_fields() -> None:
    """The console bridge supports every field type, rejects unknown."""
    bridge = WizardUiBridgeConsole(StringIO(), StringIO(), StringIO())
    assert all(bridge.supports_form_field(f) for f in all_ask_fields())
    assert not bridge.supports_form_field(unknown_field())
