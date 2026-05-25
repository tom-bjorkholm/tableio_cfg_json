#! /usr/bin/env python3
"""Write a small table with TableIO using a JSON configuration file."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
from pathlib import Path
import sys
from typing import Optional

from tableio import FileAccess, ListDataSeq, Value, access_capabilities, \
    tio_config_create
from tableio_cfg_json import TioJsonConfig


EXAMPLE_TABLE: ListDataSeq[Value] = [
    ['Capital', 'Country', 'Continent'],
    ['Copenhagen', 'Denmark', 'Europe'],
    ['Helsinki', 'Finland', 'Europe'],
    ['Lisbon', 'Portugal', 'Europe'],
    ['Tokyo', 'Japan', 'Asia']]
"""Small table written by this teaching example."""


def write_table_file(config_file: Path, output_file: Path) -> None:
    """Write the example table using one JSON-backed TableIO config.

    Args:
        config_file: JSON configuration file created for writing.
        output_file: Table file to create.
    """
    file_access = FileAccess.CREATE
    capabilities = access_capabilities(file_access, error_file=sys.stderr)
    # TioJsonConfig reads the JSON values and validates that they are usable
    # for the runtime task. Here the task is CREATE, because this program
    # creates a new table file.
    config = TioJsonConfig(capabilities=capabilities, file_access=file_access,
                           from_json_filename=config_file)
    # tio_config_create() is the TableIO helper that consumes ConfigData.
    # It validates the config again for this runtime task, filters the
    # format-specific optional settings, and creates the actual TableIO
    # backend object.
    with tio_config_create(config=config, file_name=output_file,
                           file_access=file_access,
                           capabilities=capabilities) as tableio:
        # write_table_listdata() is the simplest TableIO write method when
        # the data is already a list of rows.
        tableio.write_table_listdata(EXAMPLE_TABLE)


# ---------------------------------------------------------------------------
# Only command line handling below this line.


def build_parser() -> argparse.ArgumentParser:
    """Build the command line parser for the table writing example.

    Returns:
        Parser for command line arguments.
    """
    parser = argparse.ArgumentParser(
        description='Write a small table with a tableio-cfg-json config.')
    parser.add_argument('-c', '--cfg', dest='config_file', required=True,
                        type=Path, help='JSON configuration file to read.')
    parser.add_argument('-o', '--output', dest='output_file', required=True,
                        type=Path, help='Table file to create.')
    return parser


def main(args: Optional[list[str]] = None) -> int:
    """Parse command line arguments and write the example table.

    Args:
        args: Optional command line argument list. ``None`` means
            ``sys.argv[1:]``.
    Returns:
        Process exit code.
    """
    parsed = build_parser().parse_args(args)
    write_table_file(config_file=parsed.config_file,
                     output_file=parsed.output_file)
    return 0


if __name__ == '__main__':
    sys.exit(main())
