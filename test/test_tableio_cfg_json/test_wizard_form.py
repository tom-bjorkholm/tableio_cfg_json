#! /usr/bin/env python3
"""Tests for the wizard option form across the UI bridges.

The wizard asks all optional members of one endpoint in a single form
through WizardUiBridge.ask_form. These tests cover how the wizard builds
the form fields from the TableIO config specs, how it turns the answers
back into a validated config, and how it drives the base fallback, the
console bridge and the Textual bridge for that one form.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

# pylint: disable=protected-access

import asyncio
from io import StringIO
from typing import Optional, Sequence

from textual.widgets import Input

from tableio import ConfigSpec, CsvDialect, FileAccess, access_capabilities
from tableio_cfg_json import AskChoiceField, AskIntField, AskTextField, \
    AskField, AskFields, AnswerField, AnswerFields, PartialFormValidator, \
    TioJsonConfig, WizardUiBridge, WizardUiBridgeConsole, \
    tio_json_config_wizard
from tableio_cfg_json._wizard_ui_bridge_form import initial_answer
from tableio_cfg_json.wizard_ui_bridge_textual import _FormApp
import tableio_cfg_json.wizard as wizard_module
from .test_wizard import _ScriptedBridge, _format_index, \
    _member_answer_lines, _run_bridge, assert_csv_core
from .test_ui_textual import _CannedBridge


def _csv_specs() -> tuple[ConfigSpec, ...]:
    """Return the option specs the wizard asks for a CSV output."""
    return wizard_module._relevant_specs('CSV', ('csv',))


def _spec_index(name: str) -> int:
    """Return the position of one CSV member in the option form."""
    return [spec.name for spec in _csv_specs()].index(name)


class _FormReturnBridge(WizardUiBridge):
    """Bridge that answers the format menu and returns scripted forms.

    The format question is answered with a fixed choice. Each ask_form
    call records how it was asked and returns answers built from the
    fields' start values, overridden by one scripted dict keyed by member
    name, so a test can submit a whole option form directly, the way a
    graphical bridge would, even with a value a graphical form's own
    validator would have blocked.
    """

    def __init__(self, format_index: int,
                 forms: Sequence[dict[str, object]]) -> None:
        """Store the format index and the scripted form overrides."""
        self.format_index = format_index
        self.forms = list(forms)
        self.reasons: list[Optional[str]] = []
        self.last_fields: list[AskField] = []
        self.last_question = ''
        self.stderr_file = StringIO()
        self.format_asked = False

    def ask_choice(self, question: str, *, choices: Sequence[str],
                   default: Optional[str] = None,
                   re_ask_reason: Optional[str] = None) -> str:
        """Answer the format menu once with the scripted choice."""
        _ = (question, re_ask_reason)
        if not self.format_asked:
            self.format_asked = True
            return choices[self.format_index]
        return choices[0] if default is None else default

    def ask_form(self, long_question: str, ask_fields: AskFields, *,
                 re_ask_reason: Optional[str] = None,
                 partial_validator: Optional[PartialFormValidator] = None
                 ) -> AnswerFields:
        """Record the form and return one answer per field."""
        self.reasons.append(re_ask_reason)
        self.last_fields = list(ask_fields)
        self.last_question = long_question
        _ = partial_validator
        overrides = self.forms.pop(0)
        return [self._answer(field, overrides) for field in ask_fields]

    @staticmethod
    def _answer(field: AskField, overrides: dict[str, object]) -> AnswerField:
        """Return the field's start answer, overridden when scripted."""
        answer = initial_answer(field)
        if field.short_question in overrides:
            answer.value = overrides[field.short_question]  # type: ignore
        return answer

    def error_file(self) -> StringIO:
        """Return the stream used for validation diagnostics."""
        return self.stderr_file

    def show(self, message: str) -> None:
        """Ignore shown messages."""
        _ = message


