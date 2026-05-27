#! /usr/bin/env python3
"""Tests for the interactive TableIO JSON config wizard."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from io import StringIO
from typing import Optional, Sequence

import pytest

from tableio import Capabilities, CsvDialect, FileAccess, \
    access_capabilities, add_access_capabilities, \
    list_implementations_tableio, list_registered_tableio
from tableio_cfg_json import TioJsonConfig, get_config_member_names, \
    tio_json_config_wizard


def _run_wizard(file_access: FileAccess, answer_lines: list[str]
                ) -> tuple[TioJsonConfig, str]:
    """Run the wizard with scripted answers."""
    stdin_file = StringIO('\n'.join(answer_lines) + '\n')
    stdout_file = StringIO()
    stderr_file = StringIO()
    capabilities = access_capabilities(file_access, error_file=stderr_file)
    config = tio_json_config_wizard(capabilities, file_access, stdin_file,
                                    stdout_file, stderr_file)
    return config, stdout_file.getvalue()


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
    if len(impl_names) > 1:
        lines.append('' if impl_answer is None else impl_answer)
    for member_name in _optional_names(format_name, file_access, impl_answer):
        lines.extend(answer_map.get(member_name, ['']))
    return lines


def _optional_names(format_name: str, file_access: FileAccess,
                    impl_answer: Optional[str]) -> tuple[str, ...]:
    """Return optional wizard member names for one scripted selection."""
    capabilities = access_capabilities(file_access)
    implementation = None
    match_caps = add_access_capabilities(file_access, capabilities)
    impl_names = list_implementations_tableio(format_name=format_name,
                                              capabilities=match_caps)
    if impl_answer is not None and impl_answer != '' and len(impl_names) > 1:
        implementation = impl_names[int(impl_answer) - 1]
    member_names = get_config_member_names(capabilities=capabilities,
                                           file_access=file_access,
                                           format_name=format_name,
                                           implementation=implementation)
    return tuple(name for name in member_names
                 if name not in ('format_name', 'implementation'))


def _menu_number(choice: str, choices: Sequence[str]) -> str:
    """Return the one-based menu number for a known choice."""
    return str(choices.index(choice) + 1)


def test_public_api() -> None:
    """The wizard helper is exported from the package root."""
    assert callable(tio_json_config_wizard)


def test_wizard_csv_defaults() -> None:
    """Blank answers keep optional CSV settings out of compact JSON."""
    config, output = _run_wizard(FileAccess.CREATE,
                                 _wizard_lines('CSV', FileAccess.CREATE))
    assert config.format_name == 'CSV'
    assert config.implementation is None
    assert config.csv is None
    assert 'Select TableIO format' in output
    assert 'csv.delimiter' in output


def test_blank_impl() -> None:
    """Blank implementation keeps TableIO runtime selection enabled."""
    lines = _wizard_lines('Excel', FileAccess.READ, impl_answer='')
    config, output = _run_wizard(FileAccess.READ, lines)
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
    config, _ = _run_wizard(FileAccess.READ, lines)
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
    config, _ = _run_wizard(FileAccess.CREATE, lines)
    assert config.character_encoding == 'utf-8'
    assert config.csv is not None
    assert config.csv.dialect == CsvDialect.UNIX
    assert config.csv.delimiter == ';'
    assert config.csv.quoting == 'minimal'
    assert config.csv.quotechar == '"'


def test_bad_menu() -> None:
    """A bad numbered menu choice is rejected and asked again."""
    lines = ['999'] + _wizard_lines('CSV', FileAccess.CREATE)
    config, output = _run_wizard(FileAccess.CREATE, lines)
    assert config.format_name == 'CSV'
    assert 'Please enter one of the menu numbers.' in output


def test_bad_member() -> None:
    """A member value rejected by config validation is asked again."""
    lines = _wizard_lines('CSV', FileAccess.CREATE,
                          member_answers={'csv.delimiter': [';;', ';']})
    config, output = _run_wizard(FileAccess.CREATE, lines)
    assert config.csv is not None
    assert config.csv.delimiter == ';'
    assert 'Invalid value' in output


def test_early_eof() -> None:
    """Scripted wizard input must contain every required answer."""
    stdin_file = StringIO()
    stdout_file = StringIO()
    stderr_file = StringIO()
    with pytest.raises(EOFError):
        tio_json_config_wizard(Capabilities(), FileAccess.CREATE, stdin_file,
                               stdout_file, stderr_file)
