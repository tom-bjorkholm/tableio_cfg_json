#! /usr/local/bin/python3
"""Reusable path-input machinery for the Textual wizard bridge.

The directory tree, the editable path input and the logic that fills
the input from a tree selection are shared between the standalone path
question and the directory picker opened from a form path field. This
module holds that shared machinery: the path helpers, the _PathPick
mixin that any host screen uses, and the _PickerScreen modal that a form
opens for one path field.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from __future__ import annotations
import os
from pathlib import Path
from typing import ClassVar, Iterator, Optional
from textual import on
from textual.app import ComposeResult
from textual.binding import BindingType
from textual.message_pump import MessagePump
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Button, DirectoryTree, Footer, Input
from tableio_cfg_json.wizard_ui_bridge_arg_types import PathAskOptions, \
    WizardPathKind

_PATH_INPUT_ID = 'path_input'
_PATH_TREE_ID = 'path_tree'


def _start_dir(default: Optional[Path]) -> Path:
    """Return the directory tree root for a path question."""
    if default is None:
        return Path.cwd()
    try:
        if default.exists() and default.is_dir():
            return default
        parent = default.parent
        if parent.exists() and parent.is_dir():
            return parent
    except OSError:
        pass
    return Path.cwd()


def _start_value(value: Optional[str], default: Optional[Path]) -> str:
    """Return the initial path input text."""
    if value is not None:
        return value
    return '' if default is None else str(default)


def _new_child_prefix(path: Path) -> str:
    """Return path text ready for appending a child name."""
    text = str(path)
    return text if text.endswith(os.sep) else text + os.sep


def _selection_text(path: Path, is_dir: bool, kind: WizardPathKind) -> str:
    """Return the input text to use for a selected path."""
    if is_dir and kind in (WizardPathKind.EXISTING_FILE,
                           WizardPathKind.NON_EXISTING_FILE,
                           WizardPathKind.FILE,
                           WizardPathKind.NON_EXISTING_DIR):
        return _new_child_prefix(path)
    return str(path)


def _seed_path(value: str, default: Optional[Path]) -> Optional[Path]:
    """Return the path whose folder roots the picker's tree."""
    return Path(value) if value else default


class _PathPick(MessagePump):
    """Fill a path input from a directory-tree selection.

    A host lays out the tree and input with pick_widgets(), keeps the
    wanted WizardPathKind in _kind, and implements _confirm() to consume
    the confirmed path text. Selecting in the tree fills the input;
    Return in the input or the submit action confirms the current text.
    It derives from MessagePump so that its @on handlers register when it
    is mixed into a host screen or app.
    """

    _kind: WizardPathKind
    _path_input: Input

    def pick_widgets(self, start: Path, value: str) -> Iterator[Widget]:
        """Yield the directory tree and the editable path input."""
        yield DirectoryTree(start, id=_PATH_TREE_ID)
        self._path_input = Input(value=value, id=_PATH_INPUT_ID)
        yield self._path_input

    @on(DirectoryTree.FileSelected)
    def _file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """Use the selected file as the editable input value."""
        self._fill_input(event.path, is_dir=False)

    @on(DirectoryTree.DirectorySelected)
    def _dir_selected(self, event: DirectoryTree.DirectorySelected) -> None:
        """Use the selected directory as value or editable prefix."""
        self._fill_input(event.path, is_dir=True)

    @on(Input.Submitted, f'#{_PATH_INPUT_ID}')
    def _input_entered(self, event: Input.Submitted) -> None:
        """Confirm the entered path when Return is pressed."""
        self._confirm(event.value)

    def action_submit(self) -> None:
        """Confirm the current editable path input."""
        self._confirm(self._path_input.value)

    def _fill_input(self, path: Path, is_dir: bool) -> None:
        """Set the input from a tree selection and move focus there."""
        value = _selection_text(path, is_dir, self._kind)
        self._path_input.value = value
        self._path_input.cursor_position = len(value)
        self._path_input.focus()

    def _confirm(self, value: str) -> None:
        """Consume the confirmed path text; overridden by the host."""
        raise NotImplementedError


class _PickerScreen(_PathPick, ModalScreen[Optional[str]]):
    """Modal directory picker that fills a form path field.

    It shows a directory tree and an editable path input, like the
    standalone path question. Selecting in the tree fills the input;
    Submit or Return returns the text to the form, while Cancel or
    Escape returns nothing so the field keeps its current value.
    """

    BINDINGS: ClassVar[list[BindingType]] = [
        ('ctrl+s', 'submit', 'Submit'), ('escape', 'cancel', 'Cancel')]
    CSS = '#path_tree { height: 1fr; }'

    def __init__(self, options: PathAskOptions, value: str) -> None:
        """Store the path kind and the tree root and initial input."""
        super().__init__()
        self._kind = options.kind
        self._start = _start_dir(_seed_path(value, options.default))
        self._value = value

    def compose(self) -> ComposeResult:
        """Lay out the tree, the path input and the buttons."""
        yield from self.pick_widgets(self._start, self._value)
        yield Button('Submit', id='submit')
        yield Button('Cancel', id='cancel')
        yield Footer()

    @on(Button.Pressed, '#submit')
    def _submit_clicked(self, _event: Button.Pressed) -> None:
        """Submit the picked path when the submit button is pressed."""
        self.action_submit()

    @on(Button.Pressed, '#cancel')
    def _cancel_clicked(self, _event: Button.Pressed) -> None:
        """Close without changing the field when cancel is pressed."""
        self.action_cancel()

    def action_cancel(self) -> None:
        """Close the picker without returning a path."""
        self.dismiss(None)

    def _confirm(self, value: str) -> None:
        """Return the confirmed path text to the form."""
        self.dismiss(value)