def _gui_config(forms: Sequence[dict[str, object]],
                default: Optional[TioJsonConfig] = None,
                backward: bool = False) -> TioJsonConfig:
    """Run the wizard with a scripted graphical option form."""
    file_access = FileAccess.CREATE
    caps = access_capabilities(file_access)
    bridge = _FormReturnBridge(_format_index('CSV', file_access), forms)
    return tio_json_config_wizard(caps, file_access, bridge, default=default,
                                  backward=backward)


def test_field_kinds() -> None:
    """Each member becomes the field kind implied by its spec."""
    fields = wizard_module._option_fields(_csv_specs(), {})
    by_name = {field.short_question: field for field in fields}
    assert isinstance(by_name['csv.dialect'], AskChoiceField)
    assert isinstance(by_name['csv.delimiter'], AskTextField)
    assert isinstance(by_name['character_encoding'], AskTextField)


def test_int_field_kind() -> None:
    """An Optional[int] member becomes an integer field."""
    specs = wizard_module._relevant_specs('reST', ('mformat',))
    fields = wizard_module._option_fields(specs, {})
    by_name = {field.short_question: field for field in fields}
    assert isinstance(by_name['line_length'], AskIntField)


def test_field_help_text() -> None:
    """Every option field carries its spec description as help text."""
    specs = _csv_specs()
    fields = wizard_module._option_fields(specs, {})
    for spec, field in zip(specs, fields):
        assert field.help_text == spec.description


def test_choice_sentinel() -> None:
    """A choice field offers a leading use-the-default option."""
    fields = wizard_module._option_fields(_csv_specs(), {})
    dialect = fields[_spec_index('csv.dialect')]
    assert isinstance(dialect, AskChoiceField)
    assert dialect.choices[0] == wizard_module._AUTO_MEMBER
    assert 'EXCEL' in dialect.choices and 'UNIX' in dialect.choices


def test_form_names_format() -> None:
    """The form instruction names the chosen format."""
    bridge = _FormReturnBridge(_format_index('CSV', FileAccess.CREATE), [{}])
    tio_json_config_wizard(access_capabilities(FileAccess.CREATE),
                           FileAccess.CREATE, bridge)
    assert 'CSV' in bridge.last_question


def test_gui_values() -> None:
    """A graphical option form stores the chosen member values."""
    config = _gui_config([{'character_encoding': 'utf-8',
                           'csv.dialect': 'UNIX', 'csv.delimiter': ';'}])
    assert_csv_core(config)


def test_gui_omit_defaults() -> None:
    """Left-as-default fields stay out of the compact configuration."""
    config = _gui_config([{}])
    assert config.format_name == 'CSV'
    assert config.character_encoding is None
    assert config.csv is None


def test_gui_invalid_reask() -> None:
    """An invalid submitted option form is rejected and re-asked whole."""
    file_access = FileAccess.CREATE
    forms: list[dict[str, object]] = [
        {'csv.delimiter': ';;'}, {'csv.delimiter': ';'}]
    bridge = _FormReturnBridge(_format_index('CSV', file_access), forms)
    config = tio_json_config_wizard(access_capabilities(file_access),
                                    file_access, bridge)
    assert config.csv is not None
    assert config.csv.delimiter == ';'
    assert bridge.reasons[0] is None
    retry = bridge.reasons[1]
    assert retry is not None and 'Invalid value' in retry


def test_gui_prefill_default() -> None:
    """The form is pre-filled from a supplied default configuration."""
    file_access = FileAccess.CREATE
    default = TioJsonConfig(
        access_capabilities(file_access), file_access,
        from_json_data_text='{"format_name": "CSV", '
        '"character_encoding": "utf-8", "csv": {"delimiter": ";"}}')
    bridge = _FormReturnBridge(_format_index('CSV', file_access), [{}])
    config = tio_json_config_wizard(access_capabilities(file_access),
                                    file_access, bridge, default=default)
    by_name = {field.short_question: field for field in bridge.last_fields}
    encoding = by_name['character_encoding']
    delimiter = by_name['csv.delimiter']
    assert isinstance(encoding, AskTextField) and encoding.default == 'utf-8'
    assert isinstance(delimiter, AskTextField) and delimiter.default == ';'
    assert config.character_encoding == 'utf-8'
    assert config.csv is not None and config.csv.delimiter == ';'


