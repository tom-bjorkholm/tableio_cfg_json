#! /usr/bin/env python3
"""Tests for writing and reading individual TableIO JSON config values."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from typing import Optional, cast

import pytest
from config_as_json import ConfigBadJson, InvalidConfiguration
from tableio import CsvDialect, FileAccess, access_capabilities
from tableio_cfg_json import TioJsonConfig, TioJsonCsvConfig, \
    TioJsonHtmlConfig, TioJsonLatexConfig


FILE_ACCESS = FileAccess.CREATE
CAPABILITIES = access_capabilities(FILE_ACCESS, error_file=sys.stderr)


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
    ('format_name', 'implementation'),
    [pytest.param('CSV', 'csv', id='csv-csv'),
     pytest.param('CSV', None, id='csv-none'),
     pytest.param('Excel', 'OpenPyXL', id='excel-openpyxl'),
     pytest.param('Excel', 'XlsxWriter', id='excel-xlsxwriter'),
     pytest.param('Excel', 'pylightxl', id='excel-pylightxl'),
     pytest.param('Excel', None, id='excel-none'),
     pytest.param('HTML', 'mformat', id='html-mformat'),
     pytest.param('HTML', None, id='html-none'),
     pytest.param('LaTeX', 'mformat', id='latex-mformat'),
     pytest.param('LaTeX', None, id='latex-none'),
     pytest.param('ODS', 'odfdo', id='ods-odfdo'),
     pytest.param('ODS', None, id='ods-none'),
     pytest.param('docx', 'mformat', id='docx-mformat'),
     pytest.param('docx', None, id='docx-none'),
     pytest.param('md', 'mformat', id='md-mformat'),
     pytest.param('md', None, id='md-none'),
     pytest.param('odt', 'mformat', id='odt-mformat'),
     pytest.param('odt', None, id='odt-none'),
     pytest.param('pdf', 'mformat', id='pdf-mformat'),
     pytest.param('pdf', None, id='pdf-none'),
     pytest.param('reST', 'mformat', id='rest-mformat'),
     pytest.param('reST', None, id='rest-none'),
     pytest.param('rtf', 'mformat', id='rtf-mformat'),
     pytest.param('rtf', None, id='rtf-none'),
     pytest.param('txt', 'mformat', id='txt-mformat'),
     pytest.param('txt', None, id='txt-none')])
def test_format_impl_file(format_name: str,
                          implementation: Optional[str]) -> None:
    """Format names round-trip with matching implementations."""
    config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
    config.format_name = format_name
    config.implementation = implementation
    with TemporaryDirectory() as temp_name:
        config_file = Path(temp_name) / 'config.json'
        config.write(to_json_filename=config_file)
        read_config = TioJsonConfig(CAPABILITIES, FILE_ACCESS,
                                    from_json_filename=config_file)
        assert read_config.format_name == format_name
        assert read_config.implementation == implementation


@pytest.mark.parametrize(
    ('encoding', 'language'),
    [pytest.param('utf-8', 'en', id='utf8-en'),
     pytest.param('iso-8859-1', 'sv', id='latin1-sv')])
def test_encoding_lang_file(encoding: str, language: str) -> None:
    """Character encoding and language values round-trip."""
    config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
    config.character_encoding = encoding
    config.language = language
    with TemporaryDirectory() as temp_name:
        config_file = Path(temp_name) / 'config.json'
        config.write(to_json_filename=config_file)
        read_config = TioJsonConfig(CAPABILITIES, FILE_ACCESS,
                                    from_json_filename=config_file)
        assert read_config.character_encoding == encoding
        assert read_config.language == language


@pytest.mark.parametrize(
    ('title', 'css_file'),
    [pytest.param('Quarterly report', 'report.css', id='report-css'),
     pytest.param('City export', 'theme/main.css', id='city-css')])
def test_title_css_file(title: str, css_file: str) -> None:
    """Title and HTML CSS file values round-trip."""
    config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
    html_config = TioJsonHtmlConfig()
    config.title = title
    html_config.css_file = css_file
    config.html = html_config
    with TemporaryDirectory() as temp_name:
        config_file = Path(temp_name) / 'config.json'
        config.write(to_json_filename=config_file)
        read_config = TioJsonConfig(CAPABILITIES, FILE_ACCESS,
                                    from_json_filename=config_file)
        assert read_config.title == title
        assert isinstance(read_config.html, TioJsonHtmlConfig)
        assert read_config.html.css_file == css_file


@pytest.mark.parametrize(
    ('paper_size', 'table_alignment'),
    [pytest.param('A3', 'RIGHT', id='a3-right'),
     pytest.param('A4', 'LEFT', id='a4-left'),
     pytest.param('A5', 'LEFT_BUT_DIGITS_RIGHT', id='a5-digits'),
     pytest.param('Legal', 'CENTER', id='legal-center'),
     pytest.param('Letter', 'CENTER_BUT_DIGITS_RIGHT', id='letter-digits')])
def test_paper_align_file(paper_size: str, table_alignment: str) -> None:
    """Paper size and table alignment choices round-trip."""
    config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
    config.paper_size = paper_size
    config.table_alignment = table_alignment
    with TemporaryDirectory() as temp_name:
        config_file = Path(temp_name) / 'config.json'
        config.write(to_json_filename=config_file)
        read_config = TioJsonConfig(CAPABILITIES, FILE_ACCESS,
                                    from_json_filename=config_file)
        assert read_config.paper_size == paper_size
        assert read_config.table_alignment == table_alignment


@pytest.mark.parametrize(
    ('line_length', 'table_length'),
    [pytest.param(11, 10, id='minimums'),
     pytest.param(79, 72, id='larger-values')])
def test_line_lengths_file(line_length: int, table_length: int) -> None:
    """Line length and table line length values round-trip."""
    config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
    config.line_length = line_length
    config.table_max_line_length = table_length
    with TemporaryDirectory() as temp_name:
        config_file = Path(temp_name) / 'config.json'
        config.write(to_json_filename=config_file)
        read_config = TioJsonConfig(CAPABILITIES, FILE_ACCESS,
                                    from_json_filename=config_file)
        assert read_config.line_length == line_length
        assert read_config.table_max_line_length == table_length


@pytest.mark.parametrize(
    ('dialect', 'delimiter'),
    [pytest.param(CsvDialect.EXCEL, ',', id='excel-comma'),
     pytest.param(CsvDialect.UNIX, ';', id='unix-semicolon')])
def test_csv_dialect_delim(dialect: CsvDialect, delimiter: str) -> None:
    """CSV dialect and delimiter values round-trip."""
    config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
    csv_config = TioJsonCsvConfig()
    config.format_name = 'CSV'
    csv_config.dialect = dialect
    csv_config.delimiter = delimiter
    config.csv = csv_config
    with TemporaryDirectory() as temp_name:
        config_file = Path(temp_name) / 'config.json'
        config.write(to_json_filename=config_file)
        read_config = TioJsonConfig(CAPABILITIES, FILE_ACCESS,
                                    from_json_filename=config_file)
        assert isinstance(read_config.csv, TioJsonCsvConfig)
        assert read_config.csv.dialect == dialect
        assert read_config.csv.delimiter == delimiter


@pytest.mark.parametrize(
    ('quoting', 'lineterminator'),
    [pytest.param('all', '\n', id='all-lf'),
     pytest.param('minimal', '\r\n', id='minimal-crlf'),
     pytest.param('nonnumeric', '\n', id='nonnumeric-lf'),
     pytest.param('none', '\r\n', id='none-crlf'),
     pytest.param('strings', '\n', id='strings-lf'),
     pytest.param('notnull', '\r\n', id='notnull-crlf')])
def test_csv_quote_line(quoting: str, lineterminator: str) -> None:
    """CSV quoting and line terminator values round-trip."""
    config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
    csv_config = TioJsonCsvConfig()
    config.format_name = 'CSV'
    csv_config.quoting = quoting
    csv_config.lineterminator = lineterminator
    config.csv = csv_config
    with TemporaryDirectory() as temp_name:
        config_file = Path(temp_name) / 'config.json'
        config.write(to_json_filename=config_file)
        read_config = TioJsonConfig(CAPABILITIES, FILE_ACCESS,
                                    from_json_filename=config_file)
        assert isinstance(read_config.csv, TioJsonCsvConfig)
        assert read_config.csv.quoting == quoting
        assert read_config.csv.lineterminator == lineterminator


@pytest.mark.parametrize(
    ('quotechar', 'escapechar'),
    [pytest.param('"', '\\', id='double-backslash'),
     pytest.param("'", '/', id='single-slash')])
def test_csv_quote_escape(quotechar: str, escapechar: str) -> None:
    """CSV quote character and escape character values round-trip."""
    config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
    csv_config = TioJsonCsvConfig()
    config.format_name = 'CSV'
    csv_config.quotechar = quotechar
    csv_config.escapechar = escapechar
    config.csv = csv_config
    with TemporaryDirectory() as temp_name:
        config_file = Path(temp_name) / 'config.json'
        config.write(to_json_filename=config_file)
        read_config = TioJsonConfig(CAPABILITIES, FILE_ACCESS,
                                    from_json_filename=config_file)
        assert isinstance(read_config.csv, TioJsonCsvConfig)
        assert read_config.csv.quotechar == quotechar
        assert read_config.csv.escapechar == escapechar


@pytest.mark.parametrize(
    ('document_class', 'preamble'),
    [pytest.param('Article', '\\usepackage{booktabs}', id='article'),
     pytest.param('Report', '\\usepackage{longtable}', id='report'),
     pytest.param('Book', '\\usepackage{booktabs}', id='book'),
     pytest.param('Letter', '\\usepackage{longtable}', id='letter')])
def test_latex_values_file(document_class: str, preamble: str) -> None:
    """Document class and preamble values round-trip."""
    config = TioJsonConfig(CAPABILITIES, FILE_ACCESS)
    latex_config = TioJsonLatexConfig()
    config.format_name = 'LaTeX'
    latex_config.document_class = document_class
    latex_config.preamble = preamble
    config.latex = latex_config
    with TemporaryDirectory() as temp_name:
        config_file = Path(temp_name) / 'config.json'
        config.write(to_json_filename=config_file)
        read_config = TioJsonConfig(CAPABILITIES, FILE_ACCESS,
                                    from_json_filename=config_file)
        assert isinstance(read_config.latex, TioJsonLatexConfig)
        assert read_config.latex.document_class == document_class
        assert read_config.latex.preamble == preamble


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
