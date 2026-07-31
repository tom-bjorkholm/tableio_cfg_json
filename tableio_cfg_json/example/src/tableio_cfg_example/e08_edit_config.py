#! /usr/bin/env python3
"""Edit a stored split-cities app config and navigate its endpoints.

This builds on e07_config_wizard. That example created a fresh
SplitCitiesConfig; this one reopens a stored config and re-asks the same
items, but seeds each one with the value already stored so pressing Enter
keeps it. Two related ideas are shown:

- Editing with defaults. The stored config is passed to
  tio_json_config_wizard() as its default, so every stored value becomes
  the value the matching question suggests.
- Navigating between the application's endpoints. The same outer loop as
  e07 (run_steps) catches the back, cancel and abort exceptions the
  bridge raises out of one endpoint and uses them to move between the
  application's items. When the user goes back into an earlier endpoint,
  that endpoint is re-opened at its last question (backward=True), so the
  user lands where they left it and can walk back from there.

The exception semantics caught by run_steps (WizardBack, WizardCancelLevel
and WizardAbort) are taught on their own in the wizard_ui_bridge
navigation example (e03). The bridge is obtained with make_text_ui_bridge()
exactly as in e07, so the editor is full-screen in a terminal and
scriptable with redirected streams.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
from pathlib import Path
import sys
from typing import Optional, TextIO

from tableio import FileAccess
from tableio_cfg_example.e05_app_config import SplitCitiesConfig
from tableio_cfg_example.e07_config_wizard import INPUT_TITLE, LESS_TITLE, \
    NOT_LESS_TITLE, WizardStep, run_steps, _ask_endpoint, _ask_split_column, \
    _ask_split_limit, _build_config
from wizard_ui_bridge import WizardUiBridge, make_text_ui_bridge


def edit_config_file(config_file: Path, stdin_file: Optional[TextIO] = None,
                     stdout_file: Optional[TextIO] = None,
                     stderr_file: Optional[TextIO] = None) -> None:
    """Reopen a stored app config, edit it, and write it back.

    When the user abandons the edit nothing is written, so the stored file
    is left exactly as it was.

    Args:
        config_file: JSON application configuration file to edit.
        stdin_file: Optional input stream for tests or scripted use.
        stdout_file: Optional output stream for tests or scripted use.
        stderr_file: Optional diagnostic stream for TableIO/config errors.
    """
    in_file = sys.stdin if stdin_file is None else stdin_file
    out_file = sys.stdout if stdout_file is None else stdout_file
    err_file = sys.stderr if stderr_file is None else stderr_file
    ui_bridge = make_text_ui_bridge(out_file, in_file, err_file)
    stored = _read_stored(config_file, err_file)
    # back_reenters=True is the one difference from the create wizard: going
    # back into an earlier endpoint reopens it at its last question.
    results = run_steps(ui_bridge, _edit_steps(stored), back_reenters=True)
    if results is None:
        return
    config = _build_config(results, err_file)
    config.write(to_json_filename=config_file, stderr_file=err_file)


def _read_stored(config_file: Path, stderr_file: TextIO) -> SplitCitiesConfig:
    """Return the stored app config, or a default one when absent.

    Reading the file gives the object whose values seed the edit. When no
    file exists yet the editor simply starts from the class defaults.
    """
    if config_file.exists():
        return SplitCitiesConfig(from_json_filename=config_file,
                                 stderr_file=stderr_file)
    return SplitCitiesConfig(stderr_file=stderr_file)


def _edit_steps(stored: SplitCitiesConfig) -> list[WizardStep]:
    """Return the ordered edit steps, each seeded from the stored config.

    The step functions close over the stored config so each item suggests
    the value already stored for it. Endpoint items also pass the backward
    flag on, so going back into one reopens it at its last question; the
    two single-question items ignore that flag.
    """
    in_cfg = stored.input
    less_cfg = stored.less_than_output
    not_less_cfg = stored.not_less_than_output
    column = stored.split_column
    limit = stored.split_limit

    def edit_input(ui_bridge: WizardUiBridge, results: dict[str, object],
                   backward: bool) -> None:
        results['input'] = _ask_endpoint(INPUT_TITLE, FileAccess.READ,
                                         ui_bridge, default=in_cfg,
                                         backward=backward)

    def edit_column(ui_bridge: WizardUiBridge, results: dict[str, object],
                    _backward: bool) -> None:
        results['split_column'] = _ask_split_column(ui_bridge, default=column)

    def edit_limit(ui_bridge: WizardUiBridge, results: dict[str, object],
                   _backward: bool) -> None:
        results['split_limit'] = _ask_split_limit(ui_bridge, default=limit)

    def edit_less(ui_bridge: WizardUiBridge, results: dict[str, object],
                  backward: bool) -> None:
        results['less'] = _ask_endpoint(LESS_TITLE, FileAccess.CREATE,
                                        ui_bridge, default=less_cfg,
                                        backward=backward)

    def edit_not_less(ui_bridge: WizardUiBridge, results: dict[str, object],
                      backward: bool) -> None:
        results['not_less'] = _ask_endpoint(NOT_LESS_TITLE, FileAccess.CREATE,
                                            ui_bridge, default=not_less_cfg,
                                            backward=backward)

    return [
        (INPUT_TITLE, edit_input),
        ('the split column', edit_column),
        ('the split limit', edit_limit),
        (LESS_TITLE, edit_less),
        (NOT_LESS_TITLE, edit_not_less)]


def main(args: Optional[list[str]] = None) -> int:
    """Parse command line arguments and edit one app config file."""
    parser = argparse.ArgumentParser(
        description='Edit the split-cities app config with wizard defaults.')
    parser.add_argument('--cfg', required=True, type=Path,
                        help='JSON application configuration file to edit.')
    parsed = parser.parse_args(args)
    edit_config_file(config_file=parsed.cfg)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
