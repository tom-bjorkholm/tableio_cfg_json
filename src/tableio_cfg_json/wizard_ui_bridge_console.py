#! /usr/local/bin/python3
"""Console text user interface bridge for the configuration wizard.

This module provides the concrete console bridge used when the wizard
talks to a user through plain text streams. It recognises reserved
navigation tokens so a console user can step back, cancel the current
level or abandon the whole configuration.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional, Sequence, TextIO

from tableio_cfg_json.wizard_ui_bridge import WizardAbort, WizardBack, \
    WizardCancelLevel, WizardUiBridge, _ask_many, _ask_one, _int_text

_BACK = ':b'
_CANCEL = ':c'
_ABORT = ':q'
_NAV_HINT = '(:b=back  :c=cancel  :q=abort)'


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

    def ask(self, question: str, re_ask_reason: Optional[str] = None,
            choices: Optional[Sequence[str]] = None) -> str | int:
        """Ask a question and return the user's answer.

        Args:
            question: The question to ask the user.
            re_ask_reason: The reason for re-asking the question for
                           instance that the user's answer was invalid.
            choices: The choices to offer the user as a sequence of strings.

        Returns:
            The user's answer. If the user's answer is one of the choices,
            then the return value can be either the matching string or the
            index of what the user selected. If integer index is used it is
            0-based.
            The bridge is not required to validate the user's answer in
            any way. It is the responsibility of the caller to validate the
            user's answer.
            If the user entered/selected an empty string as answer, then the
            return value should be an empty string. The caller may interpret
            this as a request to use the default value.
        Raises:
            EOFError: The input stream ended before an answer was read.
            WizardBack: The user asked to return to the previous question.
            WizardCancelLevel: The user cancelled the current level.
            WizardAbort: The user abandoned the whole configuration.
        """
        self._emit_question(question, re_ask_reason, _menu_lines(choices))
        text = self._read_answer(question)
        if choices is None:
            return text
        return _to_index(text)

    def ask_choice(self, question: str, *, choices: Sequence[str],
                   default: Optional[str] = None,
                   re_ask_reason: Optional[str] = None) -> str:
        """Ask one choice on the console; see WizardUiBridge.ask_choice."""
        marked = None if default is None else (default,)

        def reader(reason: Optional[str]) -> str | int:
            self._emit_question(question, reason, _menu_lines(choices, marked))
            return _to_index(self._read_answer(question))
        return _ask_one(reader, choices, default, re_ask_reason)

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
        return _ask_many(reader, choices, default, min_select, max_select,
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
    index = _int_text(text)
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
