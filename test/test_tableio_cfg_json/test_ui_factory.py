#! /usr/bin/env python3
"""Tests for make_text_ui_bridge and the UiBridgeType selection."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

# pylint: disable=protected-access

import importlib
import sys
from io import StringIO

import pytest

import tableio_cfg_json
import tableio_cfg_json.wizard_ui_factory as wizard_factory
from tableio_cfg_json import UiBridgeType, WizardUiBridgeConsole, \
    WizardUiBridgeTextual, make_text_ui_bridge


class _TtyStream(StringIO):
    """In-memory stream that reports itself as a terminal."""

    def isatty(self) -> bool:
        """Pretend to be a terminal so the factory picks Textual."""
        return True


def _stream(is_tty: bool) -> StringIO:
    """Return a terminal-like stream when is_tty, else a plain one."""
    return _TtyStream() if is_tty else StringIO()


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
    """Forcing TEXTUAL without the Textual bridge raises RuntimeError."""
    monkeypatch.setattr(wizard_factory, '_TEXTUAL', None)
    blank = StringIO()
    with pytest.raises(RuntimeError, match='not installed'):
        make_text_ui_bridge(blank, blank, blank, UiBridgeType.TEXTUAL)


def test_import_no_textual() -> None:
    """Without the Textual bridge the factory falls back to console."""
    key = 'tableio_cfg_json.wizard_ui_bridge_textual'
    saved = sys.modules.get(key)
    sys.modules[key] = None  # type: ignore[assignment]
    try:
        importlib.reload(wizard_factory)
        importlib.reload(tableio_cfg_json)
        assert wizard_factory._TEXTUAL is None
        ttys = (_TtyStream(), _TtyStream(), _TtyStream())
        bridge = wizard_factory.make_text_ui_bridge(*ttys)
        assert isinstance(bridge, WizardUiBridgeConsole)
    finally:
        if saved is not None:
            sys.modules[key] = saved
        else:
            sys.modules.pop(key, None)
        importlib.reload(wizard_factory)
        importlib.reload(tableio_cfg_json)


def test_enum_members() -> None:
    """The enum offers exactly AUTO, TEXTUAL and CONSOLE."""
    names = [member.name for member in UiBridgeType]
    assert names == ['AUTO', 'TEXTUAL', 'CONSOLE']


def test_enum_exported() -> None:
    """The enum is part of the package public API."""
    assert 'UiBridgeType' in tableio_cfg_json.__all__
