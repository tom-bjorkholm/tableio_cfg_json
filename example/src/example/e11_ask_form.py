#! /usr/bin/env python3
"""Demonstrate WizardUiBridge.ask_form() with a small export form.

This teaching example is deliberately self-contained: it asks the user a
handful of related questions on one form and then prints a summary of the
answers. Nothing is written to disk, so the reader can focus entirely on
how ask_form() is used and not on the surrounding application logic.

Why ask_form() exists
---------------------
The other bridge questions (ask_text, ask_choice, ...) ask exactly one
thing at a time. That is natural on a plain console, but a graphical or
full-screen textual interface can do better: it can show several related
questions together so the user sees the whole picture and answers them in
any order before submitting. ask_form() is the bridge method for that. It
takes a description of the whole form (a list of Ask*Field objects) and
returns one Answer*Field per question.

The same call works on every bridge:

- On a graphical or textual bridge (here the Textual bridge chosen by
  make_text_ui_bridge() in a real terminal) the whole form is shown on one
  screen with a labelled input widget per field.
- On the plain console bridge the base implementation of ask_form() simply
  asks each field in turn with the ordinary typed ask methods, so the same
  program still runs when output is redirected or under tests.

Because make_text_ui_bridge() falls back to the console bridge whenever the
streams are not a real terminal, this example is both a nice full-screen
form in a terminal and a fully scriptable console program in tests.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence, TextIO

from tableio_cfg_json import make_text_ui_bridge, UiBridgeType, \
    WizardUiBridge, WizardNavigation, PathAskOptions, WizardPathKind, \
    AskField, AnswerFields, PartFormValidationResult, AskTextField, \
    AskIntField, AskPathField, AskYesNoField, AskChoiceField, \
    AskMultiChoiceField, AnswerTextField, AnswerIntField, AnswerPathField, \
    AnswerYesNoField, AnswerChoiceField, AnswerMultiChoiceField

# The form is always asked in this fixed order. Each name is the index of
# that field both in the list returned by build_export_form() and in the
# AnswerFields returned by ask_form(). Keeping them as named constants lets
# the partial validator and the summary read a specific answer by meaning
# instead of by a bare number.
_TITLE, _OUTPUT, _FORMAT, _DELIMITER, _LIMIT, _HEADER, _COLUMNS = range(7)

# The main instruction shown above the whole form. A GUI or textual bridge
# is free to wrap and lay this out nicely; the console fallback prints it
# once before the first question.
_FORM_QUESTION = (
    'Configure how the cities table will be exported.\n'
    'Fill in the fields in any order, then submit the form.')

# The output file must not exist yet, so the export never overwrites a file
# by accident. WizardPathKind carries that rule for the path field.
_OUTPUT_PATH_OPTIONS = PathAskOptions(kind=WizardPathKind.NON_EXISTING_FILE)
_COLUMN_CHOICES = ('City', 'Country', 'Continent', 'Population')
_DEFAULT_COLUMNS = ('City', 'Country', 'Continent')


def build_export_form() -> list[AskField]:
    """Describe the export form as a list of Ask*Field questions.

    Each row of the form is one Ask*Field dataclass. The Python type of the
    object is what tells the bridge which kind of input widget to show, so
    there is one class per kind of question:

    - AskTextField     free text (here the report title and the delimiter),
    - AskPathField     a file or directory path, validated with
                       PathAskOptions (here a new output file),
    - AskChoiceField   pick exactly one value from a fixed list,
    - AskIntField      an integer, optionally bounded and/or nullable,
    - AskYesNoField    a boolean, shown as a check box or toggle,
    - AskMultiChoiceField  pick several values from a fixed list.

    Every field carries a short_question (the label) and an optional
    help_text (shown as a tooltip in a graphical or textual bridge). A
    field's default, when given, is the value the input starts with, which
    the user may change. The order of the list fixes the row order and must
    match the _TITLE ... _COLUMNS index constants above.
    """
    return [
        AskTextField(short_question='Report title',
                     help_text='Heading of the exported report.',
                     default='Cities report'),
        AskPathField(short_question='Output file',
                     help_text='Path of the new output file to create.',
                     path_options=_OUTPUT_PATH_OPTIONS),
        AskChoiceField(short_question='Output format',
                       help_text='File format of the exported report.',
                       choices=('CSV', 'Excel', 'HTML'), default='CSV'),
        AskTextField(short_question='CSV delimiter',
                     help_text='Column separator, used only for CSV.',
                     default=','),
        AskIntField(short_question='Row limit', nullable=True, min_value=1,
                    help_text='Maximum rows to export, or empty for all.'),
        AskYesNoField(short_question='Include header row', default=True,
                      help_text='Write the column names as the first row.'),
        AskMultiChoiceField(short_question='Columns to export', min_select=1,
                            help_text='Columns to export; pick one or more.',
                            choices=_COLUMN_CHOICES, default=_DEFAULT_COLUMNS)
    ]


def export_validator(answers: AnswerFields,
                     _changed: int) -> PartFormValidationResult:
    """Give early per-field feedback while the export form is filled.

    ask_form() calls this after every change (on a GUI or textual bridge)
    or after every answered field (on the console fallback), passing the
    current answers and the index of the field that changed. It returns a
    PartFormValidationResult with three parts:

    - is_valid / message: advisory validity and a message to show. A
      graphical or textual bridge refuses to submit while is_valid is
      False, so a merely informational note must NOT set is_valid False;
      only a real problem the user has to fix should.
    - disable_row_idxs: rows that are irrelevant given the current answers
      and should be disabled. Disabling never blocks submit.

    This validator shows both behaviours. The delimiter only matters for
    CSV, so for any other format its row is disabled (is_valid stays True).
    For CSV the delimiter must be a single character; if it is not, an
    error message is shown and submit is blocked until it is corrected.
    """
    output_format = _choice_value(answers, _FORMAT)
    if output_format != 'CSV':
        return PartFormValidationResult(True, '', (_DELIMITER,))
    reason = _delimiter_reason(output_format, _text_value(answers, _DELIMITER))
    if reason is None:
        return PartFormValidationResult(True, '')
    return PartFormValidationResult(False, reason)


def _delimiter_reason(output_format: Optional[str],
                      delimiter: Optional[str]) -> Optional[str]:
    """Return why a CSV delimiter is invalid, or None when acceptable."""
    if output_format != 'CSV':
        return None
    if delimiter is not None and len(delimiter) != 1:
        return 'The CSV delimiter must be exactly one character.'
    return None


def ask_export_settings(bridge: WizardUiBridge,
                        out_file: TextIO) -> Optional[AnswerFields]:
    """Ask the export form until the submitted answers are consistent.

    A graphical or textual bridge already enforces the partial validator on
    submit, but the console fallback treats validator messages as advisory
    only. To behave the same on every bridge this loop re-shows the form,
    with a re_ask_reason, until a final whole-form check passes.

    Any ask method may raise a WizardNavigation request (back, cancel or
    abort) instead of returning answers. A single standalone form has no
    earlier step to go back to, so all of them are treated here as "the
    user gave up", and the function returns None.
    """
    fields = build_export_form()
    reason: Optional[str] = None
    while True:
        try:
            answers = bridge.ask_form(_FORM_QUESTION, fields,
                                      re_ask_reason=reason,
                                      partial_validator=export_validator)
        except WizardNavigation:
            out_file.write('Export configuration cancelled.\n')
            return None
        reason = _delimiter_reason(_choice_value(answers, _FORMAT),
                                   _text_value(answers, _DELIMITER))
        if reason is None:
            return answers


def summarize_answers(answers: AnswerFields) -> str:
    """Return a human-readable summary of the collected answers.

    This is where the returned AnswerFields are read. Each answer is one
    Answer*Field dataclass matching the Ask*Field that produced it; its
    value attribute holds the typed answer (str, Path, int, bool or a
    sequence of str). The small typed helpers below unpack one answer each.
    """
    return '\n'.join(['Export settings summary:'] + _summary_lines(answers))


def _summary_lines(answers: AnswerFields) -> list[str]:
    """Return one summary line per relevant answer, in reading order."""
    output_format = _choice_value(answers, _FORMAT)
    assert output_format is not None  # the format choice always has a default
    lines = [_line('Report title', str(_text_value(answers, _TITLE))),
             _line('Output file', str(_path_value(answers, _OUTPUT))),
             _line('Output format', output_format)]
    if output_format == 'CSV':
        lines.append(_line('CSV delimiter',
                           str(_text_value(answers, _DELIMITER))))
    lines.append(_line('Row limit', _limit_text(answers)))
    lines.append(_line('Header row', _header_text(answers)))
    lines.append(_line('Columns', _columns_text(answers)))
    return lines


def _line(label: str, value: str) -> str:
    """Return one indented 'label: value' summary line."""
    return f'  {label}: {value}'


def _limit_text(answers: AnswerFields) -> str:
    """Return the row-limit answer as display text."""
    limit = _int_value(answers, _LIMIT)
    return 'all rows' if limit is None else str(limit)


def _header_text(answers: AnswerFields) -> str:
    """Return the include-header answer as display text."""
    return 'included' if _bool_value(answers, _HEADER) else 'omitted'


def _columns_text(answers: AnswerFields) -> str:
    """Return the selected columns as display text."""
    columns = _multi_value(answers, _COLUMNS)
    return ', '.join(columns) if columns else '(none)'


def _text_value(answers: AnswerFields, index: int) -> Optional[str]:
    """Return the value of the AnswerTextField at index."""
    answer = answers[index]
    assert isinstance(answer, AnswerTextField)
    return answer.value


def _path_value(answers: AnswerFields, index: int) -> Optional[Path]:
    """Return the value of the AnswerPathField at index."""
    answer = answers[index]
    assert isinstance(answer, AnswerPathField)
    return answer.value


def _choice_value(answers: AnswerFields, index: int) -> Optional[str]:
    """Return the value of the AnswerChoiceField at index."""
    answer = answers[index]
    assert isinstance(answer, AnswerChoiceField)
    return answer.value


def _int_value(answers: AnswerFields, index: int) -> Optional[int]:
    """Return the value of the AnswerIntField at index."""
    answer = answers[index]
    assert isinstance(answer, AnswerIntField)
    return answer.value


def _bool_value(answers: AnswerFields, index: int) -> bool:
    """Return the value of the AnswerYesNoField at index."""
    answer = answers[index]
    assert isinstance(answer, AnswerYesNoField)
    return answer.value


def _multi_value(answers: AnswerFields, index: int) -> Sequence[str]:
    """Return the value of the AnswerMultiChoiceField at index."""
    answer = answers[index]
    assert isinstance(answer, AnswerMultiChoiceField)
    return answer.value


def collect_and_summarize(stdin_file: Optional[TextIO] = None,
                          stdout_file: Optional[TextIO] = None,
                          stderr_file: Optional[TextIO] = None,
                          bridge_type: UiBridgeType = UiBridgeType.AUTO
                          ) -> Optional[str]:
    """Ask the export form and print a summary of the answers.

    Args:
        stdin_file: Optional input stream for tests or scripted use.
        stdout_file: Optional output stream for tests or scripted use.
        stderr_file: Optional diagnostic stream for validation messages.
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
    answers = ask_export_settings(bridge, out_file)
    if answers is None:
        return None
    summary = summarize_answers(answers)
    out_file.write(summary + '\n')
    return summary


def build_parser() -> argparse.ArgumentParser:
    """Return the argument parser for the ask_form example."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ui', choices=('auto', 'console', 'textual'),
                        default='auto', help='UI bridge to use.')
    return parser


_UI_TYPES = {'auto': UiBridgeType.AUTO, 'console': UiBridgeType.CONSOLE,
             'textual': UiBridgeType.TEXTUAL}


def main(args: Optional[list[str]] = None) -> int:
    """Parse arguments, ask the export form and print the summary."""
    parsed = build_parser().parse_args(args)
    collect_and_summarize(bridge_type=_UI_TYPES[parsed.ui])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
