#! /usr/bin/env python3
"""Split a city table into two output files using JSON configuration."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
from pathlib import Path
import sys
from typing import Optional, TextIO, override

from config_as_json import Config, ConfigNesting, ConfigNestingKind, \
    MemberValidationStep, NestedConfigs, PathOrStr, StrLenValidator, \
    StrValidator, ValidationPlan
from tableio import DictData, DictDataMap, FileAccess, Value, \
    access_capabilities, tio_config_create
from tableio_cfg_json import TioJsonConfig, tio_json_config_default


CITY_COLUMNS = ('City', 'Country', 'Continent')
"""Header row expected by this teaching example."""


class SplitCitiesConfig(Config):
    """Configuration for one run of the split-cities example program."""

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Create or read the complete application configuration.

        Args:
            from_json_data_text: Optional JSON text to parse.
            from_json_filename: Optional JSON file to read.
            stderr_file: Stream receiving validation diagnostics.
        """
        # A config-as-json class is normally initialized to useful defaults.
        # Application code can then assign the specific values it wants before
        # writing JSON. The wizard example demonstrates that assignment style.
        self.input = _default_config(FileAccess.READ, stderr_file)
        self.less_than_output = _default_config(FileAccess.CREATE, stderr_file)
        self.not_less_than_output = _default_config(FileAccess.CREATE,
                                                    stderr_file)
        self.split_column = 'Country'
        self.split_limit = 'M'
        Config.__init__(self, from_json_data_text=from_json_data_text,
                        from_json_filename=from_json_filename,
                        stderr_file=stderr_file)

    @override
    def nested_configs(self) -> NestedConfigs:
        """Return nested TableIO config declarations for this config."""
        # The top-level application config owns three nested TioJsonConfig
        # objects. Each nested config needs a factory because the input member
        # is read-capable, while both output members are create-capable.
        input_nesting = ConfigNesting(kind=ConfigNestingKind.MEMBER,
                                      config_type=TioJsonConfig,
                                      factory_function=self._input_factory)
        create_nesting = ConfigNesting(kind=ConfigNestingKind.MEMBER,
                                       config_type=TioJsonConfig,
                                       factory_function=self._create_factory)
        return {
            'input': input_nesting,
            'less_than_output': create_nesting,
            'not_less_than_output': create_nesting
        }

    @override
    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return validation for the application-owned config values."""
        _ = stderr_file
        # We only validate the split column and split limit here because
        # the input and output configs are validated by the nested Configs.
        return [
            MemberValidationStep(
                member_names=['split_column'],
                validator=StrValidator(CITY_COLUMNS, ignore_case=False)),
            MemberValidationStep(
                member_names=['split_limit'],
                validator=StrLenValidator(min_length=1, max_length=None))
        ]

    def _input_factory(self, from_json_data_text: Optional[str] = None,
                       from_json_filename: Optional[PathOrStr] = None,
                       stderr_file: TextIO = sys.stderr) -> TioJsonConfig:
        """Create a nested read-capable TableIO config from JSON."""
        return _json_config(FileAccess.READ, from_json_data_text,
                            from_json_filename, stderr_file)

    def _create_factory(self, from_json_data_text: Optional[str] = None,
                        from_json_filename: Optional[PathOrStr] = None,
                        stderr_file: TextIO = sys.stderr) -> TioJsonConfig:
        """Create a nested create-capable TableIO config from JSON."""
        return _json_config(FileAccess.CREATE, from_json_data_text,
                            from_json_filename, stderr_file)


def split_city_file(config_file: Path, input_file: Path, less_than_file: Path,
                    not_less_file: Path) -> None:
    """Read one city table and write two filtered output tables.

    Args:
        config_file: Complete JSON application configuration.
        input_file: Existing table file with city rows.
        less_than_file: Output table for rows where the selected value is
            less than ``split_limit``.
        not_less_file: Output table for all remaining rows.
    Raises:
        ValueError: The input table is empty or lacks the configured column.
    """
    # File names are runtime values supplied on the command line. The JSON
    # config contains durable choices such as formats, implementations and
    # the split rule, but not the actual files for this run.
    config = SplitCitiesConfig(from_json_filename=config_file)
    rows = _read_rows(config.input, input_file)
    less_rows, not_less_rows = _split_rows(rows, config.split_column,
                                           config.split_limit)
    _write_rows(config.less_than_output, less_than_file, less_rows)
    _write_rows(config.not_less_than_output, not_less_file, not_less_rows)


def _default_config(file_access: FileAccess,
                    stderr_file: TextIO) -> TioJsonConfig:
    """Return a default nested TableIO config for one file access mode."""
    capabilities = access_capabilities(file_access, error_file=stderr_file)
    return tio_json_config_default(capabilities=capabilities,
                                   file_access=file_access)


def _json_config(file_access: FileAccess, from_json_data_text: Optional[str],
                 from_json_filename: Optional[PathOrStr],
                 stderr_file: TextIO) -> TioJsonConfig:
    """Read a nested TableIO config for one file access mode."""
    capabilities = access_capabilities(file_access, error_file=stderr_file)
    return TioJsonConfig(capabilities=capabilities, file_access=file_access,
                         from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file)


def _read_rows(config: TioJsonConfig, input_file: Path) -> DictData[Value]:
    """Read all table rows from the configured input file."""
    file_access = FileAccess.READ
    capabilities = access_capabilities(file_access, error_file=sys.stderr)
    with tio_config_create(config=config, file_name=input_file,
                           file_access=file_access,
                           capabilities=capabilities) as tableio:
        # Dict data tells TableIO to use the first table row as column names.
        # That keeps the example split logic about the application rule
        # instead of about list indexes.
        read_result = tableio.read_table_dictdata()
    return read_result.data


def _split_rows(rows: DictData[Value], split_column: str,
                split_limit: str) -> tuple[DictData[Value], DictData[Value]]:
    """Split rows using a simple case-sensitive Python string comparison."""
    if not rows:
        raise ValueError('The input table has no data rows.')
    if split_column not in rows[0]:
        message = f'The input table has no {split_column} column.'
        raise ValueError(message)
    less_rows: DictData[Value] = []
    not_less_rows: DictData[Value] = []
    # The comparison is intentionally simple because this example is about
    # TableIO configuration, not locale-aware sorting or data normalization.
    for row in rows:
        cell_text = _value_text(row.get(split_column))
        if cell_text < split_limit:
            less_rows.append(row)
        else:
            not_less_rows.append(row)
    return less_rows, not_less_rows


def _value_text(value: Value) -> str:
    """Return one TableIO value as comparable text."""
    if value is None:
        return ''
    return str(value)


def _write_rows(config: TioJsonConfig, output_file: Path,
                rows: DictDataMap[Value]) -> None:
    """Write rows with the configured output TableIO backend."""
    file_access = FileAccess.CREATE
    capabilities = access_capabilities(file_access, error_file=sys.stderr)
    with tio_config_create(config=config, file_name=output_file,
                           file_access=file_access,
                           capabilities=capabilities) as tableio:
        # Dict writing stores the configured application columns in a stable
        # order. The flags make the example tolerant of incomplete input rows
        # or extra columns supplied by a user's own file.
        tableio.write_table_dictdata(rows, column_order=list(CITY_COLUMNS),
                                     missing_ok=True, extra_ok=True)


# ---------------------------------------------------------------------------
# Only command line handling below this line.


def build_parser() -> argparse.ArgumentParser:
    """Build the command line parser for the split-cities runner."""
    parser = argparse.ArgumentParser(
        description='Split a city table using a JSON configuration.')
    parser.add_argument('-c', '--cfg', dest='config_file', required=True,
                        type=Path, help='JSON configuration file to read.')
    parser.add_argument('-i', '--input', dest='input_file', required=True,
                        type=Path, help='Table file to read.')
    parser.add_argument('--less-than-output', dest='less_than_file',
                        required=True, type=Path,
                        help='Output file for rows below the limit.')
    parser.add_argument('--not-less-than-output', dest='not_less_file',
                        required=True, type=Path,
                        help='Output file for rows not below the limit.')
    return parser


def main(args: Optional[list[str]] = None) -> int:
    """Parse command line arguments and split the configured table."""
    parsed = build_parser().parse_args(args)
    split_city_file(config_file=parsed.config_file,
                    input_file=parsed.input_file,
                    less_than_file=parsed.less_than_file,
                    not_less_file=parsed.not_less_file)
    return 0


if __name__ == '__main__':
    sys.exit(main())
