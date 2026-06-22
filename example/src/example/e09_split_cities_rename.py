#! /usr/bin/env python3
"""Split a city table and write each output with renamed columns.

This builds on e06_split_cities. The one new idea is that each output
file may rename its columns: the application config carries an
independent input-column to output-name mapping for each output, and
this program applies that mapping when it writes the file. For example
one output can rename City to Hauptstadt and Country to Land while the
other output keeps the original names. The matching wizard that creates
the configuration is e08_rename_wizard.

Everything else is reused unchanged from e06: reading the input table,
the split rule, and the actual TableIO writing. Only the small step of
renaming the columns before writing is added here.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
from pathlib import Path
from typing import Optional, TextIO, override

from config_as_json import DictKeyValueTypesValidator, \
    MemberValidationStep, PathOrStr, ValidationPlan
from tableio import DictData, Value
from tableio_cfg_json import TioJsonConfig

from example.e06_split_cities import CITY_COLUMNS, SplitCitiesConfig, \
    run_split_file_cli, _read_rows, _split_rows, _write_rows


class RenameSplitConfig(SplitCitiesConfig):
    """Split-cities config that also renames the output columns.

    It adds two application-owned members to SplitCitiesConfig:
    less_output_names and not_less_output_names. Each maps an input
    column name to the column name written in that one output file, so
    the two outputs are renamed independently. A column that is not
    listed keeps its original name.
    """

    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Create or read the rename-capable application configuration."""
        # The two mappings are open-ended dicts, so their keys are not a
        # fixed schema the Config base class can check against a default.
        # We opt out of that default key check and let the validation plan
        # own the key and value types instead.
        self._unchecked_dicts = ['less_output_names',
                                 'not_less_output_names']
        self.less_output_names: dict[str, str] = {}
        self.not_less_output_names: dict[str, str] = {}
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file)

    @override
    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the split validation plus the rename-mapping checks."""
        plan = super().get_validation_plan(stderr_file)
        names_validator = DictKeyValueTypesValidator(key_type=str,
                                                     value_type=str)
        plan.append(MemberValidationStep(
            member_names=['less_output_names', 'not_less_output_names'],
            validator=names_validator))
        return plan


def split_city_file(config_file: Path, input_file: Path, less_than_file: Path,
                    not_less_file: Path) -> None:
    """Read one city table and write two renamed, filtered output tables.

    Args:
        config_file: Complete JSON application configuration.
        input_file: Existing table file with city rows.
        less_than_file: Output table for rows where the selected value is
            less than ``split_limit``.
        not_less_file: Output table for all remaining rows.
    Raises:
        ValueError: The input table is empty or lacks the configured column.
    """
    config = RenameSplitConfig(from_json_filename=config_file)
    rows = _read_rows(config.input, input_file)
    less_rows, not_less_rows = _split_rows(rows, config.split_column,
                                           config.split_limit)
    _write_named(config.less_than_output, less_than_file, less_rows,
                 config.less_output_names)
    _write_named(config.not_less_than_output, not_less_file, not_less_rows,
                 config.not_less_output_names)


def _write_named(config: TioJsonConfig, output_file: Path,
                 rows: DictData[Value], names: dict[str, str]) -> None:
    """Write rows after renaming their columns for one output file."""
    renamed = _rename_rows(rows, names)
    column_order = [names.get(column, column) for column in CITY_COLUMNS]
    _write_rows(config, output_file, renamed, column_order)


def _rename_rows(rows: DictData[Value],
                 names: dict[str, str]) -> DictData[Value]:
    """Return rows whose keys are renamed by the names mapping."""
    return [{names.get(key, key): value for key, value in row.items()}
            for row in rows]


# ---------------------------------------------------------------------------
# Only command line handling below this line. The command line matches
# e06_split_cities, so its shared runner is reused unchanged.


def main(args: Optional[list[str]] = None) -> int:
    """Parse command line arguments and split the configured table."""
    return run_split_file_cli(split_city_file, args)


if __name__ == '__main__':
    sys.exit(main())
