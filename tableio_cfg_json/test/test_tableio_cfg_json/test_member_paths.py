#! /usr/bin/env python3
"""Tests that a diagnostic names the whole path to the refused value.

config-as-json names a configuration value by the path from the top level
down to it, and carries that path as ``member_name``. These tests check the
three places this package is part of that: the nested format sections of one
endpoint, an endpoint nested in an application configuration, and the
TableIO whole-configuration issues, whose own dotted names are joined onto
the path of the endpoint they came from.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import io
import json
import sys
import warnings
from typing import Optional, TextIO, override

import pytest
from config_as_json import Config, ConfigMissingKey, ConfigNesting, \
    ConfigNestingKind, InvalidConfiguration, NestedConfigs, PathOrStr, \
    ValidationPlan
from tableio import Capabilities, FileAccess
from tableio_cfg_json import TioJsonConfig, TioJsonCsvConfig, \
    tio_json_config_default, tio_json_loader

CAPS = Capabilities()
GOOD_CSV: dict[str, object] = {'format_name': 'CSV', 'implementation': 'csv'}


# pylint: disable-next=too-many-arguments,too-many-positional-arguments
def _endpoint(file_access: FileAccess, from_json_data_text: Optional[str],
              from_json_filename: Optional[PathOrStr], stderr_file: TextIO,
              member_name: Optional[str],
              ok_to_use_defaults: bool) -> TioJsonConfig:
    """Construct one nested endpoint, telling it where it sits."""
    return TioJsonConfig(capabilities=CAPS, file_access=file_access,
                         format_name='CSV',
                         from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file, member_name=member_name,
                         ok_to_use_defaults=ok_to_use_defaults)


class _AppConfig(Config):
    """Application configuration owning one read and one write endpoint."""

    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr, *,
                 member_name: Optional[str] = None,
                 ok_to_use_defaults: bool = False) -> None:
        """Create or read a configuration holding two named endpoints."""
        self.input = tio_json_config_default(CAPS, FileAccess.READ,
                                             format_name='CSV')
        self.output = tio_json_config_default(CAPS, FileAccess.CREATE,
                                              format_name='CSV')
        Config.__init__(self, from_json_data_text=from_json_data_text,
                        from_json_filename=from_json_filename,
                        stderr_file=stderr_file, member_name=member_name,
                        ok_to_use_defaults=ok_to_use_defaults)

    @override
    def nested_configs(self) -> NestedConfigs:
        """Return the two endpoint members as nested configurations."""
        return {
            'input': ConfigNesting(kind=ConfigNestingKind.MEMBER,
                                   config_type=TioJsonConfig,
                                   factory_function=self._read_factory),
            'output': ConfigNesting(kind=ConfigNestingKind.MEMBER,
                                    config_type=TioJsonConfig,
                                    factory_function=self._write_factory)
        }

    @override
    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return an empty plan, each endpoint validating itself."""
        _ = stderr_file
        return []

    # pylint: disable-next=too-many-arguments,too-many-positional-arguments
    def _read_factory(self, from_json_data_text: Optional[str] = None,
                      from_json_filename: Optional[PathOrStr] = None,
                      stderr_file: TextIO = sys.stderr,
                      member_name: Optional[str] = None,
                      ok_to_use_defaults: bool = False) -> TioJsonConfig:
        """Construct the read endpoint from the JSON of its member."""
        return _endpoint(FileAccess.READ, from_json_data_text,
                         from_json_filename, stderr_file, member_name,
                         ok_to_use_defaults)

    # pylint: disable-next=too-many-arguments,too-many-positional-arguments
    def _write_factory(self, from_json_data_text: Optional[str] = None,
                       from_json_filename: Optional[PathOrStr] = None,
                       stderr_file: TextIO = sys.stderr,
                       member_name: Optional[str] = None,
                       ok_to_use_defaults: bool = False) -> TioJsonConfig:
        """Construct the write endpoint from the JSON of its member."""
        return _endpoint(FileAccess.CREATE, from_json_data_text,
                         from_json_filename, stderr_file, member_name,
                         ok_to_use_defaults)


def _app_text(member: str, faults: dict[str, object]) -> str:
    """Return application JSON where one named endpoint holds faults."""
    endpoints = {'input': dict(GOOD_CSV), 'output': dict(GOOD_CSV)}
    endpoints[member].update(faults)
    return json.dumps(endpoints)


