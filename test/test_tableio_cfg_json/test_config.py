#! /usr/bin/env python3
"""Tests for tableio configuration classes using config-as-json."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import json
from pathlib import Path

import pytest
from config_as_json import Config, ConfigBadJson, InvalidConfiguration

from tableio import CAP_NEEDED, Capabilities, ConfigData, CsvDialect, \
    FileAccess, tio_config_optional_args
from tableio_cfg_json import TioJsonConfig, TioJsonCsvConfig, \
    TioJsonHtmlConfig, TioJsonLatexConfig, tio_json_config_default


def _json_text(data: dict[str, object]) -> str:
    """Return compact JSON text for one test configuration."""
    return json.dumps(data)


def _assert_no_none(value: object) -> None:
    """Assert that a decoded JSON value contains no null values."""
    assert value is not None
    if isinstance(value, dict):
        for nested_value in value.values():
            _assert_no_none(nested_value)
    if isinstance(value, list):
        for nested_value in value:
            _assert_no_none(nested_value)


def test_compact_default_bridge() -> None:
    """Compact defaults are both tableio data and config-as-json config."""
    config = tio_json_config_default(Capabilities(), FileAccess.CREATE)
    assert isinstance(config, ConfigData)
    assert isinstance(config, Config)
    assert config.format_name == 'Excel'
    assert config.implementation == 'XlsxWriter'
    assert config.csv is None
    assert config.html is None
    assert config.latex is None


def test_teaching_default_bridge() -> None:
    """Teaching defaults include bridge objects for every nested section."""
    config = tio_json_config_default(Capabilities(), FileAccess.CREATE,
                                     include_all_options=True)
    assert isinstance(config.csv, TioJsonCsvConfig)
    assert isinstance(config.html, TioJsonHtmlConfig)
    assert isinstance(config.latex, TioJsonLatexConfig)
    assert config.character_encoding is not None
    assert config.language is not None
    assert config.title is not None
    assert config.paper_size is not None
    assert config.line_length is not None
    assert config.table_max_line_length is not None
    assert config.table_alignment is not None
    assert config.csv.dialect is CsvDialect.UNIX
    assert config.csv.delimiter is not None
    assert config.csv.quoting is not None
    assert config.csv.quotechar is not None
    assert config.csv.lineterminator is not None
    assert config.csv.escapechar is not None
    assert config.html.css_file is not None
    assert config.latex.document_class is not None
    assert config.latex.preamble is not None


def test_compact_write_omits_none(tmp_path: Path) -> None:
    """Compact JSON output omits optional sections while they are None."""
    config = tio_json_config_default(Capabilities(), FileAccess.CREATE)
    config_file = tmp_path / 'tableio.json'
    config.write(to_json_filename=config_file)
    data = json.loads(config_file.read_text(encoding='utf-8'))
    assert data == {
        'format_name': 'Excel',
        'implementation': 'XlsxWriter'
    }


def test_teaching_roundtrip(tmp_path: Path) -> None:
    """Teaching JSON round-trips nested sections and enum values."""
    config = tio_json_config_default(Capabilities(), FileAccess.CREATE,
                                     include_all_options=True)
    config_file = tmp_path / 'tableio.json'
    config.write(to_json_filename=config_file)
    read_config = TioJsonConfig(Capabilities(), FileAccess.CREATE,
                                include_all_options=True,
                                from_json_filename=config_file)
    assert isinstance(read_config.csv, TioJsonCsvConfig)
    assert read_config.csv.dialect is CsvDialect.UNIX
    assert read_config.csv.delimiter == ','
    assert isinstance(read_config.html, TioJsonHtmlConfig)
    assert isinstance(read_config.latex, TioJsonLatexConfig)


def test_teaching_write_defaults(tmp_path: Path) -> None:
    """Teaching JSON writes explicit values for every default option."""
    config = tio_json_config_default(Capabilities(), FileAccess.CREATE,
                                     include_all_options=True)
    config_file = tmp_path / 'tableio.json'
    config.write(to_json_filename=config_file)
    data = json.loads(config_file.read_text(encoding='utf-8'))
    _assert_no_none(data)
    assert set(data) == {
        'format_name', 'implementation', 'character_encoding', 'language',
        'title', 'paper_size', 'line_length', 'table_max_line_length',
        'table_alignment', 'csv', 'html', 'latex'
    }
    csv = data['csv']
    assert isinstance(csv, dict)
    assert set(csv) == {
        'dialect', 'delimiter', 'quoting', 'quotechar', 'lineterminator',
        'escapechar'
    }
    assert csv['dialect'] == 'UNIX'
    html = data['html']
    assert isinstance(html, dict)
    assert set(html) == {'css_file'}
    latex = data['latex']
    assert isinstance(latex, dict)
    assert set(latex) == {'document_class', 'preamble'}


def test_compact_read_nested_section() -> None:
    """Compact JSON may still provide an optional nested section."""
    text = _json_text({
        'format_name': 'CSV',
        'implementation': 'csv',
        'csv': {'delimiter': ';'}
    })
    config = TioJsonConfig(Capabilities(), FileAccess.CREATE,
                           from_json_data_text=text)
    assert isinstance(config.csv, TioJsonCsvConfig)
    assert config.csv.delimiter == ';'
    assert config.csv.quotechar is None
    assert tio_config_optional_args(config) == {'csv_delimiter': ';'}


def test_member_choice_normalization() -> None:
    """Member validators normalize case-insensitive choices."""
    text = _json_text({
        'format_name': 'excel',
        'implementation': 'xlsxwriter',
        'paper_size': 'a4',
        'table_alignment': 'center_but_digits_right',
        'csv': {'quoting': 'ALL'}
    })
    config = TioJsonConfig(Capabilities(), FileAccess.CREATE,
                           from_json_data_text=text)
    assert config.format_name == 'Excel'
    assert config.implementation == 'XlsxWriter'
    assert config.paper_size == 'A4'
    assert config.table_alignment == 'CENTER_BUT_DIGITS_RIGHT'
    assert isinstance(config.csv, TioJsonCsvConfig)
    assert config.csv.quoting == 'all'


@pytest.mark.parametrize(
    ('dialect', 'expected'),
    [pytest.param('u', CsvDialect.UNIX, id='string-prefix'),
     pytest.param('excel', CsvDialect.EXCEL, id='string-name')])
def test_csv_dialect_parsing(dialect: object, expected: CsvDialect) -> None:
    """CSV dialect parsing uses config-as-json enum string matching."""
    text = _json_text({
        'format_name': 'CSV',
        'implementation': 'csv',
        'csv': {'dialect': dialect}
    })
    config = TioJsonConfig(Capabilities(), FileAccess.CREATE,
                           from_json_data_text=text)
    assert isinstance(config.csv, TioJsonCsvConfig)
    assert config.csv.dialect is expected


def test_csv_dialect_rejects_int() -> None:
    """CSV dialect parsing now accepts dialect names only."""
    text = _json_text({
        'format_name': 'CSV',
        'implementation': 'csv',
        'csv': {'dialect': 2}
    })
    with pytest.raises(ConfigBadJson) as exc_info:
        TioJsonConfig(Capabilities(), FileAccess.CREATE,
                      from_json_data_text=text)
    assert 'int not str' in str(exc_info.value)


@pytest.mark.parametrize(
    ('member_name', 'value'),
    [pytest.param('line_length', True, id='line-bool'),
     pytest.param('line_length', 11.0, id='line-float'),
     pytest.param('table_max_line_length', False, id='table-bool'),
     pytest.param('table_max_line_length', 10.0, id='table-float')])
def test_lengths_require_int(member_name: str, value: object) -> None:
    """Length member validators reject bool and float values."""
    data = {
        'format_name': 'CSV',
        'implementation': 'csv',
        member_name: value
    }
    with pytest.raises(InvalidConfiguration) as exc_info:
        TioJsonConfig(Capabilities(), FileAccess.CREATE,
                      from_json_data_text=_json_text(data))
    assert member_name in str(exc_info.value)


def test_member_bad_value() -> None:
    """Bridge member validators reject invalid individual values."""
    text = _json_text({
        'format_name': 'CSV',
        'implementation': 'csv',
        'csv': {'quoting': 'American'}
    })
    with pytest.raises(InvalidConfiguration) as exc_info:
        TioJsonConfig(Capabilities(), FileAccess.CREATE,
                      from_json_data_text=text)
    assert 'quoting' in str(exc_info.value)


def test_whole_impl_format() -> None:
    """Whole-config validation catches implementation format mismatch."""
    text = _json_text({
        'format_name': 'Excel',
        'implementation': 'csv'
    })
    with pytest.raises(InvalidConfiguration) as exc_info:
        TioJsonConfig(Capabilities(), FileAccess.CREATE,
                      from_json_data_text=text)
    assert 'implementation' in str(exc_info.value)


def test_whole_capabilities() -> None:
    """Whole-config validation uses application runtime capabilities."""
    caps = Capabilities(can_read_box=CAP_NEEDED)
    text = _json_text({
        'format_name': 'CSV',
        'implementation': 'csv'
    })
    with pytest.raises(InvalidConfiguration) as exc_info:
        TioJsonConfig(caps, FileAccess.CREATE, from_json_data_text=text)
    assert 'implementation' in str(exc_info.value)
