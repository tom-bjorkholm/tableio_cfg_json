#! /usr/bin/env python3
"""Create split-cities config files with an automatic text-mode UI.

This example does exactly what e05_split_cities_wizard.py does, but it
does not hard-code the console bridge. Instead it asks the library
helper make_text_ui_bridge() for the best available text-mode bridge:

- In a real terminal it returns WizardUiBridgeTextual, a full-screen
  Textual interface with selectable lists and editable tables.
- When the streams are not a terminal, for instance when input is piped
  or redirected (as the automated tests do), it returns the console
  bridge instead.

Because the choice is made at run time, the very same program gives an
interactive user a rich full-screen experience while still being fully
scriptable for tests and pipelines.

Everything else is reused unchanged from e05. The shared work of asking
the questions, building the config and writing the files lives in
e05._write_split_files, and the shared command line lives in
e05.run_split_cli. This file therefore imports both and adds only what
actually differs: the one line that builds the bridge. Compare the body
of create_split_config_files here with the one in e05 to see that the
sole difference is make_text_ui_bridge() in place of the console bridge.

The teaching point is narrow on purpose: a program that already drives
the wizard through a WizardUiBridge can move from a console interface to
a full-screen terminal interface by changing how it builds the bridge,
and nothing else.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import sys
from typing import Optional, TextIO

# make_text_ui_bridge() is the only new import compared with e05. It is a
# small factory: given the three standard streams it returns the Textual
# bridge when the program runs in a terminal, and the console bridge when
# it does not. The wizard does not care which concrete bridge it gets,
# because both are WizardUiBridge subclasses with the same methods.
from tableio_cfg_json import make_text_ui_bridge

# These are reused unchanged from e05, so this example does not repeat
# them:
#   _write_split_files(bridge, cfg, txt, err) asks the questions, builds
#       the config and writes both files; it does not depend on which
#       bridge it is given.
#   run_split_cli(create_files, description, args) provides the shared
#       --cfg/--txt command line.
from example.e05_split_cities_wizard import _write_split_files, run_split_cli

# The program description is the only command-line difference from e05.
_DESCRIPTION = 'Create split-cities config files using a text UI.'


def create_split_config_files(config_file: Path, syntax_file: Path,
                              stdin_file: Optional[TextIO] = None,
                              stdout_file: Optional[TextIO] = None,
                              stderr_file: Optional[TextIO] = None) -> None:
    """Ask questions and write a split-cities JSON config and guide.

    This mirrors e05_split_cities_wizard.create_split_config_files, but
    builds the bridge with make_text_ui_bridge(). In a real terminal that
    returns the Textual full-screen bridge; with redirected streams, as
    in the tests, it returns the console bridge, so the behaviour and the
    written files are identical to e05.

    Args:
        config_file: JSON application configuration file to write.
        syntax_file: Plain text guide for later hand-editing.
        stdin_file: Optional input stream for tests or scripted use.
        stdout_file: Optional output stream for tests or scripted use.
        stderr_file: Optional diagnostic stream for TableIO/config errors.
    """
    # The streams default to the real standard streams. Tests pass their
    # own in-memory streams instead, exactly as they do for e05. Because
    # in-memory streams report that they are not a terminal, the factory
    # below then chooses the console bridge, which keeps the example
    # scriptable.
    in_file = sys.stdin if stdin_file is None else stdin_file
    out_file = sys.stdout if stdout_file is None else stdout_file
    err_file = sys.stderr if stderr_file is None else stderr_file
    # This single line is the whole difference from e05. e05 builds
    # WizardUiBridgeConsole(out_file, in_file, err_file) here; this file
    # lets the factory pick the Textual bridge or the console bridge.
    ui_bridge = make_text_ui_bridge(out_file, in_file, err_file)
    # Everything after the bridge is identical to e05, so it is reused
    # rather than repeated.
    _write_split_files(ui_bridge, config_file, syntax_file, err_file)


# ---------------------------------------------------------------------------
# Only command line handling below this line. The shared runner lives in
# e05; this module only supplies its own program description.


def main(args: Optional[list[str]] = None) -> int:
    """Parse command line arguments and create split-cities config files.

    Run this module in a terminal to see the Textual interface; redirect
    its input to see the same wizard fall back to the console bridge.
    """
    return run_split_cli(create_split_config_files, _DESCRIPTION, args)


if __name__ == '__main__':
    sys.exit(main())
