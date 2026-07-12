#! /usr/bin/env python3
"""Tests for writing and reading valid TableIO JSON config values.

Each test round-trips one member through a written config file and back,
asserting the value survives.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional

import pytest
from tableio import CsvDialect
from tableio_cfg_json import TioJsonConfig, TioJsonCsvConfig, \
    TioJsonHtmlConfig, TioJsonLatexConfig
from .cfg_rw_support import CAPABILITIES, FILE_ACCESS


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
