#! /usr/local/bin/python3
"""Console text user interface bridge for the configuration wizard.

This module provides the concrete console bridge used when the wizard
talks to a user through plain text streams. It recognises reserved
navigation tokens so a console user can step back, cancel the current
level or abandon the whole configuration.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import getpass
from typing import Optional, Sequence, TextIO
from tableio_cfg_json.wizard_ui_bridge_arg_types import PartialCheck, \
    WizardBack, WizardCancelLevel, WizardAbort, TableColumn, TableCell
from tableio_cfg_json.wizard_ui_bridge import WizardUiBridge
from tableio_cfg_json.wizard_ui_bridge_form_defs import AskField
from tableio_cfg_json._wizard_ui_bridge_helpers import check_text_args, \
    text_answer, ask_yes_no, ask_one, ask_many, run_table, int_text, \
    question_with_default
from tableio_cfg_json.wizard_ui_bridge_table import _run_variable_table

_BACK = ':b'
_CANCEL = ':c'
_ABORT = ':q'
_NAV_HINT = '(:b=back  :c=cancel level  :q=abort)'


class WizardUiBridgeConsole(WizardUiBridge):
    """Bridge between the wizard and the console text user interface."""

    def __init__(self, stdout_file: TextIO, stdin_file: TextIO,
                 stderr_file: TextIO) -> None:
        """Initialize the bridge.

        Args:
            stdout_file: Stream to print messages to.
            stdin_file: Stream to read user answers from.
            stderr_file: Stream to print errors to.
        """
        self.stdout_file = stdout_file
        self.stdin_file = stdin_file
        self.stderr_file = stderr_file

    # pylint: disable-next=too-many-arguments
    def ask_text(self, question: str, re_ask_reason: Optional[str] = None,
                 nullable: bool = False, *, default: Optional[str] = None,
                 sensitive: bool = False) -> Optional[str]:
        """Ask for free text on the console; see WizardUiBridge.ask_text."""
        check_text_args(default, sensitive)
        prompt = question_with_default(question, default)
        self._emit_question(prompt, re_ask_reason, [])
        text = self._read_sensitive(prompt) if sensitive \
            else self._read_answer(prompt)
        return text_answer(text, nullable, default)

    def supports_form_field(self, field: AskField) -> bool:
        """Show every form field type; see WizardUiBridge.

        The inherited base ask_form() asks each field with the typed ask
        methods, so the console form handles the typed float, date, time,
        date-time and duration fields as well as the original kinds.
        """
        assert field is not None
        return True

    def ask_yes_no(self, question: str, default: bool,
                   re_ask_reason: Optional[str] = None) -> bool:
        """Ask a yes/no question on the console; see ask_yes_no."""
        def reader(reason: Optional[str]) -> str | int:
            marked = ('yes',) if default else ('no',)
            menu_lines = _menu_lines(('yes', 'no'), marked=marked)
            self._emit_question(question, reason, menu_lines)
            return _to_index(self._read_answer(question))
        return ask_yes_no(reader, default, re_ask_reason)

    # pylint: disable-next=too-many-arguments
    def ask_table(self, columns: Sequence[TableColumn],
                  cells: list[list[TableCell]], question: str, *,
                  re_ask_reason: Optional[str] = None,
                  partial_check: Optional[PartialCheck] = None,
                  min_rows: Optional[int] = None,
                  max_rows: Optional[int] = None) -> list[list[Optional[str]]]:
        """Ask the user to fill a table on the console; see ask_table.

        With both min_rows and max_rows given the table has a variable
        number of rows, edited through a row-menu interface. Otherwise the
        fixed rows in cells are filled one editable cell at a time.
        """
        if min_rows is not None and max_rows is not None:
            return _run_variable_table(self._ask_raw, self.show, columns,
                                       cells, question, re_ask_reason,
                                       partial_check, min_rows, max_rows)
        return run_table(self._ask_raw, self.show, columns, cells, question,
                         re_ask_reason, partial_check)

    def _ask_raw(self, question: str, re_ask_reason: Optional[str] = None,
                 choices: Optional[Sequence[str]] = None) -> str | int:
        """Emit one question and read a navigation-checked raw answer.

        Returns the entered text, or a 0-based index into choices when
        choices are offered, like the deprecated WizardUiBridge.ask().
        """
        self._emit_question(question, re_ask_reason, _menu_lines(choices))
        text = self._read_answer(question)
        return text if choices is None else _to_index(text)

    def ask_choice(self, question: str, *, choices: Sequence[str],
                   default: Optional[str] = None,
                   re_ask_reason: Optional[str] = None) -> str:
        """Ask one choice on the console; see WizardUiBridge.ask_choice."""
        marked = None if default is None else (default,)

        def reader(reason: Optional[str]) -> str | int:
            self._emit_question(question, reason, _menu_lines(choices, marked))
            return _to_index(self._read_answer(question))
        return ask_one(reader, choices, default, re_ask_reason)

    # pylint: disable-next=too-many-arguments
    def ask_multi(self, question: str, *, choices: Sequence[str],
                  default: Optional[Sequence[str]] = None, min_select: int = 0,
                  max_select: Optional[int] = None,
                  re_ask_reason: Optional[str] = None) -> list[str]:
        """Ask several choices on the console; see WizardUiBridge.ask_multi."""
        def reader(reason: Optional[str]) -> str | int:
            self._emit_question(_multi_question(question), reason,
                                _menu_lines(choices, default))
            return self._read_answer(question)
        return ask_many(reader, choices, default, min_select, max_select,
                        re_ask_reason, one_based=True)

    def _emit_question(self, question: str, re_ask_reason: Optional[str],
                       lines: Sequence[str]) -> None:
        """Print one question, any re-ask reason, choices and the prompt."""
        if re_ask_reason is not None:
            print(re_ask_reason, file=self.stderr_file)
        print('', file=self.stdout_file)
        print(question, file=self.stdout_file)
        for line in lines:
            print(line, file=self.stdout_file)
        print(_NAV_HINT, file=self.stdout_file)
        print('> ', end='', file=self.stdout_file)

    def _read_answer(self, question: str) -> str:
        """Read one navigation-checked answer line from the input stream."""
        answer = self.stdin_file.readline()
        if answer == '':
            raise EOFError(f'No answer supplied for {question}.')
        text = answer.rstrip('\n')
        _raise_for_navigation(text)
        return text

    def _read_sensitive(self, question: str) -> str:
        """Read sensitive text, avoiding echo on a real terminal."""
        if not self.stdin_file.isatty():
            return self._read_answer(question)
        text = getpass.getpass('', stream=self.stdout_file)
        _raise_for_navigation(text)
        return text

    def error_file(self) -> TextIO:
        """Return the stream used for validation diagnostics."""
        return self.stderr_file

    def show(self, message: str) -> None:
        """Show a message to the user.

        This method prints the message to the console.
        Args:
            message: The message to show the user.
        """
        print(message, file=self.stdout_file)


def _raise_for_navigation(text: str) -> None:
    """Raise a navigation request when text is a reserved token."""
    token = text.strip().lower()
    if token == _BACK:
        raise WizardBack()
    if token == _CANCEL:
        raise WizardCancelLevel()
    if token == _ABORT:
        raise WizardAbort()


def _to_index(text: str) -> str | int:
    """Map a numeric menu answer to a 0-based index, else keep the text."""
    index = int_text(text)
    return text if index is None else index - 1


def _menu_lines(choices: Optional[Sequence[str]],
                marked: Optional[Sequence[str]] = None) -> list[str]:
    """Return the numbered menu lines, marking any choice in marked."""
    if choices is None:
        return []
    flagged = set() if marked is None else set(marked)
    lines: list[str] = []
    for index, choice in enumerate(choices, start=1):
        suffix = ' (default)' if choice in flagged else ''
        lines.append(f'{index}: {choice}{suffix}')
    return lines


def _multi_question(question: str) -> str:
    """Return the multi-choice question with an entry hint appended."""
    return f'{question}\nEnter comma-separated numbers or names.'
