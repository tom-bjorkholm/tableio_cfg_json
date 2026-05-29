#! /usr/bin/env python3
"""Tests for the interactive TableIO JSON config wizard."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

# pylint: disable=protected-access

import sys
from io import StringIO
from typing import Optional, Sequence

import pytest

from tableio import Capabilities, ConfigSpec, CsvDialect, FileAccess, \
    access_capabilities, add_access_capabilities, \
    list_implementations_tableio, list_registered_tableio
from tableio_cfg_json import TioJsonConfig, WizardUiBridge, \
    WizardUiBridgeConsole, get_config_member_names, tio_json_config_wizard
import tableio_cfg_json.wizard as wizard_module


class _ScriptedBridge(WizardUiBridge):
    """Wizard UI bridge that returns scripted answers for tests."""

    def __init__(self, answers: list[str | int]) -> None:
        """Initialize the scripted bridge.

        Args:
            answers: Answers returned in order by ``ask()``.
        """
        self.answers = list(answers)
        self.calls: list[
            tuple[str, Optional[str], Optional[tuple[str, ...]]]] = []
        self.messages: list[str] = []
        self.stderr_file = StringIO()

    def ask(self, question: str, re_ask_reason: Optional[str] = None,
            choices: Optional[Sequence[str]] = None) -> str | int:
        """Return the next scripted answer."""
        choice_tuple = None if choices is None else tuple(choices)
        self.calls.append((question, re_ask_reason, choice_tuple))
        if not self.answers:
            raise EOFError(f'No answer supplied for {question}.')
        return self.answers.pop(0)

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
        lines.append('' if impl_answer is None else impl_answer)
        if impl_answer is not None and impl_answer != '':
            implementation = impl_names[int(impl_answer) - 1]
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


def test_public_api() -> None:
    """The wizard helper is exported from the package root."""
    assert callable(tio_json_config_wizard)
    assert WizardUiBridgeConsole is not None


def test_base_bridge_defaults() -> None:
    """The base UI bridge exposes default stream and abstract methods."""
    ui_bridge = WizardUiBridge()
    assert ui_bridge.error_file() is sys.stderr
    with pytest.raises(NotImplementedError, match='ask'):
        ui_bridge.ask('Question?')
    with pytest.raises(NotImplementedError, match='show'):
        ui_bridge.show('Message.')


def test_console_menu() -> None:
    """Console menu numbers become 0-based indexes."""
    stdin_file = StringIO('2\n')
    stdout_file = StringIO()
    stderr_file = StringIO()
    ui_bridge = WizardUiBridgeConsole(stdout_file, stdin_file, stderr_file)
    answer = ui_bridge.ask('Pick one:', choices=('first', 'second'))
    assert answer == 1
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
    impl_answer = _menu_number('OpenPyXL', impl_names)
    lines = _wizard_lines('Excel', FileAccess.READ, impl_answer=impl_answer)
    config, _, _ = _run_wizard(FileAccess.READ, lines)
    assert config.format_name == 'Excel'
    assert config.implementation == 'OpenPyXL'


def test_csv_custom() -> None:
    """The wizard stores entered CSV-specific values."""
    member_answers = {
        'character_encoding': ['utf-8'],
        'csv.dialect': ['2'],
        'csv.delimiter': [';'],
        'csv.quoting': ['2'],
        'csv.quotechar': ['"']}
    lines = _wizard_lines('CSV', FileAccess.CREATE,
                          member_answers=member_answers)
    config, _, _ = _run_wizard(FileAccess.CREATE, lines)
    assert config.character_encoding == 'utf-8'
    assert config.csv is not None
    assert config.csv.dialect == CsvDialect.UNIX
    assert config.csv.delimiter == ';'
    assert config.csv.quoting == 'minimal'
    assert config.csv.quotechar == '"'


def test_bad_menu() -> None:
    """A bad numbered menu choice is rejected and asked again."""
    lines = ['999'] + _wizard_lines('CSV', FileAccess.CREATE)
    config, _, error_output = _run_wizard(FileAccess.CREATE, lines)
    assert config.format_name == 'CSV'
    assert 'Please enter one of the listed choices.' in error_output


def test_bad_member() -> None:
    """A member value rejected by config validation is asked again."""
    lines = _wizard_lines('CSV', FileAccess.CREATE,
                          member_answers={'csv.delimiter': [';;', ';']})
    config, _, error_output = _run_wizard(FileAccess.CREATE, lines)
    assert config.csv is not None
    assert config.csv.delimiter == ';'
    assert 'Invalid value' in error_output


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
    """A bridge may return a 0-based choice index as a string."""
    member_answers: dict[str, list[str | int]] = {'csv.quoting': ['1']}
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
               if call[0].startswith('Select value for csv.dialect')]
    assert reasons == [None, 'Please enter one of the listed choices.']


def test_text_value_retries() -> None:
    """Free-text members reject non-text and malformed integer values."""
    member_answers: dict[str, list[str | int]] = {
        'line_length': [17, '72'],
        'table_max_line_length': ['not-an-int', '30']}
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
    assert 'Please enter a text value.' in reasons
    assert any('Invalid value:' in reason for reason in reasons)


def test_bad_bridge_choice() -> None:
    """A bad bridge answer is rejected and the same question is re-asked."""
    answers: list[str | int] = ['not-a-format', 0]
    answers.extend(_member_answer_lines('CSV', FileAccess.CREATE))
    ui_bridge = _ScriptedBridge(answers)
    config = _run_bridge(FileAccess.CREATE, ui_bridge)
    assert config.format_name == 'CSV'
    re_ask_reason = ui_bridge.calls[1][1]
    assert re_ask_reason is not None
    assert 'format_name' in re_ask_reason


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


def test_enum_choice_outside() -> None:
    """Enum answers that resolve outside offered choices are rejected."""
    with pytest.raises(ValueError, match='listed choices'):
        wizard_module._choice_from_enum('unix', ('EXCEL',), CsvDialect)


def test_plain_type_no_enum() -> None:
    """Only Optional enum type descriptions produce enum matching."""
    spec = ConfigSpec(name='x', description='x', value_type='str',
                      choices=('x',))
    assert wizard_module._enum_type(spec) is None


def test_scalar_json_section() -> None:
    """Setting a dotted member rejects an existing scalar section."""
    data: dict[str, object] = {'csv': 'bad'}
    with pytest.raises(ValueError, match='csv is not a JSON object'):
        wizard_module._set_json_member(data, 'csv.delimiter', ';')
    assert data == {'csv': 'bad'}
