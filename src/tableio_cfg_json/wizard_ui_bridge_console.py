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
    WizardCancelLevel, WizardUiBridge, _int_text

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
        if re_ask_reason is not None:
            print(re_ask_reason, file=self.stderr_file)
        print('', file=self.stdout_file)
        print(question, file=self.stdout_file)
        if choices is not None:
            for index, choice in enumerate(choices, start=1):
                print(f'{index}: {choice}', file=self.stdout_file)
        print(_NAV_HINT, file=self.stdout_file)
        print('> ', end='', file=self.stdout_file)
        answer = self.stdin_file.readline()
        if answer == '':
            raise EOFError(f'No answer supplied for {question}.')
        text_answer = answer.rstrip('\n')
        _raise_for_navigation(text_answer)
        if choices is not None:
            choice_index = _int_text(text_answer)
            if choice_index is not None:
                return choice_index - 1
        return text_answer

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
