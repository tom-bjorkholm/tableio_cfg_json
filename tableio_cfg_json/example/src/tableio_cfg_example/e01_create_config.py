#! /usr/bin/env python3
"""Create a TableIO configuration file and matching syntax guide."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
from pathlib import Path
import sys
from typing import Optional

from tableio import FileAccess, access_capabilities
from tableio_cfg_json import describe_config, get_general_cfg_info, \
    tio_json_config_default


def create_config_files(config_file: Path, syntax_file: Path,
                        file_access: FileAccess, format_name: Optional[str],
                        complete: bool) -> None:
    """Write a JSON config file and matching syntax guide.

    Args:
        config_file: JSON configuration file to write.
        syntax_file: Plain text syntax guide to write.
        file_access: Access mode the configuration is meant for.
        format_name: Optional TableIO format name to prefer.
        complete: Whether optional defaults should be written explicitly.
    """
    # TableIO chooses implementations by matching requested capabilities.
    # A beginner can read this as: choose the backend for what this small
    # program will actually do, not for every possible TableIO feature.
    capabilities = access_capabilities(file_access, error_file=sys.stderr)
    # tio_json_config_default() asks TableIO for the recommended durable
    # values, then wraps them in a config-as-json Config object. The same
    # object can therefore be written as JSON and later passed back to
    # TableIO as normal configuration data.
    config = tio_json_config_default(capabilities=capabilities,
                                     file_access=file_access,
                                     format_name=format_name,
                                     include_all_options=complete)
    config.write(to_json_filename=config_file)
    # The syntax text is deliberately written next to the JSON file. In a
    # real application you can give this text to users as the reference for
    # editing the configuration file by hand.
    syntax_parts = [
        get_general_cfg_info(),
        describe_config(capabilities=capabilities, file_access=file_access,
                        format_name=format_name,
                        include_compact_example=not complete,
                        include_full_example=complete)]
    syntax_file.write_text('\n\n'.join(syntax_parts) + '\n', encoding='utf-8')


# ---------------------------------------------------------------------------
# Only command line handling below this line.


def build_parser() -> argparse.ArgumentParser:
    """Build the command line parser for the configuration example.

    Returns:
        Parser for command line arguments.
    """
    parser = argparse.ArgumentParser(
        description='Create a tableio-cfg-json configuration file.')
    parser.add_argument('-c', '--cfg', dest='config_file', required=True,
                        type=Path, help='JSON configuration file to write.')
    parser.add_argument('-t', '--txt', dest='syntax_file', required=True,
                        type=Path, help='Plain text syntax guide to write.')
    parser.add_argument('-f', '--format', dest='format_name',
                        help='Optional TableIO format name.')
    parser.add_argument('--complete', action='store_true',
                        help='Write a full template with defaults visible.')
    access_group = parser.add_mutually_exclusive_group(required=True)
    access_group.add_argument('-r', '--read', action='store_true',
                              help='Create a read-capable configuration.')
    access_group.add_argument('-w', '--write', action='store_true',
                              help='Create a write-capable configuration.')
    return parser


def _access_from_args(parsed: argparse.Namespace) -> FileAccess:
    """Return the TableIO file access requested by parsed arguments.

    Args:
        parsed: Parsed command line arguments.
    Returns:
        ``FileAccess.READ`` for ``--read`` and ``FileAccess.CREATE`` for
        ``--write``.
    """
    if parsed.read:
        return FileAccess.READ
    return FileAccess.CREATE


def main(args: Optional[list[str]] = None) -> int:
    """Parse command line arguments and create the requested files.

    Args:
        args: Optional command line argument list. ``None`` means
            ``sys.argv[1:]``.
    Returns:
        Process exit code.
    """
    parsed = build_parser().parse_args(args)
    create_config_files(config_file=parsed.config_file,
                        syntax_file=parsed.syntax_file,
                        file_access=_access_from_args(parsed),
                        format_name=parsed.format_name,
                        complete=parsed.complete)
    return 0


if __name__ == '__main__':
    sys.exit(main())
