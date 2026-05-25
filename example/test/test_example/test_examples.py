#! /usr/bin/env python3
"""Tests for tableio-cfg-json teaching examples."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import json
from pathlib import Path

import pytest

from example import e01_create_config, e02_write_table, e03_read_table, \
    e04_create_custom_config


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
