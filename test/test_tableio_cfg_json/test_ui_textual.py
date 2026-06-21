#! /usr/bin/env python3
"""Tests for the Textual user interface bridge and its factory."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

# pylint: disable=protected-access

import asyncio
from io import StringIO
from typing import Any, Optional, Sequence

import pytest

from tableio_cfg_json import TableCell, TableColumn, WizardAbort, \
    WizardBack, WizardCancelLevel, WizardNavigation, WizardUiBridgeConsole, \
    WizardUiBridgeTextual, make_text_ui_bridge
from tableio_cfg_json.wizard_ui_bridge_textual import _ChoiceApp, _MultiApp, \
    _NavApp, _TableApp, _TextApp, _new_row_template


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


def test_table_prefilled() -> None:
    """Submitting unchanged returns the pre-filled cells and headers."""
    columns = (TableColumn('Parameter', read_only=True),
               TableColumn('Value'))
    cells = [[TableCell(value='alpha'), TableCell(value='one')],
             [TableCell(value='beta'),
              TableCell(value='y', choices=('x', 'y'), nullable=True)]]
    driven = drive(_TableApp(columns, cells, 'q', [], None), ['ctrl+s'])
    assert driven.return_value == [['alpha', 'one'], ['beta', 'y']]


def test_table_clear_null() -> None:
    """A cleared nullable text cell is reported as None."""
    columns = (TableColumn('Value'),)
    cells = [[TableCell(value='one', nullable=True)]]
    driven = drive(_TableApp(columns, cells, 'q', [], None),
                   ['end', 'ctrl+u', 'ctrl+s'])
    assert driven.return_value == [[None]]


def test_table_empty_freetext() -> None:
    """A cleared non-nullable text cell is reported as an empty string."""
    columns = (TableColumn('Value'),)
    cells = [[TableCell(value='one')]]
    driven = drive(_TableApp(columns, cells, 'q', [], None),
                   ['end', 'ctrl+u', 'ctrl+s'])
    assert driven.return_value == [['']]


def test_table_select_blank() -> None:
    """A nullable drop-down left blank is reported as None."""
    columns = (TableColumn('Value'),)
    cells = [[TableCell(choices=('x', 'y'), nullable=True)]]
    driven = drive(_TableApp(columns, cells, 'q', [], None), ['ctrl+s'])
    assert driven.return_value == [[None]]


def test_table_select_pick() -> None:
    """Choosing a drop-down option returns that choice."""
    columns = (TableColumn('Value'),)
    cells = [[TableCell(choices=('x', 'y'), nullable=True)]]
    driven = drive(_TableApp(columns, cells, 'q', [], None),
                   ['enter', 'down', 'enter', 'ctrl+s'])
    assert driven.return_value == [['x']]


def test_table_nav_back() -> None:
    """ctrl+b in the table records a back request and exits."""
    columns = (TableColumn('Value'),)
    cells = [[TableCell(value='one')]]
    driven = drive(_TableApp(columns, cells, 'q', [], None), ['ctrl+b'])
    assert driven.return_value is None
    assert driven.nav is WizardBack


def test_table_partial_check() -> None:
    """The partial check sees each cell change with the changed position."""
    columns = (TableColumn('Value'),)
    cells = [[TableCell(nullable=True)]]
    calls: list[tuple[list[list[Optional[str]]], tuple[int, int]]] = []

    def check(table: list[list[Optional[str]]],
              position: tuple[int, int]) -> tuple[bool, str]:
        calls.append(([row[:] for row in table], position))
        value = table[position[0]][position[1]]
        return (value != 'bad', '' if value != 'bad' else 'no good')
    app = _TableApp(columns, cells, 'q', [], check)
    driven = drive(app, ['b', 'a', 'd', 'end', 'ctrl+u', 'o', 'k', 'ctrl+s'])
    assert driven.return_value == [['ok']]
    assert ([['bad']], (0, 0)) in calls
    assert ([['ok']], (0, 0)) in calls


def test_ask_table_canned() -> None:
    """ask_table() returns the table the screen produced."""
    columns = (TableColumn('Value'),)
    cells = [[TableCell(value='one')]]
    bridge = _CannedBridge([[['one']]])
    assert bridge.ask_table(columns, cells, 'q') == [['one']]


def test_ask_table_nav() -> None:
    """ask_table() re-raises a navigation request from the screen."""
    columns = (TableColumn('Value'),)
    cells = [[TableCell(value='one')]]
    bridge = _CannedBridge([WizardCancelLevel])
    with pytest.raises(WizardCancelLevel):
        bridge.ask_table(columns, cells, 'q')


def test_new_row_uniform() -> None:
    """A new row keeps the members shared across each template column."""
    columns = (TableColumn('P', read_only=True), TableColumn('V'))
    cells = [[TableCell(value='p', choices=('a', 'b'), nullable=True),
              TableCell(value='x', choices=('a', 'b'), nullable=True)],
             [TableCell(value='p', choices=('a', 'b'), nullable=True),
              TableCell(value='y', choices=('a', 'b'), nullable=True)]]
    new_row = _new_row_template(columns, cells)
    assert new_row[0].value == 'p'
    assert new_row[0].choices == ('a', 'b')
    assert new_row[0].nullable is True
    assert new_row[1].value == ''
    assert new_row[1].choices == ('a', 'b')


def test_new_row_defaults() -> None:
    """Differing template members fall back to '', None and False."""
    columns = (TableColumn('V'),)
    cells = [[TableCell(value='x', choices=('a',), nullable=True)],
             [TableCell(value='y', choices=('a', 'b'), nullable=False)]]
    new_row = _new_row_template(columns, cells)
    assert new_row[0].value == ''
    assert new_row[0].choices is None
    assert new_row[0].nullable is False


def test_new_row_none() -> None:
    """A uniformly None value stays None in added rows."""
    columns = (TableColumn('V'),)
    cells = [[TableCell(value=None, nullable=True)],
             [TableCell(value=None, nullable=True)]]
    new_row = _new_row_template(columns, cells)
    assert new_row[0].value is None
    assert new_row[0].nullable is True


def test_table_add_row() -> None:
    """Adding a row, filling it, and submitting returns the new row."""
    columns = (TableColumn('V'),)
    cells = [[TableCell(value='a')], [TableCell(value='b')]]
    app = _TableApp(columns, cells, 'q', [], None, 2, 4)

    async def scenario() -> None:
        async with app.run_test() as pilot:
            await pilot.click('#add_row')
            await pilot.pause()
            app.query_one('#cell_2_0').focus()
            await pilot.press('c')
            await pilot.click('#submit')
    asyncio.run(scenario())
    assert app.return_value == [['a'], ['b'], ['c']]


def test_add_row_readonly() -> None:
    """A read-only column becomes editable in an added row."""
    columns = (TableColumn('P', read_only=True), TableColumn('V'))
    cells = [[TableCell(value='p1'), TableCell(value='x')],
             [TableCell(value='p2'), TableCell(value='y')]]
    app = _TableApp(columns, cells, 'q', [], None, 2, 4)

    async def scenario() -> None:
        async with app.run_test() as pilot:
            await pilot.click('#add_row')
            await pilot.pause()
            app.query_one('#cell_2_0').focus()
            await pilot.press('z')
            await pilot.click('#submit')
    asyncio.run(scenario())
    assert app.return_value == [['p1', 'x'], ['p2', 'y'], ['z', '']]


def test_table_remove_row() -> None:
    """Removing the last row drops it from the result."""
    columns = (TableColumn('V'),)
    cells = [[TableCell(value='a')], [TableCell(value='b')]]
    app = _TableApp(columns, cells, 'q', [], None, 1, 3)

    async def scenario() -> None:
        async with app.run_test() as pilot:
            await pilot.click('#remove_row')
            await pilot.pause()
            await pilot.click('#submit')
    asyncio.run(scenario())
    assert app.return_value == [['a']]


def test_table_row_bounds() -> None:
    """The table will not shrink below min_rows or grow past max_rows."""
    columns = (TableColumn('V'),)
    cells = [[TableCell(value='a')]]
    app = _TableApp(columns, cells, 'q', [], None, 1, 2)

    async def scenario() -> None:
        async with app.run_test() as pilot:
            await pilot.click('#remove_row')
            await pilot.pause()
            await pilot.click('#add_row')
            await pilot.pause()
            await pilot.click('#add_row')
            await pilot.pause()
            await pilot.click('#submit')
    asyncio.run(scenario())
    result = app.return_value
    assert result is not None
    assert len(result) == 2


def test_fixed_no_buttons() -> None:
    """A fixed table has no Add row or Remove row button."""
    columns = (TableColumn('V'),)
    cells = [[TableCell(value='a')]]
    app = _TableApp(columns, cells, 'q', [], None)

    async def scenario() -> tuple[int, int]:
        async with app.run_test():
            return (len(app.query('#add_row')), len(app.query('#remove_row')))
    assert asyncio.run(scenario()) == (0, 0)


def test_ask_table_variable() -> None:
    """ask_table passes the row bounds through to the table screen."""
    columns = (TableColumn('V'),)
    cells = [[TableCell(value='a')]]
    bridge = _CannedBridge([[['a']]])
    bridge.ask_table(columns, cells, 'q', min_rows=1, max_rows=3)
    app = bridge.launched[0]
    assert isinstance(app, _TableApp)
    assert app._variable is True
    assert (app._min_rows, app._max_rows) == (1, 3)
