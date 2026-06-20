#! /usr/bin/env python3
"""Tests for the Textual user interface bridge and its factory."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

# pylint: disable=protected-access

import asyncio
from io import StringIO
from typing import Any, Sequence

import pytest

from tableio_cfg_json import WizardAbort, WizardBack, WizardCancelLevel, \
    WizardNavigation, WizardUiBridgeConsole, WizardUiBridgeTextual, \
    make_text_ui_bridge
from tableio_cfg_json.wizard_ui_bridge_textual import _ChoiceApp, _MultiApp, \
    _NavApp, _TextApp


def drive(app: _NavApp[Any], steps: Sequence[str]) -> _NavApp[Any]:
    """Run a screen headlessly, performing each step, and return it.

    A step starting with '#' is a click on that widget id; any other
    step is a single key press.
    """
    async def scenario() -> None:
        async with app.run_test() as pilot:
            for step in steps:
                if step.startswith('#'):
                    await pilot.click(step)
                else:
                    await pilot.press(step)
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


class _TtyStream(StringIO):
    """In-memory stream that reports itself as a terminal."""

    def isatty(self) -> bool:
        """Pretend to be a terminal so the factory picks Textual."""
        return True


def test_text_returns_typed() -> None:
    """The text screen returns the characters the user typed."""
    app = drive(_TextApp('q', []), ['h', 'i', 'enter'])
    assert app.return_value == 'hi'


def test_text_empty() -> None:
    """The text screen returns an empty string for no input."""
    app = drive(_TextApp('q', []), ['enter'])
    assert app.return_value == ''


def test_text_back_nav() -> None:
    """ctrl+b records a back request and exits with no value."""
    app = drive(_TextApp('q', []), ['ctrl+b'])
    assert app.return_value is None
    assert app.nav is WizardBack


def test_text_cancel_nav() -> None:
    """ctrl+o records a cancel-level request and exits."""
    app = drive(_TextApp('q', []), ['ctrl+o'])
    assert app.return_value is None
    assert app.nav is WizardCancelLevel


def test_text_abort_quit() -> None:
    """The built-in ctrl+q quit exits with no value and no request."""
    app = drive(_TextApp('q', []), ['ctrl+q'])
    assert app.return_value is None
    assert app.nav is None


def test_choice_index() -> None:
    """The choice screen returns the index of the picked option."""
    app = drive(_ChoiceApp('q', ['a', 'b', 'c'], None, []), ['enter'])
    assert app.return_value == 0


def test_choice_default() -> None:
    """The choice screen highlights and returns the default option."""
    app = drive(_ChoiceApp('q', ['a', 'b', 'c'], 2, []), ['enter'])
    assert app.return_value == 2


def test_multi_indexes() -> None:
    """The multi screen returns the chosen indexes."""
    app = _MultiApp('q', ['a', 'b', 'c'], [0], 0, None, [])
    driven = drive(app, ['down', 'down', 'space', 'ctrl+s'])
    result = driven.return_value
    assert result is not None
    assert sorted(result) == [0, 2]


def test_multi_min() -> None:
    """The multi screen refuses to submit below the minimum count."""
    app = _MultiApp('q', ['a', 'b'], [], 1, None, [])
    driven = drive(app, ['ctrl+s', 'space', 'ctrl+s'])
    assert driven.return_value == [0]


def test_multi_button() -> None:
    """Clicking submit closes the multi screen with the selection."""
    app = _MultiApp('q', ['a', 'b'], [0], 0, None, [])
    driven = drive(app, ['#submit'])
    assert driven.return_value == [0]


def test_ask_text() -> None:
    """ask() without choices returns the typed string."""
    bridge = _CannedBridge(['typed'])
    assert bridge.ask('q') == 'typed'


def test_ask_index() -> None:
    """ask() with choices returns the selected 0-based index."""
    bridge = _CannedBridge([1])
    assert bridge.ask('q', choices=['a', 'b', 'c']) == 1


def test_ask_choice_value() -> None:
    """ask_choice() maps the chosen index back to the choice."""
    bridge = _CannedBridge([2])
    assert bridge.ask_choice('q', choices=['a', 'b', 'c']) == 'c'


@pytest.mark.parametrize('index,expected', [(0, True), (1, False)])
def test_yes_no_map(index: int, expected: bool) -> None:
    """ask_yes_no() maps the yes index to True and the no index to False."""
    bridge = _CannedBridge([index])
    assert bridge.ask_yes_no('q', default=True) is expected


def test_multi_map() -> None:
    """ask_multi() returns the chosen values in choices order."""
    bridge = _CannedBridge([[2, 0]])
    assert bridge.ask_multi('q', choices=['a', 'b', 'c']) == ['a', 'c']


def test_choice_default_idx() -> None:
    """ask_choice() highlights the default and None without a default."""
    with_default = _CannedBridge([0])
    with_default.ask_choice('q', choices=['a', 'b', 'c'], default='b')
    chosen = with_default.launched[0]
    assert isinstance(chosen, _ChoiceApp)
    assert chosen._default_index == 1
    without = _CannedBridge([0])
    without.ask_choice('q', choices=['a', 'b'])
    plain = without.launched[0]
    assert isinstance(plain, _ChoiceApp)
    assert plain._default_index is None


@pytest.mark.parametrize('nav', [WizardBack, WizardCancelLevel, WizardAbort])
def test_nav_reraised(nav: type[WizardNavigation]) -> None:
    """A recorded navigation request is re-raised by the bridge."""
    bridge = _CannedBridge([nav])
    with pytest.raises(nav):
        bridge.ask('q')


def test_quit_abort() -> None:
    """A screen that closes with no value is treated as an abort."""
    bridge = _CannedBridge([None])
    with pytest.raises(WizardAbort):
        bridge.ask('q')


def test_show_buffered() -> None:
    """A shown message appears on the next screen's header."""
    bridge = _CannedBridge(['x'])
    bridge.show('hello')
    bridge.ask('q')
    app = bridge.launched[0]
    assert isinstance(app, _TextApp)
    assert 'hello' in app._messages


def test_error_drained() -> None:
    """Diagnostics written to error_file() appear on the next screen."""
    bridge = _CannedBridge(['x'])
    bridge.error_file().write('diag line\n')
    bridge.ask('q')
    app = bridge.launched[0]
    assert isinstance(app, _TextApp)
    assert 'diag line' in app._messages


def test_reask_reason() -> None:
    """A re-ask reason is shown together with the question."""
    bridge = _CannedBridge(['x'])
    bridge.ask('q', re_ask_reason='bad value')
    app = bridge.launched[0]
    assert isinstance(app, _TextApp)
    assert 'bad value' in app._messages


def test_drained_once() -> None:
    """Buffered messages are shown once and not on later screens."""
    bridge = _CannedBridge(['x', 'y'])
    bridge.show('once')
    bridge.ask('q1')
    bridge.ask('q2')
    first = bridge.launched[0]
    second = bridge.launched[1]
    assert isinstance(first, _TextApp) and isinstance(second, _TextApp)
    assert 'once' in first._messages
    assert 'once' not in second._messages


def test_factory_console() -> None:
    """Without a terminal the factory returns the console bridge."""
    bridge = make_text_ui_bridge(StringIO(), StringIO(), StringIO())
    assert isinstance(bridge, WizardUiBridgeConsole)


def test_factory_textual() -> None:
    """With a terminal the factory returns the Textual bridge."""
    bridge = make_text_ui_bridge(_TtyStream(), _TtyStream(), _TtyStream())
    assert isinstance(bridge, WizardUiBridgeTextual)
