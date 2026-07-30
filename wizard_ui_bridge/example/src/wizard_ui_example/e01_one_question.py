#! /usr/bin/env python3
"""Ask a few free-text questions through a WizardUiBridge.

This is the first teaching example: the smallest useful program that talks
to a user through the bridge. It asks for a name, an optional nickname and
a secret code, then greets the user. Nothing is written to disk.

What a bridge is
----------------
A wizard is any code that asks a user a series of questions. A
WizardUiBridge is the user-interface-independent object the wizard asks
them through. The very same wizard code can then run on a plain console,
on a full-screen Textual interface, or on any other bridge an application
provides. (The tableio-cfg-json package is one such application; this
example needs nothing from it.)

Getting a bridge
----------------
make_text_ui_bridge(out, in_, err, kind) returns a ready-to-use text-mode
bridge:

- UiBridgeType.AUTO builds the Textual full-screen bridge when Textual is
  installed and the streams are a real terminal, and the plain console
  bridge otherwise. textual_installed() reports whether the optional
  ``wizard-ui-bridge[textual]`` extra is available, which is exactly what
  AUTO checks first.
- UiBridgeType.CONSOLE and UiBridgeType.TEXTUAL force one bridge. Tests
  force CONSOLE so the program is fully scriptable through redirected
  streams.

Asking one question
-------------------
ask_text() asks for one line of free text and returns it as a str (or
None). Three of its options appear here:

- default: an empty answer returns the default instead of an empty string.
- nullable: an empty answer with no default returns None, so the caller
  can tell "left blank" apart from a real value.
- sensitive: the bridge must not echo the text (a password field, or
  getpass on a real console). No default is allowed together with it.

show() and error_file()
-----------------------
show() presents a message to the user. On the console it prints at once,
but on a graphical or full-screen textual bridge show() only *buffers* the
message for the next question's screen, so a message with no question after
it is never seen. This example therefore ends with a short acknowledgement
question, so the greeting stays on screen until the user has read it. A GUI
(for example Tkinter) bridge needs the same following question.

error_file() returns the stream for side notes and diagnostics, kept apart
from the primary output; on the console bridge it is stderr.

Cancelling
----------
Any ask method may raise a WizardNavigation request instead of returning,
when the user asks to go back, cancel or abort (``:b``, ``:c`` or ``:q``
on the console). A single question has nowhere to go back to, so this
example treats every such request as "the user gave up".
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
import sys
from typing import Optional, TextIO

from wizard_ui_bridge import make_text_ui_bridge, UiBridgeType, \
    WizardUiBridge, WizardNavigation, textual_installed


def ui_note(bridge_type: UiBridgeType) -> str:
    """Return a short note about which text UI will be used.

    This is where textual_installed() is used: it lets a program tell the
    user in advance whether the full-screen Textual interface is available
    or the plain console will be used instead.
    """
    if bridge_type == UiBridgeType.CONSOLE:
        return 'Using the console bridge.'
    if not textual_installed():
        return ('Textual is not installed (extra "wizard-ui-bridge'
                '[textual]"); using the console bridge.')
    return 'Textual is available; a real terminal shows a full screen.'


def ask_greeting(bridge: WizardUiBridge) -> Optional[str]:
    """Ask the three questions and return a greeting, or None if cancelled.

    This is the part a real wizard is made of: a sequence of ask_* calls on
    the bridge. It never mentions the console or Textual, so it runs
    unchanged on either.
    """
    try:
        name = bridge.ask_text('What is your name?', default='World')
        nickname = bridge.ask_text('Any nickname? (optional)', nullable=True)
        code = bridge.ask_text('Enter a secret access code:', sensitive=True)
    except WizardNavigation:
        return None
    assert name is not None  # a default makes an empty answer non-None
    return _greeting(bridge, name, nickname, code)


def _greeting(bridge: WizardUiBridge, name: str, nickname: Optional[str],
              code: Optional[str]) -> str:
    """Build the greeting, noting an omitted nickname via error_file().

    When the optional nickname is left blank ask_text() returns None. That
    is a good moment to show how error_file() carries a side note that is
    not part of the primary output.
    """
    if nickname is None:
        bridge.error_file().write('No nickname given; using your name.\n')
        nickname = name
    length = 0 if code is None else len(code)
    return (f'Hello, {name}, also known as {nickname}!\n'
            f'Your access code has {length} character(s); '
            'it was never echoed.')


def present_result(bridge: WizardUiBridge, message: str) -> None:
    """Show a final message and keep it on screen until acknowledged.

    show() only buffers a message for the next question's screen on a
    graphical or textual bridge, so a final message needs a question after
    it to be seen at all. One acknowledgement question keeps the message on
    screen until the user submits; on the console show() prints at once and
    the question then waits for Enter. A GUI (for example Tkinter) bridge
    needs the same following question.
    """
    bridge.show(message)
    try:
        bridge.ask_text('Press Enter to finish.', nullable=True)
    except WizardNavigation:
        pass  # the user closed the wizard; the message was already shown


# The stream defaults, the --ui switch and main() below are the same plumbing
# in every example, so each example stays a complete program a reader can run
# and study on its own. Repeating this ceremony is a deliberate teaching
# choice, so duplicate-code is turned off from here to the end of the file.
# pylint: disable=duplicate-code
def collect_greeting(stdin_file: Optional[TextIO] = None,
                     stdout_file: Optional[TextIO] = None,
                     stderr_file: Optional[TextIO] = None,
                     bridge_type: UiBridgeType = UiBridgeType.AUTO
                     ) -> Optional[str]:
    """Build a bridge, ask the questions and show the greeting.

    Args:
        stdin_file: Optional input stream for tests or scripted use.
        stdout_file: Optional output stream for tests or scripted use.
        stderr_file: Optional diagnostic stream for side notes.
        bridge_type: Which text-mode bridge to build. AUTO selects the
                     Textual bridge in a real terminal and the console
                     bridge otherwise, which is what tests rely on.

    Returns:
        The greeting shown to the user, or None when the user cancelled.
    """
    in_file = sys.stdin if stdin_file is None else stdin_file
    out_file = sys.stdout if stdout_file is None else stdout_file
    err_file = sys.stderr if stderr_file is None else stderr_file
    bridge = make_text_ui_bridge(out_file, in_file, err_file, bridge_type)
    err_file.write(ui_note(bridge_type) + '\n')
    greeting = ask_greeting(bridge)
    if greeting is None:
        # No trailing question here: the user asked to quit, so on a
        # graphical bridge the closed wizard is answer enough.
        bridge.show('No greeting made; you cancelled.')
        return None
    present_result(bridge, greeting)
    return greeting


def build_parser() -> argparse.ArgumentParser:
    """Return the argument parser for the one-question example."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ui', choices=('auto', 'console', 'textual'),
                        default='auto', help='UI bridge to use.')
    return parser


_UI_TYPES = {'auto': UiBridgeType.AUTO, 'console': UiBridgeType.CONSOLE,
             'textual': UiBridgeType.TEXTUAL}


def main(args: Optional[list[str]] = None) -> int:
    """Parse arguments, ask the questions and show the greeting."""
    parsed = build_parser().parse_args(args)
    collect_greeting(bridge_type=_UI_TYPES[parsed.ui])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
