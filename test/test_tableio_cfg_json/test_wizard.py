#! /usr/bin/env python3
"""Tests for the interactive TableIO JSON config wizard flow.

This drives the wizard end to end through the format, implementation and
option questions, covering navigation, defaults, the deprecated bridge
API and the wizard's internal data handling.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

# pylint: disable=protected-access

import sys
import warnings
from io import StringIO
from typing import Optional, Sequence

import pytest

from tableio import Capabilities, ConfigSpec, CsvDialect, FileAccess, \
    access_capabilities, add_access_capabilities, \
    list_implementations_tableio
from tableio_cfg_json import WizardUiBridge, WizardUiBridgeConsole, \
    tio_json_config_wizard, TableCell, TableColumn, WizardAbort, WizardBack, \
    WizardCancelLevel
from tableio_cfg_json.wizard_ui_bridge import _INT_ERROR
import tableio_cfg_json.wizard as wizard_module
from .wizard_support import _ScriptedBridge, _run_wizard, _run_bridge, \
    _wizard_lines, _optional_names, _menu_number, _format_index, \
    _member_answer_lines, assert_csv_core


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


def _choice_spec() -> ConfigSpec:
    """Return a choice config spec with two string choices."""
    return ConfigSpec('csv.dialect', 'The dialect.', 'Optional[str]',
                      'None means backend default.', choices=('EXCEL', 'UNIX'))


def test_impl_default_reset() -> None:
    """A stale implementation default falls back to the auto option.

    When the previously chosen implementation is no longer offered, the
    implementation question drops the stale default and keeps the
    recommended auto behavior, so an empty answer returns None.
    """
    bridge = _ScriptedBridge([''])
    result = wizard_module._ask_implementation(['impl_a', 'impl_b'], bridge,
                                               'gone')
    assert result is None


def test_resolve_bad_choice() -> None:
    """An answered choice outside the member's options is rejected."""
    with pytest.raises(ValueError):
        wizard_module._resolve_member_value(_choice_spec(), 'NONSENSE')


def test_apply_bad_option() -> None:
    """An option value that fails conversion becomes a retry reason."""
    stderr = StringIO()
    file_access = FileAccess.CREATE
    caps = access_capabilities(file_access, error_file=stderr)
    match_caps = add_access_capabilities(file_access, caps, error_file=stderr)
    run = wizard_module._WizardRun(bridge=WizardUiBridge(), caps=caps,
                                   file_access=file_access,
                                   match_caps=match_caps, stderr=stderr,
                                   data={'format_name': 'CSV'})
    reason = wizard_module._apply_options(run, (_choice_spec(),),
                                          {'csv.dialect': 'BAD'})
    assert reason is not None and 'Invalid value' in reason


def test_clear_no_format() -> None:
    """Clearing option values with no format leaves the data empty."""
    data: dict[str, object] = {'other': 1}
    wizard_module._clear_after_format(data)
    assert not data


def test_spec_choices_none() -> None:
    """A member without choices reports no string choice tuple."""
    spec = ConfigSpec('character_encoding', 'Encoding.', 'Optional[str]',
                      'None means backend default.')
    assert wizard_module._spec_choices(spec) is None
