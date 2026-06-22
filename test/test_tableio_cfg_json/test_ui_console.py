#! /usr/bin/env python3
"""Tests for the console bridge variable-row ask_table editor."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from io import StringIO
from typing import Optional, Sequence

import pytest

from tableio_cfg_json import PartialCheck, TableCell, TableColumn, \
    WizardAbort, WizardBack, WizardCancelLevel, WizardUiBridgeConsole


# pylint: disable-next=too-many-arguments,too-many-positional-arguments
def _run_var(lines: list[str], columns: Sequence[TableColumn],
             cells: list[list[TableCell]], *, min_rows: int = 0,
             max_rows: int = 3, partial_check: Optional[PartialCheck] = None,
             re_ask_reason: Optional[str] = None
             ) -> tuple[list[list[Optional[str]]], str, str]:
    """Drive a console variable-row table with scripted answer lines."""
    stdin_file = StringIO('\n'.join(lines) + '\n')
    out_file = StringIO()
    err_file = StringIO()
    bridge = WizardUiBridgeConsole(out_file, stdin_file, err_file)
    result = bridge.ask_table(columns, cells, 'Q:', min_rows=min_rows,
                              max_rows=max_rows, partial_check=partial_check,
                              re_ask_reason=re_ask_reason)
    return result, out_file.getvalue(), err_file.getvalue()


def _two_text_rows() -> list[list[TableCell]]:
    """Return two single-column free-text rows for add/delete tests."""
    return [[TableCell(value='a')], [TableCell(value='b')]]


def test_var_keep() -> None:
    """Accepting straight away returns the pre-filled rows unchanged."""
    cols = (TableColumn('A'), TableColumn('B'))
    cells = [[TableCell(value='a'), TableCell(value='b')]]
    result, _, _ = _run_var([''], cols, cells)
    assert result == [['a', 'b']]


def test_var_edit() -> None:
    """A row number edits that row's cells; enter keeps a value."""
    cols = (TableColumn('A'), TableColumn('B'))
    cells = [[TableCell(value='a'), TableCell(value='b')]]
    result, _, _ = _run_var(['1', '', 'B2', ''], cols, cells)
    assert result == [['a', 'B2']]


def test_var_add() -> None:
    """:+ appends a row, edits it, and the new row is returned."""
    cols = (TableColumn('A'),)
    result, _, _ = _run_var([':+', 'c', ''], cols, _two_text_rows())
    assert result == [['a'], ['b'], ['c']]


def test_var_delete() -> None:
    """:- N deletes row N from the table."""
    cols = (TableColumn('A'),)
    result, _, _ = _run_var([':- 1', ''], cols, _two_text_rows())
    assert result == [['b']]


def test_var_add_max() -> None:
    """Adding past max_rows is refused and the count is unchanged."""
    cols = (TableColumn('A'),)
    result, _, err = _run_var([':+', ''], cols, _two_text_rows(), max_rows=2)
    assert result == [['a'], ['b']]
    assert 'At most 2 rows allowed.' in err


def test_var_del_min() -> None:
    """Deleting below min_rows is refused and the count is unchanged."""
    cols = (TableColumn('A'),)
    result, _, err = _run_var([':- 1', ''], cols, _two_text_rows(), min_rows=2)
    assert result == [['a'], ['b']]
    assert 'At least 2 rows required.' in err


def test_var_bad_menu() -> None:
    """An unrecognised menu token is rejected and the menu re-shown."""
    cols = (TableColumn('A'),)
    result, _, err = _run_var(['zzz', ''], cols, [[TableCell(value='a')]])
    assert result == [['a']]
    assert 'Enter a row number' in err


def test_var_bad_del() -> None:
    """A delete of a non-existent row is rejected with guidance."""
    cols = (TableColumn('A'),)
    result, _, err = _run_var([':- 9', ''], cols, [[TableCell(value='a')]])
    assert result == [['a']]
    assert 'Type :- followed by a row number' in err


