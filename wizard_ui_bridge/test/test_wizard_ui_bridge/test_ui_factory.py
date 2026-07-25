#! /usr/bin/env python3
"""Tests for make_text_ui_bridge and the UiBridgeType selection."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

# pylint: disable=protected-access

from io import StringIO

import pytest

import wizard_ui_bridge
import wizard_ui_bridge.factory as wizard_factory
from wizard_ui_bridge import UiBridgeType, WizardUiBridgeConsole, \
    WizardUiBridgeTextual, load_textual_bridge, make_text_ui_bridge

_EXTRA = r'wizard-ui-bridge\[textual\]'


class _TtyStream(StringIO):
    """In-memory stream that reports itself as a terminal."""

    def isatty(self) -> bool:
        """Pretend to be a terminal so the factory picks Textual."""
        return True


def _stream(is_tty: bool) -> StringIO:
    """Return a terminal-like stream when is_tty, else a plain one."""
    return _TtyStream() if is_tty else StringIO()


def _hide_textual(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make the factory see the optional textual package as missing."""
    monkeypatch.setattr(wizard_factory, 'find_spec', lambda name: None)


def test_default_auto() -> None:
    """Omitting bridge_type auto-selects by terminal, like AUTO."""
    on_tty = make_text_ui_bridge(_TtyStream(), _TtyStream(), _TtyStream())
    off_tty = make_text_ui_bridge(StringIO(), StringIO(), StringIO())
    assert isinstance(on_tty, WizardUiBridgeTextual)
    assert isinstance(off_tty, WizardUiBridgeConsole)


def test_auto_textual() -> None:
    """AUTO returns the Textual bridge when both streams are terminals."""
    bridge = make_text_ui_bridge(_TtyStream(), _TtyStream(), _TtyStream(),
                                 UiBridgeType.AUTO)
    assert isinstance(bridge, WizardUiBridgeTextual)


@pytest.mark.parametrize('out_tty,in_tty', [
    (False, False), (True, False), (False, True)])
def test_auto_console(out_tty: bool, in_tty: bool) -> None:
    """AUTO falls back to console unless both streams are terminals."""
    bridge = make_text_ui_bridge(_stream(out_tty), _stream(in_tty), StringIO(),
                                 UiBridgeType.AUTO)
    assert isinstance(bridge, WizardUiBridgeConsole)


def test_auto_ignores_stderr() -> None:
    """AUTO decides on stdout and stdin only, not on stderr."""
    only_err = make_text_ui_bridge(StringIO(), StringIO(), _TtyStream(),
                                   UiBridgeType.AUTO)
    not_err = make_text_ui_bridge(_TtyStream(), _TtyStream(), StringIO(),
                                  UiBridgeType.AUTO)
    assert isinstance(only_err, WizardUiBridgeConsole)
    assert isinstance(not_err, WizardUiBridgeTextual)


@pytest.mark.parametrize('is_tty', [True, False])
def test_console_forced(is_tty: bool) -> None:
    """CONSOLE always returns the console bridge, terminal or not."""
    bridge = make_text_ui_bridge(_stream(is_tty), _stream(is_tty), StringIO(),
                                 UiBridgeType.CONSOLE)
    assert isinstance(bridge, WizardUiBridgeConsole)


def test_console_streams() -> None:
    """The forced console bridge keeps the streams it is given."""
    out, inp, err = StringIO(), StringIO(), StringIO()
    bridge = make_text_ui_bridge(out, inp, err, UiBridgeType.CONSOLE)
    assert isinstance(bridge, WizardUiBridgeConsole)
    assert bridge.stdout_file is out
    assert bridge.stdin_file is inp
    assert bridge.stderr_file is err


@pytest.mark.parametrize('is_tty', [True, False])
def test_textual_forced(is_tty: bool) -> None:
    """TEXTUAL returns the Textual bridge even without a terminal."""
    bridge = make_text_ui_bridge(_stream(is_tty), _stream(is_tty), StringIO(),
                                 UiBridgeType.TEXTUAL)
    assert isinstance(bridge, WizardUiBridgeTextual)


def test_textual_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    """Forcing TEXTUAL without textual installed names the extra."""
    _hide_textual(monkeypatch)
    blank = StringIO()
    with pytest.raises(ImportError, match=_EXTRA):
        make_text_ui_bridge(blank, blank, blank, UiBridgeType.TEXTUAL)


def test_load_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    """Loading the bridge class without textual names the extra."""
    _hide_textual(monkeypatch)
    with pytest.raises(ImportError, match=_EXTRA):
        load_textual_bridge()


def test_package_attr_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    """The package attribute for the bridge class names the extra."""
    _hide_textual(monkeypatch)
    with pytest.raises(ImportError, match=_EXTRA):
        _ = wizard_ui_bridge.WizardUiBridgeTextual


def test_auto_no_textual(monkeypatch: pytest.MonkeyPatch) -> None:
    """Without textual installed AUTO falls back to the console bridge."""
    _hide_textual(monkeypatch)
    ttys = (_TtyStream(), _TtyStream(), _TtyStream())
    assert isinstance(make_text_ui_bridge(*ttys), WizardUiBridgeConsole)


def test_console_no_textual(monkeypatch: pytest.MonkeyPatch) -> None:
    """Without textual installed CONSOLE still returns a bridge."""
    _hide_textual(monkeypatch)
    blank = StringIO()
    bridge = make_text_ui_bridge(blank, blank, blank, UiBridgeType.CONSOLE)
    assert isinstance(bridge, WizardUiBridgeConsole)


def test_enum_members() -> None:
    """The enum offers exactly AUTO, TEXTUAL and CONSOLE."""
    names = [member.name for member in UiBridgeType]
    assert names == ['AUTO', 'TEXTUAL', 'CONSOLE']


def test_enum_exported() -> None:
    """The enum is part of the package public API."""
    assert 'UiBridgeType' in wizard_ui_bridge.__all__
