#! /usr/bin/env python3
"""Create a customized TableIO configuration file and syntax guide."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
from pathlib import Path
import sys
from typing import Optional

from tableio import FileAccess, access_capabilities
from tableio_cfg_json import TioJsonCsvConfig, describe_config, \
    get_general_cfg_info, tio_json_config_default


# pylint: disable-next=too-many-arguments,too-many-positional-arguments
def create_custom_files(config_file: Path, syntax_file: Path,
                        file_access: FileAccess, format_name: Optional[str],
                        complete: bool, csv_delimiter: str,
                        character_encoding: str, table_alignment: str) -> None:
    """Write a JSON config file with a few deliberate custom values.

    Args:
        config_file: JSON configuration file to write.
        syntax_file: Plain text syntax guide to write.
        file_access: Access mode the configuration is meant for.
        format_name: Optional TableIO format name to prefer.
        complete: Whether optional defaults should be written explicitly.
        csv_delimiter: CSV delimiter to store in the ``csv`` section.
        character_encoding: Character encoding to store at top level.
        table_alignment: Table alignment to store at top level.
    """
    # This example starts in the same way as e01: ask TableIO for the
    # recommended durable configuration for this runtime task.
    capabilities = access_capabilities(file_access, error_file=sys.stderr)
    config = tio_json_config_default(capabilities, file_access,
                                     format_name=format_name,
                                     include_all_options=complete)
    # The important extra teaching point is here: after creating the default
    # config object, a program can set the values it wants to store. These are
    # ordinary attributes because TioJsonConfig is also TableIO ConfigData.
    config.character_encoding = character_encoding
    config.table_alignment = table_alignment
    # CSV settings live in the optional nested "csv" object. This value is
    # stored even when the selected format is not CSV. TableIO simply ignores
    # CSV-only settings when another backend is used.
    if config.csv is None:
        config.csv = TioJsonCsvConfig(delimiter=csv_delimiter)
    else:
        config.csv.delimiter = csv_delimiter
    config.write(to_json_filename=config_file)
    syntax_text = get_general_cfg_info() + '\n\n'
    syntax_text += describe_config(capabilities=capabilities,
                                   file_access=file_access,
                                   format_name=format_name,
                                   include_compact_example=not complete,
                                   include_full_example=complete)
    syntax_file.write_text(syntax_text + '\n', encoding='utf-8')


# ---------------------------------------------------------------------------
# Only command line handling below this line.


def build_parser() -> argparse.ArgumentParser:
    """Build the command line parser for the custom config example.

    Returns:
        Parser for command line arguments.
    """
    parser = argparse.ArgumentParser(
        description='Create a customized tableio-cfg-json config.')
    for short_name, long_name, dest_name, help_text in [
            ('-c', '--cfg', 'config_file',
             'JSON configuration file to write.'),
            ('-t', '--txt', 'syntax_file',
             'Plain text syntax guide to write.')]:
        parser.add_argument(short_name, long_name, dest=dest_name,
                            required=True, type=Path, help=help_text)
    parser.add_argument('-f', '--format', dest='format_name',
                        help='Optional TableIO format name.')
    parser.add_argument('--complete', action='store_true',
                        help='Write a full template with defaults visible.')
    parser.add_argument('--csv-delimiter', default=':', metavar='CHAR',
                        help='CSV delimiter to store. Default: ":".')
    parser.add_argument('--encoding', dest='character_encoding',
                        default='utf-8',
                        help='Character encoding to store. Default: utf-8.')
    parser.add_argument('--alignment', dest='table_alignment',
                        default='CENTER',
                        help='Table alignment to store. Default: CENTER.')
    access_group = parser.add_mutually_exclusive_group(required=True)
    for short_name, long_name, help_text in [
            ('-r', '--read', 'Create a read-capable configuration.'),
            ('-w', '--write', 'Create a write-capable configuration.')]:
        access_group.add_argument(short_name, long_name, action='store_true',
                                  help=help_text)
    return parser


def main(args: Optional[list[str]] = None) -> int:
    """Parse command line arguments and create the requested files.

    Args:
        args: Optional command line argument list. ``None`` means
            ``sys.argv[1:]``.
    Returns:
        Process exit code.
    """
    parsed = build_parser().parse_args(args)
    file_access = FileAccess.READ if parsed.read else FileAccess.CREATE
    create_custom_files(config_file=parsed.config_file,
                        syntax_file=parsed.syntax_file,
                        file_access=file_access,
                        format_name=parsed.format_name,
                        complete=parsed.complete,
                        csv_delimiter=parsed.csv_delimiter,
                        character_encoding=parsed.character_encoding,
                        table_alignment=parsed.table_alignment)
    return 0


if __name__ == '__main__':
    sys.exit(main())
