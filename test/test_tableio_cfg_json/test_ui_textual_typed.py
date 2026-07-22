#! /usr/bin/env python3
"""Tests for the Textual form of the typed float and date-like fields.

This covers the text inputs for float, time and duration fields, the
calendar Pick button and '?' token for date and date-time fields, the
modal calendar screen, and the live range feedback and prefills for the
typed fields.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import asyncio
from datetime import date, datetime, time, timedelta
from typing import Sequence

import pytest
from textual.widgets import Button, Input, Static

from tableio_cfg_json import AskField, AskFloatField, AskDateField, \
    AskTimeField, AskDateTimeField, AskDurationField, AnswerField, \
    PartFormValidationResult, PrefillValues, WizardUiBridgeTextual
from tableio_cfg_json.wizard_ui_bridge_textual import _FormApp
from tableio_cfg_json._wizard_ui_bridge_calendar import _CalendarScreen, _shift
from .ui_textual_support import drive, _submitted


def _typed_form() -> list[AskField]:
    """Return a float, time and duration field for the text-input tests."""
    return [AskFloatField('Rate', None),
            AskTimeField('At', None),
            AskDurationField('For', None)]


def test_typed_widgets_submit() -> None:
    """Typed text fields parse their inputs into typed answers."""
    app = _FormApp('H', _typed_form(), [], None)

    async def scenario() -> None:
        async with app.run_test() as pilot:
            app.query_one('#field_0', Input).value = '3.5'
            app.query_one('#field_1', Input).value = '09:30'
            app.query_one('#field_2', Input).value = '1 d 02:00:00'
            await pilot.pause()
            await pilot.click('#submit')
    asyncio.run(scenario())
    assert [a.value for a in _submitted(app)] == \
        [3.5, time(9, 30), timedelta(days=1, hours=2)]


def test_float_out_of_range() -> None:
    """A float outside the field bounds refuses to submit."""
    fields: list[AskField] = [
        AskFloatField('R', None, min_value=0.0, max_value=5.0)]
    driven = drive(_FormApp('H', fields, [], None), ['9', '#submit'])
    assert driven.return_value is None


def test_float_live_error() -> None:
    """An out-of-range float shows its error while editing."""
    fields: list[AskField] = [
        AskFloatField('R', None, min_value=0.0, max_value=5.0)]
    app = _FormApp('H', fields, [], None)

    async def scenario() -> str:
        async with app.run_test() as pilot:
            app.query_one('#field_0', Input).value = '9'
            await pilot.pause()
            return str(app.query_one('#form_status', Static).render())
    assert 'between 0.0 and 5.0' in asyncio.run(scenario())


def test_date_pick() -> None:
    """The calendar Pick button fills the date field with a clicked day."""
    field = AskDateField('Day', None, default=date(2024, 3, 10))
    app = _FormApp('H', [field], [], None)
    driven = drive(app, ['#pick_0', '#next_month', '#day_15', '#submit'],
                   pause=True)
    assert _submitted(driven)[0].value == date(2024, 4, 15)


def test_datetime_keeps_time() -> None:
    """Picking a date keeps the time part of a date-time field."""
    field = AskDateTimeField('W', None, default=datetime(2024, 3, 10, 14, 30))
    app = _FormApp('H', [field], [], None)
    driven = drive(app, ['#pick_0', '#day_20', '#submit'], pause=True)
    assert _submitted(driven)[0].value == datetime(2024, 3, 20, 14, 30)


def test_magic_token_opens() -> None:
    """Typing the token into a date input opens the calendar."""
    field = AskDateField('Day', None, default=date(2024, 3, 10))
    app = _FormApp('H', [field], [], None)

    async def scenario() -> bool:
        async with app.run_test() as pilot:
            app.query_one('#field_0', Input).value = '?'
            await pilot.pause()
            return isinstance(pilot.app.screen, _CalendarScreen)
    assert asyncio.run(scenario()) is True


def test_calendar_cancel() -> None:
    """Cancelling the calendar leaves the date field unchanged."""
    field = AskDateField('Day', None, default=date(2024, 3, 10))
    app = _FormApp('H', [field], [], None)

    async def scenario() -> str:
        async with app.run_test() as pilot:
            await pilot.click('#pick_0')
            await pilot.pause()
            await pilot.press('escape')
            await pilot.pause()
            return app.query_one('#field_0', Input).value
    assert asyncio.run(scenario()) == '2024-03-10'


def test_calendar_navigation() -> None:
    """Month and year buttons move the calendar to a new title."""
    field = AskDateField('Day', None, default=date(2024, 3, 10))
    app = _FormApp('H', [field], [], None)

    async def scenario() -> str:
        async with app.run_test() as pilot:
            await pilot.click('#pick_0')
            await pilot.pause()
            await pilot.click('#next_year')
            await pilot.click('#prev_month')
            await pilot.pause()
            screen = pilot.app.screen
            return str(screen.query_one('#cal_title', Static).render())
    assert asyncio.run(scenario()) == 'February 2025'


def test_calendar_disabled() -> None:
    """A day beyond the field maximum is shown disabled in the calendar."""
    field = AskDateField('Day', None, default=date(2024, 3, 10),
                         max_value=date(2024, 3, 20))
    app = _FormApp('H', [field], [], None)

    async def scenario() -> bool:
        async with app.run_test() as pilot:
            await pilot.click('#pick_0')
            await pilot.pause()
            screen = pilot.app.screen
            return screen.query_one('#day_25', Button).disabled
    assert asyncio.run(scenario()) is True


@pytest.mark.parametrize('year, month, action, expected', [
    (2024, 3, 'prev_month', (2024, 2)),
    (2024, 1, 'prev_month', (2023, 12)),
    (2024, 12, 'next_month', (2025, 1)),
    (2024, 6, 'next_year', (2025, 6)),
    (2024, 6, 'prev_year', (2023, 6))])
def test_shift(year: int, month: int, action: str,
               expected: tuple[int, int]) -> None:
    """_shift moves the month and year and wraps at the year boundary."""
    assert _shift(year, month, action) == expected


def test_shift_clamps() -> None:
    """_shift clamps the year to the supported date range."""
    assert _shift(date.min.year, 6, 'prev_year') == (date.min.year, 6)


def test_prefill_duration() -> None:
    """A duration prefill fills and submits the target duration widget."""
    fields: list[AskField] = [AskFloatField('R', None),
                              AskDurationField('L', None)]

    def rule(answers: Sequence[AnswerField],
             changed: int) -> PartFormValidationResult:
        _ = answers
        prefill: PrefillValues = ()
        if changed == 0:
            prefill = ((1, timedelta(hours=2)),)
        return PartFormValidationResult(True, '', (), prefill)
    driven = drive(_FormApp('H', fields, [], rule), ['1', '#submit'])
    assert _submitted(driven)[1].value == timedelta(hours=2)


def test_supports_all() -> None:
    """The Textual bridge reports every typed field as supported."""
    bridge = WizardUiBridgeTextual()
    fields: list[AskField] = [
        AskFloatField('R', None), AskDateField('D', None),
        AskTimeField('T', None), AskDateTimeField('W', None),
        AskDurationField('L', None)]
    assert all(bridge.supports_form_field(field) for field in fields)
