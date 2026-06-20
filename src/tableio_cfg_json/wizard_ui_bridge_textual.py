#! /usr/local/bin/python3
"""Textual full-screen user interface bridge for the wizard.

This module provides the concrete Textual bridge used when the wizard
talks to a user through a real terminal. Each ask method runs a short
lived Textual application for one question and returns its result, which
keeps the one-question-at-a-time contract of WizardUiBridge while giving
the user a full-screen interface with selectable lists and check boxes.

Navigation keys exit a screen with no value and record which
WizardNavigation request to raise, so the bridge re-raises it after the
screen closes. Messages passed to show() and diagnostics written to
error_file() are buffered and rendered in the header of the next
screen, so nothing is written straight to the terminal where it would
corrupt the Textual display.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from __future__ import annotations
from io import StringIO
from typing import ClassVar, Iterator, Optional, Sequence, TypeVar
from textual import on
from textual.app import App, ComposeResult
from textual.binding import BindingType
from textual.widgets import Button, Footer, Input, OptionList, \
    SelectionList, Static
from textual.widgets.selection_list import Selection
from tableio_cfg_json.wizard_ui_bridge import WizardAbort, WizardBack, \
    WizardCancelLevel, WizardNavigation, WizardUiBridge, _multi_count_error

_T = TypeVar('_T')


class _NavApp(App[_T]):
    """Base screen translating navigation keys into wizard requests.

    A subclass lays out one question. ctrl+b records a request to go
    back and ctrl+o a request to cancel the current level; both exit the
    screen with no value so the bridge can raise the matching request.
    The built-in ctrl+q quit also exits with no value, which the bridge
    treats as an abort. These keys avoid the editing shortcuts that the
    text input widget binds, so they work on every screen.
    """

    BINDINGS: ClassVar[list[BindingType]] = [
        ('ctrl+b', 'nav_back', 'Back'),
        ('ctrl+o', 'nav_cancel', 'Cancel level')]

    def __init__(self) -> None:
        """Initialize with no pending navigation request."""
        super().__init__()
        self.nav: Optional[type[WizardNavigation]] = None

    def action_nav_back(self) -> None:
        """Record a request to return to the previous question.

        The name avoids App.action_back, the built-in screen-history
        action, so this records a wizard back request instead.
        """
        self.nav = WizardBack
        self.exit()

    def action_nav_cancel(self) -> None:
        """Record a request to cancel the current level."""
        self.nav = WizardCancelLevel
        self.exit()


def _header_widgets(messages: list[str], question: str) -> Iterator[Static]:
    """Yield one static line per message and one for the question."""
    for line in messages:
        yield Static(line)
    yield Static(question)


class _TextApp(_NavApp[str]):
    """Free-text screen returning the string the user typed."""

    def __init__(self, question: str, messages: list[str]) -> None:
        """Store the prompt and any buffered messages."""
        super().__init__()
        self._question = question
        self._messages = messages

    def compose(self) -> ComposeResult:
        """Lay out the header, the input field and the footer."""
        yield from _header_widgets(self._messages, self._question)
        yield Input()
        yield Footer()

    @on(Input.Submitted)
    def _entered(self, event: Input.Submitted) -> None:
        """Exit returning the entered text, empty when nothing typed."""
        self.exit(event.value)


class _ChoiceApp(_NavApp[int]):
    """Single-choice screen returning the chosen 0-based index."""

    def __init__(self, question: str, choices: list[str],
                 default_index: Optional[int], messages: list[str]) -> None:
        """Store the prompt, choices and the index to highlight."""
        super().__init__()
        self._question = question
        self._choices = choices
        self._default_index = default_index
        self._messages = messages

    def compose(self) -> ComposeResult:
        """Lay out the header, the option list and the footer."""
        yield from _header_widgets(self._messages, self._question)
        yield OptionList(*self._choices)
        yield Footer()

    def on_mount(self) -> None:
        """Highlight the default option when one is given."""
        if self._default_index is not None:
            self.query_one(OptionList).highlighted = self._default_index

    @on(OptionList.OptionSelected)
    def _picked(self, event: OptionList.OptionSelected) -> None:
        """Exit returning the index of the selected option."""
        self.exit(event.option_index)


class _MultiApp(_NavApp[list[int]]):
    """Multi-choice screen returning the chosen 0-based indexes."""

    BINDINGS: ClassVar[list[BindingType]] = [('ctrl+s', 'submit', 'Submit')]
    _list: SelectionList[int]

    # pylint: disable-next=too-many-arguments,too-many-positional-arguments
    def __init__(self, question: str, choices: list[str],
                 preselected: list[int], min_select: int,
                 max_select: Optional[int], messages: list[str]) -> None:
        """Store the prompt, choices, preselection and count limits."""
        super().__init__()
        self._question = question
        self._choices = choices
        self._preselected = set(preselected)
        self._min_select = min_select
        self._max_select = max_select
        self._messages = messages

    def compose(self) -> ComposeResult:
        """Lay out the header, the check-box list, submit and footer."""
        yield from _header_widgets(self._messages, self._question)
        self._list = SelectionList[int](*self._selections())
        yield self._list
        yield Button('Submit', id='submit')
        yield Static('', id='multi_error')
        yield Footer()

    def _selections(self) -> list[Selection[int]]:
        """Return one selection per choice, preselected as requested."""
        return [Selection(choice, index, index in self._preselected)
                for index, choice in enumerate(self._choices)]

    @on(Button.Pressed)
    def _clicked(self, _event: Button.Pressed) -> None:
        """Treat a click on the submit button like the submit action."""
        self.action_submit()

    def action_submit(self) -> None:
        """Exit with the selection, or show why the count is wrong."""
        chosen = list(self._list.selected)
        if self._count_ok(len(chosen)):
            self.exit(chosen)
            return
        message = _multi_count_error(self._min_select, self._max_select)
        self.query_one('#multi_error', Static).update(message)

    def _count_ok(self, count: int) -> bool:
        """Return whether count is within the allowed selection range."""
        if count < self._min_select:
            return False
        return self._max_select is None or count <= self._max_select


def _default_index(choices: Sequence[str],
                   default: Optional[str]) -> Optional[int]:
    """Return the index of default within choices, or None."""
    if default is not None and default in choices:
        return list(choices).index(default)
    return None


def _preselected(choices: Sequence[str],
                 default: Optional[Sequence[str]]) -> list[int]:
    """Return the indexes of the default values within choices."""
    if default is None:
        return []
    wanted = set(default)
    return [index for index, choice in enumerate(choices)
            if choice in wanted]


class WizardUiBridgeTextual(WizardUiBridge):
    """Bridge between the wizard and a Textual terminal interface.

    Each ask method runs a short-lived Textual application for one
    question and returns its result. Validation diagnostics written to
    error_file() and messages passed to show() are buffered and rendered
    in the header of the next question's screen, so nothing reaches the
    terminal directly where it would corrupt the Textual display.

    This bridge draws on the controlling terminal itself, so it takes no
    streams. Use make_text_ui_bridge() to obtain this bridge when a
    terminal is available and a console bridge otherwise.
    """

    def __init__(self) -> None:
        """Start with an empty diagnostics buffer and message list."""
        self._error_buffer = StringIO()
        self._pending: list[str] = []

    def ask(self, question: str, re_ask_reason: Optional[str] = None,
            choices: Optional[Sequence[str]] = None) -> str | int:
        """Ask one question; see WizardUiBridge.ask."""
        messages = self._collect(re_ask_reason)
        if choices is None:
            return self._run(_TextApp(question, messages))
        return self._run(_ChoiceApp(question, list(choices), None, messages))

    def ask_yes_no(self, question: str, default: bool,
                   re_ask_reason: Optional[str] = None) -> bool:
        """Ask a yes/no question; see WizardUiBridge.ask_yes_no."""
        messages = self._collect(re_ask_reason)
        default_index = 0 if default else 1
        chosen = self._run(_ChoiceApp(question, ['yes', 'no'], default_index,
                                      messages))
        return chosen == 0

    def ask_choice(self, question: str, *, choices: Sequence[str],
                   default: Optional[str] = None,
                   re_ask_reason: Optional[str] = None) -> str:
        """Ask the user to pick one choice; see ask_choice."""
        messages = self._collect(re_ask_reason)
        index = self._run(_ChoiceApp(question, list(choices),
                                     _default_index(choices, default),
                                     messages))
        return choices[index]

    # pylint: disable-next=too-many-arguments
    def ask_multi(self, question: str, *, choices: Sequence[str],
                  default: Optional[Sequence[str]] = None, min_select: int = 0,
                  max_select: Optional[int] = None,
                  re_ask_reason: Optional[str] = None) -> list[str]:
        """Ask the user to pick several choices; see ask_multi."""
        messages = self._collect(re_ask_reason)
        chosen = self._run(_MultiApp(question, list(choices),
                                     _preselected(choices, default),
                                     min_select, max_select, messages))
        return [choices[index] for index in sorted(chosen)]

    def _run(self, app: _NavApp[_T]) -> _T:
        """Run one screen and translate its outcome.

        A recorded navigation request is re-raised. A screen that ends
        with no value, such as the built-in quit, is treated as an
        abort.
        """
        result = self._launch(app)
        if app.nav is not None:
            raise app.nav()
        if result is None:
            raise WizardAbort()
        return result

    def _launch(self, app: _NavApp[_T]) -> Optional[_T]:
        """Run the app and return its result.

        This is the only place that drives the terminal, so tests
        override it to exercise the bridge without a real terminal.
        """
        return app.run()

    def _collect(self, re_ask_reason: Optional[str]) -> list[str]:
        """Drain buffered messages and append any re-ask reason."""
        lines = self._drain_messages()
        if re_ask_reason is not None:
            lines.append(re_ask_reason)
        return lines

    def _drain_messages(self) -> list[str]:
        """Return and clear buffered show() and diagnostic lines."""
        text = self._error_buffer.getvalue()
        self._error_buffer.seek(0)
        self._error_buffer.truncate(0)
        diagnostics = [line for line in text.splitlines() if line]
        lines = self._pending + diagnostics
        self._pending = []
        return lines

    def error_file(self) -> StringIO:
        """Return the in-memory stream shown on the next screen."""
        return self._error_buffer

    def show(self, message: str) -> None:
        """Buffer a message for the next question's screen.

        A message shown when no further question follows is not
        displayed, because only a Textual screen renders it.
        """
        self._pending.append(message)