def test_gui_prefill_choice() -> None:
    """A stored choice pre-selects that choice in the form."""
    file_access = FileAccess.CREATE
    default = TioJsonConfig(
        access_capabilities(file_access), file_access,
        from_json_data_text='{"format_name": "CSV", '
        '"csv": {"dialect": "UNIX"}}')
    bridge = _FormReturnBridge(_format_index('CSV', file_access), [{}])
    tio_json_config_wizard(access_capabilities(file_access), file_access,
                           bridge, default=default)
    dialect = bridge.last_fields[_spec_index('csv.dialect')]
    assert isinstance(dialect, AskChoiceField)
    assert dialect.default == 'UNIX'


def _validator() -> PartialFormValidator:
    """Return the wizard's option-form validator for a CSV output."""
    caps = access_capabilities(FileAccess.CREATE)
    run = wizard_module._WizardRun(bridge=WizardUiBridge(), caps=caps,
                                   file_access=FileAccess.CREATE,
                                   match_caps=caps, stderr=StringIO(),
                                   data={'format_name': 'CSV'})
    return wizard_module._options_validator(run, _csv_specs())


def _csv_answers(overrides: dict[str, object]) -> list[AnswerField]:
    """Return option-form answers for CSV, overridden by member name."""
    fields = wizard_module._option_fields(_csv_specs(), {})
    return [_FormReturnBridge._answer(field, overrides) for field in fields]


def test_validator_rejects() -> None:
    """The partial validator reports a bad value as invalid."""
    result = _validator()(_csv_answers({'csv.delimiter': ';;'}), 0)
    assert result.is_valid is False
    assert 'Invalid value' in result.message


def test_validator_accepts() -> None:
    """The partial validator accepts an all-default form."""
    result = _validator()(_csv_answers({}), 0)
    assert result.is_valid is True
    assert result.message == ''


def test_excel_no_members() -> None:
    """A multi-implementation format may expose no option members."""
    assert not wizard_module._relevant_specs('Excel', ('OpenPyXL',))


def test_impl_no_form() -> None:
    """With no option members the wizard asks the impl but no form."""
    file_access = FileAccess.READ
    caps = access_capabilities(file_access)
    idx = _format_index('Excel', file_access)
    bridge = _ImplFormBridge(idx)
    config = tio_json_config_wizard(caps, file_access, bridge)
    assert config.format_name == 'Excel'
    assert bridge.calls == 2
    assert bridge.form_asked is False


class _ImplFormBridge(WizardUiBridge):
    """Bridge that accepts the format and implementation, then a form."""

    def __init__(self, format_index: int) -> None:
        """Store the format index and start with nothing asked."""
        self.format_index = format_index
        self.calls = 0
        self.form_asked = False
        self.stderr_file = StringIO()

    def ask_choice(self, question: str, *, choices: Sequence[str],
                   default: Optional[str] = None,
                   re_ask_reason: Optional[str] = None) -> str:
        """Answer the format menu, then keep the implementation default."""
        _ = (question, re_ask_reason)
        self.calls += 1
        if self.calls == 1:
            return choices[self.format_index]
        return choices[0] if default is None else default

    def ask_form(self, long_question: str, ask_fields: AskFields, *,
                 re_ask_reason: Optional[str] = None,
                 partial_validator: Optional[PartialFormValidator] = None
                 ) -> AnswerFields:
        """Accept the option form with every field left at its default."""
        _ = (long_question, re_ask_reason, partial_validator)
        self.form_asked = True
        return [initial_answer(field) for field in ask_fields]

    def error_file(self) -> StringIO:
        """Return the stream used for validation diagnostics."""
        return self.stderr_file

    def show(self, message: str) -> None:
        """Ignore shown messages."""
        _ = message


