#! /usr/bin/env python3
"""Edit a stored split-cities app config in the wizard.

This builds on e07_config_wizard. That example created a fresh
SplitCitiesConfig; this one reopens a stored config and re-asks the same
wizard items, but seeds each one with the value already stored so pressing
Enter keeps it. (Editing the whole file at once in a folding config editor
is a different thing, and is shown by e11_config_editor.) Three related
ideas are shown:

- Reading a stored file that lacks values. The file is read with
  ok_to_use_defaults=True, so a file that a user trimmed by hand still
  opens. Each value it lacks keeps its default, and
  Config.kept_value_paths() tells which ones those are, so the user can be
  told before the wizard starts. This is not how a file written by an
  older version of the program is read: that is what the "Read Old
  Configuration File" (ROCF) rules of config-as-json are for.
- Editing in the wizard with defaults. The stored config is passed to
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
exactly as in e07, so the wizard is full-screen in a terminal when
Textual is installed, and scriptable with redirected streams.
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


def edit_in_wizard(config_file: Path, stdin_file: Optional[TextIO] = None,
                   stdout_file: Optional[TextIO] = None,
                   stderr_file: Optional[TextIO] = None) -> None:
    """Reopen a stored app config, edit it in the wizard, and write it back.

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
    _show_kept(stored, ui_bridge)
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
    file exists yet the wizard simply starts from the class defaults.
    """
    if not config_file.exists():
        return SplitCitiesConfig(stderr_file=stderr_file)
    # Without ok_to_use_defaults=True a file lacking split_limit, or an
    # endpoint lacking format_name, is refused with ConfigMissingKey. With
    # it, a missing value keeps its default instead: the default that
    # SplitCitiesConfig.__init__ assigns for its own members, and the
    # default TableIO recommends for the format of an endpoint. Values that
    # are present are still validated as strictly as ever.
    #
    # Use this for a file of the current format that simply leaves values
    # out, not for a file written by an older version of the program. An
    # older format is read with the ROCF rules of config-as-json (see its
    # examples e31 and e37), which migrate renamed, moved and removed keys
    # and report every change. ok_to_use_defaults would only hide them.
    return SplitCitiesConfig(from_json_filename=config_file,
                             stderr_file=stderr_file, ok_to_use_defaults=True)


def _show_kept(stored: SplitCitiesConfig, ui_bridge: WizardUiBridge) -> None:
    """Tell the user which values the stored file did not hold.

    The wizard suggests the default for each of them, so pressing Enter
    stores a value the file never had. Saying so first keeps that from
    being a surprise.
    """
    # kept_value_paths() returns one JsonPath tuple per value that the file
    # lacked, such as ('split_limit',) or ('input', 'format_name') for a
    # value inside a nested endpoint. When a whole member is missing only
    # that member is named, not every value inside it. The order of the
    # list is not guaranteed, so it is sorted for a stable message.
    names = sorted('.'.join(str(part) for part in path)
                   for path in stored.kept_value_paths())
    if names:
        ui_bridge.show('The stored file does not hold ' + ', '.join(names)
                       + '. The wizard suggests the default for each.')


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
        description='Edit the split-cities app config in the wizard.')
    parser.add_argument('--cfg', required=True, type=Path,
                        help='JSON application configuration file to edit.')
    parsed = parser.parse_args(args)
    edit_in_wizard(config_file=parsed.cfg)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