def test_var_choice() -> None:
    """A choice cell accepts a one-based menu number."""
    cols = (TableColumn('A'),)
    cells = [[TableCell(value='x', choices=('x', 'y', 'z'))]]
    result, out, _ = _run_var(['1', '2', ''], cols, cells)
    assert result == [['y']]
    assert '2: y' in out


def test_var_overview() -> None:
    """The whole table is shown each round with row numbers."""
    cols = (TableColumn('A'), TableColumn('B'))
    cells = [[TableCell(value='a'), TableCell(value='b')]]
    _, out, _ = _run_var([''], cols, cells)
    assert '#' in out
    assert 'A' in out and 'B' in out
    overview = [line for line in out.splitlines() if line.startswith('1')]
    assert overview and 'a' in overview[0] and 'b' in overview[0]


def test_var_reask() -> None:
    """An initial re-ask reason is shown with the first menu."""
    cols = (TableColumn('A'),)
    _, _, err = _run_var([''], cols, [[TableCell(value='a')]],
                         re_ask_reason='retry me')
    assert 'retry me' in err


def test_var_check() -> None:
    """A partial check re-asks an edited cell until it is accepted."""
    cols = (TableColumn('A'),)
    cells = [[TableCell()]]

    def check(table: list[list[Optional[str]]],
              position: tuple[int, int]) -> tuple[bool, str]:
        value = table[position[0]][position[1]]
        return (False, 'no good') if value == 'bad' else (True, '')
    result, _, err = _run_var(['1', 'bad', 'ok', ''], cols, cells,
                              partial_check=check)
    assert result == [['ok']]
    assert 'no good' in err


def test_var_back_menu() -> None:
    """Back from a row's first cell returns to the menu, not out."""
    cols = (TableColumn('A'),)
    _, out, _ = _run_var(['1', ':b', ''], cols, [[TableCell(value='a')]])
    assert out.count('Q:') >= 2


def test_var_back_cell() -> None:
    """Back from a later cell re-asks the previous cell of the row."""
    cols = (TableColumn('A'), TableColumn('B'))
    cells = [[TableCell(value='a'), TableCell(value='b')]]
    result, _, _ = _run_var(['1', 'X', ':b', 'Y', 'Z', ''], cols, cells)
    assert result == [['Y', 'Z']]


def test_var_ro_added() -> None:
    """A read-only column becomes editable in an added row."""
    cols = (TableColumn('P', read_only=True), TableColumn('V'))
    cells = [[TableCell(value='p1'), TableCell(value='x')]]
    result, _, _ = _run_var([':+', 'PZ', 'VZ', ''], cols, cells)
    assert result == [['p1', 'x'], ['PZ', 'VZ']]


@pytest.mark.parametrize('token, error', [
    (':b', WizardBack), (':c', WizardCancelLevel), (':q', WizardAbort)])
def test_var_nav(token: str, error: type[BaseException]) -> None:
    """Reserved navigation tokens at the menu raise their requests."""
    cols = (TableColumn('A'),)
    cells = [[TableCell(value='a')]]
    bridge = WizardUiBridgeConsole(StringIO(), StringIO(token + '\n'),
                                   StringIO())
    with pytest.raises(error):
        bridge.ask_table(cols, cells, 'Q:', min_rows=0, max_rows=3)


def test_var_empty_start() -> None:
    """A table that starts empty can grow a row and be accepted."""
    cols = (TableColumn('A'),)
    result, _, _ = _run_var([':+', 'first', ''], cols, [])
    assert result == [['first']]


def test_var_min_only() -> None:
    """Only one bound given keeps the fixed-row, cell-by-cell behavior."""
    cols = (TableColumn('A'),)
    cells = [[TableCell(value='a')]]
    stdin_file = StringIO('\n')
    bridge = WizardUiBridgeConsole(StringIO(), stdin_file, StringIO())
    result = bridge.ask_table(cols, cells, 'Q:', min_rows=5)
    assert result == [['a']]
