#! /usr/bin/env python3
"""Tests for tableio-cfg-json teaching examples."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import json
import csv
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from tableio import FileAccess, access_capabilities, \
    add_access_capabilities, list_implementations_tableio, \
    list_registered_tableio
from tableio_cfg_json import get_config_member_names

from example import e01_create_config, e02_write_table, e03_read_table, \
    e04_create_custom_config, e05_split_cities_wizard, e06_split_cities


def _read_json(json_file: Path) -> dict[str, object]:
    """Read one JSON object from a file.

    Args:
        json_file: JSON file to read.
    Returns:
        Parsed JSON object.
    """
    data = json.loads(json_file.read_text(encoding='utf-8'))
    assert isinstance(data, dict)
    return data


def _expected_text() -> str:
    """Return the stdout text expected from the read example.

    Returns:
        Tab-separated text for ``EXAMPLE_TABLE``.
    """
    lines = [
        '\t'.join(str(value) for value in row)
        for row in e02_write_table.EXAMPLE_TABLE
    ]
    return '\n'.join(lines) + '\n'


def _assert_line_limit(text: str) -> None:
    """Assert that example-generated text is wrapped for plain text use."""
    long_lines = [line for line in text.splitlines() if len(line) > 79]
    assert long_lines == []


def _create_config(config_file: Path, syntax_file: Path, access_arg: str,
                   format_name: str, complete: bool = False) -> None:
    """Run the config-creation example with common test arguments.

    Args:
        config_file: JSON configuration file to write.
        syntax_file: Syntax guide to write.
        access_arg: Either ``--read`` or ``--write``.
        format_name: TableIO format name to request.
        complete: Whether to request a complete template.
    """
    args = ['--cfg', str(config_file), '--txt', str(syntax_file),
            access_arg, '--format', format_name]
    if complete:
        args.append('--complete')
    assert e01_create_config.main(args) == 0


def _csv_wizard_answers(file_access: FileAccess) -> list[str]:
    """Return blank-default wizard answers for one CSV endpoint config.

    Args:
        file_access: Access mode requested by the example wizard.
    Returns:
        Scripted answers that choose CSV and accept optional defaults.
    """
    capabilities = access_capabilities(file_access)
    match_caps = add_access_capabilities(file_access, capabilities)
    format_names = list_registered_tableio(capabilities=match_caps)
    impl_names = list_implementations_tableio(format_name='CSV',
                                              capabilities=match_caps)
    lines = [str(format_names.index('CSV') + 1)]
    if len(impl_names) > 1:
        lines.append('')
    member_names = get_config_member_names(capabilities=capabilities,
                                           file_access=file_access,
                                           format_name='CSV')
    optional_count = len([
        name for name in member_names
        if name not in ('format_name', 'implementation')
    ])
    lines.extend([''] * optional_count)
    return lines


def _create_split_config(config_file: Path, syntax_file: Path) -> None:
    """Create the split-cities config through the teaching wizard.

    Args:
        config_file: JSON configuration file to write.
        syntax_file: Plain text syntax guide to write.
    """
    answer_lines = []
    answer_lines.extend(_csv_wizard_answers(FileAccess.READ))
    answer_lines.append('')
    answer_lines.append('M')
    answer_lines.extend(_csv_wizard_answers(FileAccess.CREATE))
    answer_lines.extend(_csv_wizard_answers(FileAccess.CREATE))
    stdin_file = StringIO('\n'.join(answer_lines) + '\n')
    stdout_file = StringIO()
    stderr_file = StringIO()
    create_files = e05_split_cities_wizard.create_split_config_files
    create_files(config_file=config_file, syntax_file=syntax_file,
                 stdin_file=stdin_file, stdout_file=stdout_file,
                 stderr_file=stderr_file)


def _write_city_input(input_file: Path, header: str) -> None:
    """Write a small CSV input table for the split-cities example.

    Args:
        input_file: CSV file to write.
        header: Header row to place before the fixed data rows.
    """
    input_file.write_text(
        header + '\n'
        'Copenhagen,Denmark,Europe\n'
        'Tokyo,Japan,Asia\n'
        'Lisbon,Portugal,Europe\n',
        encoding='utf-8')


def _read_city_output(output_file: Path) -> list[dict[str, str]]:
    """Read a CSV output file written by the split-cities example.

    Args:
        output_file: CSV file created by the example runner.
    Returns:
        Output rows as dictionaries keyed by the expected city columns.
    """
    rows: list[dict[str, str]] = []
    with output_file.open(encoding='utf-8', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        assert reader.fieldnames == list(e06_split_cities.CITY_COLUMNS)
        for row in reader:
            text_row: dict[str, str] = {}
            for key, value in row.items():
                assert value is not None
                text_row[key] = value
            rows.append(text_row)
    return rows


def test_csv_write_config(tmp_path: Path) -> None:
    """The first example writes a compact CSV config and syntax guide."""
    config_file = tmp_path / 'csv-write.json'
    syntax_file = tmp_path / 'csv-write.txt'
    _create_config(config_file=config_file, syntax_file=syntax_file,
                   access_arg='--write', format_name='CSV')
    config_data = _read_json(config_file)
    syntax_text = syntax_file.read_text(encoding='utf-8')
    assert config_data == {'format_name': 'CSV'}
    assert 'Matching formats: CSV.' in syntax_text
    assert 'Compact example (CREATE)' in syntax_text
    assert 'Full example' not in syntax_text


def test_excel_read_full(tmp_path: Path) -> None:
    """The complete flag writes full Excel read config documentation."""
    config_file = tmp_path / 'excel-read.json'
    syntax_file = tmp_path / 'excel-read.txt'
    _create_config(config_file=config_file, syntax_file=syntax_file,
                   access_arg='--read', format_name='Excel', complete=True)
    config_data = _read_json(config_file)
    syntax_text = syntax_file.read_text(encoding='utf-8')
    assert config_data['format_name'] == 'Excel'
    assert 'implementation' in config_data
    assert 'line_length' in config_data
    assert 'Full example (READ)' in syntax_text
    assert 'Compact example' not in syntax_text


def test_csv_write_and_read(tmp_path: Path,
                            capsys: pytest.CaptureFixture[str]) -> None:
    """The examples can write and read the table as CSV."""
    config_file = tmp_path / 'csv.json'
    syntax_file = tmp_path / 'csv.txt'
    output_file = tmp_path / 'capitals.csv'
    _create_config(config_file=config_file, syntax_file=syntax_file,
                   access_arg='--write', format_name='CSV')
    assert e02_write_table.main(['--cfg', str(config_file),
                                 '--output', str(output_file)]) == 0
    assert 'Capital' in output_file.read_text(encoding='utf-8')
    assert e03_read_table.main(['--cfg', str(config_file),
                                '--input', str(output_file)]) == 0
    assert capsys.readouterr().out == _expected_text()


def test_custom_csv_config(tmp_path: Path) -> None:
    """The custom example writes explicit CSV and general values."""
    config_file = tmp_path / 'custom-csv.json'
    syntax_file = tmp_path / 'custom-csv.txt'
    assert e04_create_custom_config.main([
        '--cfg', str(config_file),
        '--txt', str(syntax_file),
        '--write',
        '--format', 'CSV']) == 0
    config_data = _read_json(config_file)
    assert config_data == {
        'character_encoding': 'utf-8',
        'csv': {'delimiter': ':'},
        'format_name': 'CSV',
        'table_alignment': 'CENTER'
    }
    assert 'File formats' in syntax_file.read_text(encoding='utf-8')


def test_custom_full_defaults(tmp_path: Path) -> None:
    """The custom example keeps other defaults in complete output."""
    config_file = tmp_path / 'custom-full.json'
    syntax_file = tmp_path / 'custom-full.txt'
    assert e04_create_custom_config.main([
        '--cfg', str(config_file),
        '--txt', str(syntax_file),
        '--write',
        '--format', 'CSV',
        '--complete']) == 0
    config_data = _read_json(config_file)
    csv_config = config_data['csv']
    assert isinstance(csv_config, dict)
    assert config_data['implementation'] == 'csv'
    assert csv_config['delimiter'] == ':'
    assert 'dialect' in csv_config


def test_custom_excel_table(tmp_path: Path,
                            capsys: pytest.CaptureFixture[str]) -> None:
    """CSV-only custom values may be stored with an Excel config."""
    write_file = tmp_path / 'custom-excel-write.json'
    write_text = tmp_path / 'custom-excel-write.txt'
    read_file = tmp_path / 'custom-excel-read.json'
    read_text = tmp_path / 'custom-excel-read.txt'
    output_file = tmp_path / 'custom-capitals.xlsx'
    assert e04_create_custom_config.main([
        '--cfg', str(write_file), '--txt', str(write_text), '--write',
        '--format', 'Excel', '--csv-delimiter', ':',
        '--alignment', 'LEFT']) == 0
    assert e04_create_custom_config.main([
        '--cfg', str(read_file), '--txt', str(read_text), '--read',
        '--format', 'Excel', '--csv-delimiter', ':']) == 0
    write_data = _read_json(write_file)
    assert write_data['format_name'] == 'Excel'
    assert write_data['csv'] == {'delimiter': ':'}
    assert 'implementation' not in write_data
    assert e02_write_table.main(['--cfg', str(write_file),
                                 '--output', str(output_file)]) == 0
    assert e03_read_table.main(['--cfg', str(read_file),
                                '--input', str(output_file)]) == 0
    assert capsys.readouterr().out == _expected_text()


def test_excel_write_and_read(tmp_path: Path,
                              capsys: pytest.CaptureFixture[str]) -> None:
    """The examples can write and read the table as an Excel workbook."""
    write_file = tmp_path / 'excel-write.json'
    write_text = tmp_path / 'excel-write.txt'
    read_file = tmp_path / 'excel-read.json'
    read_text = tmp_path / 'excel-read.txt'
    output_file = tmp_path / 'capitals.xlsx'
    _create_config(config_file=write_file, syntax_file=write_text,
                   access_arg='--write', format_name='Excel')
    _create_config(config_file=read_file, syntax_file=read_text,
                   access_arg='--read', format_name='Excel')
    assert e02_write_table.main(['--cfg', str(write_file),
                                 '--output', str(output_file)]) == 0
    assert output_file.is_file()
    assert e03_read_table.main(['--cfg', str(read_file),
                                '--input', str(output_file)]) == 0
    assert capsys.readouterr().out == _expected_text()


def test_split_cities(tmp_path: Path) -> None:
    """The split-cities examples create config and split a CSV file."""
    config_file = tmp_path / 'split-cities.json'
    syntax_file = tmp_path / 'split-cities.txt'
    input_file = tmp_path / 'cities.csv'
    less_file = tmp_path / 'less.csv'
    not_less_file = tmp_path / 'not-less.csv'
    _create_split_config(config_file, syntax_file)
    config_data = _read_json(config_file)
    assert config_data['input'] == {'format_name': 'CSV'}
    assert config_data['less_than_output'] == {'format_name': 'CSV'}
    assert config_data['not_less_than_output'] == {'format_name': 'CSV'}
    assert config_data['split_column'] == 'Country'
    assert config_data['split_limit'] == 'M'
    syntax_text = syntax_file.read_text(encoding='utf-8')
    _assert_line_limit(syntax_text)
    assert 'input' in syntax_text
    assert 'less_than_output' in syntax_text
    assert 'not_less_than_output' in syntax_text
    assert 'Configuration member reference' in syntax_text
    assert 'format_name choices: CSV, Excel, ODS.' in syntax_text
    assert 'HTML' in syntax_text
    assert 'latex.document_class' in syntax_text
    _write_city_input(input_file, 'City,Country,Continent')
    assert e06_split_cities.main([
        '--cfg', str(config_file),
        '--input', str(input_file),
        '--less-than-output', str(less_file),
        '--not-less-than-output', str(not_less_file)]) == 0
    less_text = less_file.read_text(encoding='utf-8')
    not_less_text = not_less_file.read_text(encoding='utf-8')
    assert 'City' in less_text
    assert 'Country' in less_text
    assert 'Continent' in less_text
    assert 'Denmark' in less_text
    assert 'Japan' in less_text
    assert 'Portugal' not in less_text
    assert 'Portugal' in not_less_text
    assert 'Denmark' not in not_less_text


def test_split_sample_data() -> None:
    """The wizard config can split the checked-in sample city data."""
    sample_file = Path(__file__).parents[2] / 'data' / 'cities_input.csv'
    with TemporaryDirectory() as temp_name:
        temp_dir = Path(temp_name)
        config_file = temp_dir / 'split-cities.json'
        syntax_file = temp_dir / 'split-cities.txt'
        less_file = temp_dir / 'less.csv'
        not_less_file = temp_dir / 'not-less.csv'
        _create_split_config(config_file, syntax_file)
        assert e06_split_cities.main([
            '--cfg', str(config_file),
            '--input', str(sample_file),
            '--less-than-output', str(less_file),
            '--not-less-than-output', str(not_less_file)]) == 0
        less_rows = _read_city_output(less_file)
        not_less_rows = _read_city_output(not_less_file)
    less_countries = {row['Country'] for row in less_rows}
    not_less_countries = {row['Country'] for row in not_less_rows}
    assert less_countries == {
        'China', 'Denmark', 'Egypt', 'Finland', 'France', 'Germany',
        'India', 'Japan', 'Kenya'
    }
    assert not_less_countries == {
        'Morocco', 'Nigeria', 'Portugal', 'South Africa', 'South Korea',
        'Thailand'
    }
    assert len(less_rows) == 18
    assert len(not_less_rows) == 12
    assert all(row['Country'] < 'M' for row in less_rows)
    assert all(row['Country'] >= 'M' for row in not_less_rows)


def test_split_missing_column(tmp_path: Path) -> None:
    """The runner reports a missing configured input column."""
    config_file = tmp_path / 'split-cities.json'
    syntax_file = tmp_path / 'split-cities.txt'
    input_file = tmp_path / 'cities.csv'
    less_file = tmp_path / 'less.csv'
    not_less_file = tmp_path / 'not-less.csv'
    _create_split_config(config_file, syntax_file)
    _write_city_input(input_file, 'City,Nation,Continent')
    with pytest.raises(ValueError, match='no Country column'):
        e06_split_cities.split_city_file(config_file=config_file,
                                         input_file=input_file,
                                         less_than_file=less_file,
                                         not_less_file=not_less_file)
