#! /usr/bin/env python3
"""Shared fixtures for the ask_form bridge tests."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Sequence

import pytest

from tableio_cfg_json import AskField, AskChoiceField, AskYesNoField, \
    AnswerField, AnswerYesNoField, PartFormValidationResult, \
    PartialFormValidator


@pytest.fixture
def toggle_fields() -> list[AskField]:
    """Return a yes/no field that gates a following choice field."""
    return [AskYesNoField('Color?', None, True),
            AskChoiceField('Color', None, choices=('r', 'g', 'b'))]


@pytest.fixture
def toggle_validator() -> PartialFormValidator:
    """Return a validator disabling the choice when the yes/no is off."""
    def validator(answers: Sequence[AnswerField],
                  index: int) -> PartFormValidationResult:
        _ = index
        first = answers[0]
        assert isinstance(first, AnswerYesNoField)
        disable = () if first.value else (1,)
        return PartFormValidationResult(True, '', disable)
    return validator
