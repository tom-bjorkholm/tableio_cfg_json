#! /usr/bin/env python3
"""Tests for the option-form field defaults built by the wizard."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

# pylint: disable=protected-access

from typing import Optional
import pytest
from tableio import ConfigSpec
from tableio_cfg_json import AskChoiceField, AskIntField, AskTextField
import tableio_cfg_json.wizard as wizard_module


def _int_spec(default: Optional[str]) -> ConfigSpec:
    """Return an integer config spec with an optional default text."""
    return ConfigSpec('line_length', 'Line length.', 'Optional[int]', default)


def _str_spec(default: Optional[str]) -> ConfigSpec:
    """Return a string config spec with an optional default text."""
    return ConfigSpec('encoding', 'Character encoding.', 'Optional[str]',
                      default)


def _choice_spec() -> ConfigSpec:
    """Return a choice config spec with two choices."""
    return ConfigSpec('csv.dialect', 'The dialect.', 'Optional[str]',
                      'None means backend default.', choices=('EXCEL', 'UNIX'))


def test_member_default() -> None:
    """The default helper returns only concrete parseable values."""
    assert wizard_module._member_default(_int_spec('12')) == '12'
    assert wizard_module._member_default(_int_spec('auto')) is None
    assert wizard_module._member_default(_str_spec('utf-8')) == 'utf-8'
    assert wizard_module._member_default(
        _str_spec('None means backend default.')) is None


@pytest.mark.parametrize('current, expected', [(7, 7), (None, 40)])
def test_int_default(current: Optional[int], expected: int) -> None:
    """An integer field starts from the current value or spec default."""
    assert wizard_module._int_default(_int_spec('40'), current) == expected


def test_int_default_none() -> None:
    """An integer field with no current value and no default is empty."""
    assert wizard_module._int_default(_int_spec(None), None) is None


@pytest.mark.parametrize('current, expected', [
    ('cp1252', 'cp1252'), (None, 'utf-8')])
def test_text_default(current: Optional[str], expected: str) -> None:
    """A text field starts from the current value or spec default."""
    assert wizard_module._text_default(_str_spec('utf-8'), current) == expected


def test_text_default_none() -> None:
    """A text field with no current value and no default is empty."""
    assert wizard_module._text_default(
        _str_spec('None means backend default.'), None) is None


def test_option_field_int() -> None:
    """An Optional[int] member becomes a nullable integer field."""
    field = wizard_module._option_field(_int_spec('None means default.'), 5)
    assert isinstance(field, AskIntField)
    assert field.nullable is True
    assert field.default == 5
    assert field.help_text == 'Line length.'


def test_option_field_text() -> None:
    """An Optional[str] member becomes a nullable text field."""
    field = wizard_module._option_field(_str_spec('None means default.'), None)
    assert isinstance(field, AskTextField)
    assert field.nullable is True
    assert field.default is None


def test_option_field_choice() -> None:
    """A member with choices becomes a choice field with a default option."""
    field = wizard_module._option_field(_choice_spec(), 'UNIX')
    assert isinstance(field, AskChoiceField)
    assert field.choices[0] == wizard_module._AUTO_MEMBER
    assert 'EXCEL' in field.choices and 'UNIX' in field.choices
    assert field.default == 'UNIX'


def test_choice_no_current() -> None:
    """A choice field with no current value uses the use-the-default option."""
    field = wizard_module._choice_field(_choice_spec(), None)
    assert field.default == wizard_module._AUTO_MEMBER
