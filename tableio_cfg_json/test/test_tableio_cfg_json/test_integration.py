#! /usr/bin/env python3
"""Integration tests for TableIO JSON config files."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import json
from dataclasses import dataclass
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

from odfdo import Document
from odfdo.body import Spreadsheet
import pylightxl  # type: ignore[import-untyped]
from tableio import CsvDialect, FileAccess, ListDataSeq, Value, \
    access_capabilities, tio_config_create
from tableio_cfg_json import TioJsonConfig, TioJsonCsvConfig


@dataclass(frozen=True)
class IntegrationFiles:
    """Temporary files created by the integration test."""

    step2: Path
    to_from_ods: Path
    to_from_excel: Path
    cities_ods: Path
    cities_xlsx: Path
    cities_csv: Path


def _integration_files(temp_dir: Path) -> IntegrationFiles:
    """Return the temporary file paths used by the integration test."""
    return IntegrationFiles(step2=temp_dir / 'step2.cfg',
                            to_from_ods=temp_dir / 'to_from_ods.cfg',
                            to_from_excel=temp_dir / 'to_from_excel.cfg',
                            cities_ods=temp_dir / 'cities.ods',
                            cities_xlsx=temp_dir / 'cities.xlsx',
                            cities_csv=temp_dir / 'cities.csv')


def _json_object(raw_text: str) -> dict[str, object]:
    """Return one decoded JSON object from raw config text."""
    data = json.loads(raw_text)
    assert isinstance(data, dict)
    return data


def _csv_reader_config() -> TioJsonConfig:
    """Create a CSV reader config using Excel dialect comma separation."""
    file_access = FileAccess.READ
    capabilities = access_capabilities(file_access, error_file=sys.stderr)
    config = TioJsonConfig(capabilities=capabilities, file_access=file_access,
                           format_name='CSV')
    config.csv = TioJsonCsvConfig(dialect=CsvDialect.EXCEL,
                                  lineterminator='\r')
    return config


def _read_write_config(format_name: str) -> TioJsonConfig:
    """Create a config that lets TableIO choose the runtime implementation."""
    file_access = FileAccess.UPDATE
    capabilities = access_capabilities(file_access, error_file=sys.stderr)
    return TioJsonConfig(capabilities=capabilities, file_access=file_access,
                         format_name=format_name, implementation=None)


def _config_from_file(config_file: Path,
                      file_access: FileAccess) -> TioJsonConfig:
    """Read one TableIO JSON config for the requested file access."""
    capabilities = access_capabilities(file_access, error_file=sys.stderr)
    return TioJsonConfig(capabilities=capabilities, file_access=file_access,
                         from_json_filename=config_file)


def _read_rows(config_file: Path, input_file: Path) -> ListDataSeq[Value]:
    """Read list data from one file through one TableIO config file."""
    file_access = FileAccess.READ
    capabilities = access_capabilities(file_access, error_file=sys.stderr)
    config = _config_from_file(config_file, file_access)
    with tio_config_create(config=config, file_name=input_file,
                           file_access=file_access,
                           capabilities=capabilities) as tableio:
        read_result = tableio.read_table_listdata()
    return read_result.data


def _write_rows(config_file: Path, output_file: Path,
                city_rows: ListDataSeq[Value]) -> None:
    """Write list data to one file through one TableIO config file."""
    file_access = FileAccess.CREATE
    capabilities = access_capabilities(file_access, error_file=sys.stderr)
    config = _config_from_file(config_file, file_access)
    with tio_config_create(config=config, file_name=output_file,
                           file_access=file_access,
                           capabilities=capabilities) as tableio:
        tableio.write_table_listdata(city_rows)


def _copy_csv_to_ods(csv_config: Path, ods_config: Path, csv_file: Path,
                     ods_file: Path) -> None:
    """Read CSV city data and write the same local list to ODS."""
    # Step 7.1 and 7.3.
    city_rows = _read_rows(csv_config, csv_file)
    # Step 7.2 and 7.4.
    _write_rows(ods_config, ods_file, city_rows)


def _copy_ods_to_excel(ods_config: Path, excel_config: Path, ods_file: Path,
                       excel_file: Path) -> None:
    """Read ODS city data and write the same local list to Excel."""
    # Step 12.1 and 12.3.
    city_rows = _read_rows(ods_config, ods_file)
    # Step 12.2 and 12.4.
    _write_rows(excel_config, excel_file, city_rows)


def _copy_excel_to_csv(excel_config: Path, csv_config: Path, excel_file: Path,
                       csv_file: Path) -> None:
    """Read Excel city data and write the same local list to CSV."""
    # Step 14.1 and 14.3.
    city_rows = _read_rows(excel_config, excel_file)
    # Step 14.2 and 14.4.
    _write_rows(csv_config, csv_file, city_rows)


def _ods_cell_texts(ods_file: Path) -> list[str]:
    """Read one ODS spreadsheet and return all cell values as text."""
    document = Document(ods_file)
    assert document.get_type() == 'spreadsheet'
    body = document.body
    assert isinstance(body, Spreadsheet)
    table = body.get_table(position=0)
    assert table is not None
    return [str(cell) for row in table.get_values() for cell in row]


def _excel_cell_texts(excel_file: Path) -> list[str]:
    """Read one Excel workbook and return all cell values as text."""
    workbook = pylightxl.readxl(excel_file)
    sheet_names = workbook.ws_names
    assert len(sheet_names) > 0
    worksheet = workbook.ws(sheet_names[0])
    return [str(cell) for row in worksheet.rows for cell in row]


def test_format_chain() -> None:
    """Config files can move city data through CSV, ODS and Excel."""
    sample_file = Path(__file__).parents[2] / 'example' / 'data' / \
        'cities_input.csv'
    expected_city = 'Copenhagen'
    with TemporaryDirectory() as temp_name:
        temp_dir = Path(temp_name)
        files = _integration_files(temp_dir)
        # Step 1. Create a CSV reader config with comma delimiter.
        csv_config = _csv_reader_config()
        # Step 2. Write the CSV config to step2.cfg.
        csv_config.write(to_json_filename=files.step2)
        # Step 3. Verify the raw step2.cfg text describes CSV files.
        raw_text = files.step2.read_text(encoding='utf-8')
        config_data = _json_object(raw_text)
        assert 'CSV' in raw_text
        assert 'implementation' not in config_data
        assert config_data == {
            'csv': {
                'dialect': 'EXCEL',
                'lineterminator': '\r'
            },
            'format_name': 'CSV'
        }
        # Step 4. Create an ODS config for reading and writing.
        ods_config = _read_write_config('ODS')
        # Step 5. Write the ODS config to to_from_ods.cfg.
        ods_config.write(to_json_filename=files.to_from_ods)
        # Step 6. Verify the raw ODS config text.
        raw_text = files.to_from_ods.read_text(encoding='utf-8')
        config_data = _json_object(raw_text)
        assert 'ODS' in raw_text
        assert 'implementation' not in config_data
        assert config_data == {'format_name': 'ODS'}
        # Step 7. Copy the sample CSV file to ODS through config files.
        _copy_csv_to_ods(files.step2, files.to_from_ods, sample_file,
                         files.cities_ods)
        # Step 8. Verify the ODS file with odfdo.
        assert expected_city in _ods_cell_texts(files.cities_ods)
        # Step 9. Create an Excel config with implementation=None.
        excel_config = _read_write_config('Excel')
        # Step 10. Write the Excel config to to_from_excel.cfg.
        excel_config.write(to_json_filename=files.to_from_excel)
        # Step 11. Verify the raw Excel config text omits implementation.
        raw_text = files.to_from_excel.read_text(encoding='utf-8')
        config_data = _json_object(raw_text)
        assert 'Excel' in raw_text
        assert 'implementation' not in config_data
        assert config_data == {'format_name': 'Excel'}
        # Step 12. Copy the ODS file to Excel through config files.
        _copy_ods_to_excel(files.to_from_ods, files.to_from_excel,
                           files.cities_ods, files.cities_xlsx)
        # Step 13. Verify the Excel file with pylightxl.
        assert expected_city in _excel_cell_texts(files.cities_xlsx)
        # Step 14. Copy the Excel file back to CSV through config files.
        _copy_excel_to_csv(files.to_from_excel, files.step2, files.cities_xlsx,
                           files.cities_csv)
        # Step 15. Verify the final CSV text matches the sample CSV text.
        actual_text = files.cities_csv.read_text(encoding='utf-8')
        expected_text = sample_file.read_text(encoding='utf-8')
        assert actual_text == expected_text
