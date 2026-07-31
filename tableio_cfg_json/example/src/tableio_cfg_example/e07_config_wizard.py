#! /usr/bin/env python3
"""Interactively build the split-cities application config.

The e05_app_config example built the SplitCitiesConfig object directly in
code. This example builds the very same object by asking the user, which
is the other common way to produce an application configuration. Nothing
about the config depends on a wizard; the wizard is just one producer of
it.

The program obtains a user-interface bridge from make_text_ui_bridge()
and calls tio_json_config_wizard() once for each TableIO endpoint (the
input, the less-than output and the not-less-than output). It also asks
the application's own two questions, the split column and the split
limit, with the bridge's ask methods. The collected answers are assembled
into a SplitCitiesConfig and written as the same JSON and syntax-guide
files that e05_app_config wrote.

Choosing the user interface is a single line:

    ui_bridge = make_text_ui_bridge(out_file, in_file, err_file)

make_text_ui_bridge() returns the full-screen Textual bridge when the
program runs in a real terminal, and the plain console bridge when the
streams are redirected, as the tests do. The same program is therefore
both a rich interactive tool and fully scriptable, with no branching in
this file.

This example teaches only the minimal wizard mechanics it needs. The
wizard_ui_bridge package has its own example set for the pieces used
here: obtaining a bridge (e01), the one-question-at-a-time ask methods
(e02), the back/cancel/abort navigation caught below (e03), table
questions (e04) and whole forms (e05, e06).
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import sys
from typing import Callable, Optional, Sequence, TextIO

from tableio import FileAccess, access_capabilities
from tableio_cfg_example.e05_app_config import CITY_COLUMNS, \
    SplitCitiesConfig, run_cfg_txt_cli, _syntax_text
from tableio_cfg_json import TioJsonConfig, tio_json_config_wizard
from wizard_ui_bridge import WizardAbort, WizardBack, WizardCancelLevel, \
    WizardUiBridge, make_text_ui_bridge

INPUT_TITLE = 'Input table configuration'
LESS_TITLE = 'Less-than output table configuration'
NOT_LESS_TITLE = 'Not-less-than output table configuration'

type WizardStep = tuple[
    str, Callable[[WizardUiBridge, dict[str, object], bool], None]]
"""One navigable wizard item as a (title, ask-function) pair.

