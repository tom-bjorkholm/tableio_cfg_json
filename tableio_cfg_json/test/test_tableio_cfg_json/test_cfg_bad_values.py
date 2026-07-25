#! /usr/bin/env python3
"""Tests that invalid TableIO JSON config values are rejected.

Each test injects one bad value, either on the config object before
writing or into a written config file before reading, and asserts the
write or read fails without producing a usable config.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional, cast

import pytest
from config_as_json import ConfigBadJson, InvalidConfiguration
from tableio import CsvDialect
from tableio_cfg_json import TioJsonConfig, TioJsonCsvConfig, \
    TioJsonHtmlConfig, TioJsonLatexConfig
from .cfg_rw_support import CAPABILITIES, FILE_ACCESS


def _read_json_object(config_file: Path) -> dict[str, object]:
    """Return one decoded JSON object from a config file."""
    data = json.loads(config_file.read_text(encoding='utf-8'))
    assert isinstance(data, dict)
    return data


def _write_json_object(config_file: Path, data: dict[str, object]) -> None:
    """Write one decoded JSON object back to a config file."""
    config_file.write_text(json.dumps(data, indent=4), encoding='utf-8')


def _assert_write_fails(config: TioJsonConfig, config_file: Path,
                        exception: type[Exception], error_text: str) -> None:
    """Assert that writing bad config data fails without creating a file."""
    with pytest.raises(exception) as exc_info:
        config.write(to_json_filename=config_file)
    assert error_text in str(exc_info.value)
    assert not config_file.exists()


def _assert_read_fails(config_file: Path, exception: type[Exception],
                       error_text: str) -> None:
    """Assert that reading bad config data fails with the expected text."""
    with pytest.raises(exception) as exc_info:
        TioJsonConfig(CAPABILITIES, FILE_ACCESS,
                      from_json_filename=config_file)
    assert error_text in str(exc_info.value)


@pytest.mark.parametrize(
    ('format_name', 'exception', 'error_text'),
    [pytest.param('bad-format', InvalidConfiguration, 'format_name',
                  id='unknown'),
     pytest.param(7, InvalidConfiguration, 'format_name', id='int')])
def test_bad_format_name(format_name: object, exception: type[Exception],
                         error_text: str) -> None:
    """Invalid format names fail both writing and reading."""
    config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
    config.format_name = cast(str, format_name)
    with TemporaryDirectory() as temp_name:
        config_file = Path(temp_name) / 'config.json'
        _assert_write_fails(config, config_file, exception, error_text)
        valid_config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
        valid_config.write(to_json_filename=config_file)
        data = _read_json_object(config_file)
        data['format_name'] = format_name
        _write_json_object(config_file, data)
        _assert_read_fails(config_file, exception, error_text)


@pytest.mark.parametrize(
    ('format_name', 'implementation', 'exception', 'error_text'),
    [pytest.param('Excel', 'bad-impl', InvalidConfiguration, 'implementation',
                  id='unknown'),
     pytest.param('Excel', 7, InvalidConfiguration, 'implementation',
                  id='int'),
     pytest.param('Excel', 'csv', InvalidConfiguration, 'implementation',
                  id='wrong-format')])
def test_bad_implementation(format_name: str, implementation: object,
                            exception: type[Exception],
                            error_text: str) -> None:
    """Invalid implementations fail both writing and reading."""
    config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
    config.format_name = format_name
    config.implementation = cast(Optional[str], implementation)
    with TemporaryDirectory() as temp_name:
        config_file = Path(temp_name) / 'config.json'
        _assert_write_fails(config, config_file, exception, error_text)
        valid_config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
        valid_config.format_name = format_name
        valid_config.write(to_json_filename=config_file)
        data = _read_json_object(config_file)
        data['implementation'] = implementation
        _write_json_object(config_file, data)
        _assert_read_fails(config_file, exception, error_text)


@pytest.mark.parametrize(
    ('encoding', 'exception', 'error_text'),
    [pytest.param('bad-encoding-name', InvalidConfiguration,
                  'character_encoding', id='unknown'),
     pytest.param(7, InvalidConfiguration, 'character_encoding', id='int')])
def test_bad_encoding_file(encoding: object, exception: type[Exception],
                           error_text: str) -> None:
    """Invalid character encodings fail both writing and reading."""
    config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
    config.character_encoding = cast(Optional[str], encoding)
    with TemporaryDirectory() as temp_name:
        config_file = Path(temp_name) / 'config.json'
        _assert_write_fails(config, config_file, exception, error_text)
        valid_config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
        valid_config.write(to_json_filename=config_file)
        data = _read_json_object(config_file)
        data['character_encoding'] = encoding
        _write_json_object(config_file, data)
        _assert_read_fails(config_file, exception, error_text)


@pytest.mark.parametrize(
    ('language', 'exception', 'error_text'),
    [pytest.param(7, InvalidConfiguration, 'language', id='int'),
     pytest.param(['en'], InvalidConfiguration, 'language', id='list')])
def test_bad_language_file(language: object, exception: type[Exception],
                           error_text: str) -> None:
    """Invalid languages fail both writing and reading."""
    config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
    config.language = cast(Optional[str], language)
    with TemporaryDirectory() as temp_name:
        config_file = Path(temp_name) / 'config.json'
        _assert_write_fails(config, config_file, exception, error_text)
        valid_config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
        valid_config.write(to_json_filename=config_file)
        data = _read_json_object(config_file)
        data['language'] = language
        _write_json_object(config_file, data)
        _assert_read_fails(config_file, exception, error_text)


@pytest.mark.parametrize(
    ('title', 'exception', 'error_text'),
    [pytest.param(7, InvalidConfiguration, 'title', id='int'),
     pytest.param(['Title'], InvalidConfiguration, 'title', id='list')])
def test_bad_title_file(title: object, exception: type[Exception],
                        error_text: str) -> None:
    """Invalid titles fail both writing and reading."""
    config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
    config.title = cast(Optional[str], title)
    with TemporaryDirectory() as temp_name:
        config_file = Path(temp_name) / 'config.json'
        _assert_write_fails(config, config_file, exception, error_text)
        valid_config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
        valid_config.write(to_json_filename=config_file)
        data = _read_json_object(config_file)
        data['title'] = title
        _write_json_object(config_file, data)
        _assert_read_fails(config_file, exception, error_text)


@pytest.mark.parametrize(
    ('paper_size', 'exception', 'error_text'),
    [pytest.param('A2', InvalidConfiguration, 'paper_size', id='unknown'),
     pytest.param(7, InvalidConfiguration, 'paper_size', id='int')])
def test_bad_paper_size_file(paper_size: object, exception: type[Exception],
                             error_text: str) -> None:
    """Invalid paper sizes fail both writing and reading."""
    config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
    config.paper_size = cast(Optional[str], paper_size)
    with TemporaryDirectory() as temp_name:
        config_file = Path(temp_name) / 'config.json'
        _assert_write_fails(config, config_file, exception, error_text)
        valid_config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
        valid_config.write(to_json_filename=config_file)
        data = _read_json_object(config_file)
        data['paper_size'] = paper_size
        _write_json_object(config_file, data)
        _assert_read_fails(config_file, exception, error_text)


@pytest.mark.parametrize(
    ('line_length', 'exception', 'error_text'),
    [pytest.param(10, InvalidConfiguration, 'line_length', id='too-small'),
     pytest.param(11.0, InvalidConfiguration, 'line_length', id='float'),
     pytest.param(False, InvalidConfiguration, 'line_length', id='bool')])
def test_bad_line_length_file(line_length: object, exception: type[Exception],
                              error_text: str) -> None:
    """Invalid line lengths fail both writing and reading."""
    config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
    config.line_length = cast(Optional[int], line_length)
    with TemporaryDirectory() as temp_name:
        config_file = Path(temp_name) / 'config.json'
        _assert_write_fails(config, config_file, exception, error_text)
        valid_config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
        valid_config.write(to_json_filename=config_file)
        data = _read_json_object(config_file)
        data['line_length'] = line_length
        _write_json_object(config_file, data)
        _assert_read_fails(config_file, exception, error_text)


@pytest.mark.parametrize(
    ('table_length', 'exception', 'error_text'),
    [pytest.param(9, InvalidConfiguration, 'table_max_line_length',
                  id='too-small'),
     pytest.param(10.0, InvalidConfiguration, 'table_max_line_length',
                  id='float'),
     pytest.param(False, InvalidConfiguration, 'table_max_line_length',
                  id='bool')])
def test_bad_table_len_file(table_length: object, exception: type[Exception],
                            error_text: str) -> None:
    """Invalid table line lengths fail both writing and reading."""
    config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
    config.table_max_line_length = cast(Optional[int], table_length)
    with TemporaryDirectory() as temp_name:
        config_file = Path(temp_name) / 'config.json'
        _assert_write_fails(config, config_file, exception, error_text)
        valid_config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
        valid_config.write(to_json_filename=config_file)
        data = _read_json_object(config_file)
        data['table_max_line_length'] = table_length
        _write_json_object(config_file, data)
        _assert_read_fails(config_file, exception, error_text)


@pytest.mark.parametrize(
    ('alignment', 'exception', 'error_text'),
    [pytest.param('MIDDLE', InvalidConfiguration, 'table_alignment',
                  id='unknown'),
     pytest.param(7, InvalidConfiguration, 'table_alignment', id='int')])
def test_bad_table_align_file(alignment: object, exception: type[Exception],
                              error_text: str) -> None:
    """Invalid table alignments fail both writing and reading."""
    config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
    config.table_alignment = cast(Optional[str], alignment)
    with TemporaryDirectory() as temp_name:
        config_file = Path(temp_name) / 'config.json'
        _assert_write_fails(config, config_file, exception, error_text)
        valid_config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
        valid_config.write(to_json_filename=config_file)
        data = _read_json_object(config_file)
        data['table_alignment'] = alignment
        _write_json_object(config_file, data)
        _assert_read_fails(config_file, exception, error_text)


@pytest.mark.parametrize(
    ('dialect', 'exception', 'error_text', 'read_exception', 'read_text'),
    [pytest.param('BOGUS', InvalidConfiguration, 'csv.dialect', ConfigBadJson,
                  'EXCEL, UNIX', id='unknown'),
     pytest.param(7, InvalidConfiguration, 'csv.dialect', ConfigBadJson,
                  'int not str', id='int')])
def test_bad_csv_dialect_file(dialect: object, exception: type[Exception],
                              error_text: str, read_exception: type[Exception],
                              read_text: str) -> None:
    """Invalid CSV dialects fail both writing and reading."""
    config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
    csv_config = TioJsonCsvConfig()
    config.format_name = 'CSV'
    csv_config.dialect = cast(Optional[CsvDialect], dialect)
    config.csv = csv_config
    with TemporaryDirectory() as temp_name:
        config_file = Path(temp_name) / 'config.json'
        _assert_write_fails(config, config_file, exception, error_text)
        valid_config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
        valid_csv = TioJsonCsvConfig()
        valid_config.format_name = 'CSV'
        valid_config.csv = valid_csv
        valid_config.write(to_json_filename=config_file)
        data = _read_json_object(config_file)
        csv_data = data['csv']
        assert isinstance(csv_data, dict)
        csv_data['dialect'] = dialect
        _write_json_object(config_file, data)
        _assert_read_fails(config_file, read_exception, read_text)


@pytest.mark.parametrize(
    ('delimiter', 'exception', 'error_text'),
    [pytest.param('', InvalidConfiguration, 'delimiter', id='empty'),
     pytest.param('::', InvalidConfiguration, 'delimiter', id='long'),
     pytest.param(7, InvalidConfiguration, 'delimiter', id='int')])
def test_bad_csv_delim_file(delimiter: object, exception: type[Exception],
                            error_text: str) -> None:
    """Invalid CSV delimiters fail both writing and reading."""
    config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
    csv_config = TioJsonCsvConfig()
    config.format_name = 'CSV'
    csv_config.delimiter = cast(Optional[str], delimiter)
    config.csv = csv_config
    with TemporaryDirectory() as temp_name:
        config_file = Path(temp_name) / 'config.json'
        _assert_write_fails(config, config_file, exception, error_text)
        valid_config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
        valid_csv = TioJsonCsvConfig()
        valid_config.format_name = 'CSV'
        valid_config.csv = valid_csv
        valid_config.write(to_json_filename=config_file)
        data = _read_json_object(config_file)
        csv_data = data['csv']
        assert isinstance(csv_data, dict)
        csv_data['delimiter'] = delimiter
        _write_json_object(config_file, data)
        _assert_read_fails(config_file, exception, error_text)


@pytest.mark.parametrize(
    ('quoting', 'exception', 'error_text'),
    [pytest.param('invalid', InvalidConfiguration, 'quoting', id='unknown'),
     pytest.param(7, InvalidConfiguration, 'quoting', id='int')])
def test_bad_csv_quoting_file(quoting: object, exception: type[Exception],
                              error_text: str) -> None:
    """Invalid CSV quoting values fail both writing and reading."""
    config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
    csv_config = TioJsonCsvConfig()
    config.format_name = 'CSV'
    csv_config.quoting = cast(Optional[str], quoting)
    config.csv = csv_config
    with TemporaryDirectory() as temp_name:
        config_file = Path(temp_name) / 'config.json'
        _assert_write_fails(config, config_file, exception, error_text)
        valid_config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
        valid_csv = TioJsonCsvConfig()
        valid_config.format_name = 'CSV'
        valid_config.csv = valid_csv
        valid_config.write(to_json_filename=config_file)
        data = _read_json_object(config_file)
        csv_data = data['csv']
        assert isinstance(csv_data, dict)
        csv_data['quoting'] = quoting
        _write_json_object(config_file, data)
        _assert_read_fails(config_file, exception, error_text)


@pytest.mark.parametrize(
    ('quotechar', 'exception', 'error_text'),
    [pytest.param('', InvalidConfiguration, 'quotechar', id='empty'),
     pytest.param('""', InvalidConfiguration, 'quotechar', id='long'),
     pytest.param(7, InvalidConfiguration, 'quotechar', id='int')])
def test_bad_csv_quote_file(quotechar: object, exception: type[Exception],
                            error_text: str) -> None:
    """Invalid CSV quote characters fail both writing and reading."""
    config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
    csv_config = TioJsonCsvConfig()
    config.format_name = 'CSV'
    csv_config.quotechar = cast(Optional[str], quotechar)
    config.csv = csv_config
    with TemporaryDirectory() as temp_name:
        config_file = Path(temp_name) / 'config.json'
        _assert_write_fails(config, config_file, exception, error_text)
        valid_config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
        valid_csv = TioJsonCsvConfig()
        valid_config.format_name = 'CSV'
        valid_config.csv = valid_csv
        valid_config.write(to_json_filename=config_file)
        data = _read_json_object(config_file)
        csv_data = data['csv']
        assert isinstance(csv_data, dict)
        csv_data['quotechar'] = quotechar
        _write_json_object(config_file, data)
        _assert_read_fails(config_file, exception, error_text)


@pytest.mark.parametrize(
    ('lineterminator', 'exception', 'error_text'),
    [pytest.param('', InvalidConfiguration, 'lineterminator', id='empty'),
     pytest.param(7, InvalidConfiguration, 'lineterminator', id='int')])
def test_bad_csv_line_file(lineterminator: object, exception: type[Exception],
                           error_text: str) -> None:
    """Invalid CSV line terminators fail both writing and reading."""
    config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
    csv_config = TioJsonCsvConfig()
    config.format_name = 'CSV'
    csv_config.lineterminator = cast(Optional[str], lineterminator)
    config.csv = csv_config
    with TemporaryDirectory() as temp_name:
        config_file = Path(temp_name) / 'config.json'
        _assert_write_fails(config, config_file, exception, error_text)
        valid_config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
        valid_csv = TioJsonCsvConfig()
        valid_config.format_name = 'CSV'
        valid_config.csv = valid_csv
        valid_config.write(to_json_filename=config_file)
        data = _read_json_object(config_file)
        csv_data = data['csv']
        assert isinstance(csv_data, dict)
        csv_data['lineterminator'] = lineterminator
        _write_json_object(config_file, data)
        _assert_read_fails(config_file, exception, error_text)


@pytest.mark.parametrize(
    ('escapechar', 'exception', 'error_text'),
    [pytest.param('', InvalidConfiguration, 'escapechar', id='empty'),
     pytest.param('\\\\', InvalidConfiguration, 'escapechar', id='long'),
     pytest.param(7, InvalidConfiguration, 'escapechar', id='int')])
def test_bad_csv_escape_file(escapechar: object, exception: type[Exception],
                             error_text: str) -> None:
    """Invalid CSV escape characters fail both writing and reading."""
    config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
    csv_config = TioJsonCsvConfig()
    config.format_name = 'CSV'
    csv_config.escapechar = cast(Optional[str], escapechar)
    config.csv = csv_config
    with TemporaryDirectory() as temp_name:
        config_file = Path(temp_name) / 'config.json'
        _assert_write_fails(config, config_file, exception, error_text)
        valid_config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
        valid_csv = TioJsonCsvConfig()
        valid_config.format_name = 'CSV'
        valid_config.csv = valid_csv
        valid_config.write(to_json_filename=config_file)
        data = _read_json_object(config_file)
        csv_data = data['csv']
        assert isinstance(csv_data, dict)
        csv_data['escapechar'] = escapechar
        _write_json_object(config_file, data)
        _assert_read_fails(config_file, exception, error_text)


@pytest.mark.parametrize(
    ('css_file', 'exception', 'error_text'),
    [pytest.param(7, InvalidConfiguration, 'css_file', id='int'),
     pytest.param(['style.css'], InvalidConfiguration, 'css_file', id='list')])
def test_bad_html_css_file(css_file: object, exception: type[Exception],
                           error_text: str) -> None:
    """Invalid HTML CSS files fail both writing and reading."""
    config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
    html_config = TioJsonHtmlConfig()
    html_config.css_file = cast(Optional[str], css_file)
    config.html = html_config
    with TemporaryDirectory() as temp_name:
        config_file = Path(temp_name) / 'config.json'
        _assert_write_fails(config, config_file, exception, error_text)
        valid_config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
        valid_html = TioJsonHtmlConfig()
        valid_config.html = valid_html
        valid_config.write(to_json_filename=config_file)
        data = _read_json_object(config_file)
        html_data = data['html']
        assert isinstance(html_data, dict)
        html_data['css_file'] = css_file
        _write_json_object(config_file, data)
        _assert_read_fails(config_file, exception, error_text)


@pytest.mark.parametrize(
    ('document_class', 'exception', 'error_text'),
    [pytest.param('Memo', InvalidConfiguration, 'document_class',
                  id='unknown'),
     pytest.param(7, InvalidConfiguration, 'document_class', id='int')])
def test_bad_latex_class(document_class: object, exception: type[Exception],
                         error_text: str) -> None:
    """Invalid LaTeX document classes fail both writing and reading."""
    config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
    latex_config = TioJsonLatexConfig()
    config.format_name = 'LaTeX'
    latex_config.document_class = cast(Optional[str], document_class)
    config.latex = latex_config
    with TemporaryDirectory() as temp_name:
        config_file = Path(temp_name) / 'config.json'
        _assert_write_fails(config, config_file, exception, error_text)
        valid_config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
        valid_latex = TioJsonLatexConfig()
        valid_config.format_name = 'LaTeX'
        valid_config.latex = valid_latex
        valid_config.write(to_json_filename=config_file)
        data = _read_json_object(config_file)
        latex_data = data['latex']
        assert isinstance(latex_data, dict)
        latex_data['document_class'] = document_class
        _write_json_object(config_file, data)
        _assert_read_fails(config_file, exception, error_text)


@pytest.mark.parametrize(
    ('preamble', 'exception', 'error_text'),
    [pytest.param(7, InvalidConfiguration, 'preamble', id='int'),
     pytest.param(['\\usepackage{booktabs}'], InvalidConfiguration, 'preamble',
                  id='list')])
def test_bad_latex_preamble(preamble: object, exception: type[Exception],
                            error_text: str) -> None:
    """Invalid LaTeX preambles fail both writing and reading."""
    config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
    latex_config = TioJsonLatexConfig()
    config.format_name = 'LaTeX'
    latex_config.preamble = cast(Optional[str], preamble)
    config.latex = latex_config
    with TemporaryDirectory() as temp_name:
        config_file = Path(temp_name) / 'config.json'
        _assert_write_fails(config, config_file, exception, error_text)
        valid_config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
        valid_latex = TioJsonLatexConfig()
        valid_config.format_name = 'LaTeX'
        valid_config.latex = valid_latex
        valid_config.write(to_json_filename=config_file)
        data = _read_json_object(config_file)
        latex_data = data['latex']
        assert isinstance(latex_data, dict)
        latex_data['preamble'] = preamble
        _write_json_object(config_file, data)
        _assert_read_fails(config_file, exception, error_text)
