#! /usr/local/bin/python3
"""Helpers shared by the WizardUiBridge form question."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from tableio_cfg_json.wizard_ui_bridge_form_defs import AskField, \
    AnswerField, AskTextField, AskIntField, AskPathField, AskYesNoField, \
    AskChoiceField, AskMultiChoiceField, AnswerTextField, AnswerIntField, \
    AnswerPathField, AnswerYesNoField, AnswerChoiceField, \
    AnswerMultiChoiceField


def initial_answer(field: AskField) -> AnswerField:
    """Return the starting answer for a field before the user edits it.

    The value is the field's default, or the empty or not-yet-answered
    state when the field has no default. A choice field with no default
    starts as None, which tells a partial validator the choice is not
    answered yet; a bridge must not leave that None in a submitted form.
    """
    if isinstance(field, AskTextField):
        return AnswerTextField(field, field.default)
    if isinstance(field, AskIntField):
        return AnswerIntField(field, field.default)
    if isinstance(field, AskPathField):
        return AnswerPathField(field, field.path_options.default)
    if isinstance(field, AskYesNoField):
        return AnswerYesNoField(field, field.default)
    if isinstance(field, AskChoiceField):
        return AnswerChoiceField(field, field.default)
    assert isinstance(field, AskMultiChoiceField)
    values = [] if field.default is None else list(field.default)
    return AnswerMultiChoiceField(field, values)
