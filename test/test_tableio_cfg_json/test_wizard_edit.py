#! /usr/bin/env python3
"""Tests for editing defaults in the interactive wizard."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

# pylint: disable=protected-access

import json

from tableio import FileAccess, access_capabilities
from tableio_cfg_json import TioJsonConfig, WizardBack, tio_json_config_wizard
from .test_wizard import _ScriptedBridge, _format_index, \
    _member_answer_lines, _run_bridge


def _json_default(file_access: FileAccess,
                  data: dict[str, object]) -> TioJsonConfig:
    """Return a TioJsonConfig read from compact JSON test data."""
    capabilities = access_capabilities(file_access)
    return TioJsonConfig(capabilities, file_access,
                         from_json_data_text=json.dumps(data))


def test_default_values() -> None:
    """The wizard uses a supplied config as defaults for all questions."""
    file_access = FileAccess.CREATE
    default = _json_default(file_access, {
        'format_name': 'CSV',
        'character_encoding': 'utf-8',
        'csv': {'delimiter': ';'}})
    answers: list[str | int] = ['']
    answers.extend(_member_answer_lines('CSV', file_access))
    capabilities = access_capabilities(file_access)
    bridge = _ScriptedBridge(answers)
    config = tio_json_config_wizard(capabilities, file_access, bridge,
                                    default=default)
    assert config.format_name == 'CSV'
    assert config.character_encoding == 'utf-8'
    assert config.csv is not None
    assert config.csv.delimiter == ';'


def test_default_impl() -> None:
    """Blank implementation input keeps the implementation default."""
    file_access = FileAccess.READ
    default = _json_default(file_access, {
        'format_name': 'Excel',
        'implementation': 'OpenPyXL'})
    answers: list[str | int] = ['', '']
    answers.extend(_member_answer_lines('Excel', file_access, 'OpenPyXL'))
    capabilities = access_capabilities(file_access)
    bridge = _ScriptedBridge(answers)
    config = tio_json_config_wizard(capabilities, file_access, bridge,
                                    default=default)
    assert config.format_name == 'Excel'
    assert config.implementation == 'OpenPyXL'


def test_backward_start() -> None:
    """Backward mode starts at the last question implied by defaults."""
    file_access = FileAccess.CREATE
    default = _json_default(file_access, {
        'format_name': 'CSV',
        'csv': {'delimiter': ';'}})
    capabilities = access_capabilities(file_access)
    bridge = _ScriptedBridge(_member_answer_lines('CSV', file_access))
    config = tio_json_config_wizard(capabilities, file_access, bridge,
                                    default=default, backward=True)
    assert config.csv is not None
    assert config.csv.delimiter == ';'
    assert all(call[0] != 'Select TableIO format:' for call in bridge.calls)


def test_back_default() -> None:
    """Going back re-asks the previous question with its old answer."""
    file_access = FileAccess.CREATE
    answers: list[str | int | BaseException] = [
        _format_index('CSV', file_access), 'utf-8', WizardBack(), '']
    answers.extend(_member_answer_lines('CSV', file_access))
    config = _run_bridge(file_access, _ScriptedBridge(answers))
    assert config.format_name == 'CSV'
    assert config.character_encoding == 'utf-8'


def test_change_drops_old() -> None:
    """Changing format discards option values from the old format."""
    file_access = FileAccess.CREATE
    default = _json_default(file_access, {
        'format_name': 'CSV',
        'csv': {'delimiter': ';'}})
    answers: list[str | int] = ['rest']
    answers.extend(_member_answer_lines('reST', file_access))
    capabilities = access_capabilities(file_access)
    bridge = _ScriptedBridge(answers)
    config = tio_json_config_wizard(capabilities, file_access, bridge,
                                    default=default)
    assert config.format_name == 'reST'
    assert config.csv is None
