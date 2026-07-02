#! /usr/bin/env python3
"""Tests for wizard text defaults and bridge adaptation."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

# pylint: disable=protected-access

from typing import Optional, Sequence

import pytest

from tableio import ConfigSpec
from tableio_cfg_json import WizardUiBridge
import tableio_cfg_json.wizard as wizard_module


class _ModernBridge(WizardUiBridge):
    """Bridge that records default-aware text questions."""

    def __init__(self, answers: Sequence[str]) -> None:
        """Store text answers and start with no recorded calls."""
        self.answers = list(answers)
        self.calls: list[tuple[str, Optional[str], Optional[str]]] = []

    def ask_text(self, question: str, re_ask_reason: Optional[str] = None,
                 nullable: bool = False, *, default: Optional[str] = None,
                 sensitive: bool = False) -> Optional[str]:
        """Return scripted text, honoring the default argument."""
        _ = sensitive
        self.calls.append((question, re_ask_reason, default))
        answer = self.answers.pop(0)
        if answer == '' and default is not None:
            return default
        return None if nullable and answer == '' else answer

    def show(self, message: str) -> None:
        """Ignore shown messages."""
        _ = message


class _KwBridge(WizardUiBridge):
    """Bridge that accepts default through keyword arguments."""

    def __init__(self, answers: Sequence[str]) -> None:
        """Store text answers and start with no recorded calls."""
        self.answers = list(answers)
        self.calls: list[tuple[str, Optional[str], Optional[str]]] = []

    def ask_text(self, question: str, re_ask_reason: Optional[str] = None,
                 nullable: bool = False, **kwargs: object) -> Optional[str]:
        """Return scripted text, accepting default through kwargs."""
        default_value = kwargs.get('default')
        assert default_value is None or isinstance(default_value, str)
        default = default_value
        self.calls.append((question, re_ask_reason, default))
        answer = self.answers.pop(0)
        if answer == '' and default is not None:
            return default
        return None if nullable and answer == '' else answer

    def show(self, message: str) -> None:
        """Ignore shown messages."""
        _ = message


class _OldBridge(WizardUiBridge):
    """Bridge with the old ask_text signature."""

    def __init__(self, answers: Sequence[str]) -> None:
        """Store text answers and start with no recorded calls."""
        self.answers = list(answers)
        self.calls: list[tuple[str, Optional[str]]] = []

    # pylint: disable-next=arguments-differ
    def ask_text(self, question: str,  # type: ignore[override]
                 re_ask_reason: Optional[str] = None,
                 nullable: bool = False) -> Optional[str]:
        """Return scripted text using the old signature."""
        self.calls.append((question, re_ask_reason))
        answer = self.answers.pop(0)
        return None if nullable and answer == '' else answer

    def show(self, message: str) -> None:
        """Ignore shown messages."""
        _ = message


def _int_spec(default: Optional[str]) -> ConfigSpec:
    """Return an integer config spec with an optional default text."""
    return ConfigSpec('line_length', 'Line length.', 'Optional[int]', default)


def _str_spec(default: Optional[str]) -> ConfigSpec:
    """Return a string config spec with an optional default text."""
    desc = 'Character encoding.'
    return ConfigSpec('encoding', desc, 'Optional[str]', default)


def test_modern_default() -> None:
    """The wizard passes concrete defaults to modern bridges."""
    bridge = _ModernBridge([''])
    value = wizard_module._ask_text_member_value(_int_spec('72'), bridge, None)
    assert value == 72
    assert bridge.calls == [('line_length:\nLine length.\nType: '
                             'Optional[int]\nPress Enter to use the '
                             'default.', None, '72')]


def test_kwargs_default() -> None:
    """The wizard recognizes bridges that accept arbitrary keywords."""
    bridge = _KwBridge([''])
    value = wizard_module._ask_text_member_value(_int_spec('64'), bridge, None)
    assert value == 64
    assert bridge.calls[0][2] == '64'


def test_old_default_warns() -> None:
    """Old bridges get a warning and a bracketed prompt fallback."""
    bridge = _OldBridge([''])
    with pytest.warns(DeprecationWarning, match='_OldBridge.*default keyword'):
        value = wizard_module._ask_text_member_value(_int_spec('80'), bridge,
                                                     None)
    assert value == 80
    assert bridge.calls[0][0].endswith('Press Enter to use the default. [80]')


def test_bad_default_skipped() -> None:
    """Unparseable integer default text is not passed as a default."""
    bridge = _ModernBridge([''])
    assert wizard_module._ask_text_member_value(_int_spec('automatic'), bridge,
                                                None) is None
    assert bridge.calls[0][2] is None


def test_none_description_skipped() -> None:
    """None-means descriptions are not treated as concrete strings."""
    bridge = _ModernBridge([''])
    spec = _str_spec('None means backend default.')
    assert wizard_module._ask_text_member_value(spec, bridge, None) is None
    assert bridge.calls[0][2] is None


def test_invalid_retry_keeps_default() -> None:
    """A retry keeps passing the default and shows the parse error."""
    bridge = _ModernBridge(['bad', ''])
    value = wizard_module._ask_text_member_value(_int_spec('40'), bridge, None)
    assert value == 40
    assert bridge.calls[1][1] is not None
    assert bridge.calls[1][2] == '40'


def test_member_default_helper() -> None:
    """The default helper returns only concrete parseable values."""
    assert wizard_module._member_default(_int_spec('12')) == '12'
    assert wizard_module._member_default(_int_spec('auto')) is None
    assert wizard_module._member_default(_str_spec('utf-8')) == 'utf-8'
    assert wizard_module._member_default(
        _str_spec('None means backend default.')) is None
