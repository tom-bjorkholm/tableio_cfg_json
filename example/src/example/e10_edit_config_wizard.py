#! /usr/bin/env python3
"""Edit one TableIO JSON config with wizard defaults."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
from pathlib import Path
import sys
from typing import Optional, TextIO

from tableio import FileAccess, access_capabilities
from tableio_cfg_json import TioJsonConfig, WizardAbort, WizardBack, \
    WizardCancelLevel, WizardUiBridge, WizardUiBridgeConsole, \
    tio_json_config_wizard


def edit_config_file(config_file: Path, stdin_file: Optional[TextIO] = None,
                     stdout_file: Optional[TextIO] = None,
                     stderr_file: Optional[TextIO] = None) -> None:
    """Ask questions and write one edited TableIO JSON config.

    Args:
        config_file: JSON file to create or edit.
        stdin_file: Optional input stream for tests or scripted use.
        stdout_file: Optional output stream for tests or scripted use.
        stderr_file: Optional diagnostic stream for validation messages.
    """
    in_file = sys.stdin if stdin_file is None else stdin_file
    out_file = sys.stdout if stdout_file is None else stdout_file
    err_file = sys.stderr if stderr_file is None else stderr_file
    ui_bridge = WizardUiBridgeConsole(out_file, in_file, err_file)
    default = _read_default(config_file, err_file)
    config = _ask_confirmed(ui_bridge, default, err_file)
    if config is not None:
        config.write(to_json_filename=config_file, stderr_file=err_file)


def _read_default(config_file: Path,
                  stderr_file: TextIO) -> Optional[TioJsonConfig]:
    """Read the previous config file when it exists."""
    if not config_file.exists():
        return None
    capabilities = access_capabilities(FileAccess.CREATE,
                                       error_file=stderr_file)
    # The object read here is passed as ``default`` to the wizard. That means
    # every stored value becomes the value shown in the matching wizard
    # question. The user can press Enter to keep it instead of typing it again.
    return TioJsonConfig(capabilities, FileAccess.CREATE,
                         from_json_filename=config_file,
                         stderr_file=stderr_file)


def _ask_confirmed(ui_bridge: WizardUiBridge, default: Optional[TioJsonConfig],
                   stderr_file: TextIO) -> Optional[TioJsonConfig]:
    """Ask for a config until the enclosing confirmation accepts it."""
    current = default
    backward = False
    while True:
        try:
            current = _ask_config(ui_bridge, current, backward, stderr_file)
        except WizardBack:
            ui_bridge.show('Already at the first TableIO question.')
            backward = False
            continue
        except WizardCancelLevel:
            ui_bridge.show('Restarting the TableIO configuration.')
            backward = False
            continue
        except WizardAbort:
            ui_bridge.show('Configuration abandoned; no file written.')
            return None
        try:
            if ui_bridge.ask_yes_no('Is this configuration OK for you?',
                                    default=True):
                return current
        except WizardBack:
            ui_bridge.show('Going back into the TableIO configuration.')
            backward = True
            continue
        except WizardCancelLevel:
            ui_bridge.show('Going back into the TableIO configuration.')
            backward = True
            continue
        except WizardAbort:
            ui_bridge.show('Configuration abandoned; no file written.')
            return None
        # This is the enclosing wizard use case: the confirmation question is
        # outside tio_json_config_wizard(). When the user answers "no", the
        # application calls the TableIO wizard again with the config it just
        # returned as ``default``. Passing ``backward=True`` starts at the last
        # TableIO question, so the user can walk back from there if needed.
        ui_bridge.show('Going back into the TableIO configuration.')
        backward = True


def _ask_config(ui_bridge: WizardUiBridge, default: Optional[TioJsonConfig],
                backward: bool, stderr_file: TextIO) -> TioJsonConfig:
    """Ask the TableIO wizard for one write-capable endpoint config."""
    capabilities = access_capabilities(FileAccess.CREATE,
                                       error_file=stderr_file)
    # FileAccess.CREATE means this example edits the configuration for a file
    # the application will write. A read-side editor would use FileAccess.READ
    # and otherwise keep the same default/backward pattern.
    return tio_json_config_wizard(capabilities, FileAccess.CREATE, ui_bridge,
                                  default=default, backward=backward)


def main(args: Optional[list[str]] = None) -> int:
    """Parse command line arguments and edit one config file."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cfg', required=True, type=Path,
                        help='JSON TableIO configuration file to edit.')
    parsed = parser.parse_args(args)
    edit_config_file(config_file=parsed.cfg)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
