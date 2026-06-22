#! /usr/local/bin/python3
"""Factory selecting a text-mode user interface bridge.

The wizard talks to the user through a WizardUiBridge. This factory
returns a Textual full-screen bridge when Textual is installed and the
streams are a real terminal, and falls back to the console bridge
otherwise, such as when output is redirected, when running under tests,
or where Textual is not available. The fallback keeps the library
importable and usable even if Textual has been uninstalled.

This factory chooses between text-mode bridges only. An application
with a graphical user interface should provide and use its own
graphical bridge instead.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional, TextIO
from enum import Enum, auto
from tableio_cfg_json.wizard_ui_bridge import WizardUiBridge
from tableio_cfg_json.wizard_ui_bridge_console import WizardUiBridgeConsole
try:
    from tableio_cfg_json.wizard_ui_bridge_textual import \
        WizardUiBridgeTextual
    _TEXTUAL: Optional[type[WizardUiBridgeTextual]] = WizardUiBridgeTextual
except ImportError:
    _TEXTUAL = None


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
        RuntimeError: If Textual is selected but Textual bridge is not
                      installed.

    Returns:
        A Textual bridge when Textual is installed and both streams are
        a terminal, otherwise a console bridge.
    """
    if bridge_type == UiBridgeType.TEXTUAL:
        if _TEXTUAL is None:
            raise RuntimeError("Textual bridge is not installed")
        return _TEXTUAL()
    if bridge_type == UiBridgeType.CONSOLE:
        return WizardUiBridgeConsole(stdout_file, stdin_file, stderr_file)
    if _TEXTUAL is not None and _is_tty(stdin_file) and _is_tty(stdout_file):
        return _TEXTUAL()
    return WizardUiBridgeConsole(stdout_file, stdin_file, stderr_file)


def _is_tty(stream: TextIO) -> bool:
    """Return whether a stream reports that it is a terminal."""
    return stream.isatty()
