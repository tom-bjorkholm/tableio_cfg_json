#! /usr/bin/env python3
"""Demonstrate the typed form fields and validator prefills of ask_form().

This teaching example builds on e11_ask_form.py. Where e11 uses the six
original field kinds (text, integer, path, yes/no, single choice and
multi choice), this example shows the five typed fields added on top of
them, and it shows how a partial validator can *prefill* one field from
the answers to others.

The typed fields
----------------
Besides making the answer a real Python object instead of a string, the
typed fields let a graphical or textual bridge offer a better editor:

- AskFloatField      a number (here a ticket price),
- AskDateField       a calendar date (the Textual bridge opens a calendar
                     picker for it),
- AskTimeField       a wall-clock time,
- AskDateTimeField   a date together with a time (the calendar picker
                     fills the date part, the time is typed),
- AskDurationField   a length of time, written as ``<days> d HH:MM:SS`` or
                     as a plain number of seconds, which is friendlier than
                     forcing the user to enter one large second count.

On the plain console bridge each field is still asked as text and parsed,
so the very same program runs under tests and with redirected input. That
is why this example is fully scriptable even though it shows a calendar in
a real terminal.

Prefilling a field
------------------
The form has an "Ends at" date-time field that the user rarely wants to
compute by hand. The partial validator computes it from the event date,
the start time and the duration and returns it as a *prefill*: the bridge
places the value into the "Ends at" input exactly as if the user had
typed it, and the user is still free to change it afterwards. The same
validator also *disables* the ticket-price row when the event is marked
free, so the price question disappears while it is irrelevant.

Nothing is written to disk, so the reader can concentrate on ask_form().
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
import sys
from datetime import date, datetime, time, timedelta
from typing import Optional, TextIO

from tableio_cfg_json import make_text_ui_bridge, UiBridgeType, \
    WizardUiBridge, WizardNavigation, AskField, AnswerFields, \
    PartFormValidationResult, PrefillValues, AskTextField, AskYesNoField, \
    AskFloatField, AskDateField, AskTimeField, AskDateTimeField, \
    AskDurationField, AnswerTextField, AnswerYesNoField, AnswerFloatField, \
    AnswerDateField, AnswerTimeField, AnswerDateTimeField, AnswerDurationField

# Each name is the index of one field in build_schedule_form() and in the
# AnswerFields that ask_form() returns. Naming them lets the validator and
# the summary read a specific answer by meaning instead of by a bare number.
_TITLE, _DATE, _START, _DURATION, _END, _FREE, _PRICE = range(7)

# The main instruction shown above the whole form. A graphical or textual
# bridge lays it out nicely; the console fallback prints it once.
_FORM_QUESTION = (
    'Describe the event to schedule.\n'
    'Fill in the fields in any order; the end time is computed for you.')

# The fields whose change should recompute the "Ends at" prefill.
_END_INPUTS = (_DATE, _START, _DURATION)


def build_schedule_form() -> list[AskField]:
    """Describe the scheduling form as a list of Ask*Field questions.

    The Python type of each object is what tells the bridge which editor
    to show, so there is one class per kind of question. A typed field
    carries the same short_question and help_text as any other field, and
    its default (when given) is the value the editor starts with.
    """
    return [
        AskTextField(short_question='Event title',
                     help_text='A short name for the event.',
                     default='Team workshop'),
        # A required date: with no default and nullable False the console
        # re-asks until a valid YYYY-MM-DD date is entered, and the Textual
        # bridge offers a calendar picker (button or the "?" token).
        AskDateField(short_question='Event date',
                     help_text='The day the event takes place.'),
        AskTimeField(short_question='Start time',
                     help_text='When the event starts (HH:MM).',
                     default=time(9, 0)),
        # A duration accepts "1 d 02:30:00", "02:30:00" or a plain number of
        # seconds, which is far friendlier than one large second count.
        AskDurationField(short_question='Duration',
                         help_text='How long the event lasts.',
                         default=timedelta(hours=1)),
        # "Ends at" is nullable because it is empty until the fields it is
        # computed from are all filled; the validator prefills it then.
        AskDateTimeField(short_question='Ends at', nullable=True,
                         help_text='Computed from date, start and duration; '
                         'change it if you like.'),
        AskYesNoField(short_question='Free event', default=False,
                      help_text='Tick when there is no ticket price.'),
        # A price is never negative, so the field enforces a lower bound.
        AskFloatField(short_question='Ticket price', min_value=0.0,
                      default=0.0,
                      help_text='Price per ticket in whole currency units.')
    ]


def schedule_validator(answers: AnswerFields,
                       changed: int) -> PartFormValidationResult:
    """Give early feedback while the scheduling form is filled.

    ask_form() calls this after every change (graphical or textual bridge)
    or after every answered field (console fallback), passing the current
    answers and the index of the field that changed. This validator uses
    two of the three parts of a PartFormValidationResult:

    - disable_row_idxs: a free event has no price, so the price row is
      disabled while "Free event" is ticked. Disabling never blocks
      submitting the form; it only hides an irrelevant question.
    - prefill_values: whenever the event date, the start time or the
      duration changes, the end date-time is recomputed and offered as a
      prefill for the "Ends at" field. A prefill aimed at the row that just
      changed is ignored by the bridge, so this never fights the user's own
      edit of "Ends at".

    is_valid stays True here: an informational prefill or a disabled row is
    not an error, so the form may always be submitted.
    """
    disable = () if not _is_free(answers) else (_PRICE,)
    return PartFormValidationResult(True, '', disable,
                                    _end_prefill(answers, changed))


def _end_prefill(answers: AnswerFields, changed: int) -> PrefillValues:
    """Return a prefill of the computed end time, or nothing.

    The end time is only recomputed when one of the fields it depends on
    changed, so a stable value is emitted and the prefill does not loop.
    """
    if changed not in _END_INPUTS:
        return ()
    end = _computed_end(answers)
    return () if end is None else ((_END, end),)


def _computed_end(answers: AnswerFields) -> Optional[datetime]:
    """Return event start plus duration, or None when data is missing."""
    day = _date_value(answers, _DATE)
    start = _time_value(answers, _START)
    length = _duration_value(answers, _DURATION)
    if day is None or start is None or length is None:
        return None
    return datetime.combine(day, start) + length


def _is_free(answers: AnswerFields) -> bool:
    """Return whether the event is marked as free.

    The yes/no answer is read inline here rather than through a shared
    helper, keeping this example self-contained.
    """
    answer = answers[_FREE]
    assert isinstance(answer, AnswerYesNoField)
    return answer.value


def ask_schedule(bridge: WizardUiBridge,
                 out_file: TextIO) -> Optional[AnswerFields]:
    """Ask the scheduling form once and return the answers.

    Any ask method may raise a WizardNavigation request (back, cancel or
    abort) instead of returning answers. A single standalone form has no
    earlier step to go back to, so all of them are treated here as "the
    user gave up", and the function returns None.
    """
    try:
        return bridge.ask_form(_FORM_QUESTION, build_schedule_form(),
                               partial_validator=schedule_validator)
    except WizardNavigation:
        out_file.write('Scheduling cancelled.\n')
        return None


def summarize_answers(answers: AnswerFields) -> str:
    """Return a human-readable summary of the collected answers.

    Each answer is one Answer*Field dataclass matching the Ask*Field that
    produced it, and its value attribute holds the typed answer: a str, a
    date, a time, a datetime, a timedelta, a bool or a float.
    """
    return '\n'.join(['Scheduled event:'] + _summary_lines(answers))


def _summary_lines(answers: AnswerFields) -> list[str]:
    """Return one summary line per relevant answer, in reading order."""
    price = 'free' if _is_free(answers) \
        else str(_float_value(answers, _PRICE))
    return [_line('Title', _title_text(answers)),
            _line('Date', str(_date_value(answers, _DATE))),
            _line('Start', str(_time_value(answers, _START))),
            _line('Duration', _duration_text(answers)),
            _line('Ends at', str(_datetime_value(answers, _END))),
            _line('Price', price)]


def _line(label: str, value: str) -> str:
    """Return one indented 'label: value' summary line."""
    return f'  {label}: {value}'


def _duration_text(answers: AnswerFields) -> str:
    """Return the duration answer as display text."""
    length = _duration_value(answers, _DURATION)
    return 'unset' if length is None else str(length)


def _title_text(answers: AnswerFields) -> str:
    """Return the event title as display text, empty when unset."""
    answer = answers[_TITLE]
    assert isinstance(answer, AnswerTextField)
    return '' if answer.value is None else answer.value


def _date_value(answers: AnswerFields, index: int) -> Optional[date]:
    """Return the value of the AnswerDateField at index."""
    answer = answers[index]
    assert isinstance(answer, AnswerDateField)
    return answer.value


def _time_value(answers: AnswerFields, index: int) -> Optional[time]:
    """Return the value of the AnswerTimeField at index."""
    answer = answers[index]
    assert isinstance(answer, AnswerTimeField)
    return answer.value


def _datetime_value(answers: AnswerFields, index: int) -> Optional[datetime]:
    """Return the value of the AnswerDateTimeField at index."""
    answer = answers[index]
    assert isinstance(answer, AnswerDateTimeField)
    return answer.value


def _duration_value(answers: AnswerFields, index: int) -> Optional[timedelta]:
    """Return the value of the AnswerDurationField at index."""
    answer = answers[index]
    assert isinstance(answer, AnswerDurationField)
    return answer.value


def _float_value(answers: AnswerFields, index: int) -> Optional[float]:
    """Return the value of the AnswerFloatField at index."""
    answer = answers[index]
    assert isinstance(answer, AnswerFloatField)
    return answer.value


def collect_and_summarize(bridge_type: UiBridgeType = UiBridgeType.AUTO,
                          stdin_file: Optional[TextIO] = None,
                          stdout_file: Optional[TextIO] = None,
                          stderr_file: Optional[TextIO] = None
                          ) -> Optional[str]:
    """Ask the scheduling form and print a summary of the answers.

    Args:
        bridge_type: Which text-mode bridge to build. AUTO selects the
                     Textual bridge in a real terminal and the console
                     bridge otherwise, which is what tests rely on.
        stdin_file: Optional input stream for tests or scripted use.
        stdout_file: Optional output stream for tests or scripted use.
        stderr_file: Optional diagnostic stream for validation messages.

    Returns:
        The printed summary text, or None when the user cancelled.
    """
    out_file = sys.stdout if stdout_file is None else stdout_file
    bridge = make_text_ui_bridge(
        out_file, sys.stdin if stdin_file is None else stdin_file,
        sys.stderr if stderr_file is None else stderr_file, bridge_type)
    answers = ask_schedule(bridge, out_file)
    if answers is None:
        return None
    return _write_summary(answers, out_file)


def _write_summary(answers: AnswerFields, out_file: TextIO) -> str:
    """Write and return the summary of the collected answers."""
    summary = summarize_answers(answers)
    out_file.write(summary + '\n')
    return summary


def build_parser() -> argparse.ArgumentParser:
    """Return the argument parser for the scheduling example."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ui', default='auto',
                        choices=('auto', 'console', 'textual'),
                        help='Which text-mode UI bridge to use.')
    return parser


def main(args: Optional[list[str]] = None) -> int:
    """Parse arguments, ask the scheduling form and print the summary."""
    ui_name = build_parser().parse_args(args).ui
    bridge = {'auto': UiBridgeType.AUTO, 'console': UiBridgeType.CONSOLE,
              'textual': UiBridgeType.TEXTUAL}[ui_name]
    collect_and_summarize(bridge)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