def _refusal(text: str) -> str:
    """Return the message of the refusal of one application JSON text."""
    with pytest.raises(InvalidConfiguration) as exc_info:
        _AppConfig(from_json_data_text=text, stderr_file=io.StringIO())
    return str(exc_info.value)


@pytest.mark.parametrize('member', ['input', 'output'])
def test_nested_section(member: str) -> None:
    """A section of a nested endpoint is named below that endpoint."""
    text = _app_text(member, {'csv': {'delimiter': '::'}})
    assert f'{member}.csv.delimiter' in _refusal(text)


def test_nested_member() -> None:
    """A member of a nested endpoint is named below that endpoint."""
    text = _app_text('input', {'line_length': 11.0})
    assert 'input.line_length' in _refusal(text)


def test_nested_whole_cfg() -> None:
    """A TableIO whole-config issue is named below its endpoint."""
    text = _app_text('output', {'implementation': 'odfdo'})
    message = _refusal(text)
    assert message.startswith('output.implementation: ')


def test_top_level_plain() -> None:
    """The same fault at the top level is named without any prefix."""
    text = json.dumps(dict(GOOD_CSV) | {'csv': {'delimiter': '::'}})
    with pytest.raises(InvalidConfiguration) as exc_info:
        TioJsonConfig(CAPS, FileAccess.CREATE, from_json_data_text=text,
                      stderr_file=io.StringIO())
    message = str(exc_info.value)
    assert 'csv.delimiter' in message and 'input' not in message


def test_section_alone() -> None:
    """A section constructed on its own is named by the path it is told."""
    text = json.dumps({'delimiter': '::'})
    with pytest.raises(InvalidConfiguration) as exc_info:
        TioJsonCsvConfig(from_json_data_text=text,
                         member_name='reports[1].csv',
                         stderr_file=io.StringIO())
    assert 'reports[1].csv.delimiter' in str(exc_info.value)


def test_loader_path() -> None:
    """A loader told where its configuration sits names the path."""
    loader = tio_json_loader(CAPS, FileAccess.CREATE, format_name='CSV',
                             include_all_options=False, member_name='input')
    text = json.dumps(dict(GOOD_CSV) | {'csv': {'delimiter': '::'}})
    with pytest.raises(InvalidConfiguration) as exc_info:
        loader(from_json_data_text=text, stderr_file=io.StringIO())
    assert 'input.csv.delimiter' in str(exc_info.value)


@pytest.mark.parametrize('ok_to_use_defaults', [False, True])
def test_no_deprecation(ok_to_use_defaults: bool) -> None:
    """Accepting member_name and ok_to_use_defaults leaves nothing to warn.

    config-as-json passes ok_to_use_defaults to a factory only when the
    application configuration is read with it, so both ways are read here.
    """
    err = io.StringIO()
    with warnings.catch_warnings(record=True) as records:
        warnings.simplefilter('always')
        config = _AppConfig(from_json_data_text=_app_text('input', {}),
                            stderr_file=err,
                            ok_to_use_defaults=ok_to_use_defaults)
        config.validate(err)
        config.as_json_string(err)
    deprecated = [str(record.message) for record in records
                  if issubclass(record.category, DeprecationWarning)]
    assert deprecated == []


def test_nested_kept() -> None:
    """A value an endpoint lacks is kept, and named below that endpoint.

    The endpoint is built by a factory, so it is the factory passing
    ok_to_use_defaults on that lets the endpoint keep a default at all.
    """
    text = json.dumps({'input': dict(GOOD_CSV), 'output': {}})
    config = _AppConfig(from_json_data_text=text, stderr_file=io.StringIO(),
                        ok_to_use_defaults=True)
    assert config.kept_value_paths() == [('output', 'format_name')]
    assert config.output.format_name == 'CSV'
    assert config.output.file_access is FileAccess.CREATE


def test_nested_strict() -> None:
    """Read strictly, an endpoint lacking its format is refused."""
    text = json.dumps({'input': dict(GOOD_CSV), 'output': {}})
    with pytest.raises(ConfigMissingKey) as exc_info:
        _AppConfig(from_json_data_text=text, stderr_file=io.StringIO())
    assert 'output.format_name' in str(exc_info.value)
