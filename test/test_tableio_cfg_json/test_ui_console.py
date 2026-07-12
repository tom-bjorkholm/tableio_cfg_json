#! /usr/bin/env python3
"""Tests for the console user interface bridge.

This covers the console bridge variable-row ask_table editor and the
console yes/no question. Other console ask methods are tested in
test_wizard.py alongside the wizard that drives them.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import getpass
from io import StringIO
from typing import Callable, Optional, Sequence

import pytest

from tableio_cfg_json import AskField, AskChoiceField, AskIntField, \
    AskMultiChoiceField, AskTextField, AskYesNoField, PartialFormValidator, \
    PartialCheck, TableCell, TableColumn, \
    WizardAbort, WizardBack, WizardCancelLevel, WizardUiBridgeConsole
from tableio_cfg_json import AnswerField, PartFormValidationResult


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


def test_var_below_min() -> None:
    """Accepting below min_rows is refused until a row is added."""
    cols = (TableColumn('A'),)
    result, _, err = _run_var(['', ':+', 'c', ''], cols,
                              [[TableCell(value='a')]], min_rows=2)
    assert result == [['a'], ['c']]
    assert 'Please keep at least 2 rows.' in err


def test_var_above_max() -> None:
    """Accepting above max_rows is refused until a row is deleted."""
    cols = (TableColumn('A'),)
    cells = [[TableCell(value='a')], [TableCell(value='b')],
             [TableCell(value='c')]]
    result, _, err = _run_var(['', ':- 1', ''], cols, cells, max_rows=2)
    assert result == [['b'], ['c']]
    assert 'Please keep at most 2 rows.' in err


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


def test_var_del_nonnum() -> None:
    """A :- with a non-numeric row argument is rejected with guidance."""
    cols = (TableColumn('A'),)
    result, _, err = _run_var([':- x', ''], cols, [[TableCell(value='a')]])
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


def test_text_default() -> None:
    """An empty console text answer selects the shown default."""
    out_file = StringIO()
    bridge = WizardUiBridgeConsole(out_file, StringIO('\n'), StringIO())
    assert bridge.ask_text('Name?', default='Tom') == 'Tom'
    assert 'Name? [Tom]' in out_file.getvalue()


def test_text_default_overridden() -> None:
    """An explicit console text answer overrides the default."""
    bridge = WizardUiBridgeConsole(StringIO(), StringIO('Ada\n'), StringIO())
    assert bridge.ask_text('Name?', default='Tom') == 'Ada'


def test_text_nullable() -> None:
    """An empty nullable text answer with no default returns None."""
    bridge = WizardUiBridgeConsole(StringIO(), StringIO('\n'), StringIO())
    assert bridge.ask_text('Name?', nullable=True) is None


def test_text_sensitive_default() -> None:
    """Sensitive text questions reject defaults."""
    bridge = WizardUiBridgeConsole(StringIO(), StringIO('\n'), StringIO())
    with pytest.raises(ValueError, match='default'):
        bridge.ask_text('Password?', default='secret', sensitive=True)


def test_text_sensitive_scripted() -> None:
    """Scripted sensitive text is read without being printed."""
    out_file = StringIO()
    bridge = WizardUiBridgeConsole(out_file, StringIO('secret\n'), StringIO())
    assert bridge.ask_text('Password?', sensitive=True) == 'secret'
    assert 'secret' not in out_file.getvalue()


def test_text_sensitive_nav() -> None:
    """A navigation token also works at a sensitive text question."""
    bridge = WizardUiBridgeConsole(StringIO(), StringIO(':q\n'), StringIO())
    with pytest.raises(WizardAbort):
        bridge.ask_text('Password?', sensitive=True)


def test_int_default() -> None:
    """The inherited integer question uses console text defaults."""
    out_file = StringIO()
    bridge = WizardUiBridgeConsole(out_file, StringIO('\n'), StringIO())
    assert bridge.ask_int('Count?', default=7) == 7
    assert 'Count? [7]' in out_file.getvalue()


@pytest.mark.parametrize('answer, default, expected', [
    ('1', False, True), ('2', True, False), ('', True, True),
    ('', False, False), ('yes', False, True), ('no', True, False),
    ('y', False, True), ('n', True, False), ('true', False, True),
    ('false', True, False)])
def test_yes_no_map(answer: str, default: bool, expected: bool) -> None:
    """The console yes/no menu maps numbers, text and blank to a bool."""
    bridge = WizardUiBridgeConsole(StringIO(), StringIO(answer + '\n'),
                                   StringIO())
    assert bridge.ask_yes_no('OK?', default) is expected


def test_yes_no_retry() -> None:
    """An unrecognised console yes/no answer re-asks with guidance."""
    out = StringIO()
    err = StringIO()
    bridge = WizardUiBridgeConsole(out, StringIO('3\nyes\n'), err)
    assert bridge.ask_yes_no('OK?', False) is True
    assert '1: yes' in out.getvalue()
    assert '2: no' in out.getvalue()
    assert 'Please answer yes or no.' in err.getvalue()


@pytest.mark.parametrize('token, error', [
    (':b', WizardBack), (':c', WizardCancelLevel), (':q', WizardAbort)])
def test_yes_no_nav(token: str, error: type[BaseException]) -> None:
    """A reserved token at a console yes/no question navigates."""
    bridge = WizardUiBridgeConsole(StringIO(), StringIO(token + '\n'),
                                   StringIO())
    with pytest.raises(error):
        bridge.ask_yes_no('OK?', True)


def _console(lines: str) -> tuple[WizardUiBridgeConsole, StringIO]:
    """Return a console bridge scripted with lines and its output stream."""
    out_file = StringIO()
    bridge = WizardUiBridgeConsole(out_file, StringIO(lines), StringIO())
    return bridge, out_file


def _sample_form() -> list[AskField]:
    """Return one field of each kind for the console form tests."""
    return [AskTextField('Name', None),
            AskIntField('Age', None, default=30),
            AskYesNoField('Subscribe?', None, True),
            AskChoiceField('Color', None, choices=('red', 'green', 'blue')),
            AskMultiChoiceField('Tags', None, choices=('a', 'b', 'c'))]


def test_console_all_kinds() -> None:
    """The base ask_form drives every console typed question in order."""
    bridge, out_file = _console('Tom\n\n\ngreen\na,c\n')
    answers = bridge.ask_form('Please fill in', _sample_form())
    assert [answer.value for answer in answers] == \
        ['Tom', 30, True, 'green', ['a', 'c']]
    assert 'Please fill in' in out_file.getvalue()


def test_console_disable(toggle_fields: list[AskField],
                         toggle_validator: PartialFormValidator) -> None:
    """A disabled console field is skipped and keeps its start value."""
    bridge, _ = _console('2\n')
    answers = bridge.ask_form('H', toggle_fields,
                              partial_validator=toggle_validator)
    assert answers[0].value is False
    assert answers[1].value is None


def test_console_back() -> None:
    """A back request at a console form field re-asks the previous field."""
    fields = [AskTextField('A', None), AskTextField('B', None)]
    bridge, _ = _console('x\n:b\ny\nz\n')
    answers = bridge.ask_form('H', fields)
    assert [answer.value for answer in answers] == ['y', 'z']


def test_console_back_first() -> None:
    """A back request at the first console form field propagates out."""
    bridge, _ = _console(':b\n')
    with pytest.raises(WizardBack):
        bridge.ask_form('H', [AskTextField('A', None)])


class _Tty(StringIO):
    """A text stream that reports itself as an interactive terminal."""

    def isatty(self) -> bool:
        """Report the stream as a terminal to trigger hidden input."""
        return True


def _reply(reply: str) -> Callable[..., str]:
    """Return a getpass stand-in that yields a fixed reply."""
    def fake(prompt: str = '', stream: Optional[object] = None) -> str:
        """Ignore the prompt and stream and return the fixed reply."""
        _ = (prompt, stream)
        return reply
    return fake


def test_sensitive_tty(monkeypatch: pytest.MonkeyPatch) -> None:
    """On a real terminal sensitive text is read hidden via getpass."""
    monkeypatch.setattr(getpass, 'getpass', _reply('topsecret'))
    bridge = WizardUiBridgeConsole(StringIO(), _Tty(), StringIO())
    assert bridge.ask_text('Password?', sensitive=True) == 'topsecret'


def test_sensitive_tty_nav(monkeypatch: pytest.MonkeyPatch) -> None:
    """A navigation token typed at a hidden prompt still navigates."""
    monkeypatch.setattr(getpass, 'getpass', _reply(':q'))
    bridge = WizardUiBridgeConsole(StringIO(), _Tty(), StringIO())
    with pytest.raises(WizardAbort):
        bridge.ask_text('Password?', sensitive=True)


def test_fixed_table_back() -> None:
    """Back from a later cell of a fixed table re-asks the previous cell."""
    cols = (TableColumn('A'), TableColumn('B'))
    cells = [[TableCell(value='a'), TableCell(value='b')]]
    bridge = WizardUiBridgeConsole(StringIO(), StringIO('X\n:b\nY\nZ\n'),
                                   StringIO())
    assert bridge.ask_table(cols, cells, 'Q:') == [['Y', 'Z']]


def test_fixed_back_first() -> None:
    """Back from the first cell of a fixed table propagates the request."""
    cols = (TableColumn('A'),)
    cells = [[TableCell(value='a')]]
    bridge = WizardUiBridgeConsole(StringIO(), StringIO(':b\n'), StringIO())
    with pytest.raises(WizardBack):
        bridge.ask_table(cols, cells, 'Q:')


def _disable_second(answers: Sequence[AnswerField],
                    index: int) -> PartFormValidationResult:
    """Return a validator result that always disables the second field."""
    _ = (answers, index)
    return PartFormValidationResult(True, '', (1,))


def test_back_over_disabled() -> None:
    """Back past a disabled field re-asks the nearest enabled field."""
    fields = [AskTextField('A', None), AskTextField('B', None),
              AskTextField('C', None)]
    bridge, _ = _console('a\n:b\nA2\nc\n')
    answers = bridge.ask_form('H', fields, partial_validator=_disable_second)
    assert [answer.value for answer in answers] == ['A2', None, 'c']
