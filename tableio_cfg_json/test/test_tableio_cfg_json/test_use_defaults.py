#! /usr/bin/env python3
"""Tests for reading a JSON source that may leave members out.

config-as-json lets a JSON source lack members when it is read with
``ok_to_use_defaults=True``. Each of them then keeps its default, and
``kept_value_paths()`` tells which ones did. These tests check that every
class of this package accepts that keyword and passes it on, and that
TioJsonConfig then builds its defaults for the format that the JSON source
selects rather than for the preferred format given to the constructor.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import io
import json
from functools import partial
from pathlib import Path
from typing import Callable, Optional

import pytest
from config_as_json import Config, ConfigBadJson, ConfigMissingKey
from tableio import Capabilities, FileAccess
from tableio_cfg_json import TioJsonConfig, TioJsonCsvConfig, \
    TioJsonHtmlConfig, TioJsonLatexConfig, tio_json_config_default
from tableio_cfg_json.config import _json_selection

CAPS = Capabilities()
CSV_TEXT = json.dumps({'format_name': 'CSV'})
SECTIONS: list[tuple[Callable[..., Config], str, str]] = [
    (partial(TioJsonCsvConfig, delimiter=';'), 'delimiter', ';'),
    (partial(TioJsonHtmlConfig, css_file='site.css'), 'css_file', 'site.css'),
    (partial(TioJsonLatexConfig, preamble='%'), 'preamble', '%')]


def _written(config: Config) -> dict[str, object]:
    """Return the JSON that one configuration writes."""
    value = json.loads(config.as_json_string(stderr_file=io.StringIO()))
    assert isinstance(value, dict)
    return value


def _csv_endpoint(tmp_path: Path, as_file: bool,
                  ok_to_use_defaults: bool) -> TioJsonConfig:
    """Read a CSV endpoint that prefers Excel and wants every option.

    Args:
        tmp_path: Directory for the JSON file when one is used.
        as_file: Whether the JSON is given as a file rather than as text.
        ok_to_use_defaults: Whether the JSON may leave members out.
    Returns:
        The endpoint read from JSON that holds only the CSV format name.
    """
    json_file = tmp_path / 'endpoint.json'
    json_file.write_text(CSV_TEXT, encoding='utf-8')
    text: Optional[str] = None if as_file else CSV_TEXT
    filename: Optional[Path] = json_file if as_file else None
    return TioJsonConfig(CAPS, FileAccess.CREATE, format_name='Excel',
                         include_all_options=True, from_json_data_text=text,
                         from_json_filename=filename,
                         stderr_file=io.StringIO(),
                         ok_to_use_defaults=ok_to_use_defaults)


@pytest.mark.parametrize('section,member,value', SECTIONS)
def test_section_kept(section: Callable[..., Config], member: str,
                      value: str) -> None:
    """A section member that the source lacks keeps its default."""
    config = section(from_json_data_text='{}', ok_to_use_defaults=True)
    assert getattr(config, member) == value
    assert config.kept_value_paths() == [(member,)]


@pytest.mark.parametrize('section,member,value', SECTIONS)
def test_section_strict(section: Callable[..., Config], member: str,
                        value: str) -> None:
    """Read strictly, a section member that the source lacks is None."""
    config = section(from_json_data_text='{}')
    assert getattr(config, member) is None
    assert value not in _written(config).values()
    assert not config.kept_value_paths()


@pytest.mark.parametrize('as_file', [False, True])
def test_format_from_source(tmp_path: Path, as_file: bool) -> None:
    """Missing members get the defaults of the format the source selects."""
    config = _csv_endpoint(tmp_path, as_file, ok_to_use_defaults=True)
    expected = tio_json_config_default(CAPS, FileAccess.CREATE,
                                       format_name='CSV',
                                       include_all_options=True)
    assert _written(config) == _written(expected)
    assert ('implementation',) in config.kept_value_paths()


@pytest.mark.parametrize('as_file', [False, True])
def test_strict_compact(tmp_path: Path, as_file: bool) -> None:
    """Read strictly, only what the source holds is in the endpoint."""
    config = _csv_endpoint(tmp_path, as_file, ok_to_use_defaults=False)
    assert _written(config) == {'format_name': 'CSV'}
    assert not config.kept_value_paths()


def test_format_kept() -> None:
    """A source without a format keeps the preferred format."""
    config = TioJsonConfig(CAPS, FileAccess.CREATE, format_name='ODS',
                           from_json_data_text='{}', ok_to_use_defaults=True)
    assert config.format_name == 'ODS'
    assert config.kept_value_paths() == [('format_name',)]


def test_format_required() -> None:
    """Read strictly, a source without a format is refused."""
    with pytest.raises(ConfigMissingKey):
        TioJsonConfig(CAPS, FileAccess.CREATE, format_name='ODS',
                      from_json_data_text='{}', stderr_file=io.StringIO())


@pytest.mark.parametrize('text', ['not json at all', '[1, 2]', '"text"'])
def test_bad_text_refused(text: str) -> None:
    """Text that is no JSON object is refused by the parse as before."""
    with pytest.raises(ConfigBadJson):
        TioJsonConfig(CAPS, FileAccess.CREATE, from_json_data_text=text,
                      stderr_file=io.StringIO(), ok_to_use_defaults=True)


def test_missing_file_refused(tmp_path: Path) -> None:
    """A missing file is refused by the read as before."""
    with pytest.raises(SystemExit):
        TioJsonConfig(CAPS, FileAccess.CREATE,
                      from_json_filename=tmp_path / 'missing.json',
                      stderr_file=io.StringIO(), ok_to_use_defaults=True)


@pytest.mark.parametrize('text,expected', [
    (None, ('kept', None)),
    ('not json at all', ('kept', None)),
    ('[1, 2]', ('kept', None)),
    ('"text"', ('kept', None)),
    ('{"format_name": null}', ('kept', None)),
    ('{"other": 1}', ('kept', None)),
    ('{"format_name": "CSV"}', ('CSV', None)),
    ('{"implementation": "csv"}', ('kept', 'csv'))])
def test_json_selection(text: Optional[str],
                        expected: tuple[str, Optional[str]]) -> None:
    """Only a JSON object holding a member as a string selects it."""
    assert _json_selection(text, None, 'kept', None) == expected


@pytest.mark.parametrize('content,expected', [
    (CSV_TEXT.encode('utf-8'), 'CSV'),
    (b'\xff\xfe not UTF-8', 'kept')])
def test_selection_file(tmp_path: Path, content: bytes, expected: str) \
        -> None:
    """A file is read for its selection, and an unreadable one is not."""
    json_file = tmp_path / 'endpoint.json'
    json_file.write_bytes(content)
    assert _json_selection(None, json_file, 'kept', None) == (expected, None)


def test_selection_no_file(tmp_path: Path) -> None:
    """A file that does not exist selects nothing."""
    missing = tmp_path / 'missing.json'
    assert _json_selection(None, missing, 'kept', 'impl') == ('kept', 'impl')
