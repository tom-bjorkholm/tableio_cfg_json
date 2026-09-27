#! /usr/bin/env python3
"""Tests for which file access and names the descriptions settle on."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

# pylint: disable=protected-access

from typing import Optional, TextIO

import pytest

from tableio import CAP_NEEDED, Capabilities, ConfigError, ConfigIssue, \
    FileAccess
from tableio_cfg_json import TioJsonConfig, describe_config, \
    describe_config_members, get_config_member_names, \
    tio_json_config_default
import tableio_cfg_json.describe as describe_module

READ_FLAGS = ('can_read', 'can_read_box', 'can_find_value_position')

WRITE_FLAGS = ('can_write', 'can_fmt_row', 'can_fmt_value',
               'filtered_data_range', 'can_write_box', 'can_write_highlight',
               'multi_sheet', 'can_write_borders')

READ_ORDER = [FileAccess.READ, FileAccess.UPDATE, FileAccess.CREATE]
WRITE_ORDER = [FileAccess.CREATE, FileAccess.UPDATE, FileAccess.READ]
BOTH_ORDER = [FileAccess.UPDATE, FileAccess.READ, FileAccess.CREATE]


def _needing(*flags: str) -> Capabilities:
    """Return capabilities that need each named capability."""
    return Capabilities(**{flag: CAP_NEEDED for flag in flags})


@pytest.mark.parametrize('flag', READ_FLAGS)
def test_read_flag_order(flag: str) -> None:
    """Each reading capability on its own makes READ the first try."""
    assert describe_module._example_accesses(_needing(flag), None) == \
        READ_ORDER


@pytest.mark.parametrize('flag', WRITE_FLAGS)
def test_write_flag_order(flag: str) -> None:
    """Each writing capability on its own makes CREATE the first try."""
    assert describe_module._example_accesses(_needing(flag), None) == \
        WRITE_ORDER


@pytest.mark.parametrize('read_flag', READ_FLAGS)
@pytest.mark.parametrize('write_flag', ['can_fmt_row', 'can_write_borders'])
def test_both_flags_order(read_flag: str, write_flag: str) -> None:
    """Reading and writing capabilities together make UPDATE the first."""
    caps = _needing(read_flag, write_flag)
    assert describe_module._example_accesses(caps, None) == BOTH_ORDER


def test_no_flag_order() -> None:
    """Without read or write capabilities CREATE is tried first."""
    assert describe_module._example_accesses(Capabilities(), None) == \
        [FileAccess.CREATE, FileAccess.READ, FileAccess.UPDATE]


@pytest.mark.parametrize('access', list(FileAccess))
def test_given_access_only(access: FileAccess) -> None:
    """A given file access is the only one tried, whatever is needed."""
    caps = _needing('can_read', 'can_write')
    assert describe_module._example_accesses(caps, access) == [access]


def _failing_first(monkeypatch: pytest.MonkeyPatch) -> list[FileAccess]:
    """Make the first default lookup fail and record every access tried."""
    tried: list[FileAccess] = []

    # pylint: disable-next=too-many-arguments,too-many-positional-arguments
    def fake(capabilities: Capabilities, file_access: FileAccess,
             format_name: Optional[str] = None,
             implementation: Optional[str] = None,
             include_all_options: bool = False,
             stderr_file: Optional[TextIO] = None) -> TioJsonConfig:
        """Refuse the first access, and answer the others for real."""
        _ = stderr_file
        tried.append(file_access)
        if len(tried) == 1:
            raise ConfigError((ConfigIssue('format_name', 'refused'),))
        return tio_json_config_default(capabilities, file_access, format_name,
                                       implementation, include_all_options)
    monkeypatch.setattr(describe_module, 'tio_json_config_default', fake)
    return tried


def test_example_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    """A refused first access falls back to the next one in the order."""
    tried = _failing_first(monkeypatch)
    text = describe_config(capabilities=_needing('can_read'),
                           format_name='CSV')
    assert tried == [FileAccess.READ, FileAccess.UPDATE]
    assert 'Compact example (UPDATE)' in text


@pytest.mark.parametrize('format_name,impl,wanted', [
    ('csv', None, 'CSV'), ('EXCEL', 'openpyxl', 'Excel'),
    (None, 'OPENPYXL', 'Excel')])
def test_names_any_case(format_name: Optional[str], impl: Optional[str],
                        wanted: str) -> None:
    """Names match in any case and are shown the way TableIO spells them."""
    text = describe_config_members(format_name=format_name,
                                   implementation=impl)
    assert f'format_name choices: {wanted}.' in text
    if impl is not None:
        assert f'{wanted}: OpenPyXL.' in text


@pytest.mark.parametrize('format_name,expected', [
    ('CSV', True), ('txt', True), ('Excel', False), ('ODS', False)])
def test_timedelta_relevance(format_name: str, expected: bool) -> None:
    """The timedelta fallback belongs only to formats without timedelta."""
    names = get_config_member_names(file_access=FileAccess.CREATE,
                                    format_name=format_name)
    assert ('timedelta_fallback' in names) == expected
