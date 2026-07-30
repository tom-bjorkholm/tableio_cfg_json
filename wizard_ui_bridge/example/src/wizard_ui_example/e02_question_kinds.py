#! /usr/bin/env python3
"""Ask export settings one question at a time, using every ask method.

This second teaching example builds on e01_one_question.py. Where e01 asks
only free text, this one uses each of the one-at-a-time ask methods exactly
once to gather a small "export settings" configuration:

- ask_text    the report title (free text, with a default),
- ask_choice  the output format (pick one of a fixed list),
- ask_path    the output file to create (a path question),
- ask_int     an optional row limit (an integer, bounded and nullable),
- ask_yes_no  whether to write a header row (a boolean),
- ask_multi   which columns to export (pick several of a fixed list).

The same "export settings" appear again in e05_ask_form.py, where the whole
set is shown as one form. Reading e02 then e05 is the intended way to see
the difference between asking questions one at a time and asking them all
at once.

The ask methods validate for you
--------------------------------
Each ask method already re-asks on input it can judge on its own:
ask_int rejects non-integers and out-of-range values, ask_choice and
ask_multi reject unknown items, and ask_path rejects a path of the wrong
kind. The program does not loop for those.

re_ask_reason: application-level checks
--------------------------------------
Some rules only the application knows. Here the output file should end with
the extension that matches the chosen format. ask_path cannot know that
rule, so ask_output_path() checks it and, when it fails, calls ask_path()
again with a re_ask_reason that explains why. re_ask_reason is the shared
argument every ask method takes for exactly this: showing why a question is
being asked again.

Note that per-question help text is not a feature of the one-at-a-time ask
methods; it belongs to the form fields shown in e05_ask_form.py.

Cancelling and scripting
-----------------------
Any ask method may raise a WizardNavigation request (``:b``, ``:c`` or
``:q`` on the console). This example treats any of them as "the user gave
up" and stops. Tests force the console bridge and feed answers through a
redirected input stream, so the program is fully scriptable.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence, TextIO

from wizard_ui_bridge import make_text_ui_bridge, UiBridgeType, \
    WizardUiBridge, WizardNavigation, PathAskOptions, WizardPathKind

_FORMATS = ('CSV', 'Excel', 'HTML')
_EXTENSIONS = {'CSV': '.csv', 'Excel': '.xlsx', 'HTML': '.html'}
_COLUMNS = ('City', 'Country', 'Continent', 'Population')
_DEFAULT_COLUMNS = ('City', 'Country', 'Continent')
# The output file must not exist yet, so the export never overwrites a file
# by accident. WizardPathKind carries that rule for the path question.
_NEW_FILE = PathAskOptions(kind=WizardPathKind.NON_EXISTING_FILE)


@dataclass(frozen=True)
class ExportSettings:
    """The answers collected by the export-settings wizard."""

    title: str
    output_format: str
    output_file: Path
    row_limit: Optional[int]
    include_header: bool
    columns: Sequence[str]


def ask_output_path(bridge: WizardUiBridge, output_format: str) -> Path:
    """Ask for the output file, re-asking until the extension matches.

    ask_path() guarantees a new (not yet existing) file, but only the
    application knows that a CSV export should be a ``.csv`` file and so
    on. When the extension does not match, ask_path() is called again with
    a re_ask_reason that explains the mismatch.
    """
    expected = _EXTENSIONS[output_format]
    reason: Optional[str] = None
    while True:
        path = bridge.ask_path('Output file to create', re_ask_reason=reason,
                               options=_NEW_FILE)
        assert path is not None  # a non-existing-file question is not nullable
        if path.suffix.lower() == expected:
            return path
        reason = (f'A {output_format} export should end with "{expected}", '
                  f'not "{path.suffix}".')


def ask_export_settings(bridge: WizardUiBridge) -> Optional[ExportSettings]:
    """Ask the six questions and return the settings, or None if cancelled.

    Like a real wizard this is just a sequence of ask_* calls on the
    bridge, one per kind of question. It never names the console or Textual
    bridge, so it runs unchanged on either.

    This example does not handle any WizardNavigation requests.
    How to handle them is shown in e03 on navigation.
    """
    try:
        title = bridge.ask_text('Report title', default='Cities report')
        output_format = bridge.ask_choice('Output format', choices=_FORMATS,
                                          default='CSV')
        output_file = ask_output_path(bridge, output_format)
        row_limit = bridge.ask_int('Row limit (blank = all rows)',
                                   nullable=True, min_value=1)
        include_header = bridge.ask_yes_no('Include a header row?',
                                           default=True)
        columns = bridge.ask_multi('Columns to export', choices=_COLUMNS,
                                   default=_DEFAULT_COLUMNS, min_select=1)
    except WizardNavigation:
        return None
    assert title is not None  # a default makes an empty answer non-None
    return ExportSettings(title=title, output_format=output_format,
                          output_file=output_file, row_limit=row_limit,
                          include_header=include_header, columns=columns)


def _limit_text(row_limit: Optional[int]) -> str:
    """Return the row-limit answer as display text."""
    return 'all rows' if row_limit is None else str(row_limit)


def _header_text(include_header: bool) -> str:
    """Return the include-header answer as display text."""
    return 'included' if include_header else 'omitted'


def summarize(settings: ExportSettings) -> str:
    """Return a human-readable summary of the collected settings."""
    lines = ['Export settings summary:',
             f'  Report title: {settings.title}',
             f'  Output format: {settings.output_format}',
             f'  Output file: {settings.output_file}',
             f'  Row limit: {_limit_text(settings.row_limit)}',
             f'  Header row: {_header_text(settings.include_header)}',
             f'  Columns: {", ".join(settings.columns)}']
    return '\n'.join(lines)


# The stream defaults, the --ui switch and main() below are the same plumbing
# in every example, so each example stays a complete program a reader can run
# and study on its own. Repeating this ceremony is a deliberate teaching
# choice, so duplicate-code is turned off from here to the end of the file.
# pylint: disable=duplicate-code
def collect_and_summarize(stdin_file: Optional[TextIO] = None,
                          stdout_file: Optional[TextIO] = None,
                          stderr_file: Optional[TextIO] = None,
                          bridge_type: UiBridgeType = UiBridgeType.AUTO
                          ) -> Optional[str]:
    """Ask the export settings and print a summary of the answers.

    Args:
        stdin_file: Optional input stream for tests or scripted use.
        stdout_file: Optional output stream for tests or scripted use.
        stderr_file: Optional diagnostic stream for re-ask messages.
        bridge_type: Which text-mode bridge to build. AUTO selects the
                     Textual bridge in a real terminal and the console
                     bridge otherwise, which is what tests rely on.

    Returns:
        The printed summary text, or None when the user cancelled.
    """
    in_file = sys.stdin if stdin_file is None else stdin_file
    out_file = sys.stdout if stdout_file is None else stdout_file
    err_file = sys.stderr if stderr_file is None else stderr_file
    bridge = make_text_ui_bridge(out_file, in_file, err_file, bridge_type)
    settings = ask_export_settings(bridge)
    if settings is None:
        out_file.write('Export configuration cancelled.\n')
        return None
    summary = summarize(settings)
    out_file.write(summary + '\n')
    return summary


def build_parser() -> argparse.ArgumentParser:
    """Return the argument parser for the question-kinds example."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ui', choices=('auto', 'console', 'textual'),
                        default='auto', help='UI bridge to use.')
    return parser


_UI_TYPES = {'auto': UiBridgeType.AUTO, 'console': UiBridgeType.CONSOLE,
             'textual': UiBridgeType.TEXTUAL}


def main(args: Optional[list[str]] = None) -> int:
    """Parse arguments, ask the export settings and print the summary."""
    parsed = build_parser().parse_args(args)
    collect_and_summarize(bridge_type=_UI_TYPES[parsed.ui])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
