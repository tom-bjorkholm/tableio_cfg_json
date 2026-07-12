#! /usr/bin/env python3
"""Tests for the Textual table screen and its variable-row editor."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

# pylint: disable=protected-access

import asyncio
from typing import Optional

import pytest
from tableio_cfg_json import TableCell, TableColumn, WizardBack, \
    WizardCancelLevel
from tableio_cfg_json.wizard_ui_bridge_textual import _TableApp, \
    _parse_cell_id
from tableio_cfg_json.wizard_ui_bridge_table import _new_row_template
from .ui_textual_support import drive, _CannedBridge


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


def test_parse_cell_id() -> None:
    """A cell id parses to its position; other ids parse to None."""
    assert _parse_cell_id('cell_2_3') == (2, 3)
    assert _parse_cell_id(None) is None
    assert _parse_cell_id('submit') is None


def test_make_select_nonnull() -> None:
    """A non-nullable empty drop-down defaults to its first choice."""
    columns = (TableColumn('Value'),)
    cells = [[TableCell(choices=('x', 'y'))]]
    driven = drive(_TableApp(columns, cells, 'q', [], None), ['ctrl+s'])
    assert driven.return_value == [['x']]


def test_focus_empty_rows() -> None:
    """A table with no rows mounts and submits an empty result."""
    columns = (TableColumn('Value'),)
    driven = drive(_TableApp(columns, [], 'q', [], None, 0, 2), ['ctrl+s'])
    assert driven.return_value == []


def test_focus_all_readonly() -> None:
    """A first row of only read-only cells leaves nothing focused."""
    columns = (TableColumn('P', read_only=True),)
    cells = [[TableCell(value='x')]]
    driven = drive(_TableApp(columns, cells, 'q', [], None), ['ctrl+s'])
    assert driven.return_value == [['x']]


def test_recheck_none() -> None:
    """A cell change with no parsed position is ignored."""
    columns = (TableColumn('Value'),)
    app = _TableApp(columns, [[TableCell(value='a')]], 'q', [], None)
    app._recheck(None)
    assert app._table == [['a']]


def test_add_past_max() -> None:
    """Adding beyond max_rows is refused and the row count holds."""
    columns = (TableColumn('Value'),)
    cells = [[TableCell(value='a')]]
    app = _TableApp(columns, cells, 'q', [], None, 1, 2)

    async def scenario() -> int:
        async with app.run_test() as pilot:
            app._add_row()
            await pilot.pause()
            app._add_row()
            await pilot.pause()
            return len(app._rows)
    assert asyncio.run(scenario()) == 2
