#! /usr/local/bin/python3
"""Public API for the wizard user interface bridge.

A wizard asks a user a series of questions. WizardUiBridge is the
user-interface-independent way to ask them, so that one wizard can run
on a plain console, on a full-screen Textual user interface, or on any
other bridge an application implements.

The Textual bridge needs the optional textual package, installed with
the extra `wizard-ui-bridge[textual]`. Textual is imported only when
the Textual bridge is actually used, so importing this package, or
asking for WizardUiBridgeConsole, never imports Textual. Asking for
WizardUiBridgeTextual without textual installed raises ImportError
naming the extra to install.

Helpers for implementing a bridge of your own are in the modules
wizard_ui_bridge.bridge_helpers and wizard_ui_bridge.form_helpers.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import TYPE_CHECKING
from wizard_ui_bridge.bridge import WizardUiBridge
from wizard_ui_bridge.arg_types import PartialCheck, TableCell, \
    PathAskOptions, TableColumn, WizardAbort, WizardBack, WizardCancelLevel, \
    WizardNavigation, WizardPathKind
from wizard_ui_bridge.console import WizardUiBridgeConsole
from wizard_ui_bridge.form_defs import AskField, AskFields, AnswerField, \
    AnswerFields, PartialFormValidator, PartFormValidationResult, \
    PrefillValues, PrefillValueType, AskTextField, AskIntField, \
    AskPathField, AskYesNoField, AskChoiceField, AskMultiChoiceField, \
    AskFloatField, AskDateField, AskTimeField, AskDateTimeField, \
    AskDurationField, AnswerTextField, AnswerIntField, AnswerPathField, \
    AnswerYesNoField, AnswerChoiceField, AnswerMultiChoiceField, \
    AnswerFloatField, AnswerDateField, AnswerTimeField, AnswerDateTimeField, \
    AnswerDurationField
from wizard_ui_bridge.factory import make_text_ui_bridge, UiBridgeType, \
    textual_installed, load_textual_bridge
if TYPE_CHECKING:
    from wizard_ui_bridge.textual_bridge import WizardUiBridgeTextual


def __getattr__(name: str) -> object:
    """Return the Textual bridge class, imported on first use.

    Textual is an optional dependency, so the Textual bridge is not
    imported when this package is imported. Asking for it without
    textual installed raises ImportError naming the extra to install.
    """
    if name == 'WizardUiBridgeTextual':
        return load_textual_bridge()
    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')


__all__ = ['WizardUiBridge', 'WizardUiBridgeConsole', 'WizardUiBridgeTextual',
           'WizardNavigation', 'WizardBack', 'WizardCancelLevel',
           'WizardAbort', 'TableColumn', 'TableCell', 'PartialCheck',
           'make_text_ui_bridge', 'UiBridgeType', 'textual_installed',
           'load_textual_bridge', 'PathAskOptions', 'WizardPathKind',
           'AskField', 'AskFields', 'AnswerField', 'AnswerFields',
           'PartialFormValidator', 'PartFormValidationResult',
           'PrefillValues', 'PrefillValueType',
           'AskTextField', 'AskIntField', 'AskPathField', 'AskYesNoField',
           'AskChoiceField', 'AskMultiChoiceField', 'AskFloatField',
           'AskDateField', 'AskTimeField', 'AskDateTimeField',
           'AskDurationField', 'AnswerTextField',
           'AnswerIntField', 'AnswerPathField', 'AnswerYesNoField',
           'AnswerChoiceField', 'AnswerMultiChoiceField', 'AnswerFloatField',
           'AnswerDateField', 'AnswerTimeField', 'AnswerDateTimeField',
           'AnswerDurationField']