The title labels the item in the back and cancel messages. The function
asks that one item and stores its answer in the shared results dict. Its
third argument is a backward flag: True asks the item as if entered from
a later item, so an endpoint opens at its last question. run_steps drives
a sequence of these; e08_edit_config and e08_rename_wizard supply their
own sequences, the edit example seeding each item from a stored config.
"""


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
    # The one line that decides the user interface. In a terminal this is
    # the full-screen Textual bridge; with redirected streams it is the
    # console bridge, which keeps the example scriptable and testable.
    ui_bridge = make_text_ui_bridge(out_file, in_file, err_file)
    _write_split_files(ui_bridge, config_file, syntax_file, err_file)


def _write_split_files(ui_bridge: WizardUiBridge, config_file: Path,
                       syntax_file: Path, err_file: TextIO) -> None:
    """Collect answers, build the config and write both files."""
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
    return run_steps(ui_bridge, steps)


def run_steps(ui_bridge: WizardUiBridge, steps: Sequence[WizardStep],
              back_reenters: bool = False) -> Optional[dict[str, object]]:
    """Ask every step in order, honoring back, cancel and abort.

    Each step is a (title, function) pair; the function asks one item and
    stores its answer in the shared results. This is the generic outer
    navigation loop reused by e08_edit_config and e08_rename_wizard, which
    supply their own step lists.

    The snapshot stack lets going back restore the answers as they were
    before the previous item, exactly as the wizard does for its
    questions.

    Args:
        ui_bridge: Bridge between the wizard and the user interface.
        steps: The ordered items to ask.
        back_reenters: When True, a step re-entered by going back is asked
            with its backward flag set, so an endpoint opens at its last
            question. The create wizards leave this False and always start
            a re-entered endpoint at its first question; the edit example
            sets it True.
    Returns:
        The collected answers keyed by item, or None when the user aborts.
    """
    results: dict[str, object] = {}
    history: list[dict[str, object]] = []
    index = 0
    backward = False
    while index < len(steps):
        snapshot = dict(results)
        try:
            steps[index][1](ui_bridge, results, backward)
        except WizardAbort:
            ui_bridge.show('Configuration abandoned; no files written.')
            return None
        except WizardBack:
            if index == 0:
                ui_bridge.show('Already at the first item; please answer it.')
                backward = False
                continue
            index -= 1
            results = history.pop()
            ui_bridge.show(f'Going back to: {steps[index][0]}')
            backward = back_reenters
            continue
        except WizardCancelLevel:
            results = dict(snapshot)
            ui_bridge.show('There is no outer level to return to.')
            ui_bridge.show(f'Restarting {steps[index][0]}.')
            backward = False
            continue
        history.append(snapshot)
        index += 1
        backward = False
    return results


def _step_input(ui_bridge: WizardUiBridge, results: dict[str, object],
                _backward: bool) -> None:
    """Configure the input endpoint."""
    results['input'] = _ask_endpoint(INPUT_TITLE, FileAccess.READ, ui_bridge)


def _step_split_column(ui_bridge: WizardUiBridge, results: dict[str, object],
                       _backward: bool) -> None:
    """Ask the application-owned split column."""
    # The split rule is deliberately application-owned configuration. TableIO
    # knows how to read and write tables, but it does not know which city rows
    # this particular program wants in each output file.
    results['split_column'] = _ask_split_column(ui_bridge)


def _step_split_limit(ui_bridge: WizardUiBridge, results: dict[str, object],
                      _backward: bool) -> None:
    """Ask the application-owned split limit."""
    results['split_limit'] = _ask_split_limit(ui_bridge)


def _step_less(ui_bridge: WizardUiBridge, results: dict[str, object],
               _backward: bool) -> None:
    """Configure the less-than output endpoint."""
    results['less'] = _ask_endpoint(LESS_TITLE, FileAccess.CREATE, ui_bridge)


def _step_not_less(ui_bridge: WizardUiBridge, results: dict[str, object],
                   _backward: bool) -> None:
    """Configure the not-less-than output endpoint."""
    results['not_less'] = _ask_endpoint(NOT_LESS_TITLE, FileAccess.CREATE,
                                        ui_bridge)


def _build_config(results: dict[str, object],
                  stderr_file: TextIO) -> SplitCitiesConfig:
    """Assemble the application config from the collected answers."""
    # A config object is first created with defaults. The application then
    # assigns the specific values it collected, just as a real program often
    # starts with defaults and overrides the choices made by the user.
    config = SplitCitiesConfig(stderr_file=stderr_file)
    _assign_split(config, results)
    return config


def _assign_split(config: SplitCitiesConfig,
                  results: dict[str, object]) -> None:
    """Assign the five shared split-cities members from the answers.

    e08_rename_wizard reuses this on a RenameSplitConfig and then assigns
    its two extra column-rename members, so the shared assignment lives in
    one place.
    """
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
    config.input = input_config
    config.less_than_output = less_config
    config.not_less_than_output = not_less_config
    config.split_column = split_column
    config.split_limit = split_limit


def _ask_endpoint(title: str, file_access: FileAccess,
                  ui_bridge: WizardUiBridge, *,
                  default: Optional[TioJsonConfig] = None,
                  backward: bool = False) -> TioJsonConfig:
    """Ask all wizard questions for one TableIO endpoint config.

    Passing default seeds the endpoint questions with a stored config, and
    backward opens the endpoint at its last question. The create wizard
    uses neither; the edit example uses both.
    """
    # File access is part of the runtime task. Passing it here means an input
    # endpoint only offers read-capable formats, while output endpoints only
    # offer create-capable formats.
    capabilities = access_capabilities(file_access,
                                       error_file=ui_bridge.error_file())
    ui_bridge.show(title)
    return tio_json_config_wizard(capabilities, file_access, ui_bridge,
                                  default=default, backward=backward)


def _ask_split_column(ui_bridge: WizardUiBridge,
                      default: str = 'Country') -> str:
    """Ask which input column should decide the split.

    The question goes through the bridge, so the same back, cancel and abort
    controls the wizard offers also work between application items here.
    """
    # ask_choice() offers the finite set of column names and returns exactly
    # one of them. It accepts a menu number, a column name or a unique name
    # prefix and re-asks an unusable answer itself, so the application does
    # not interpret the raw answer. An empty answer selects the default,
    # which the bridge shows next to the question. The program only supports
    # these three column names because the teaching input file is
    # intentionally small and predictable.
    title = 'Select the column whose value decides the split:'
    return ui_bridge.ask_choice(title, choices=CITY_COLUMNS, default=default)


def _ask_split_limit(ui_bridge: WizardUiBridge, default: str = 'M') -> str:
    """Ask for the string value used as split limit."""
    # ask_text() returns the entered text, or the default for an empty answer.
    # The bridge shows the default next to the question, so pressing Enter
    # keeps it.
    title = 'Split values less than this text into the first output:'
    answer = ui_bridge.ask_text(title, default=default)
    return default if answer is None else answer


# ---------------------------------------------------------------------------
# Only command line handling below this line. The --cfg/--txt runner is
# shared with the in-code builder, so both expose the same command line.


def main(args: Optional[list[str]] = None) -> int:
    """Parse command line arguments and create split-cities config files.

    Run this module in a terminal to see the Textual interface; redirect
    its input to see the same wizard fall back to the console bridge.
    """
    return run_cfg_txt_cli(create_split_config_files,
                           'Interactively build the split-cities app config.',
                           args)


if __name__ == '__main__':
    sys.exit(main())
