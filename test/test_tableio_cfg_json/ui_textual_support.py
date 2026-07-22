#! /usr/bin/env python3
"""Shared helpers for the Textual user interface bridge tests.

These helpers drive short-lived Textual screens headlessly and provide a
bridge whose screens return scripted outcomes, so the several Textual
test modules can share one screen driver and one canned bridge.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

# pylint: disable=protected-access

import asyncio
from typing import Any, Optional, Sequence

from textual.pilot import Pilot
from textual.widgets import Input

from tableio_cfg_json import WizardNavigation, WizardUiBridgeTextual
from tableio_cfg_json.wizard_ui_bridge_form_defs import AnswerField
from tableio_cfg_json.wizard_ui_bridge_textual import _NavApp
from tableio_cfg_json._wizard_ui_bridge_path import _PickerScreen


def drive(app: _NavApp[Any], steps: Sequence[str],
          pause: bool = False) -> _NavApp[Any]:
    """Run a screen headlessly, performing each step, and return it.

    A step starting with '#' is a click on that widget id; any other
    step is a single key press. When pause is True the driver pauses
    after each step, which lets a pushed modal screen (such as the
    calendar) mount before the next step acts on it.
    """
    async def scenario() -> None:
        async with app.run_test() as pilot:
            for step in steps:
                if step.startswith('#'):
                    await pilot.click(step)
                else:
                    await pilot.press(step)
                if pause:
                    await pilot.pause()
    asyncio.run(scenario())
    return app


class _CannedBridge(WizardUiBridgeTextual):
    """Textual bridge whose screens return scripted outcomes.

    Each scripted outcome is one of: a WizardNavigation subclass, which
    is recorded as the screen's navigation request; None, which acts as
    a screen closed with no value; or any other value, returned as the
    screen's result. The launched apps are kept so tests can inspect the
    messages they were given.
    """

    def __init__(self, outcomes: list[object]) -> None:
        """Store the scripted outcomes and an empty launch log."""
        super().__init__()
        self._outcomes = outcomes
        self.launched: list[_NavApp[Any]] = []

    def _launch(self, app: _NavApp[Any]) -> Any:
        """Record the app and return the next scripted outcome."""
        self.launched.append(app)
        outcome = self._outcomes.pop(0)
        if isinstance(outcome, type) and issubclass(outcome, WizardNavigation):
            app.nav = outcome
            return None
        return outcome


def _submitted(app: _NavApp[Any]) -> list[AnswerField]:
    """Return the answers a submitted form produced, asserting success."""
    result = app.return_value
    assert isinstance(result, list)
    return result


async def focused_day(pilot: Pilot[Any], *keys: str) -> Optional[str]:
    """Open the field-0 calendar, press keys, return the focused id.

    The calendar is opened from the Pick button of the first form date
    field and each key in keys is pressed in turn, so a test can move the
    day focus and read the id of the day button left focused.
    """
    await pilot.click('#pick_0')
    await pilot.pause()
    for key in keys:
        await pilot.press(key)
    await pilot.pause()
    focused = pilot.app.screen.focused
    return None if focused is None else focused.id


async def open_picker(pilot: Pilot[Any], value: str) -> _PickerScreen:
    """Open the field-0 directory picker and seed its path input.

    The picker is opened from the Browse button of the first form path
    field and its editable input is set to value, ready for a test to
    submit or cancel it.
    """
    await pilot.click('#browse_0')
    await pilot.pause()
    screen = pilot.app.screen
    assert isinstance(screen, _PickerScreen)
    screen.query_one('#path_input', Input).value = value
    return screen
