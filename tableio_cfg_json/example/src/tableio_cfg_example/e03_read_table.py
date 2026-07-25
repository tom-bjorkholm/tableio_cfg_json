#! /usr/bin/env python3
"""Read a table with TableIO using a JSON configuration file."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
from pathlib import Path
import sys
from typing import Optional, TextIO

from tableio import FileAccess, ListDataSeq, Value, access_capabilities, \
    tio_config_create
from tableio_cfg_json import TioJsonConfig


def read_table_file(config_file: Path, input_file: Path,
                    stdout_file: Optional[TextIO] = None) -> None:
    """Read a table file and print it to stdout-style text.

    Args:
        config_file: JSON configuration file created for reading.
        input_file: Existing table file to read.
        stdout_file: Optional output stream for tests or callers.
    """
    out_file = sys.stdout if stdout_file is None else stdout_file
    file_access = FileAccess.READ
    capabilities = access_capabilities(file_access, error_file=sys.stderr)
    # This mirrors the write example, but the runtime task is READ. For Excel
    # this matters: the best writer and best reader are usually different
    # TableIO implementations.
    config = TioJsonConfig(capabilities=capabilities, file_access=file_access,
                           from_json_filename=config_file)
    # tio_config_create() is the matching read-side bridge: it turns the
    # JSON-backed ConfigData into the concrete TableIO reader.
    with tio_config_create(config=config, file_name=input_file,
                           file_access=file_access,
                           capabilities=capabilities) as tableio:
        # read_table_listdata() returns both headings and the table. These
        # examples do not write headings, but printing them makes the example
        # useful for files that do contain heading text.
        read_result = tableio.read_table_listdata()
    _print_headings(read_result.headings, out_file)
    _print_rows(read_result.data, out_file)


def _print_rows(data: ListDataSeq[Value], stdout_file: TextIO) -> None:
    """Print rows as tab-separated text.

    Args:
        data: Rows read from the table file.
        stdout_file: Stream to write to.
    """
    for row in data:
        print('\t'.join(_cell_text(value) for value in row), file=stdout_file)


def _print_headings(headings: list[str], stdout_file: TextIO) -> None:
    """Print TableIO headings before the table rows.

    Args:
        headings: Heading lines read before the table.
        stdout_file: Stream to write to.
    """
    for heading in headings:
        print(f'# {heading}', file=stdout_file)


def _cell_text(value: Value) -> str:
    """Return one TableIO cell value as plain stdout text.

    Args:
        value: Cell value read by TableIO.
    Returns:
        Text representation used by this teaching example.
    """
    if value is None:
        return ''
    return str(value)


# ---------------------------------------------------------------------------
# Only command line handling below this line.


def build_parser() -> argparse.ArgumentParser:
    """Build the command line parser for the table reading example.

    Returns:
        Parser for command line arguments.
    """
    parser = argparse.ArgumentParser(
        description='Read a table with a tableio-cfg-json config.')
    parser.add_argument('-c', '--cfg', dest='config_file', required=True,
                        type=Path, help='JSON configuration file to read.')
    parser.add_argument('-i', '--input', dest='input_file', required=True,
                        type=Path, help='Table file to read.')
    return parser


def main(args: Optional[list[str]] = None) -> int:
    """Parse command line arguments and print the table.

    Args:
        args: Optional command line argument list. ``None`` means
            ``sys.argv[1:]``.
    Returns:
        Process exit code.
    """
    parsed = build_parser().parse_args(args)
    read_table_file(config_file=parsed.config_file,
                    input_file=parsed.input_file)
    return 0


if __name__ == '__main__':
    sys.exit(main())
