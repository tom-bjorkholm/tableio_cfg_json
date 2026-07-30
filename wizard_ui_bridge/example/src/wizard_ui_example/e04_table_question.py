#! /usr/bin/env python3
"""Ask the user to edit tables with ask_table.

This fourth teaching example builds on e02_question_kinds.py. It asks two
table questions: first a table with a fixed number of rows, then a table
whose rows the user can add and remove.

Describing a table
------------------
A table question is described by two things:

- one TableColumn per column, giving the column header and whether the
  whole column is read-only (fixed text the user cannot edit), and
- a grid of TableCell objects, one per column in each starting row, giving
  each cell's initial value and its value constraints (a finite set of
  choices, and whether an empty cell is allowed).

ask_table() shows the table, lets the user edit the editable cells, and
returns the whole table as rows of strings (or None for an empty cell),
including the read-only columns.

Fixed rows: renaming columns
----------------------------
The first table reviews a fixed set of source columns. Its first column is
read-only (the original name); the second is free text (the new name); the
third is a per-row choice (the data type), which shows how a TableCell can
carry its own set of choices.

Variable rows: a guest list
---------------------------
The second table starts from a couple of example guests and lets the user
add rows (``:+`` on the console, an Add-row button in a graphical bridge)
and remove them (``:- N`` on the console), within a minimum and maximum row
count.

Early feedback vs final verification
-----------------------------------
The variable table passes a PartialCheck. It is meant as *advisory* early
feedback: a graphical or Textual bridge shows the message beside the cell
as the user types, without blocking. A console has nowhere to show an
unobtrusive inline hint, so in practice the console bridge re-asks the cell
until the check passes. Either way the wizard must not trust the bridge to
enforce anything: a bridge may skip the check entirely, so after
ask_table() returns the wizard verifies the whole table itself and, if
something is wrong, calls ask_table() again with a re_ask_reason.
ask_guest_list() shows exactly this loop; it also enforces a rule a
per-cell check cannot see: that the guest names are unique.

Navigation and scripting
------------------------
Editing a table also honors the navigation requests covered in
e03_navigation.py; this example simply treats any request that propagates
out of a table as "cancelled". Tests force the console bridge and script
the cell answers and row actions through a redirected input stream.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
import sys
from dataclasses import dataclass
from typing import Optional, TextIO

from wizard_ui_bridge import make_text_ui_bridge, UiBridgeType, \
    WizardUiBridge, WizardNavigation, TableColumn, TableCell

_SOURCE_COLUMNS = (('city', 'text'), ('population', 'number'),
                   ('founded', 'date'))
_DATA_TYPES = ('text', 'number', 'date')
RENAME_COLUMNS = (TableColumn('Source column', read_only=True),
                  TableColumn('Rename to'), TableColumn('Data type'))
_RENAME_Q = 'Review the columns. Rename any column and set its data type.'
GUEST_COLUMNS = (TableColumn('Guest'), TableColumn('Seats'))
_GUEST_Q = 'Edit the guest list. Add or remove rows as needed.'
_INITIAL_GUESTS = (('Alex', '2'), ('Bo', '3'))
_MAX_SEATS = 10
_MIN_GUESTS = 1
_MAX_GUESTS = 5
_NAME_COL = 0
_SEATS_COL = 1


@dataclass(frozen=True)
class RenameRule:
    """One column's new name and chosen data type."""

    source: str
    new_name: str
    data_type: str


@dataclass(frozen=True)
class Guest:
    """One guest and the number of seats reserved for them."""

    name: str
    seats: int


def _text(value: Optional[str]) -> str:
    """Return a cell value as text, treating an empty cell as ''."""
    return '' if value is None else value


def _int_or_none(value: Optional[str]) -> Optional[int]:
    """Return value parsed as an integer, or None when it is not one."""
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def build_rename_cells() -> list[list[TableCell]]:
    """Return the starting rows for the column-rename table.

    Each row has a read-only source-name cell, a free-text new-name cell
    prefilled with the source name, and a choice cell prefilled with the
    column's data type. The choice cell shows how one TableCell carries its
    own set of accepted values.
    """
    return [[TableCell(value=name), TableCell(value=name),
             TableCell(value=dtype, choices=_DATA_TYPES)]
            for name, dtype in _SOURCE_COLUMNS]


def ask_rename_rules(bridge: WizardUiBridge) -> list[RenameRule]:
    """Ask the fixed-row rename table and return one rule per row."""
    table = bridge.ask_table(RENAME_COLUMNS, build_rename_cells(), _RENAME_Q)
    return [RenameRule(_text(row[0]), _text(row[1]), _text(row[2]))
            for row in table]


