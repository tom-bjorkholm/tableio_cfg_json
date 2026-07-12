#! /usr/bin/env python3
"""Tests for the wizard UI bridge answer interpreters.

These cover how the console and scripted bridges map raw answers to
choices, multi-choices, yes/no values, integers and table cells,
independent of the wizard flow that drives them.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

# pylint: disable=protected-access

from io import StringIO
from typing import Optional

import pytest

from tableio_cfg_json import WizardUiBridgeConsole, TableCell, TableColumn, \
    WizardAbort, WizardBack, WizardCancelLevel, WizardNavigation
from tableio_cfg_json.wizard_ui_bridge import _INT_ERROR
from .wizard_support import _ScriptedBridge


@pytest.mark.parametrize('answer, default, expected', [
    ('', True, True), ('', False, False), (0, False, True), (1, True, False),
    ('y', False, True), ('no', True, False), ('TRUE', False, True),
    ('n', True, False)])
def test_yes_no_fallback(answer: str | int, default: bool,
                         expected: bool) -> None:
    """ask_yes_no maps scripted bridge answers to booleans."""
    bridge = _ScriptedBridge([answer])
    assert bridge.ask_yes_no('OK?', default) is expected


def test_yes_no_retry() -> None:
    """ask_yes_no re-asks until it understands the answer."""
    bridge = _ScriptedBridge(['maybe', 'yes'])
    assert bridge.ask_yes_no('OK?', False) is True
    assert bridge.calls[1][1] == 'Please answer yes or no.'


@pytest.mark.parametrize('token, error', [
    (':b', WizardBack), (':c', WizardCancelLevel), (':q', WizardAbort)])
def test_console_nav_tokens(token: str, error: type[BaseException]) -> None:
    """Console reserved tokens raise the matching navigation request."""
    bridge = WizardUiBridgeConsole(StringIO(), StringIO(token + '\n'),
                                   StringIO())
    with pytest.raises(error):
        bridge.ask_text('Question?')


def test_descriptor_defaults() -> None:
    """Table descriptors default to editable free-text non-null cells."""
    column = TableColumn('Value')
    cell = TableCell()
    assert column.read_only is False
    assert (cell.value, cell.choices, cell.nullable) == (None, None, False)


def test_table_keep_and_erase() -> None:
    """ask_table keeps a value on enter and erases on the token."""
    columns = (TableColumn('Parameter', read_only=True), TableColumn('Value'))
    cells = [[TableCell(value='impl'), TableCell(value='Lib', nullable=True)]]
    keep = _ScriptedBridge(['']).ask_table(columns, cells, 'Pick:')
    erase = _ScriptedBridge([':e']).ask_table(columns, cells, 'Pick:')
    assert keep == [['impl', 'Lib']]
    assert erase == [['impl', None]]


def test_table_partial_check() -> None:
    """ask_table re-asks a cell until the partial check passes."""
    columns = (TableColumn('Value'),)
    cells = [[TableCell(nullable=True)]]

    def check(table: list[list[Optional[str]]],
              position: tuple[int, int]) -> tuple[bool, str]:
        value = table[position[0]][position[1]]
        return (False, 'no good') if value == 'bad' else (True, '')
    bridge = _ScriptedBridge(['bad', 'good'])
    result = bridge.ask_table(columns, cells, 'Enter:', partial_check=check)
    assert result == [['good']]
    assert bridge.calls[1][1] == 'no good'


def test_ask_choice_index() -> None:
    """ask_choice maps a 0-based answer index to a choice."""
    bridge = _ScriptedBridge([1])
    assert bridge.ask_choice('Pick:', choices=('a', 'b', 'c')) == 'b'


def test_ask_choice_default() -> None:
    """An empty answer selects the default choice."""
    bridge = _ScriptedBridge([''])
    assert bridge.ask_choice('Pick:', choices=('a', 'b'), default='a') == 'a'


def test_ask_choice_required() -> None:
    """With no default an empty answer is rejected and re-asked."""
    bridge = _ScriptedBridge(['', 0])
    assert bridge.ask_choice('Pick:', choices=('a', 'b')) == 'a'
    assert bridge.calls[1][1] == 'Please enter one of the listed choices.'


def test_ask_choice_prefix() -> None:
    """ask_choice accepts a unique name prefix."""
    bridge = _ScriptedBridge(['ban'])
    assert bridge.ask_choice('Pick:', choices=('apple', 'banana')) == 'banana'


def test_ask_choice_nav() -> None:
    """A navigation request raised inside ask_choice propagates."""
    bridge = _ScriptedBridge([WizardBack()])
    with pytest.raises(WizardBack):
        bridge.ask_choice('Pick:', choices=('a', 'b'))


def test_console_choice_num() -> None:
    """The console choice menu maps a 1-based number to a choice."""
    bridge = WizardUiBridgeConsole(StringIO(), StringIO('2\n'), StringIO())
    assert bridge.ask_choice('Pick:', choices=('a', 'b', 'c')) == 'b'


def test_console_choice_def() -> None:
    """The console choice menu marks and selects the default."""
    out = StringIO()
    bridge = WizardUiBridgeConsole(out, StringIO('\n'), StringIO())
    assert bridge.ask_choice('Pick:', choices=('a', 'b'), default='b') == 'b'
    assert 'b (default)' in out.getvalue()


def test_ask_multi_basic() -> None:
    """ask_multi returns chosen items in choices order."""
    bridge = _ScriptedBridge(['0,2'])
    assert bridge.ask_multi('Pick:', choices=('a', 'b', 'c')) == ['a', 'c']


def test_ask_multi_names() -> None:
    """ask_multi accepts names and orders them by choices."""
    bridge = _ScriptedBridge(['b , a'])
    assert bridge.ask_multi('Pick:', choices=('a', 'b', 'c')) == ['a', 'b']


def test_ask_multi_dedupe() -> None:
    """ask_multi drops duplicate selections."""
    bridge = _ScriptedBridge(['2,0,0'])
    assert bridge.ask_multi('Pick:', choices=('a', 'b', 'c')) == ['a', 'c']


def test_ask_multi_default() -> None:
    """An empty multi answer selects the default set."""
    bridge = _ScriptedBridge([''])
    result = bridge.ask_multi('Pick:', choices=('a', 'b'), default=('b',))
    assert result == ['b']


def test_ask_multi_empty() -> None:
    """An empty multi answer with no default selects nothing."""
    bridge = _ScriptedBridge([''])
    assert bridge.ask_multi('Pick:', choices=('a', 'b')) == []


def test_ask_multi_min() -> None:
    """Too few selections are rejected and re-asked."""
    bridge = _ScriptedBridge(['0', '0,1'])
    result = bridge.ask_multi('Pick:', choices=('a', 'b'), min_select=2)
    assert result == ['a', 'b']
    assert bridge.calls[1][1] == 'Please select at least 2.'


def test_ask_multi_exact() -> None:
    """An exact-count requirement reports the exact message."""
    bridge = _ScriptedBridge(['0', '0,1'])
    result = bridge.ask_multi('Pick:', choices=('a', 'b'), min_select=2,
                              max_select=2)
    assert result == ['a', 'b']
    assert bridge.calls[1][1] == 'Please select exactly 2.'


def test_ask_multi_max() -> None:
    """Too many selections are rejected and re-asked."""
    bridge = _ScriptedBridge(['0,1', '1'])
    result = bridge.ask_multi('Pick:', choices=('a', 'b'), max_select=1)
    assert result == ['b']
    assert bridge.calls[1][1] == 'Please select between 0 and 1.'


def test_ask_multi_bad_token() -> None:
    """An unmatched token is rejected and the answer is re-asked."""
    bridge = _ScriptedBridge(['x', '0'])
    assert bridge.ask_multi('Pick:', choices=('a', 'b')) == ['a']
    assert bridge.calls[1][1] == 'Please enter one of the listed choices.'


def test_console_multi() -> None:
    """The console multi menu maps 1-based numbers to choices."""
    bridge = WizardUiBridgeConsole(StringIO(), StringIO('1,3\n'), StringIO())
    assert bridge.ask_multi('Pick:', choices=('a', 'b', 'c')) == ['a', 'c']


def test_ask_table_reask() -> None:
    """ask_table shows a re-ask reason above the table."""
    columns = (TableColumn('Value'),)
    cells = [[TableCell(value='x')]]
    bridge = _ScriptedBridge([''])
    bridge.ask_table(columns, cells, 'Pick:', re_ask_reason='try again')
    assert 'try again' in bridge.messages


def test_cell_bool_invalid() -> None:
    """A boolean cell answer is rejected and the cell is re-asked."""
    columns = (TableColumn('Value'),)
    cells = [[TableCell()]]
    bridge = _ScriptedBridge([True, 'ok'])
    assert bridge.ask_table(columns, cells, 'Pick:') == [['ok']]
    assert bridge.calls[1][1] == 'Please enter a value.'


@pytest.mark.parametrize('answer', [True, False])
def test_yes_no_bool(answer: bool) -> None:
    """A boolean bridge answer maps straight to that boolean."""
    bridge = _ScriptedBridge([answer])
    assert bridge.ask_yes_no('OK?', not answer) is answer


def test_yes_no_bad_index() -> None:
    """An out-of-range index answer is re-asked as yes or no."""
    bridge = _ScriptedBridge([7, 0])
    assert bridge.ask_yes_no('OK?', False) is True
    assert bridge.calls[1][1] == 'Please answer yes or no.'


def test_erase_freetext() -> None:
    """Erasing a non-nullable free-text cell yields an empty string."""
    columns = (TableColumn('Value'),)
    cells = [[TableCell(value='x')]]
    bridge = _ScriptedBridge([':e'])
    assert bridge.ask_table(columns, cells, 'Pick:') == [['']]


def test_erase_choice() -> None:
    """Erasing a non-nullable choice cell is rejected and re-asked."""
    columns = (TableColumn('Value'),)
    cells = [[TableCell(choices=('a', 'b'))]]
    bridge = _ScriptedBridge([':e', 0])
    assert bridge.ask_table(columns, cells, 'Pick:') == [['a']]
    assert bridge.calls[1][1] == 'Please enter a value.'


def test_cell_index_oob() -> None:
    """An out-of-range choice index is rejected and the cell re-asked."""
    columns = (TableColumn('Value'),)
    cells = [[TableCell(choices=('a', 'b'))]]
    bridge = _ScriptedBridge([9, 1])
    assert bridge.ask_table(columns, cells, 'Pick:') == [['b']]
    assert bridge.calls[1][1] == 'Please enter a value.'


def test_multi_bool() -> None:
    """A boolean multi answer is rejected and the answer re-asked."""
    bridge = _ScriptedBridge([True, '0'])
    assert bridge.ask_multi('Pick:', choices=('a', 'b')) == ['a']
    assert bridge.calls[1][1] == 'Please enter one of the listed choices.'


def test_multi_int_index() -> None:
    """A single integer multi answer selects that one choice."""
    bridge = _ScriptedBridge([1])
    assert bridge.ask_multi('Pick:', choices=('a', 'b', 'c')) == ['b']


def test_multi_int_oob() -> None:
    """An out-of-range integer multi answer is re-asked."""
    bridge = _ScriptedBridge([9, '0'])
    assert bridge.ask_multi('Pick:', choices=('a', 'b')) == ['a']
    assert bridge.calls[1][1] == 'Please enter one of the listed choices.'


def test_multi_empty_token() -> None:
    """Empty tokens between commas are ignored in a multi answer."""
    bridge = _ScriptedBridge(['0,,1'])
    assert bridge.ask_multi('Pick:', choices=('a', 'b')) == ['a', 'b']


@pytest.mark.parametrize('answer, expected', [
    ('42', 42), (' 7 ', 7), ('-3', -3), ('+5', 5), ('1_000', 1000)])
def test_ask_int_value(answer: str, expected: int) -> None:
    """ask_int parses a single integer answer like Python int()."""
    bridge = _ScriptedBridge([answer])
    assert bridge.ask_int('How many?') == expected


def test_ask_int_null() -> None:
    """A nullable empty answer is reported as None."""
    bridge = _ScriptedBridge([''])
    assert bridge.ask_int('How many?', nullable=True) is None


@pytest.mark.parametrize('first', ['', 'abc'])
def test_ask_int_bad(first: str) -> None:
    """An empty or non-integer answer is re-asked as not an integer."""
    bridge = _ScriptedBridge([first, '9'])
    assert bridge.ask_int('How many?') == 9
    assert bridge.calls[1][1] == _INT_ERROR


@pytest.mark.parametrize(
    'answers, min_value, max_value, expected, reason', [
        (['0', '5'], 1, 10, 5, 'between 1 and 10'),
        (['11', '4'], 1, 10, 4, 'between 1 and 10'),
        (['0', '3'], 1, None, 3, 'at least 1'),
        (['11', '7'], None, 10, 7, 'at most 10'),
        (['1'], 1, 10, 1, None),
        (['10'], 1, 10, 10, None)])
def test_ask_int_range(answers: list[str], min_value: Optional[int],
                       max_value: Optional[int], expected: int,
                       reason: Optional[str]) -> None:
    """Values outside the inclusive bounds are re-asked with a reason."""
    bridge = _ScriptedBridge(answers)
    result = bridge.ask_int('How many?', min_value=min_value,
                            max_value=max_value)
    assert result == expected
    if reason is None:
        assert bridge.calls[0][1] is None
    else:
        assert reason in (bridge.calls[1][1] or '')


def test_ask_int_reason() -> None:
    """A given re_ask_reason is shown on the first prompt."""
    bridge = _ScriptedBridge(['5'])
    assert bridge.ask_int('How many?', 'Was rejected.') == 5
    assert bridge.calls[0][1] == 'Was rejected.'


@pytest.mark.parametrize('error', [
    WizardBack(), WizardCancelLevel(), WizardAbort()])
def test_ask_int_nav(error: WizardNavigation) -> None:
    """Navigation requests propagate out of ask_int."""
    bridge = _ScriptedBridge([error])
    with pytest.raises(type(error)):
        bridge.ask_int('How many?')


def test_ask_int_minmax() -> None:
    """ask_int rejects a min_value above max_value."""
    bridge = _ScriptedBridge([])
    with pytest.raises(AssertionError):
        bridge.ask_int('How many?', min_value=5, max_value=3)
