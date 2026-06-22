#! /usr/bin/env python3
"""Interactively create config files that rename the output columns.

This builds on e05_split_cities_wizard and e07_split_cities_textual. It
asks the same input, split and output questions, and adds one variable-
row table question per output that maps input columns to the column
names written in that output file. The collected configuration is a
RenameSplitConfig, which e09_split_cities_rename later uses to split a
table and rename each output independently.

Two ideas are demonstrated here:

- A wizard ask_table with a variable number of rows. The user adds and
  deletes rows to build a mapping of any size, instead of filling a
  fixed set of rows. In a terminal the Textual bridge offers Add row and
  Remove row buttons; on the console the row-menu interface offers :+ to
  add a row and :- N to delete row N.
- Forcing the user interface bridge from the command line. The --ui
  option selects between the console bridge and the full-screen Textual
  bridge through make_text_ui_bridge, instead of letting it auto-select
  by whether the program runs in a terminal.

Everything that does not differ from e05 is reused from it: the outer
navigation loop run_steps, the per-item step functions, the shared
member assignment _assign_split and the syntax-guide text.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
from pathlib import Path
import sys
from typing import Callable, Optional, TextIO

from tableio_cfg_json import TableCell, TableColumn, UiBridgeType, \
    WizardUiBridge, make_text_ui_bridge

from example.e06_split_cities import CITY_COLUMNS
from example.e09_split_cities_rename import RenameSplitConfig
from example.e05_split_cities_wizard import INPUT_TITLE, LESS_TITLE, \
    NOT_LESS_TITLE, run_steps, _assign_split, _paragraph, _step_input, \
    _step_less, _step_not_less, _step_split_column, _step_split_limit, \
    _syntax_text

LESS_NAMES_TITLE = 'Less-than output column names'
NOT_LESS_NAMES_TITLE = 'Not-less-than output column names'


# pylint: disable-next=too-many-arguments,too-many-positional-arguments
def create_split_config_files(config_file: Path, syntax_file: Path,
                              bridge_type: UiBridgeType = UiBridgeType.AUTO,
                              stdin_file: Optional[TextIO] = None,
                              stdout_file: Optional[TextIO] = None,
                              stderr_file: Optional[TextIO] = None) -> None:
    """Ask questions and write a rename-split JSON config and guide.

    Args:
        config_file: JSON application configuration file to write.
        syntax_file: Plain text guide for later hand-editing.
        bridge_type: Which user interface bridge to use. AUTO selects the
            Textual bridge in a terminal and the console bridge otherwise;
            CONSOLE and TEXTUAL force one regardless of the terminal.
        stdin_file: Optional input stream for tests or scripted use.
        stdout_file: Optional output stream for tests or scripted use.
        stderr_file: Optional diagnostic stream for TableIO/config errors.
    """
    in_file = sys.stdin if stdin_file is None else stdin_file
    out_file = sys.stdout if stdout_file is None else stdout_file
    err_file = sys.stderr if stderr_file is None else stderr_file
    # make_text_ui_bridge honors bridge_type: AUTO decides by terminal,
    # while CONSOLE and TEXTUAL force the choice. This is the one place
    # the --ui command line switch reaches.
    ui_bridge = make_text_ui_bridge(out_file, in_file, err_file, bridge_type)
    _write_files(ui_bridge, config_file, syntax_file, err_file)


def _write_files(ui_bridge: WizardUiBridge, config_file: Path,
                 syntax_file: Path, err_file: TextIO) -> None:
    """Collect answers, build the config and write both files."""
    results = run_steps(ui_bridge, _build_steps())
    if results is None:
        return
    config = _build_config(results, err_file)
    config.write(to_json_filename=config_file, stderr_file=err_file)
    text = _syntax_text(config, err_file) + '\n\n' + _rename_guide()
    syntax_file.write_text(text + '\n', encoding='utf-8')


def _build_steps() -> list[tuple[str, Callable[..., None]]]:
    """Return the ordered (title, step) pairs for the rename wizard.

    Each output's column-rename step follows the step that configured
    that output endpoint, so related questions stay together.
    """
    return [
        (INPUT_TITLE, _step_input),
        ('the split column', _step_split_column),
        ('the split limit', _step_split_limit),
        (LESS_TITLE, _step_less),
        (LESS_NAMES_TITLE, _step_less_names),
        (NOT_LESS_TITLE, _step_not_less),
        (NOT_LESS_NAMES_TITLE, _step_not_less_names)]


def _step_less_names(ui_bridge: WizardUiBridge,
                     results: dict[str, object]) -> None:
    """Ask the column renaming for the less-than output."""
    results['less_names'] = _ask_output_names(ui_bridge, LESS_NAMES_TITLE)


def _step_not_less_names(ui_bridge: WizardUiBridge,
                         results: dict[str, object]) -> None:
    """Ask the column renaming for the not-less-than output."""
    results['not_less_names'] = _ask_output_names(ui_bridge,
                                                  NOT_LESS_NAMES_TITLE)


def _ask_output_names(ui_bridge: WizardUiBridge, title: str) -> dict[str, str]:
    """Ask a variable-row table mapping input columns to output names.

    The left column chooses one input column; the right column is the
    name written for it. A row whose either cell is empty is ignored, so
    an unlisted or unfilled column keeps its original name.
    """
    columns = (TableColumn('Source column'), TableColumn('Output name'))
    question = f'{title} (map input columns to output names):'
    result = ui_bridge.ask_table(columns, _start_rename_cells(), question,
                                 min_rows=0, max_rows=len(CITY_COLUMNS))
    return _names_from_table(result)


def _start_rename_cells() -> list[list[TableCell]]:
    """Return two pre-filled rename rows for the rename table.

    The table is deliberately seeded with two identity rows only so this
    teaching example naturally exercises both adding a row and deleting a
    row. Pre-filling rows is not a general UX recommendation; a real
    program would usually start an optional mapping empty.
    """
    return [[TableCell(value=name, choices=CITY_COLUMNS),
             TableCell(value=name)]
            for name in CITY_COLUMNS[:2]]


def _names_from_table(result: list[list[Optional[str]]]) -> dict[str, str]:
    """Build the source-to-output mapping from a filled rename table."""
    names: dict[str, str] = {}
    for source, output in result:
        if source and output:
            names[source] = output
    return names


def _build_config(results: dict[str, object],
                  stderr_file: TextIO) -> RenameSplitConfig:
    """Assemble the rename-split config from the collected answers."""
    config = RenameSplitConfig(stderr_file=stderr_file)
    _assign_split(config, results)
    less_names = results['less_names']
    not_less_names = results['not_less_names']
    assert isinstance(less_names, dict)
    assert isinstance(not_less_names, dict)
    config.less_output_names = less_names
    config.not_less_output_names = not_less_names
    return config


def _rename_guide() -> str:
    """Return the syntax-guide section describing the rename members."""
    text = (
        'Output column renaming\n\n'
        'The members less_output_names and not_less_output_names each map '
        'an input column name (City, Country or Continent) to the column '
        'name written in that output file. A column that is not listed '
        'keeps its original name, and the two outputs are renamed '
        'independently.')
    title, body = text.split('\n\n', maxsplit=1)
    return title + '\n\n' + _paragraph(body)


# ---------------------------------------------------------------------------
# Only command line handling below this line.


_DESCRIPTION = 'Create rename-split config files for the split example.'
_UI_TYPES = {'auto': UiBridgeType.AUTO, 'console': UiBridgeType.CONSOLE,
             'textual': UiBridgeType.TEXTUAL}


def build_parser() -> argparse.ArgumentParser:
    """Build the command line parser for the rename wizard."""
    parser = argparse.ArgumentParser(description=_DESCRIPTION)
    parser.add_argument('-c', '--cfg', dest='config_file', required=True,
                        type=Path, help='JSON configuration file to write.')
    parser.add_argument('-t', '--txt', dest='syntax_file', required=True,
                        type=Path, help='Plain text syntax guide to write.')
    parser.add_argument('--ui', dest='ui', default='auto',
                        choices=sorted(_UI_TYPES),
                        help='Force the UI bridge (default: auto).')
    return parser


def main(args: Optional[list[str]] = None) -> int:
    """Parse command line arguments and create rename-split config files."""
    parsed = build_parser().parse_args(args)
    create_split_config_files(config_file=parsed.config_file,
                              syntax_file=parsed.syntax_file,
                              bridge_type=_UI_TYPES[parsed.ui])
    return 0


if __name__ == '__main__':
    sys.exit(main())