def build_guest_cells() -> list[list[TableCell]]:
    """Return the starting rows for the guest-list table."""
    return [[TableCell(value=name), TableCell(value=seats)]
            for name, seats in _INITIAL_GUESTS]


def guest_check(table: list[list[Optional[str]]],
                position: tuple[int, int]) -> tuple[bool, str]:
    """Give per-cell feedback while the guest table is edited.

    This is a PartialCheck: it sees the whole table and the changed
    (row, column) position, and returns whether the cell is acceptable
    together with a message. It checks only the one changed cell, because
    it runs while the table is still being filled.
    """
    value = table[position[0]][position[1]]
    if position[1] == _NAME_COL:
        return _check_name(value)
    return _check_seats(value)


def _check_name(value: Optional[str]) -> tuple[bool, str]:
    """Accept a non-empty guest name."""
    if value is None or value.strip() == '':
        return (False, 'Please enter a guest name.')
    return (True, '')


def _check_seats(value: Optional[str]) -> tuple[bool, str]:
    """Accept a seat count that is a whole number in range."""
    seats = _int_or_none(value)
    if seats is None or not 1 <= seats <= _MAX_SEATS:
        return (False, f'Seats must be a whole number 1-{_MAX_SEATS}.')
    return (True, '')


def ask_guest_list(bridge: WizardUiBridge) -> list[Guest]:
    """Ask the variable-row guest table, verifying the final table.

    ask_table() is asked with a PartialCheck for early feedback, but the
    wizard cannot trust a bridge to have enforced it, so _guest_error()
    verifies the whole returned table. When it finds a problem the table is
    asked again with the reason and the user's current rows, so no work is
    lost. The uniqueness rule is only checked here, because a per-cell
    check cannot compare rows.
    """
    cells = build_guest_cells()
    reason: Optional[str] = None
    while True:
        table = bridge.ask_table(GUEST_COLUMNS, cells, _GUEST_Q,
                                 re_ask_reason=reason,
                                 partial_check=guest_check,
                                 min_rows=_MIN_GUESTS, max_rows=_MAX_GUESTS)
        reason = _guest_error(table)
        if reason is None:
            return [_to_guest(row) for row in table]
        cells = _cells_from_table(table)


def _guest_error(table: list[list[Optional[str]]]) -> Optional[str]:
    """Return the first problem with the whole guest table, or None."""
    for row in table:
        for accepted, message in (_check_name(row[_NAME_COL]),
                                  _check_seats(row[_SEATS_COL])):
            if not accepted:
                return message
    names = [_text(row[_NAME_COL]) for row in table]
    if len(set(names)) != len(names):
        return 'Two guests share a name; please make them unique.'
    return None


def _to_guest(row: list[Optional[str]]) -> Guest:
    """Build a Guest from a row the final verification accepted."""
    seats = _int_or_none(row[_SEATS_COL])
    assert seats is not None  # the final verification accepted this row
    return Guest(_text(row[_NAME_COL]), seats)


def _cells_from_table(table: list[list[Optional[str]]]
                      ) -> list[list[TableCell]]:
    """Rebuild editable starting cells from the rows the user left.

    Passing these back to ask_table() on a re-ask keeps the user's edits,
    so a rejected table is corrected rather than retyped.
    """
    return [[TableCell(value=_text(row[_NAME_COL])),
             TableCell(value=_text(row[_SEATS_COL]))] for row in table]


def summarize(rules: list[RenameRule], guests: list[Guest]) -> str:
    """Return a human-readable summary of both edited tables."""
    lines = ['Column rename rules:']
    lines += [f'  {rule.source} -> {rule.new_name} ({rule.data_type})'
              for rule in rules]
    lines.append('Guest list:')
    lines += [f'  {guest.name}: {guest.seats} seat(s)' for guest in guests]
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
    """Ask both table questions and print a summary of the answers.

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
    try:
        rules = ask_rename_rules(bridge)
        guests = ask_guest_list(bridge)
    except WizardNavigation:
        out_file.write('Table editing cancelled.\n')
        return None
    summary = summarize(rules, guests)
    out_file.write(summary + '\n')
    return summary


def build_parser() -> argparse.ArgumentParser:
    """Return the argument parser for the table-question example."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ui', choices=('auto', 'console', 'textual'),
                        default='auto', help='UI bridge to use.')
    return parser


_UI_TYPES = {'auto': UiBridgeType.AUTO, 'console': UiBridgeType.CONSOLE,
             'textual': UiBridgeType.TEXTUAL}


def main(args: Optional[list[str]] = None) -> int:
    """Parse arguments, ask the table questions and print the summary."""
    parsed = build_parser().parse_args(args)
    collect_and_summarize(bridge_type=_UI_TYPES[parsed.ui])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
