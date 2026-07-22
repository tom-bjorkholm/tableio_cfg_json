#! /usr/local/bin/python3
"""Public API for the tableio config-as-json bridge."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from tableio_cfg_json.config import TioJsonConfig, TioJsonCsvConfig, \
    TioJsonHtmlConfig, TioJsonLatexConfig, tio_json_config_default
from tableio_cfg_json.describe import describe_config, \
    describe_config_example, describe_config_members, \
    describe_config_reference, get_config_member_names, get_general_cfg_info
from tableio_cfg_json.wizard import tio_json_config_wizard
from tableio_cfg_json.wizard_ui_bridge import WizardUiBridge
from tableio_cfg_json.wizard_ui_bridge_arg_types import PartialCheck, \
    TableCell, PathAskOptions, TableColumn, WizardAbort, WizardBack, \
    WizardCancelLevel, WizardNavigation, WizardPathKind
from tableio_cfg_json.wizard_ui_bridge_console import WizardUiBridgeConsole
from tableio_cfg_json.wizard_ui_bridge_form_defs import AskField, AskFields, \
    AnswerField, AnswerFields, PartialFormValidator, \
    PartFormValidationResult, PrefillValues, PrefillValueType, AskTextField, \
    AskIntField, AskPathField, AskYesNoField, AskChoiceField, \
    AskMultiChoiceField, AskFloatField, AskDateField, AskTimeField, \
    AskDateTimeField, AskDurationField, AnswerTextField, AnswerIntField, \
    AnswerPathField, AnswerYesNoField, AnswerChoiceField, \
    AnswerMultiChoiceField, AnswerFloatField, AnswerDateField, \
    AnswerTimeField, AnswerDateTimeField, AnswerDurationField
from tableio_cfg_json.wizard_ui_factory import make_text_ui_bridge, \
    UiBridgeType
try:
    from tableio_cfg_json.wizard_ui_bridge_textual import \
        WizardUiBridgeTextual
except ImportError:
    pass

__all__ = ['TioJsonConfig', 'TioJsonCsvConfig', 'TioJsonHtmlConfig',
           'TioJsonLatexConfig', 'describe_config',
           'describe_config_example', 'describe_config_members',
           'describe_config_reference', 'get_config_member_names',
           'get_general_cfg_info', 'tio_json_config_default',
           'tio_json_config_wizard', 'WizardUiBridge',
           'WizardUiBridgeConsole', 'WizardNavigation', 'WizardBack',
           'WizardCancelLevel', 'WizardAbort', 'TableColumn', 'TableCell',
           'PartialCheck', 'make_text_ui_bridge', 'WizardUiBridgeTextual',
           'UiBridgeType', 'PathAskOptions', 'WizardPathKind',
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