def test_base_fallback_names() -> None:
    """The base fallback resolves each field kind from named answers."""
    member_answers: dict[str, list[str | int]] = {
        'character_encoding': ['utf-8'], 'csv.dialect': ['unix'],
        'csv.delimiter': [';'], 'csv.quoting': ['minimal']}
    answers: list[str | int] = [_format_index('CSV', FileAccess.CREATE)]
    answers.extend(_member_answer_lines('CSV', FileAccess.CREATE,
                                        member_answers=member_answers))
    config = _run_bridge(FileAccess.CREATE, _ScriptedBridge(answers))
    assert_csv_core(config)
    assert config.csv is not None
    assert config.csv.quoting == 'minimal'


def test_base_fallback_int() -> None:
    """An integer option field is asked as an integer in the fallback."""
    member_answers: dict[str, list[str | int]] = {'line_length': ['72']}
    answers: list[str | int] = [_format_index('reST', FileAccess.CREATE)]
    answers.extend(_member_answer_lines('reST', FileAccess.CREATE,
                                        member_answers=member_answers))
    config = _run_bridge(FileAccess.CREATE, _ScriptedBridge(answers))
    assert config.format_name == 'reST'
    assert config.line_length == 72


def _console(lines: list[str]) -> tuple[TioJsonConfig, str]:
    """Run the wizard for a CSV output through real console streams."""
    file_access = FileAccess.CREATE
    fmt = str(_format_index('CSV', file_access) + 1)
    stdin = StringIO('\n'.join([fmt] + lines) + '\n')
    out = StringIO()
    bridge = WizardUiBridgeConsole(out, stdin, StringIO())
    caps = access_capabilities(file_access)
    config = tio_json_config_wizard(caps, file_access, bridge)
    return config, out.getvalue()


def test_console_defaults() -> None:
    """Blank console answers keep every option at its backend default."""
    config, output = _console([''] * len(_csv_specs()))
    assert config.csv is None
    assert 'Configure options for CSV' in output


def test_console_choice_menu() -> None:
    """The console option form numbers a choice member after the default."""
    lines = [''] * len(_csv_specs())
    lines[_spec_index('csv.dialect')] = '3'
    config, output = _console(lines)
    assert config.csv is not None
    assert config.csv.dialect == CsvDialect.UNIX
    assert '1: use the default' in output


def _textual_answers(overrides: dict[str, object]) -> list[AnswerField]:
    """Return option-form answers for the Textual canned form bridge."""
    return _csv_answers(overrides)


def test_textual_wizard_form() -> None:
    """The Textual bridge runs the format screen then the option form."""
    file_access = FileAccess.CREATE
    answers = _textual_answers({'csv.dialect': 'UNIX', 'csv.delimiter': ';'})
    bridge = _CannedBridge([_format_index('CSV', file_access), answers])
    config = tio_json_config_wizard(access_capabilities(file_access),
                                    file_access, bridge)
    assert config.csv is not None
    assert config.csv.dialect == CsvDialect.UNIX
    assert config.csv.delimiter == ';'
    form_app = bridge.launched[1]
    assert isinstance(form_app, _FormApp)
    assert form_app._validator is not None


def test_textual_validator() -> None:
    """The Textual option form blocks a submit the wizard rejects."""
    fields = wizard_module._option_fields(_csv_specs(), {})
    app = _FormApp('Configure', fields, [], _validator())
    idx = _spec_index('csv.delimiter')

    async def scenario() -> bool:
        async with app.run_test() as pilot:
            app.query_one(f'#field_{idx}', Input).value = ';;'
            await pilot.pause()
            app.action_submit()
            await pilot.pause()
            blocked = app.return_value is None
            app.query_one(f'#field_{idx}', Input).value = ';'
            await pilot.pause()
            app.action_submit()
            await pilot.pause()
            return blocked
    assert asyncio.run(scenario()) is True
    result = app.return_value
    assert result is not None
    answer = result[idx]
    assert answer.value == ';'
