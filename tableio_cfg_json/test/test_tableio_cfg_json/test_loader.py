#! /usr/bin/env python3
"""Tests for constructing a TioJsonConfig inside a config editor."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

# pylint: disable=protected-access

import json
from pathlib import Path
import sys
from typing import Optional

import pytest

from edit_cfg_json import ConfigLoader, LoadPolicy, editor_model, \
    model_as_text
from tableio import Capabilities, ConfigError, FileAccess, \
    access_capabilities
from tableio_cfg_json import TIO_JSON_DESCRIPTIONS, TioJsonConfig, \
    tio_json_config_default, tio_json_create_loader, tio_json_loader, \
    tio_json_read_loader, tio_json_update_loader
from tableio_cfg_json.loader import NO_FILE_NAME, _json_member

CAPS = Capabilities()

READY_MADE = [(tio_json_read_loader, FileAccess.READ),
              (tio_json_create_loader, FileAccess.CREATE),
              (tio_json_update_loader, FileAccess.UPDATE)]


def _loader(include_all_options: bool = True,
            file_access: FileAccess = FileAccess.CREATE) -> ConfigLoader:
    """Return a loader for one endpoint of the tests."""
    return tio_json_loader(CAPS, file_access,
                           include_all_options=include_all_options)


def _loaded(text: Optional[str],
            include_all_options: bool = True) -> TioJsonConfig:
    """Return the configuration that one loader makes of JSON text."""
    config = _loader(include_all_options)(from_json_data_text=text,
                                          ok_to_use_defaults=True)
    assert isinstance(config, TioJsonConfig)
    return config


def _written(config: TioJsonConfig) -> dict[str, object]:
    """Return the JSON that one configuration writes."""
    value = json.loads(config.as_json_string(stderr_file=sys.stderr))
    assert isinstance(value, dict)
    return value


def test_loader_without_json() -> None:
    """With no JSON text the loader answers with TableIO defaults."""
    config = _loaded(None)
    assert config.format_name is not None
    assert config.file_access is FileAccess.CREATE


@pytest.mark.parametrize('format_name', ['CSV', 'Excel', 'HTML'])
def test_format_from_json(format_name: str) -> None:
    """The format in the JSON text decides the defaults built on."""
    config = _loaded(json.dumps({'format_name': format_name}))
    assert config.format_name == format_name
    assert config.implementation is not None


def test_compact_gains_opts() -> None:
    """A compact file opens with every option present as a value."""
    written = _written(_loaded(json.dumps({'format_name': 'CSV'})))
    for name in ['implementation', 'character_encoding', 'paper_size',
                 'csv', 'html', 'latex']:
        assert name in written


def test_thin_stays_compact() -> None:
    """Without all options the loader keeps what the file held."""
    config = _loaded(json.dumps({'format_name': 'CSV'}),
                     include_all_options=False)
    assert _written(config) == {'format_name': 'CSV'}


def test_impl_kept() -> None:
    """An implementation named in the file survives the load."""
    text = json.dumps({'format_name': 'Excel', 'implementation': 'OpenPyXL'})
    assert _loaded(text).implementation == 'OpenPyXL'


def test_preferred_format() -> None:
    """A preferred format is used while the JSON text names none."""
    loader = tio_json_loader(CAPS, FileAccess.CREATE, format_name='CSV')
    config = loader()
    assert isinstance(config, TioJsonConfig)
    assert config.format_name == 'CSV'


def test_json_text_wins() -> None:
    """The format in the file wins over the preferred one."""
    loader = tio_json_loader(CAPS, FileAccess.CREATE, format_name='CSV')
    config = loader(from_json_data_text=json.dumps({'format_name': 'HTML'}),
                    ok_to_use_defaults=True)
    assert isinstance(config, TioJsonConfig)
    assert config.format_name == 'HTML'


@pytest.mark.parametrize('text,expected', [
    (None, 'kept'),
    ('not json at all', 'kept'),
    ('[1, 2]', 'kept'),
    ('"text"', 'kept'),
    ('{"format_name": null}', 'kept'),
    ('{"other": 1}', 'kept'),
    ('{"format_name": "CSV"}', 'CSV')])
def test_peeked_member(text: Optional[str], expected: str) -> None:
    """Only a JSON object holding that member as a string answers."""
    assert _json_member(text, 'format_name', 'kept') == expected


@pytest.mark.parametrize('text', ['not json at all', '[1, 2]', '"text"',
                                  '{"format_name": null}', '{"other": 1}'])
def test_unusable_text(text: str) -> None:
    """Text the class cannot read is refused the way the editor expects."""
    with pytest.raises((ValueError, KeyError)):
        _loaded(text)


def test_file_name_refused() -> None:
    """A file name is refused rather than quietly ignored."""
    with pytest.raises(ValueError) as caught:
        _loader()(from_json_filename='some_file.json')
    assert NO_FILE_NAME in str(caught.value)


def test_bad_format_refused() -> None:
    """An unregistered format is reported and not worked around."""
    with pytest.raises(ConfigError):
        _loaded(json.dumps({'format_name': 'Nonsense'}))


def test_file_access_kept() -> None:
    """The file access of the endpoint reaches the configuration."""
    config = _loader(file_access=FileAccess.READ)()
    assert isinstance(config, TioJsonConfig)
    assert config.file_access is FileAccess.READ


def _model_text(in_file: Path) -> str:
    """Return the editor model of one configuration file as text."""
    config = tio_json_config_default(CAPS, FileAccess.CREATE)
    model = editor_model(config, descriptions=TIO_JSON_DESCRIPTIONS,
                         in_file=in_file, loader=_loader(),
                         policy=LoadPolicy.DEFAULTS)
    return model_as_text(model)


@pytest.fixture(name='csv_file')
def fixture_csv_file(tmp_path: Path) -> Path:
    """Return a compact configuration file selecting CSV."""
    in_file = tmp_path / 'endpoint.json'
    in_file.write_text(json.dumps({'format_name': 'CSV'}), encoding='utf-8')
    return in_file


def test_editor_shows_text(csv_file: Path) -> None:
    """An editing session shows what this package says about a member."""
    text = _model_text(csv_file)
    assert 'The TableIO format name to use.' in text
    assert 'Choices: A3, A4, A5, Legal, Letter.' in text
    assert 'These settings are used only by the formats named below.' in text


def test_editor_nested_text(csv_file: Path) -> None:
    """The descriptions of a nested section reach the rows below it."""
    text = _model_text(csv_file)
    assert 'all: Quote every field.' in text
    assert 'UNIX: Comma separated' in text
    # The editor lists the names of an enum itself, and the description of
    # that member must not list them a second time.
    assert text.count('EXCEL, UNIX') == 1


@pytest.mark.parametrize('loader,file_access', READY_MADE)
def test_ready_made_access(loader: ConfigLoader,
                           file_access: FileAccess) -> None:
    """Each ready-made loader is the loader of the access it names."""
    config = loader()
    assert isinstance(config, TioJsonConfig)
    assert config.file_access is file_access


@pytest.mark.parametrize('loader,file_access', READY_MADE)
def test_ready_made_loads(loader: ConfigLoader,
                          file_access: FileAccess) -> None:
    """A ready-made loader is a loader and not a factory of one.

    This is what makes it usable as the --loader name of a program that is
    told a name on a command line, which cannot call anything.
    """
    _ = file_access
    assert isinstance(loader, ConfigLoader)
    config = loader(from_json_data_text=json.dumps({'format_name': 'CSV'}),
                    ok_to_use_defaults=True)
    assert isinstance(config, TioJsonConfig)
    assert config.format_name == 'CSV'


def test_ready_made_caps() -> None:
    """A ready-made loader asks for no capability beyond its access."""
    config = tio_json_create_loader()
    assert isinstance(config, TioJsonConfig)
    assert config.capabilities == access_capabilities(FileAccess.CREATE)


def test_read_refuses_write() -> None:
    """A write-only format is refused by the read loader and not by write."""
    text = json.dumps({'format_name': 'HTML'})
    written = tio_json_create_loader(from_json_data_text=text,
                                     ok_to_use_defaults=True)
    assert isinstance(written, TioJsonConfig)
    with pytest.raises(ValueError):
        tio_json_read_loader(from_json_data_text=text, ok_to_use_defaults=True)
