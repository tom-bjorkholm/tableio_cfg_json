#! /usr/bin/env python3
"""Tests for base WizardUiBridge text, integer and path helpers."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import warnings
from pathlib import Path
from typing import Optional, Sequence

import pytest

from tableio_cfg_json import PathAskOptions as PublicPathAskOptions, \
    WizardPathKind as PublicPathKind, WizardUiBridge
from tableio_cfg_json.wizard_ui_bridge import PathAskOptions, WizardPathKind


class _TextBridge(WizardUiBridge):
    """Bridge that feeds scripted text answers to base helper methods."""

    def __init__(self, answers: Sequence[str | int | BaseException]) -> None:
        """Store scripted answers and start with an empty call log."""
        self.answers: list[str | int | BaseException] = list(answers)
        self.calls: list[tuple[str, Optional[str]]] = []

    def _next(self) -> str | int:
        """Return the next scripted answer, raising scripted exceptions."""
        try:
            answer = self.answers.pop(0)
        except IndexError as error:
            raise EOFError('No scripted answer left.') from error
        if isinstance(answer, BaseException):
            raise answer
        return answer

    def ask_text(self, question: str, re_ask_reason: Optional[str] = None,
                 nullable: bool = False, *, default: Optional[str] = None,
                 sensitive: bool = False) -> Optional[str]:
        """Return the next scripted answer using ask_text semantics."""
        if sensitive and default is not None:
            raise ValueError('default is not allowed for sensitive input')
        self.calls.append((question, re_ask_reason))
        return _scripted_text(self._next(), nullable, default)

    def show(self, message: str) -> None:
        """Ignore shown messages."""
        _ = message


def _scripted_text(answer: str | int, nullable: bool,
                   default: Optional[str]) -> Optional[str]:
    """Return ask_text semantics for one scripted raw answer."""
    text = answer if isinstance(answer, str) else str(answer)
    if text == '' and default is not None:
        return default
    return None if (nullable and text == '') else text


def test_path_api_exported() -> None:
    """The package root exports the path question API."""
    assert PublicPathAskOptions is PathAskOptions
    assert PublicPathKind is WizardPathKind


with warnings.catch_warnings():
    warnings.simplefilter('ignore', DeprecationWarning)

    class _OldBridge(WizardUiBridge):
        """Old bridge that only implements deprecated ask()."""

        def __init__(self, answers: Sequence[str | int]) -> None:
            """Store scripted raw answers returned in order by ask()."""
            self.answers: list[str | int] = list(answers)

        def ask(self, question: str, re_ask_reason: Optional[str] = None,
                choices: Optional[Sequence[str]] = None) -> str | int:
            """Return the next scripted raw answer."""
            _ = (question, re_ask_reason, choices)
            try:
                return self.answers.pop(0)
            except IndexError as error:
                raise EOFError('No scripted answer left.') from error

        def show(self, message: str) -> None:
            """Ignore shown messages."""
            _ = message


def test_text_default() -> None:
    """The ask_text fallback returns default for an empty answer."""
    bridge = _OldBridge([''])
    with pytest.warns(DeprecationWarning, match='ask_text'):
        assert bridge.ask_text('q', default='fallback') == 'fallback'


def test_text_sensitive() -> None:
    """The deprecated ask() fallback refuses sensitive text input."""
    bridge = _OldBridge(['secret'])
    with pytest.raises(NotImplementedError, match='sensitive'):
        bridge.ask_text('q', sensitive=True)


def test_text_secret_default() -> None:
    """Sensitive text questions reject defaults."""
    bridge = _OldBridge([''])
    with pytest.raises(ValueError, match='default'):
        bridge.ask_text('q', default='secret', sensitive=True)


def test_int_default() -> None:
    """An empty integer answer selects the default."""
    bridge = _TextBridge([''])
    assert bridge.ask_int('How many?', default=12) == 12


def test_int_default_range() -> None:
    """An integer default must be inside the allowed range."""
    bridge = _TextBridge([])
    with pytest.raises(AssertionError):
        bridge.ask_int('How many?', min_value=1, max_value=5, default=9)


def _path_case_paths(tmp_path: Path) -> dict[str, Path]:
    """Return existing and missing paths for path validation tests."""
    file_path = tmp_path / 'file.txt'
    file_path.write_text('content', encoding='utf-8')
    dir_path = tmp_path / 'folder'
    dir_path.mkdir()
    return {
        'file': file_path,
        'dir': dir_path,
        'missing_file': tmp_path / 'missing.txt',
        'missing_dir': tmp_path / 'missing_dir'}


@pytest.mark.parametrize(
    'kind, bad_key, good_key, error', [
        (WizardPathKind.EXISTING_FILE, 'missing_file', 'file',
         'does not exist'),
        (WizardPathKind.NON_EXISTING_FILE, 'file', 'missing_file',
         'already exists'),
        (WizardPathKind.FILE, 'dir', 'missing_file', 'not a file'),
        (WizardPathKind.EXISTING_DIR, 'missing_dir', 'dir',
         'does not exist'),
        (WizardPathKind.NON_EXISTING_DIR, 'dir', 'missing_dir',
         'already exists'),
        (WizardPathKind.DIR, 'file', 'missing_dir', 'not a directory')])
def test_path_kind(tmp_path: Path, kind: WizardPathKind, bad_key: str,
                   good_key: str, error: str) -> None:
    """ask_path re-asks until the answer satisfies its path kind."""
    paths = _path_case_paths(tmp_path)
    bridge = _TextBridge([str(paths[bad_key]), str(paths[good_key])])
    options = PathAskOptions(kind=kind)
    assert bridge.ask_path('Path?', options=options) == paths[good_key]
    assert error in (bridge.calls[1][1] or '')


def test_path_nullable() -> None:
    """A nullable empty path answer is reported as None."""
    bridge = _TextBridge([''])
    options = PathAskOptions(nullable=True)
    assert bridge.ask_path('Path?', options=options) is None


def test_path_default(tmp_path: Path) -> None:
    """An empty path answer selects the default path."""
    paths = _path_case_paths(tmp_path)
    options = PathAskOptions(kind=WizardPathKind.EXISTING_FILE,
                             default=paths['file'])
    result = _TextBridge(['']).ask_path('Path?', options=options)
    assert result == paths['file']


def test_path_empty(tmp_path: Path) -> None:
    """A non-nullable empty path answer is rejected."""
    paths = _path_case_paths(tmp_path)
    bridge = _TextBridge(['', str(paths['file'])])
    assert bridge.ask_path('Path?') == paths['file']
    assert 'enter a path' in (bridge.calls[1][1] or '')
