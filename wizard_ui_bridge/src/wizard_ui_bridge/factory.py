#! /usr/local/bin/python3
"""Factory selecting a text-mode user interface bridge.

The wizard talks to the user through a WizardUiBridge. This factory
returns a Textual full-screen bridge when Textual is installed and the
streams are a real terminal, and falls back to the console bridge
otherwise, such as when output is redirected, when running under tests,
or where Textual is not available. The fallback keeps the library
importable and usable even if Textual has been uninstalled.

Textual is an optional dependency, installed with the extra
`wizard-ui-bridge[textual]`. The Textual bridge is therefore imported
only when it is about to be used, and asking for it without Textual
installed raises ImportError instead of degrading silently.

This factory chooses between text-mode bridges only. An application
with a graphical user interface should provide and use its own
graphical bridge instead.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from enum import Enum, auto
from importlib.util import find_spec
from typing import TextIO
from wizard_ui_bridge.bridge import WizardUiBridge
from wizard_ui_bridge.console import WizardUiBridgeConsole

TEXTUAL_MISSING = (
    'The Textual wizard UI bridge needs the textual package, which is '
    'not installed. Install it with: pip install wizard-ui-bridge[textual]')


def textual_installed() -> bool:
    """Return whether the optional textual package is installed."""
    return find_spec('textual') is not None


def load_textual_bridge() -> type[WizardUiBridge]:
    """Return the Textual bridge class, importing it on demand.

    Textual is only imported here, so that a program that never asks
    for the Textual bridge never pays for importing Textual. The
    availability check keeps the missing-package case a clear
    ImportError, while any other import error in the Textual bridge
    itself is still reported as the error it is.

    Raises:
        ImportError: If the optional textual package is not installed.
    """
    if not textual_installed():
        raise ImportError(TEXTUAL_MISSING)
    # pylint: disable-next=import-outside-toplevel
    from wizard_ui_bridge.textual_bridge import WizardUiBridgeTextual
    return WizardUiBridgeTextual


class UiBridgeType(Enum):
    """Type of wizard user interface bridge.

    AUTO: Auto-select the best bridge based on the environment.
          This will use Textual if it is installed and the streams
          are a terminal, else a console bridge.
    TEXTUAL: Use the Textual bridge, even if it might fail.
    CONSOLE: Use the console bridge, even if Textual could be used.
    """

    AUTO = auto()
    TEXTUAL = auto()
    CONSOLE = auto()


def make_text_ui_bridge(stdout_file: TextIO, stdin_file: TextIO,
                        stderr_file: TextIO,
                        bridge_type: UiBridgeType = UiBridgeType.AUTO) \
        -> WizardUiBridge:
    """Return a Textual bridge for a terminal, else a console bridge.

    Args:
        stdout_file: Stream the console bridge prints to, also checked
                     for being a terminal.
        stdin_file: Stream the console bridge reads from, also checked
                    for being a terminal.
        stderr_file: Stream the console bridge prints errors to.
        bridge_type: Type of bridge to use. Defaults to AUTO.
                     If AUTO, select the best bridge based on the environment.
                     If TEXTUAL, use the Textual bridge that might fail.
                     If CONSOLE, use the console bridge.

    Raises:
        ImportError: If TEXTUAL is asked for but textual is not installed.

    Returns:
        A Textual bridge when Textual is installed and both streams are
        a terminal, otherwise a console bridge.
    """
    if bridge_type == UiBridgeType.TEXTUAL:
        return load_textual_bridge()()
    if bridge_type == UiBridgeType.CONSOLE:
        return WizardUiBridgeConsole(stdout_file, stdin_file, stderr_file)
    if textual_installed() and _is_tty(stdin_file) and _is_tty(stdout_file):
        return load_textual_bridge()()
    return WizardUiBridgeConsole(stdout_file, stdin_file, stderr_file)


def _is_tty(stream: TextIO) -> bool:
    """Return whether a stream reports that it is a terminal."""
    return stream.isatty()
