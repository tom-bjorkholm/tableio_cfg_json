#! /usr/bin/env python3
"""Let the user move around a multi-step wizard with navigation.

This third teaching example builds on e02_question_kinds.py. Where e01 and
e02 only move forward, this one lets the user step back, cancel a nested
section or abandon everything, by catching the navigation requests a bridge
raises.

The account-setup wizard
------------------------
The wizard collects an account: a username, an email address, an account
type and a password. Choosing the "Organization" account type opens a
*nested level* of extra questions (the organization name and its number of
members). That nested level is what makes the difference between the two
"go somewhere" requests visible.

The three navigation requests
-----------------------------
Any ask method may raise a WizardNavigation subclass instead of returning:

- WizardBack (``:b`` on the console) steps to the previous question. At the
  first question of a level there is no earlier question in that level, so
  it is left to the enclosing level.
- WizardCancelLevel (``:c`` on the console) leaves the whole current level
  and returns to the question that opened it, however deep in the level the
  user is. Here it leaves the organization sub-section and re-asks the
  account type. The level's answers are not thrown away: like every other
  answer they are kept and offered again as defaults if the level is
  re-entered, unless a changed outer answer has made them invalid.
- WizardAbort (``:q`` on the console) abandons the whole wizard.

The driver pattern
------------------
drive_level() is the small reusable driver a wizard author writes around
the ask methods. It walks a list of step functions, stepping back on
WizardBack. A nested level runs the same driver; it re-raises a WizardBack
from its first question and any WizardCancelLevel, so the driver that opened
it (ask_account_details) can re-ask the opening question. WizardAbort is
never caught by a level; it propagates out so run_account_setup can stop.

Answers become the new default
------------------------------
Whenever the user returns to a question, the answer given earlier is offered
as its default, so pressing enter keeps it. This example does that by
keeping every answer in a draft object and passing the stored value back as
the ask method's default. The password is the one exception: a sensitive
question cannot carry a default, so it is entered again on return.

Cancelling and scripting
-----------------------
Tests force the console bridge and feed the navigation tokens (``:b``,
``:c``, ``:q``) through a redirected input stream, so the whole flow is
fully scriptable.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
import sys
from dataclasses import dataclass, field
from typing import Callable, Optional, Sequence, TextIO, TypeVar

from wizard_ui_bridge import make_text_ui_bridge, UiBridgeType, \
    WizardUiBridge, WizardBack, WizardCancelLevel, WizardAbort

_PERSONAL = 'Personal'
_ORGANIZATION = 'Organization'
_ACCOUNT_TYPES = (_PERSONAL, _ORGANIZATION)
_DEFAULT_USER = 'guest'
_DEFAULT_EMAIL = 'guest@example.com'
_DEFAULT_ORG = 'Acme Inc'
_AT_FIRST = 'Already at the first question; nothing to go back to.'
_NO_OUTER = 'This is the top level; there is nothing to cancel out to.'


@dataclass
class OrgDraft:
    """Mutable organization answers, kept so a return remembers them."""

    name: Optional[str] = None
    members: Optional[int] = None


@dataclass
class AccountDraft:
    """Mutable account answers gathered as the wizard runs.

    Every answer is stored here as soon as it is given, so a question
    revisited through navigation can offer the earlier answer as its
    default. The organization answers live in a nested OrgDraft that is
    kept even for a personal account, so switching back to an organization
    account remembers them.
    """

    username: Optional[str] = None
    email: Optional[str] = None
    account_type: Optional[str] = None
    password: Optional[str] = None
    org: OrgDraft = field(default_factory=OrgDraft)


_Draft = TypeVar('_Draft')


def drive_level(bridge: WizardUiBridge,
                steps: Sequence[Callable[[WizardUiBridge, _Draft], None]],
                draft: _Draft, is_top: bool) -> None:
    """Run one level's steps, honoring back and cancel navigation.

    The steps are asked in order. WizardBack steps to the previous step.
    WizardCancelLevel leaves this level: an inner level re-raises it so the
    driver that opened the level can re-ask the opening question, while the
    top level has no outer level and re-asks the current step with a note.
    WizardAbort is never caught here; it propagates out to abandon the
    whole wizard.
    """
    position = 0
    while position < len(steps):
        try:
            steps[position](bridge, draft)
            position += 1
        except WizardBack:
            if position == 0 and not is_top:
                raise  # first step of a nested level: the outer level handles
            position = _prev_step(bridge, position)
        except WizardCancelLevel:
            if not is_top:
                raise  # the driver that opened this level re-asks its opener
            bridge.show(_NO_OUTER)


def _prev_step(bridge: WizardUiBridge, position: int) -> int:
    """Return the previous step index, re-asking the top's first step.

    This is only reached when there is somewhere to go: a later step, or
    the top level's first step, which simply re-asks itself with a note.
    """
    if position > 0:
        return position - 1
    bridge.show(_AT_FIRST)
    return 0


def ask_org_name(bridge: WizardUiBridge, org: OrgDraft) -> None:
    """Ask the organization name, defaulting to the earlier answer."""
    org.name = bridge.ask_text('Organization name',
                               default=org.name or _DEFAULT_ORG)


def ask_org_members(bridge: WizardUiBridge, org: OrgDraft) -> None:
    """Ask the member count, defaulting to the earlier answer."""
    org.members = bridge.ask_int('Number of members', min_value=1,
                                 default=org.members or 1)


ORG_STEPS: list[Callable[[WizardUiBridge, OrgDraft], None]] = [
    ask_org_name, ask_org_members]


def run_org_section(bridge: WizardUiBridge, draft: AccountDraft) -> None:
    """Ask the organization sub-level questions into the account draft.

    This is a nested wizard level, driven by the same drive_level() as the
    top level but with is_top False, so a WizardBack from its first question
    and any WizardCancelLevel are re-raised for ask_account_details to
    handle.
    """
    drive_level(bridge, ORG_STEPS, draft.org, is_top=False)


def ask_account_details(bridge: WizardUiBridge, draft: AccountDraft) -> None:
    """Ask the account type and open the organization level for one.

    Choosing an organization account opens the nested organization level.
    A WizardBack out of that level's first question, or a WizardCancelLevel
    from anywhere inside it, both return here to re-ask the account type;
    this is how the user "changes what opened the level". The organization
    answers persist in the draft, so re-entering the level offers them
    again as defaults. A WizardBack from the account-type question itself
    is not caught here, so it propagates and the enclosing level steps to
    the previous question.
    """
    while True:
        draft.account_type = bridge.ask_choice(
            'Account type', choices=_ACCOUNT_TYPES,
            default=draft.account_type or _PERSONAL)
        if draft.account_type != _ORGANIZATION:
            return
        try:
            run_org_section(bridge, draft)
            return
        except (WizardBack, WizardCancelLevel):
            continue


def ask_username(bridge: WizardUiBridge, draft: AccountDraft) -> None:
    """Ask the username, defaulting to the earlier answer."""
    draft.username = bridge.ask_text('Username',
                                     default=draft.username or _DEFAULT_USER)


def ask_email(bridge: WizardUiBridge, draft: AccountDraft) -> None:
    """Ask the email address, defaulting to the earlier answer."""
    draft.email = bridge.ask_text('Email address',
                                  default=draft.email or _DEFAULT_EMAIL)


def ask_password(bridge: WizardUiBridge, draft: AccountDraft) -> None:
    """Ask the password without echoing it.

    A sensitive question cannot carry a default, so unlike the other
    questions the password is entered again whenever it is revisited.
    """
    draft.password = bridge.ask_text('Choose a password', sensitive=True)


TOP_STEPS: list[Callable[[WizardUiBridge, AccountDraft], None]] = [
    ask_username, ask_email, ask_account_details, ask_password]


def run_account_setup(bridge: WizardUiBridge) -> Optional[AccountDraft]:
    """Drive the whole wizard, returning the draft or None if abandoned.

    WizardAbort is the only navigation request that reaches here; the
    others are handled inside the levels. It means the user abandoned the
    wizard, so the collected draft is thrown away.
    """
    draft = AccountDraft()
    try:
        drive_level(bridge, TOP_STEPS, draft, is_top=True)
    except WizardAbort:
        return None
    return draft


def summarize(draft: AccountDraft) -> str:
    """Return a human-readable summary of the collected account."""
    length = 0 if draft.password is None else len(draft.password)
    lines = ['Account summary:',
             f'  Username: {draft.username}',
             f'  Email: {draft.email}',
             f'  Account type: {draft.account_type}']
    if draft.account_type == _ORGANIZATION:
        lines.append(f'  Organization: {draft.org.name}')
        lines.append(f'  Members: {draft.org.members}')
    lines.append(f'  Password: {length} character(s), never echoed')
    return '\n'.join(lines)


# The stream defaults, the --ui switch and main() below are the same plumbing
# in every example, so each example stays a complete program a reader can run
# and study on its own. Repeating this ceremony is a deliberate teaching
# choice, so duplicate-code is turned off from here to the end of the file.
# pylint: disable=duplicate-code
def collect_account(stdin_file: Optional[TextIO] = None,
                    stdout_file: Optional[TextIO] = None,
                    stderr_file: Optional[TextIO] = None,
                    bridge_type: UiBridgeType = UiBridgeType.AUTO
                    ) -> Optional[str]:
    """Run the account-setup wizard and print a summary of the answers.

    Args:
        stdin_file: Optional input stream for tests or scripted use.
        stdout_file: Optional output stream for tests or scripted use.
        stderr_file: Optional diagnostic stream for navigation notes.
        bridge_type: Which text-mode bridge to build. AUTO selects the
                     Textual bridge in a real terminal and the console
                     bridge otherwise, which is what tests rely on.

    Returns:
        The printed summary text, or None when the user abandoned setup.
    """
    in_file = sys.stdin if stdin_file is None else stdin_file
    out_file = sys.stdout if stdout_file is None else stdout_file
    err_file = sys.stderr if stderr_file is None else stderr_file
    bridge = make_text_ui_bridge(out_file, in_file, err_file, bridge_type)
    draft = run_account_setup(bridge)
    if draft is None:
        out_file.write('Account setup abandoned.\n')
        return None
    summary = summarize(draft)
    out_file.write(summary + '\n')
    return summary


def build_parser() -> argparse.ArgumentParser:
    """Return the argument parser for the navigation example."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ui', choices=('auto', 'console', 'textual'),
                        default='auto', help='UI bridge to use.')
    return parser


_UI_TYPES = {'auto': UiBridgeType.AUTO, 'console': UiBridgeType.CONSOLE,
             'textual': UiBridgeType.TEXTUAL}


def main(args: Optional[list[str]] = None) -> int:
    """Parse arguments, run the wizard and show the summary."""
    parsed = build_parser().parse_args(args)
    collect_account(bridge_type=_UI_TYPES[parsed.ui])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
