#! /usr/bin/env python3
"""Shared helpers for the supports_form_field bridge tests.

These build one instance of every supported form field type and a
throwaway field type that no bridge supports, so the console and Textual
support tests share the same field samples.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from dataclasses import dataclass
from typing import cast
from tableio_cfg_json import AskField, AskTextField, AskIntField, \
    AskPathField, AskYesNoField, AskChoiceField, AskMultiChoiceField, \
    AskFloatField, AskDateField, AskTimeField, AskDateTimeField, \
    AskDurationField, PathAskOptions
from tableio_cfg_json.wizard_ui_bridge_form_defs import AskFieldCommon


def all_ask_fields() -> list[AskField]:
    """Return one field of every supported form field type."""
    return [AskTextField('Text', None), AskIntField('Int', None),
            AskPathField('Path', None, PathAskOptions()),
            AskYesNoField('Flag', None, False),
            AskChoiceField('One', None, choices=('a', 'b')),
            AskMultiChoiceField('Many', None, choices=('a', 'b')),
            AskFloatField('Rate', None), AskDateField('Day', None),
            AskTimeField('At', None), AskDateTimeField('When', None),
            AskDurationField('For', None)]


@dataclass
class UnknownField(AskFieldCommon):
    """A form field type that no bridge supports, for rejection tests."""


def unknown_field() -> AskField:
    """Return a field of a type that no bridge supports.

    The instance is an UnknownField, which is not one of the AskField
    types, so the cast deliberately lies about its type to exercise the
    runtime rejection path of supports_form_field().
    """
    return cast(AskField, UnknownField('x', None))
