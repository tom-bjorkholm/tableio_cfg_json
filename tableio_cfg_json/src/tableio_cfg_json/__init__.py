#! /usr/local/bin/python3
"""Public API for the tableio config-as-json bridge.

The wizard user interface bridge that used to be part of this package
is now the separate package wizard_ui_bridge, which does not depend on
TableIO. Its names are still available from here, deprecated, so that
applications keep working while their maintainers change the imports.
See tableio_cfg_json._moved for how the deprecation is reported.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import TYPE_CHECKING
from tableio_cfg_json.config import TioJsonConfig, TioJsonCsvConfig, \
    TioJsonHtmlConfig, TioJsonLatexConfig, tio_json_config_default
from tableio_cfg_json.describe import describe_config, \
    describe_config_example, describe_config_members, \
    describe_config_reference, get_config_member_names, get_general_cfg_info
from tableio_cfg_json.wizard import tio_json_config_wizard
from tableio_cfg_json._moved import MOVED_NAMES, WizardUiBridgeMoved, \
    moved_attr
if TYPE_CHECKING:
    from wizard_ui_bridge import AnswerChoiceField, AnswerDateField, \
        AnswerDateTimeField, AnswerDurationField, AnswerField, AnswerFields, \
        AnswerFloatField, AnswerIntField, AnswerMultiChoiceField, \
        AnswerPathField, AnswerTextField, AnswerTimeField, AnswerYesNoField, \
        AskChoiceField, AskDateField, AskDateTimeField, AskDurationField, \
        AskField, AskFields, AskFloatField, AskIntField, \
        AskMultiChoiceField, AskPathField, \
        AskTextField, AskTimeField, AskYesNoField, PartFormValidationResult, \
        PartialCheck, PartialFormValidator, PathAskOptions, PrefillValueType, \
        PrefillValues, TableCell, TableColumn, UiBridgeType, WizardAbort, \
        WizardBack, WizardCancelLevel, WizardNavigation, WizardPathKind, \
        WizardUiBridge, WizardUiBridgeConsole, WizardUiBridgeTextual, \
        make_text_ui_bridge

__all__ = ['TioJsonConfig', 'TioJsonCsvConfig', 'TioJsonHtmlConfig',
           'TioJsonLatexConfig', 'describe_config', 'describe_config_example',
           'describe_config_members', 'describe_config_reference',
           'get_config_member_names', 'get_general_cfg_info',
           'tio_json_config_default', 'tio_json_config_wizard',
           'WizardUiBridgeMoved',
           'AnswerChoiceField', 'AnswerDateField', 'AnswerDateTimeField',
           'AnswerDurationField', 'AnswerField', 'AnswerFields',
           'AnswerFloatField', 'AnswerIntField', 'AnswerMultiChoiceField',
           'AnswerPathField', 'AnswerTextField', 'AnswerTimeField',
           'AnswerYesNoField', 'AskChoiceField', 'AskDateField',
           'AskDateTimeField', 'AskDurationField', 'AskField', 'AskFields',
           'AskFloatField', 'AskIntField', 'AskMultiChoiceField',
           'AskPathField', 'AskTextField', 'AskTimeField', 'AskYesNoField',
           'PartFormValidationResult', 'PartialCheck', 'PartialFormValidator',
           'PathAskOptions', 'PrefillValueType', 'PrefillValues', 'TableCell',
           'TableColumn', 'UiBridgeType', 'WizardAbort', 'WizardBack',
           'WizardCancelLevel', 'WizardNavigation', 'WizardPathKind',
           'WizardUiBridge', 'WizardUiBridgeConsole', 'WizardUiBridgeTextual',
           'make_text_ui_bridge']
"""The names this package offers, the moved ones being deprecated."""


def __getattr__(name: str) -> object:
    """Return a moved wizard UI bridge name, warning that it moved."""
    if name not in MOVED_NAMES:
        raise AttributeError(f'module {__name__!r} has no attribute '
                             f'{name!r}')
    return moved_attr(__name__, 'wizard_ui_bridge', name)
