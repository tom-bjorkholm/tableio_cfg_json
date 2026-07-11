#! /usr/bin/env python3
"""Tests for the interactive TableIO JSON config wizard."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

# pylint: disable=protected-access

import sys
import warnings
from io import StringIO
from typing import Callable, Optional, Sequence

import pytest

from tableio import Capabilities, CsvDialect, FileAccess, \
    access_capabilities, add_access_capabilities, \
    list_implementations_tableio, list_registered_tableio
from tableio_cfg_json import TioJsonConfig, WizardUiBridge, \
    WizardUiBridgeConsole, get_config_member_names, tio_json_config_wizard, \
    TableCell, TableColumn, WizardAbort, WizardBack, WizardCancelLevel, \
    PartialCheck, WizardNavigation
from tableio_cfg_json.wizard_ui_bridge import _INT_ERROR
from tableio_cfg_json._wizard_ui_bridge_helpers import ask_many, ask_one, \
    ask_yes_no, run_table
import tableio_cfg_json.wizard as wizard_module


class _ScriptedBridge(WizardUiBridge):
    """Wizard UI bridge that returns scripted answers for tests.

    The bridge implements the typed ask methods directly, like a real
    bridge, by feeding scripted raw answers into the shared answer
    interpreters. A scripted answer that is an exception is raised
    instead, which lets tests drive navigation requests.
    """

    def __init__(self, answers: Sequence[str | int | BaseException]) -> None:
        """Store raw answers returned in order to the ask methods."""
        self.answers: list[str | int | BaseException] = list(answers)
        self.calls: list[
            tuple[str, Optional[str], Optional[tuple[str, ...]]]] = []
        self.messages: list[str] = []
        self.stderr_file = StringIO()

    def _next(self) -> str | int:
        """Return the next scripted answer, raising scripted exceptions."""
        if not self.answers:
            raise EOFError('No scripted answer left.')
        answer = self.answers.pop(0)
        if isinstance(answer, BaseException):
            raise answer
        return answer

    def _reader(self, question: str, choices: Optional[Sequence[str]]
                ) -> Callable[[Optional[str]], str | int]:
        """Return a reader that records each call and pops an answer."""
        choice_tuple = None if choices is None else tuple(choices)

        def read(reason: Optional[str]) -> str | int:
            self.calls.append((question, reason, choice_tuple))
            return self._next()
        return read

    def ask_text(self, question: str, re_ask_reason: Optional[str] = None,
                 nullable: bool = False, *, default: Optional[str] = None,
                 sensitive: bool = False) -> Optional[str]:
        """Return the next scripted answer as text."""
        if sensitive and default is not None:
            raise ValueError('default is not allowed for sensitive input')
        self.calls.append((question, re_ask_reason, None))
        answer = self._next()
        text = answer if isinstance(answer, str) else str(answer)
        if text == '' and default is not None:
            return default
        return None if (nullable and text == '') else text

    def ask_choice(self, question: str, *, choices: Sequence[str],
                   default: Optional[str] = None,
                   re_ask_reason: Optional[str] = None) -> str:
        """Pick one scripted choice; see WizardUiBridge.ask_choice."""
        return ask_one(self._reader(question, choices), choices, default,
                       re_ask_reason)

    # pylint: disable-next=too-many-arguments
    def ask_multi(self, question: str, *, choices: Sequence[str],
                  default: Optional[Sequence[str]] = None, min_select: int = 0,
                  max_select: Optional[int] = None,
                  re_ask_reason: Optional[str] = None) -> list[str]:
        """Pick several scripted choices; see WizardUiBridge.ask_multi."""
        return ask_many(self._reader(question, choices), choices, default,
                        min_select, max_select, re_ask_reason, one_based=False)

    def ask_yes_no(self, question: str, default: bool,
                   re_ask_reason: Optional[str] = None) -> bool:
        """Answer a scripted yes/no question; see ask_yes_no."""
        return ask_yes_no(self._reader(question, ('yes', 'no')), default,
                          re_ask_reason)

    # pylint: disable-next=too-many-arguments
    def ask_table(self, columns: Sequence[TableColumn],
                  cells: list[list[TableCell]], question: str, *,
                  re_ask_reason: Optional[str] = None,
                  partial_check: Optional[PartialCheck] = None,
                  min_rows: Optional[int] = None,
                  max_rows: Optional[int] = None) -> list[list[Optional[str]]]:
        """Fill a table from scripted answers; see ask_table."""
        _ = (min_rows, max_rows)
        return run_table(self._cell_reader, self.show, columns, cells,
                         question, re_ask_reason, partial_check)

    def _cell_reader(self, prompt: str, re_ask_reason: Optional[str] = None,
                     choices: Optional[Sequence[str]] = None) -> str | int:
        """Record one table-cell prompt and return the next answer."""
        choice_tuple = None if choices is None else tuple(choices)
        self.calls.append((prompt, re_ask_reason, choice_tuple))
        return self._next()

    def error_file(self) -> StringIO:
        """Return the stream used for validation diagnostics."""
        return self.stderr_file

    def show(self, message: str) -> None:
        """Store a shown message."""
        self.messages.append(message)


def _run_wizard(file_access: FileAccess, answer_lines: list[str]
                ) -> tuple[TioJsonConfig, str, str]:
    """Run the wizard with scripted answers."""
    stdin_file = StringIO('\n'.join(answer_lines) + '\n')
    stdout_file = StringIO()
    stderr_file = StringIO()
    ui_bridge = WizardUiBridgeConsole(stdout_file, stdin_file, stderr_file)
    capabilities = access_capabilities(file_access, error_file=stderr_file)
    config = tio_json_config_wizard(capabilities, file_access, ui_bridge)
    return config, stdout_file.getvalue(), stderr_file.getvalue()


def _run_bridge(file_access: FileAccess,
                ui_bridge: WizardUiBridge) -> TioJsonConfig:
    """Run the wizard through a supplied bridge."""
    capabilities = access_capabilities(file_access,
                                       error_file=ui_bridge.error_file())
    return tio_json_config_wizard(capabilities, file_access, ui_bridge)


def _wizard_lines(format_name: str, file_access: FileAccess,
                  impl_answer: Optional[str] = None,
                  member_answers: Optional[dict[str, list[str]]] = None
                  ) -> list[str]:
    """Return scripted answers for one format and optional member values."""
    capabilities = access_capabilities(file_access)
    match_caps = add_access_capabilities(file_access, capabilities)
    format_names = list_registered_tableio(capabilities=match_caps)
    impl_names = list_implementations_tableio(format_name=format_name,
                                              capabilities=match_caps)
    answer_map = {} if member_answers is None else member_answers
    lines = [_menu_number(format_name, format_names)]
    implementation = None
    if len(impl_names) > 1:
        impl_menu = (wizard_module._AUTO_IMPL,) + tuple(impl_names)
        lines.append('' if impl_answer is None else impl_answer)
        if impl_answer is not None and impl_answer != '':
            implementation = impl_menu[int(impl_answer) - 1]
    for member_name in _optional_names(format_name, file_access,
                                       implementation):
        lines.extend(answer_map.get(member_name, ['']))
    return lines


def _optional_names(format_name: str, file_access: FileAccess,
                    implementation: Optional[str]) -> tuple[str, ...]:
    """Return optional wizard member names for one scripted selection."""
    capabilities = access_capabilities(file_access)
    member_names = get_config_member_names(capabilities=capabilities,
                                           file_access=file_access,
                                           format_name=format_name,
                                           implementation=implementation)
    return tuple(name for name in member_names
                 if name not in ('format_name', 'implementation'))


def _menu_number(choice: str, choices: Sequence[str]) -> str:
    """Return the one-based menu number for a known choice."""
    return str(choices.index(choice) + 1)


def _format_index(format_name: str, file_access: FileAccess) -> int:
    """Return the 0-based index of one format for scripted answers."""
    capabilities = access_capabilities(file_access)
    match_caps = add_access_capabilities(file_access, capabilities)
    return list_registered_tableio(capabilities=match_caps).index(format_name)


def _member_answer_lines(format_name: str, file_access: FileAccess,
                         implementation: Optional[str] = None,
                         member_answers: Optional[dict[str, list[str | int]]]
                         = None) -> list[str | int]:
    """Return scripted answers for optional members."""
    answer_map = {} if member_answers is None else member_answers
    lines: list[str | int] = []
    for member_name in _optional_names(format_name, file_access,
                                       implementation):
        lines.extend(answer_map.get(member_name, ['']))
    return lines


def assert_csv_core(config: TioJsonConfig) -> None:
    """Assert the CSV option values shared by several wizard tests."""
    assert config.character_encoding == 'utf-8'
    assert config.csv is not None
    assert config.csv.dialect == CsvDialect.UNIX
    assert config.csv.delimiter == ';'


def test_public_api() -> None:
    """The wizard helper is exported from the package root."""
    assert callable(tio_json_config_wizard)
    assert WizardUiBridgeConsole is not None


def test_base_bridge_defaults() -> None:
    """The base UI bridge exposes default stream and abstract methods."""
    ui_bridge = WizardUiBridge()
    assert ui_bridge.error_file() is sys.stderr
    with pytest.raises(NotImplementedError, match='ask_text'):
        ui_bridge.ask_text('Question?')
    with pytest.raises(NotImplementedError, match='show'):
        ui_bridge.show('Message.')


def test_console_menu() -> None:
    """Console choice menus number choices and return the chosen one."""
    stdin_file = StringIO('2\n')
    stdout_file = StringIO()
    stderr_file = StringIO()
    ui_bridge = WizardUiBridgeConsole(stdout_file, stdin_file, stderr_file)
    answer = ui_bridge.ask_choice('Pick one:', choices=('first', 'second'))
    assert answer == 'second'
    assert '1: first' in stdout_file.getvalue()
    assert '2: second' in stdout_file.getvalue()
    assert stderr_file.getvalue() == ''


def test_console_show() -> None:
    """Console show writes the message to the configured output stream."""
    stdout_file = StringIO()
    ui_bridge = WizardUiBridgeConsole(stdout_file, StringIO(), StringIO())
    ui_bridge.show('Done.')
    assert stdout_file.getvalue() == 'Done.\n'


def test_wizard_csv_defaults() -> None:
    """Blank answers keep optional CSV settings out of compact JSON."""
    config, output, _ = _run_wizard(FileAccess.CREATE,
                                    _wizard_lines('CSV', FileAccess.CREATE))
    assert config.format_name == 'CSV'
    assert config.implementation is None
    assert config.csv is None
    assert 'Select TableIO format' in output
    assert 'Configure options for CSV' in output
    assert 'csv.delimiter' in output


def test_blank_impl() -> None:
    """Blank implementation keeps TableIO runtime selection enabled."""
    lines = _wizard_lines('Excel', FileAccess.READ, impl_answer='')
    config, output, _ = _run_wizard(FileAccess.READ, lines)
    assert config.format_name == 'Excel'
    assert config.implementation is None
    assert 'let TableIO choose (recommended)' in output


def test_lock_impl() -> None:
    """A numbered implementation answer stores that implementation."""
    capabilities = access_capabilities(FileAccess.READ)
    match_caps = add_access_capabilities(FileAccess.READ, capabilities)
    impl_names = list_implementations_tableio(format_name='Excel',
                                              capabilities=match_caps)
    impl_menu = (wizard_module._AUTO_IMPL,) + tuple(impl_names)
    impl_answer = _menu_number('OpenPyXL', impl_menu)
    lines = _wizard_lines('Excel', FileAccess.READ, impl_answer=impl_answer)
    config, _, _ = _run_wizard(FileAccess.READ, lines)
    assert config.format_name == 'Excel'
    assert config.implementation == 'OpenPyXL'


def test_csv_custom() -> None:
    """The wizard stores entered CSV-specific values.

    The console option form is a choice menu per member. The leading
    "use the default" option takes menu number 1, so UNIX is 3 in the
    dialect menu and minimal is 3 in the quoting menu.
    """
    member_answers = {
        'character_encoding': ['utf-8'],
        'csv.dialect': ['3'],
        'csv.delimiter': [';'],
        'csv.quoting': ['3'],
        'csv.quotechar': ['"']}
    lines = _wizard_lines('CSV', FileAccess.CREATE,
                          member_answers=member_answers)
    config, _, _ = _run_wizard(FileAccess.CREATE, lines)
    assert_csv_core(config)
    assert config.csv is not None
    assert config.csv.quoting == 'minimal'
    assert config.csv.quotechar == '"'


def test_bad_menu() -> None:
    """A bad numbered menu choice is rejected and asked again."""
    lines = ['999'] + _wizard_lines('CSV', FileAccess.CREATE)
    config, _, error_output = _run_wizard(FileAccess.CREATE, lines)
    assert config.format_name == 'CSV'
    assert 'Please enter one of the listed choices.' in error_output


def _csv_form_lines(delimiter: str) -> list[str]:
    """Return one console option-form pass for CSV with one delimiter."""
    names = _optional_names('CSV', FileAccess.CREATE, None)
    return [delimiter if name == 'csv.delimiter' else '' for name in names]


def test_bad_member() -> None:
    """A member value rejected by config validation re-asks the form.

    The option form is submitted as a whole, so a value that fails final
    validation re-asks the entire form. The bad delimiter is entered on
    the first pass and corrected on the second.
    """
    fmt = str(_format_index('CSV', FileAccess.CREATE) + 1)
    lines = [fmt] + _csv_form_lines(';;') + _csv_form_lines(';')
    config, output, _ = _run_wizard(FileAccess.CREATE, lines)
    assert config.csv is not None
    assert config.csv.delimiter == ';'
    assert 'Invalid value' in output


def test_bridge_int_index() -> None:
    """A bridge may return a 0-based integer choice index."""
    answers: list[str | int] = [0]
    answers.extend(_member_answer_lines('CSV', FileAccess.CREATE))
    config = _run_bridge(FileAccess.CREATE, _ScriptedBridge(answers))
    assert config.format_name == 'CSV'


def test_bool_choice_rejected() -> None:
    """Boolean bridge answers are not accepted as integer menu indexes."""
    answers: list[str | int] = [True, 0]
    answers.extend(_member_answer_lines('CSV', FileAccess.CREATE))
    ui_bridge = _ScriptedBridge(answers)
    config = _run_bridge(FileAccess.CREATE, ui_bridge)
    assert config.format_name == 'CSV'
    re_ask_reason = ui_bridge.calls[1][1]
    assert re_ask_reason == 'Please enter one of the listed choices.'


def test_bridge_str_index() -> None:
    """A bridge may return a 0-based choice index as a string.

    The option form prepends a "use the default" choice, so index 2 of
    the quoting field selects minimal.
    """
    member_answers: dict[str, list[str | int]] = {'csv.quoting': ['2']}
    answers: list[str | int] = ['0']
    answers.extend(_member_answer_lines('CSV', FileAccess.CREATE,
                                        member_answers=member_answers))
    config = _run_bridge(FileAccess.CREATE, _ScriptedBridge(answers))
    assert config.csv is not None
    assert config.csv.quoting == 'minimal'


def test_bridge_prefix_format() -> None:
    """A bridge may return a unique string prefix for a choice."""
    answers: list[str | int] = ['cs']
    answers.extend(_member_answer_lines('CSV', FileAccess.CREATE))
    config = _run_bridge(FileAccess.CREATE, _ScriptedBridge(answers))
    assert config.format_name == 'CSV'


def test_impl_prefix() -> None:
    """Implementation choices accept unique string prefixes."""
    answers: list[str | int] = ['excel', 'op']
    answers.extend(_member_answer_lines('Excel', FileAccess.READ, 'OpenPyXL'))
    config = _run_bridge(FileAccess.READ, _ScriptedBridge(answers))
    assert config.format_name == 'Excel'
    assert config.implementation == 'OpenPyXL'


def test_enum_prefix() -> None:
    """Enum-backed choices use enum-name best matching."""
    member_answers: dict[str, list[str | int]] = {'csv.dialect': ['un']}
    answers: list[str | int] = [0]
    answers.extend(_member_answer_lines('CSV', FileAccess.CREATE,
                                        member_answers=member_answers))
    config = _run_bridge(FileAccess.CREATE, _ScriptedBridge(answers))
    assert config.csv is not None
    assert config.csv.dialect == CsvDialect.UNIX


def test_enum_bad_text_retry() -> None:
    """Enum-backed choices reject invalid text and then ask again."""
    member_answers: dict[str, list[str | int]] = {
        'csv.dialect': ['not-a-dialect', 'excel']}
    answers: list[str | int] = [0]
    answers.extend(_member_answer_lines('CSV', FileAccess.CREATE,
                                        member_answers=member_answers))
    ui_bridge = _ScriptedBridge(answers)
    config = _run_bridge(FileAccess.CREATE, ui_bridge)
    assert config.csv is not None
    assert config.csv.dialect == CsvDialect.EXCEL
    reasons = [call[1] for call in ui_bridge.calls
               if call[0].startswith('csv.dialect')]
    retry_reason = reasons[1]
    assert reasons[0] is None
    assert retry_reason is not None
    assert 'Please enter one of the listed choices.' in retry_reason


def test_text_value_retries() -> None:
    """Integer members reject malformed values and ask again.

    Integer members are integer form fields, so the base ask_int loop
    re-asks the same field until it parses, using the integer error.
    """
    member_answers: dict[str, list[str | int]] = {
        'line_length': ['not-an-int', '72'],
        'table_max_line_length': ['oops', '30']}
    answers: list[str | int] = ['rest']
    answers.extend(_member_answer_lines('reST', FileAccess.CREATE,
                                        member_answers=member_answers))
    ui_bridge = _ScriptedBridge(answers)
    config = _run_bridge(FileAccess.CREATE, ui_bridge)
    assert config.format_name == 'reST'
    assert config.line_length == 72
    assert config.table_max_line_length == 30
    reasons = [call[1] for call in ui_bridge.calls
               if call[1] is not None]
    assert any(_INT_ERROR in reason for reason in reasons)


def test_bad_bridge_choice() -> None:
    """A bad bridge answer is rejected and the same question is re-asked."""
    answers: list[str | int] = ['not-a-format', 0]
    answers.extend(_member_answer_lines('CSV', FileAccess.CREATE))
    ui_bridge = _ScriptedBridge(answers)
    config = _run_bridge(FileAccess.CREATE, ui_bridge)
    assert config.format_name == 'CSV'
    re_ask_reason = ui_bridge.calls[1][1]
    assert re_ask_reason == 'Please enter one of the listed choices.'


def test_early_eof() -> None:
    """Scripted wizard input must contain every required answer."""
    stdin_file = StringIO()
    stdout_file = StringIO()
    stderr_file = StringIO()
    ui_bridge = WizardUiBridgeConsole(stdout_file, stdin_file, stderr_file)
    with pytest.raises(EOFError):
        tio_json_config_wizard(Capabilities(), FileAccess.CREATE, ui_bridge)


def test_unrestricted_match() -> None:
    """Wizard metadata without restrictions matches requested choices."""
    assert wizard_module._matches(None, ('CSV',)) is True


def test_scalar_json_section() -> None:
    """Setting a dotted member rejects an existing scalar section."""
    data: dict[str, object] = {'csv': 'bad'}
    with pytest.raises(ValueError, match='csv is not a JSON object'):
        wizard_module._set_json_member(data, 'csv.delimiter', ';')
    assert data == {'csv': 'bad'}


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


def test_cancel_options() -> None:
    """Cancelling the option form returns to the format question."""
    answers: list[str | int | BaseException] = [
        _format_index('CSV', FileAccess.CREATE), '', WizardCancelLevel(),
        WizardAbort()]
    bridge = _ScriptedBridge(answers)
    with pytest.raises(WizardAbort):
        _run_bridge(FileAccess.CREATE, bridge)
    formats = [call for call in bridge.calls
               if call[0] == 'Select TableIO format:']
    assert len(formats) == 2


def test_cancel_at_format() -> None:
    """Cancel at the format question propagates out for the application."""
    with pytest.raises(WizardCancelLevel):
        _run_bridge(FileAccess.CREATE, _ScriptedBridge([WizardCancelLevel()]))


def test_abort_propagates() -> None:
    """Abort raised in the option form propagates out of the wizard."""
    answers: list[str | int | BaseException] = [
        _format_index('CSV', FileAccess.CREATE), '', WizardAbort()]
    with pytest.raises(WizardAbort):
        _run_bridge(FileAccess.CREATE, _ScriptedBridge(answers))


def test_back_first_question() -> None:
    """Back from the first question propagates out for the application."""
    with pytest.raises(WizardBack):
        _run_bridge(FileAccess.CREATE, _ScriptedBridge([WizardBack()]))


def test_back_to_format() -> None:
    """Back from the first option field returns to the format question."""
    answers: list[str | int | BaseException] = [
        _format_index('CSV', FileAccess.CREATE), WizardBack(),
        _format_index('CSV', FileAccess.CREATE)]
    answers.extend(_member_answer_lines('CSV', FileAccess.CREATE))
    bridge = _ScriptedBridge(answers)
    config = _run_bridge(FileAccess.CREATE, bridge)
    assert config.format_name == 'CSV'
    formats = [call for call in bridge.calls
               if call[0] == 'Select TableIO format:']
    assert len(formats) == 2


def test_back_within_form() -> None:
    """Back to an earlier option field keeps the fields before it.

    The base ask_form fallback re-asks the field stepped back to from its
    starting value, while fields already answered before it are kept.
    """
    answers: list[str | int | BaseException] = [
        _format_index('CSV', FileAccess.CREATE), 'utf-8', '', WizardBack(),
        'unix', ';', '', '', '', '']
    config = _run_bridge(FileAccess.CREATE, _ScriptedBridge(answers))
    assert_csv_core(config)


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


def test_ask_impl_single() -> None:
    """A single implementation needs no question and returns None."""
    bridge = _ScriptedBridge([])
    assert wizard_module._ask_implementation(('only',), bridge, None) is None


with warnings.catch_warnings():
    warnings.simplefilter('ignore', DeprecationWarning)

    class _OldStyleBridge(WizardUiBridge):
        """Old-style bridge that overrides only the deprecated ask().

        It exercises the temporary backward-compatibility code: the base
        class still backs the typed ask methods with this bridge's ask()
        while warning that the typed methods should be overridden. Its
        definition is wrapped so the override warning is not raised at
        import time; test_deprecated_ask_override_warns asserts it.
        """

        def __init__(self, answers: Sequence[str | int]) -> None:
            """Store scripted raw answers returned in order by ask()."""
            self.answers: list[str | int] = list(answers)
            self.shown: list[str] = []

        def ask(self, question: str, re_ask_reason: Optional[str] = None,
                choices: Optional[Sequence[str]] = None) -> str | int:
            """Return the next scripted raw answer."""
            _ = (question, re_ask_reason, choices)
            return self.answers.pop(0)

        def show(self, message: str) -> None:
            """Record the shown message."""
            self.shown.append(message)


def test_dep_override_warns() -> None:
    """Defining a bridge that overrides ask() warns it is deprecated."""
    def stand_in(*_args: object) -> str:
        """Stand-in ask() used only to trigger the override warning."""
        return ''
    with pytest.warns(DeprecationWarning, match='Overriding'):
        type('_Overrider', (WizardUiBridge,), {'ask': stand_in})


def test_dep_ask_call_warns() -> None:
    """Calling the deprecated ask() warns and dispatches by arguments."""
    text_bridge = _ScriptedBridge(['typed'])
    with pytest.warns(DeprecationWarning, match='deprecated'):
        assert text_bridge.ask('q') == 'typed'
    choice_bridge = _ScriptedBridge([1])
    with pytest.warns(DeprecationWarning, match='deprecated'):
        assert choice_bridge.ask('q', choices=('a', 'b')) == 'b'


def test_dep_fallback_warns() -> None:
    """The base typed-method fallbacks warn while backing an old bridge."""
    bridge = _OldStyleBridge(['hi', 0, 0, True])
    with pytest.warns(DeprecationWarning, match='ask_text'):
        assert bridge.ask_text('q') == 'hi'
    with pytest.warns(DeprecationWarning, match='ask_choice'):
        assert bridge.ask_choice('q', choices=('a', 'b')) == 'a'
    with pytest.warns(DeprecationWarning, match='ask_multi'):
        assert bridge.ask_multi('q', choices=('a', 'b')) == ['a']
    with pytest.warns(DeprecationWarning, match='ask_yes_no'):
        assert bridge.ask_yes_no('q', default=False) is True


def test_dep_table_warns() -> None:
    """The base ask_table fallback warns and fills cells via ask()."""
    columns = (TableColumn('Value'),)
    cells = [[TableCell(value='x')]]
    bridge = _OldStyleBridge([''])
    with pytest.warns(DeprecationWarning, match='ask_table'):
        assert bridge.ask_table(columns, cells, 'Pick:') == [['x']]


def test_typed_no_impl() -> None:
    """A bridge implementing neither ask() nor a typed method raises."""
    bridge = WizardUiBridge()
    with pytest.raises(NotImplementedError, match='ask_choice'):
        bridge.ask_choice('q', choices=('a', 'b'))


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
