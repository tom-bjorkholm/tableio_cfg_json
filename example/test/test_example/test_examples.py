#! /usr/bin/env python3
"""Tests for tableio-cfg-json teaching examples."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import json
import csv
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional

import pytest

from tableio import FileAccess, access_capabilities, \
    add_access_capabilities, list_implementations_tableio, \
    list_registered_tableio
from tableio_cfg_json import get_config_member_names, UiBridgeType

from example import e01_create_config, e02_write_table, e03_read_table, \
    e04_create_custom_config, e05_split_cities_wizard, e06_split_cities, \
    e07_split_cities_textual, e08_rename_wizard, e09_split_cities_rename, \
    e10_edit_config_wizard


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


def _csv_wizard_answers(file_access: FileAccess,
                        member_answers: Optional[dict[str, str]] = None
                        ) -> list[str]:
    """Return blank-default wizard answers for one CSV endpoint config.

    Args:
        file_access: Access mode requested by the example wizard.
    Returns:
        Scripted answers that choose CSV and accept optional defaults.
    """
    answer_map = {} if member_answers is None else member_answers
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
    lines.extend(
        answer_map.get(name, '') for name in member_names
        if name not in ('format_name', 'implementation'))
    return lines


def _csv_member_answers(file_access: FileAccess,
                        member_answers: dict[str, str]) -> list[str]:
    """Return option-form answers for every CSV member, in wizard order."""
    capabilities = access_capabilities(file_access)
    member_names = get_config_member_names(capabilities=capabilities,
                                           file_access=file_access,
                                           format_name='CSV')
    return [member_answers.get(name, '') for name in member_names
            if name not in ('format_name', 'implementation')]


def _split_happy_answers() -> list[str]:
    """Return blank-default answers for the whole split-cities wizard."""
    answer_lines = []
    answer_lines.extend(_csv_wizard_answers(FileAccess.READ))
    answer_lines.append('')
    answer_lines.append('M')
    answer_lines.extend(_csv_wizard_answers(FileAccess.CREATE))
    answer_lines.extend(_csv_wizard_answers(FileAccess.CREATE))
    return answer_lines


def _run_split(answer_lines: list[str], config_file: Path,
               syntax_file: Path) -> None:
    """Run the split-cities wizard with scripted answers."""
    stdin_file = StringIO('\n'.join(answer_lines) + '\n')
    create_files = e05_split_cities_wizard.create_split_config_files
    create_files(config_file=config_file, syntax_file=syntax_file,
                 stdin_file=stdin_file, stdout_file=StringIO(),
                 stderr_file=StringIO())


def _create_split_config(config_file: Path, syntax_file: Path) -> None:
    """Create the split-cities config through the teaching wizard.

    Args:
        config_file: JSON configuration file to write.
        syntax_file: Plain text syntax guide to write.
    """
    _run_split(_split_happy_answers(), config_file, syntax_file)


def test_e07_matches_e05(tmp_path: Path) -> None:
    """e07 writes the same files as e05 through make_text_ui_bridge.

    The test streams are in-memory, so the factory inside e07 falls back
    to the console bridge and must produce byte-identical files to e05.
    """
    answers = _split_happy_answers()
    e05_cfg = tmp_path / 'e05.json'
    e05_txt = tmp_path / 'e05.txt'
    e07_cfg = tmp_path / 'e07.json'
    e07_txt = tmp_path / 'e07.txt'
    _run_split(answers, e05_cfg, e05_txt)
    create_files = e07_split_cities_textual.create_split_config_files
    create_files(config_file=e07_cfg, syntax_file=e07_txt,
                 stdin_file=StringIO('\n'.join(answers) + '\n'),
                 stdout_file=StringIO(), stderr_file=StringIO())
    got_cfg = e07_cfg.read_text(encoding='utf-8')
    got_txt = e07_txt.read_text(encoding='utf-8')
    assert got_cfg == e05_cfg.read_text(encoding='utf-8')
    assert got_txt == e05_txt.read_text(encoding='utf-8')


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


def test_split_abort(tmp_path: Path) -> None:
    """Aborting the wizard at the first question writes no files."""
    config_file = tmp_path / 'split-cities.json'
    syntax_file = tmp_path / 'split-cities.txt'
    _run_split([':q'], config_file, syntax_file)
    assert not config_file.exists()
    assert not syntax_file.exists()


def test_split_back(tmp_path: Path) -> None:
    """Going back from a later endpoint re-asks an earlier item."""
    config_file = tmp_path / 'split-cities.json'
    syntax_file = tmp_path / 'split-cities.txt'
    answer_lines = []
    answer_lines.extend(_csv_wizard_answers(FileAccess.READ))
    answer_lines.append('')      # split column -> Country
    answer_lines.append('M')     # split limit, first answer
    answer_lines.append(':b')    # less-output format: step back one item
    answer_lines.append('L')     # split limit, re-answered
    answer_lines.extend(_csv_wizard_answers(FileAccess.CREATE))
    answer_lines.extend(_csv_wizard_answers(FileAccess.CREATE))
    _run_split(answer_lines, config_file, syntax_file)
    config_data = _read_json(config_file)
    assert config_data['split_limit'] == 'L'
    assert config_data['split_column'] == 'Country'


def test_edit_keeps_old(tmp_path: Path) -> None:
    """e10 uses an existing config file as wizard defaults."""
    config_file = tmp_path / 'edit-csv.json'
    config_file.write_text(
        '{\n'
        '    "format_name": "CSV",\n'
        '    "character_encoding": "utf-8",\n'
        '    "csv": {\n'
        '        "delimiter": ";"\n'
        '    }\n'
        '}\n',
        encoding='utf-8')
    answers = _csv_wizard_answers(FileAccess.CREATE)
    answers.append('')
    e10_edit_config_wizard.edit_config_file(config_file=config_file,
                                            stdin_file=StringIO(
                                                '\n'.join(answers) + '\n'),
                                            stdout_file=StringIO(),
                                            stderr_file=StringIO())
    assert _read_json(config_file) == {
        'character_encoding': 'utf-8',
        'csv': {'delimiter': ';'},
        'format_name': 'CSV'
    }


def test_edit_goes_back(tmp_path: Path) -> None:
    """e10 can go back from its enclosing confirmation question."""
    config_file = tmp_path / 'edit-back.csv.json'
    answers = _csv_wizard_answers(FileAccess.CREATE, {'csv.delimiter': ';'})
    answers.append('n')
    answers.extend(_csv_member_answers(FileAccess.CREATE,
                                       {'csv.delimiter': ','}))
    answers.append('')
    e10_edit_config_wizard.edit_config_file(config_file=config_file,
                                            stdin_file=StringIO(
                                                '\n'.join(answers) + '\n'),
                                            stdout_file=StringIO(),
                                            stderr_file=StringIO())
    assert _read_json(config_file) == {
        'csv': {'delimiter': ','},
        'format_name': 'CSV'
    }


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


def _rename_happy_answers() -> list[str]:
    """Return scripted answers that rename columns for both outputs.

    The less-than output edits one row, deletes another, and adds a third
    through the variable-row table, while the not-less-than output accepts
    the two identity rows unchanged. This exercises editing, deleting and
    adding rows in the console row-menu editor.
    """
    lines = list(_csv_wizard_answers(FileAccess.READ))
    lines.append('')
    lines.append('M')
    lines.extend(_csv_wizard_answers(FileAccess.CREATE))
    lines.extend(['1', '', 'Hauptstadt', ':- 2', ':+', '3', 'Kontinent', ''])
    lines.extend(_csv_wizard_answers(FileAccess.CREATE))
    lines.append('')
    return lines


def _run_rename(lines: list[str], config_file: Path,
                syntax_file: Path) -> None:
    """Run the rename wizard with scripted answers and in-memory streams."""
    stdin_file = StringIO('\n'.join(lines) + '\n')
    create_files = e08_rename_wizard.create_split_config_files
    create_files(config_file=config_file, syntax_file=syntax_file,
                 stdin_file=stdin_file, stdout_file=StringIO(),
                 stderr_file=StringIO())


def test_rename_split(tmp_path: Path) -> None:
    """The rename wizard config renames each output independently."""
    config_file = tmp_path / 'rename.json'
    syntax_file = tmp_path / 'rename.txt'
    input_file = tmp_path / 'cities.csv'
    less_file = tmp_path / 'less.csv'
    not_less_file = tmp_path / 'not-less.csv'
    _run_rename(_rename_happy_answers(), config_file, syntax_file)
    config_data = _read_json(config_file)
    assert config_data['less_output_names'] == {
        'City': 'Hauptstadt', 'Continent': 'Kontinent'}
    assert config_data['not_less_output_names'] == {
        'City': 'City', 'Country': 'Country'}
    assert config_data['split_column'] == 'Country'
    syntax_text = syntax_file.read_text(encoding='utf-8')
    _assert_line_limit(syntax_text)
    assert 'Output column renaming' in syntax_text
    assert 'less_output_names' in syntax_text
    _write_city_input(input_file, 'City,Country,Continent')
    assert e09_split_cities_rename.main([
        '--cfg', str(config_file),
        '--input', str(input_file),
        '--less-than-output', str(less_file),
        '--not-less-than-output', str(not_less_file)]) == 0
    less_lines = less_file.read_text(encoding='utf-8').splitlines()
    not_less_lines = not_less_file.read_text(encoding='utf-8').splitlines()
    assert next(csv.reader([less_lines[0]])) == [
        'Hauptstadt', 'Country', 'Kontinent']
    assert next(csv.reader([not_less_lines[0]])) == [
        'City', 'Country', 'Continent']
    less_text = '\n'.join(less_lines)
    assert 'Denmark' in less_text and 'Japan' in less_text
    assert 'Portugal' not in less_text
    assert 'Portugal' in '\n'.join(not_less_lines)


def test_e08_console(tmp_path: Path) -> None:
    """Forcing the console bridge matches the auto-selected console run."""
    answers = _rename_happy_answers()
    auto_cfg = tmp_path / 'auto.json'
    auto_txt = tmp_path / 'auto.txt'
    forced_cfg = tmp_path / 'forced.json'
    forced_txt = tmp_path / 'forced.txt'
    _run_rename(answers, auto_cfg, auto_txt)
    stdin_file = StringIO('\n'.join(answers) + '\n')
    create_files = e08_rename_wizard.create_split_config_files
    create_files(config_file=forced_cfg, syntax_file=forced_txt,
                 bridge_type=UiBridgeType.CONSOLE, stdin_file=stdin_file,
                 stdout_file=StringIO(), stderr_file=StringIO())
    assert forced_cfg.read_text(encoding='utf-8') == \
        auto_cfg.read_text(encoding='utf-8')
    assert forced_txt.read_text(encoding='utf-8') == \
        auto_txt.read_text(encoding='utf-8')


def test_e08_ui_option() -> None:
    """The --ui option defaults to auto and accepts the bridge names."""
    parser = e08_rename_wizard.build_parser()
    default = parser.parse_args(['--cfg', 'c', '--txt', 't'])
    assert default.ui == 'auto'
    forced = parser.parse_args(['--cfg', 'c', '--txt', 't', '--ui', 'console'])
    assert forced.ui == 'console'


def test_e08_main_ui(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """main() maps the --ui choice to the bridge and writes the config."""
    answers = _rename_happy_answers()
    monkeypatch.setattr('sys.stdin', StringIO('\n'.join(answers) + '\n'))
    monkeypatch.setattr('sys.stdout', StringIO())
    config_file = tmp_path / 'main.json'
    syntax_file = tmp_path / 'main.txt'
    assert e08_rename_wizard.main([
        '--cfg', str(config_file), '--txt', str(syntax_file),
        '--ui', 'console']) == 0
    config_data = _read_json(config_file)
    assert config_data['less_output_names'] == {
        'City': 'Hauptstadt', 'Continent': 'Kontinent'}


def test_rename_back(tmp_path: Path) -> None:
    """Back from a rename table re-asks the previous output endpoint."""
    config_file = tmp_path / 'rename.json'
    syntax_file = tmp_path / 'rename.txt'
    lines = list(_csv_wizard_answers(FileAccess.READ))
    lines.append('')
    lines.append('M')
    lines.extend(_csv_wizard_answers(FileAccess.CREATE))
    lines.append(':b')
    lines.extend(_csv_wizard_answers(FileAccess.CREATE))
    lines.append('')
    lines.extend(_csv_wizard_answers(FileAccess.CREATE))
    lines.append('')
    _run_rename(lines, config_file, syntax_file)
    config_data = _read_json(config_file)
    assert config_data['less_output_names'] == {
        'City': 'City', 'Country': 'Country'}
