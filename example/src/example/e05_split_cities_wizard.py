#! /usr/bin/env python3
"""Interactively create config files for the split-cities example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
from pathlib import Path
import sys
from textwrap import wrap
from typing import Callable, Optional, Sequence, TextIO

from tableio import Capabilities, FileAccess, access_capabilities
from tableio_cfg_json import TioJsonConfig, describe_config_members, \
    describe_config_reference, get_config_member_names, \
    get_general_cfg_info, WizardAbort, WizardBack, WizardCancelLevel, \
    WizardUiBridge, WizardUiBridgeConsole, tio_json_config_wizard

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

    The application collects answers through a small navigation loop. When
    the user abandons configuration nothing is written, so any previous
    files are left untouched.

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
    _write_split_files(ui_bridge, config_file, syntax_file, err_file)


def _write_split_files(ui_bridge: WizardUiBridge, config_file: Path,
                       syntax_file: Path, err_file: TextIO) -> None:
    """Collect answers, build the config and write both files.

    This is the part of the work that does not depend on which bridge is
    used. e05 calls it with the console bridge; e07 calls it with the
    bridge that make_text_ui_bridge chooses, so the two examples differ
    only in how they build the bridge.
    """
    results = _collect_answers(ui_bridge)
    if results is None:
        return
    config = _build_config(results, err_file)
    config.write(to_json_filename=config_file, stderr_file=err_file)
    # The text file is for the human who later opens the JSON by hand. It is
    # intentionally broader than the choices just made by the wizard.
    syntax_file.write_text(_syntax_text(config, err_file) + '\n',
                           encoding='utf-8')


def _collect_answers(ui_bridge: WizardUiBridge) -> Optional[dict[str, object]]:
    """Ask every configuration item, honoring back, cancel and abort.

    tio_json_config_wizard() navigates the questions inside one endpoint.
    This application owns the list of items above the endpoints, so it runs
    the same kind of loop one level up. When the wizard cannot navigate any
    further inside an endpoint it raises a WizardNavigation out to here:

    - WizardAbort abandons the whole configuration; nothing is written.
    - WizardBack steps to the previous item.
    - WizardCancelLevel means "leave the current level and change the
      choice that opened it". This flat application has no configuration
      level outside its list of items, so there is no such choice to
      return to; following the bridge contract it re-asks the current item
      and tells the user there is no outer level.

    The snapshot stack lets going back restore the answers as they were
    before the previous item, exactly as the wizard does for its questions.

    Returns:
        The collected answers keyed by item, or None when the user aborts.
    """
    steps = [
        (INPUT_TITLE, _step_input),
        ('the split column', _step_split_column),
        ('the split limit', _step_split_limit),
        (LESS_TITLE, _step_less),
        (NOT_LESS_TITLE, _step_not_less)]
    results: dict[str, object] = {}
    history: list[dict[str, object]] = []
    index = 0
    while index < len(steps):
        snapshot = dict(results)
        try:
            steps[index][1](ui_bridge, results)
        except WizardAbort:
            ui_bridge.show('Configuration abandoned; no files written.')
            return None
        except WizardBack:
            if index == 0:
                ui_bridge.show('Already at the first item; please answer it.')
                continue
            index -= 1
            results = history.pop()
            ui_bridge.show(f'Going back to: {steps[index][0]}')
            continue
        except WizardCancelLevel:
            results = dict(snapshot)
            ui_bridge.show('There is no outer level to return to.')
            ui_bridge.show(f'Restarting {steps[index][0]}.')
            continue
        history.append(snapshot)
        index += 1
    return results


def _step_input(ui_bridge: WizardUiBridge, results: dict[str, object]) -> None:
    """Configure the input endpoint."""
    results['input'] = _ask_endpoint(INPUT_TITLE, FileAccess.READ, ui_bridge)


def _step_split_column(ui_bridge: WizardUiBridge,
                       results: dict[str, object]) -> None:
    """Ask the application-owned split column."""
    # The split rule is deliberately application-owned configuration. TableIO
    # knows how to read and write tables, but it does not know which city rows
    # this particular program wants in each output file.
    results['split_column'] = _ask_split_column(ui_bridge)


def _step_split_limit(ui_bridge: WizardUiBridge,
                      results: dict[str, object]) -> None:
    """Ask the application-owned split limit."""
    results['split_limit'] = _ask_split_limit(ui_bridge)


def _step_less(ui_bridge: WizardUiBridge, results: dict[str, object]) -> None:
    """Configure the less-than output endpoint."""
    results['less'] = _ask_endpoint(LESS_TITLE, FileAccess.CREATE, ui_bridge)


def _step_not_less(ui_bridge: WizardUiBridge,
                   results: dict[str, object]) -> None:
    """Configure the not-less-than output endpoint."""
    results['not_less'] = _ask_endpoint(NOT_LESS_TITLE, FileAccess.CREATE,
                                        ui_bridge)


def _build_config(results: dict[str, object],
                  stderr_file: TextIO) -> SplitCitiesConfig:
    """Assemble the application config from the collected answers."""
    # A config object is first created with defaults. The application then
    # assigns the specific values it collected, just as a real program often
    # starts with defaults and overrides the choices made by the user.
    input_config = results['input']
    less_config = results['less']
    not_less_config = results['not_less']
    split_column = results['split_column']
    split_limit = results['split_limit']
    assert isinstance(input_config, TioJsonConfig)
    assert isinstance(less_config, TioJsonConfig)
    assert isinstance(not_less_config, TioJsonConfig)
    assert isinstance(split_column, str)
    assert isinstance(split_limit, str)
    config = SplitCitiesConfig(stderr_file=stderr_file)
    config.input = input_config
    config.less_than_output = less_config
    config.not_less_than_output = not_less_config
    config.split_column = split_column
    config.split_limit = split_limit
    return config


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


def _ask_split_column(ui_bridge: WizardUiBridge) -> str:
    """Ask which input column should decide the split.

    The question goes through the bridge, so the same back, cancel and abort
    controls the wizard offers also work between application items here.
    """
    # ask_choice() offers the finite set of column names and returns exactly
    # one of them. It accepts a menu number, a column name or a unique name
    # prefix and re-asks an unusable answer itself, so the application does
    # not interpret the raw answer. An empty answer selects the default.
    # The program only supports these three column names because the teaching
    # input file is intentionally small and predictable.
    title = 'Select split column:\nEnter: Country (recommended)'
    return ui_bridge.ask_choice(title, choices=CITY_COLUMNS, default='Country')


def _ask_split_limit(ui_bridge: WizardUiBridge) -> str:
    """Ask for the string value used as split limit."""
    # ask_text() returns the entered text, or None for an empty answer when
    # nullable is True. An empty answer selects the default limit 'M'.
    title = ('Split values less than this text into the first output.\n'
             'Enter: M (recommended)')
    answer = ui_bridge.ask_text(title, nullable=True)
    return 'M' if answer is None else answer


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


_DESCRIPTION = 'Create config files for the split-cities example.'


def run_split_cli(create_files: Callable[..., None], description: str,
                  args: Optional[list[str]] = None) -> int:
    """Parse the --cfg and --txt arguments and run create_files.

    Shared by e05 and e07 so both expose the same command line, differing
    only in the program description and the create_files they run.
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-c', '--cfg', dest='config_file', required=True,
                        type=Path, help='JSON configuration file to write.')
    parser.add_argument('-t', '--txt', dest='syntax_file', required=True,
                        type=Path, help='Plain text syntax guide to write.')
    parsed = parser.parse_args(args)
    create_files(config_file=parsed.config_file,
                 syntax_file=parsed.syntax_file)
    return 0


def main(args: Optional[list[str]] = None) -> int:
    """Parse command line arguments and create split-cities config files."""
    return run_split_cli(create_split_config_files, _DESCRIPTION, args)


if __name__ == '__main__':
    sys.exit(main())
