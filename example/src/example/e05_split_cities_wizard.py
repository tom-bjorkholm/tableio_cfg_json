#! /usr/bin/env python3
"""Interactively create config files for the split-cities example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
from pathlib import Path
import sys
from textwrap import wrap
from typing import Optional, Sequence, TextIO

from tableio import Capabilities, FileAccess, access_capabilities
from tableio_cfg_json import TioJsonConfig, describe_config_members, \
    describe_config_reference, get_config_member_names, \
    get_general_cfg_info, WizardUiBridge, WizardUiBridgeConsole, \
    tio_json_config_wizard

from example.e06_split_cities import CITY_COLUMNS, SplitCitiesConfig


INPUT_TITLE = 'Input table configuration'
LESS_TITLE = 'Less-than output table configuration'
NOT_LESS_TITLE = 'Not-less-than output table configuration'
_WIDTH = 79


def create_split_config_files(config_file: Path, syntax_file: Path,
                              stdin_file: Optional[TextIO] = None,
                              stdout_file: Optional[TextIO] = None,
                              stderr_file: Optional[TextIO] = None) -> None:
    """Ask questions and write a split-cities JSON config and guide.

    Args:
        config_file: JSON application configuration file to write.
        syntax_file: Plain text guide for later hand-editing.
        stdin_file: Optional input stream for tests or scripted use.
        stdout_file: Optional output stream for tests or scripted use.
        stderr_file: Optional diagnostic stream for TableIO/config errors.
    """
    in_file = sys.stdin if stdin_file is None else stdin_file
    out_file = sys.stdout if stdout_file is None else stdout_file
    err_file = sys.stderr if stderr_file is None else stderr_file
    ui_bridge = WizardUiBridgeConsole(out_file, in_file, err_file)
    # tio_json_config_wizard(), provided by tableio_cfg_json, creates exactly
    # one TableIO endpoint config. This application composes three endpoint
    # configs into one larger config-as-json configuration file.
    input_config = _ask_endpoint(INPUT_TITLE, FileAccess.READ, ui_bridge)
    # The split rule is deliberately application-owned configuration. TableIO
    # knows how to read and write tables, but it does not know which city rows
    # this particular program wants in each output file.
    split_column = _ask_split_column(in_file, out_file)
    split_limit = _ask_split_limit(in_file, out_file)
    less_config = _ask_endpoint(LESS_TITLE, FileAccess.CREATE, ui_bridge)
    not_less_config = _ask_endpoint(NOT_LESS_TITLE, FileAccess.CREATE,
                                    ui_bridge)
    # A config object is first created with defaults. The application then
    # assigns the specific values it collected, just as a real program often
    # starts with defaults and overrides the choices made by the user.
    config = SplitCitiesConfig(stderr_file=err_file)
    config.input = input_config
    config.less_than_output = less_config
    config.not_less_than_output = not_less_config
    config.split_column = split_column
    config.split_limit = split_limit
    config.write(to_json_filename=config_file, stderr_file=err_file)
    # The text file is for the human who later opens the JSON by hand. It is
    # intentionally broader than the choices just made by the wizard.
    syntax_file.write_text(_syntax_text(config, err_file) + '\n',
                           encoding='utf-8')


def _ask_endpoint(title: str, file_access: FileAccess,
                  ui_bridge: WizardUiBridge) -> TioJsonConfig:
    """Ask all wizard questions for one TableIO endpoint config."""
    # File access is part of the runtime task. Passing it here means an input
    # endpoint only offers read-capable formats, while output endpoints only
    # offer create-capable formats.
    capabilities = access_capabilities(file_access,
                                       error_file=ui_bridge.error_file())
    ui_bridge.show(title)
    return tio_json_config_wizard(capabilities, file_access, ui_bridge)


def _ask_split_column(stdin_file: TextIO, stdout_file: TextIO) -> str:
    """Ask which input column should decide the split."""
    while True:
        # The program only supports these three column names because the
        # teaching input file is intentionally small and predictable.
        print('', file=stdout_file)
        print('Select split column:', file=stdout_file)
        print('Enter: Country (recommended)', file=stdout_file)
        for index, column_name in enumerate(CITY_COLUMNS, start=1):
            print(f'{index}: {column_name}', file=stdout_file)
        answer = _read_answer('split column', stdin_file, stdout_file)
        if answer == '':
            return 'Country'
        if answer in CITY_COLUMNS:
            return answer
        try:
            column_index = int(answer)
        except ValueError:
            print('Please enter a column name or one of the menu numbers.',
                  file=stdout_file)
            continue
        if 1 <= column_index <= len(CITY_COLUMNS):
            return CITY_COLUMNS[column_index - 1]
        print('Please enter a column name or one of the menu numbers.',
              file=stdout_file)


def _ask_split_limit(stdin_file: TextIO, stdout_file: TextIO) -> str:
    """Ask for the string value used as split limit."""
    while True:
        print('', file=stdout_file)
        print('Split values less than this text into the first output.',
              file=stdout_file)
        print('Enter: M (recommended)', file=stdout_file)
        answer = _read_answer('split limit', stdin_file, stdout_file)
        if answer == '':
            return 'M'
        if answer:
            return answer
        print('Please enter a non-empty split limit.', file=stdout_file)


def _read_answer(prompt_name: str, stdin_file: TextIO,
                 stdout_file: TextIO) -> str:
    """Read one answer and fail clearly if scripted input ends early."""
    print('> ', end='', file=stdout_file)
    line = stdin_file.readline()
    if line != '':
        return line.rstrip('\n')
    message = f'No answer supplied for {prompt_name}.'
    raise EOFError(message)


def _syntax_text(config: SplitCitiesConfig, stderr_file: TextIO) -> str:
    """Build the plain text guide written next to the JSON config."""
    read_caps = access_capabilities(FileAccess.READ, error_file=stderr_file)
    create_caps = access_capabilities(FileAccess.CREATE,
                                      error_file=stderr_file)
    name_lists = [
        _member_names(read_caps, FileAccess.READ),
        _member_names(create_caps, FileAccess.CREATE)]
    less_intro = ('This output receives rows with the selected value below '
                  'the split limit.')
    not_less_intro = 'This output receives the remaining data rows.'
    parts = [
        get_general_cfg_info(),
        _application_guide(),
        _endpoint_guide('input', 'The input endpoint reads the city table.',
                        config.input, read_caps, FileAccess.READ, stderr_file),
        _endpoint_guide('less_than_output', less_intro,
                        config.less_than_output, create_caps,
                        FileAccess.CREATE, stderr_file),
        _endpoint_guide('not_less_than_output', not_less_intro,
                        config.not_less_than_output, create_caps,
                        FileAccess.CREATE, stderr_file),
        'Configuration member reference\n\n'
        + describe_config_reference(member_names=_unique_names(name_lists))]
    return '\n\n'.join(parts)


def _application_guide() -> str:
    """Return the application-owned part of the syntax guide."""
    text = (
        'Split-cities application configuration\n\n'
        'The top-level JSON object has five members. The members input, '
        'less_than_output and not_less_than_output are nested TableIO '
        'endpoint configurations. The member split_column selects one of '
        'City, Country or Continent. The member split_limit is a normal '
        'Python string, and the example compares strings case-sensitively.')
    title, paragraph = text.split('\n\n', maxsplit=1)
    return title + '\n\n' + _paragraph(paragraph)


# pylint: disable-next=too-many-arguments,too-many-positional-arguments
def _endpoint_guide(member_name: str, intro_text: str, config: TioJsonConfig,
                    capabilities: Capabilities, file_access: FileAccess,
                    stderr_file: TextIO) -> str:
    """Return the syntax guide for one nested TableIO endpoint config."""
    format_name = _format_name(config)
    member_text = describe_config_members(capabilities=capabilities,
                                          file_access=file_access)
    selected_text = config.as_json_string(stderr_file=stderr_file)
    intro = _paragraph(
        f'{intro_text} It currently uses the {format_name} format.')
    return (
        f'{member_name}\n\n'
        + intro
        + '\n\nEditable endpoint choices and members:\n\n'
        + member_text
        + '\n\nCurrently selected endpoint JSON:\n\n'
        + selected_text)


def _member_names(capabilities: Capabilities,
                  file_access: FileAccess) -> list[str]:
    """Return relevant TableIO member names for one endpoint config."""
    member_names = get_config_member_names(capabilities=capabilities,
                                           file_access=file_access)
    return list(member_names)


def _format_name(config: TioJsonConfig) -> str:
    """Return the required format name from a validated config object."""
    assert isinstance(config.format_name, str)
    return config.format_name


def _unique_names(name_lists: Sequence[Sequence[str]]) -> list[str]:
    """Return unique names in first-seen order."""
    member_names: list[str] = []
    for name_list in name_lists:
        for member_name in name_list:
            if member_name not in member_names:
                member_names.append(member_name)
    return member_names


def _paragraph(text: str) -> str:
    """Return one wrapped plain text paragraph."""
    return '\n'.join(wrap(text, width=_WIDTH))


# ---------------------------------------------------------------------------
# Only command line handling below this line.


def build_parser() -> argparse.ArgumentParser:
    """Build the command line parser for the split-cities wizard."""
    parser = argparse.ArgumentParser(
        description='Create config files for the split-cities example.')
    parser.add_argument('-c', '--cfg', dest='config_file', required=True,
                        type=Path, help='JSON configuration file to write.')
    parser.add_argument('-t', '--txt', dest='syntax_file', required=True,
                        type=Path, help='Plain text syntax guide to write.')
    return parser


def main(args: Optional[list[str]] = None) -> int:
    """Parse command line arguments and create split-cities config files."""
    parsed = build_parser().parse_args(args)
    create_split_config_files(config_file=parsed.config_file,
                              syntax_file=parsed.syntax_file)
    return 0


if __name__ == '__main__':
    sys.exit(main())
