#! /usr/bin/env python3
"""Tests for the form question types and the base ask_form fallback."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional, Sequence

import pytest

from tableio_cfg_json import AskField, AskChoiceField, AskIntField, \
    AskMultiChoiceField, AskPathField, AskTextField, AskYesNoField, \
    AnswerChoiceField, AnswerIntField, AnswerMultiChoiceField, \
    AnswerPathField, AnswerTextField, AnswerYesNoField, \
    PartFormValidationResult, PartialFormValidator, PathAskOptions, \
    WizardBack, WizardUiBridge
from tableio_cfg_json._wizard_ui_bridge_form import initial_answer


class _FormBridge(WizardUiBridge):
    """Bridge that feeds scripted answers to the typed ask methods.

    A scripted answer that is an exception is raised, so a test can make
    a particular field request navigation. Shown messages and the order
    of asked fields are recorded for inspection.
    """

    def __init__(self, answers: Sequence[object]) -> None:
        """Store scripted answers and empty shown and asked logs."""
        self._answers = list(answers)
        self.shown: list[str] = []
        self.asked: list[str] = []

    def _next(self) -> object:
        """Return the next scripted answer, raising a scripted exception."""
        item = self._answers.pop(0)
        if isinstance(item, BaseException):
            raise item
        return item

    def show(self, message: str) -> None:
        """Record a shown message."""
        self.shown.append(message)

    def ask_text(self, question: str, re_ask_reason: Optional[str] = None,
                 nullable: bool = False, *, default: Optional[str] = None,
                 sensitive: bool = False) -> Optional[str]:
        """Return the next scripted text answer."""
        self.asked.append(question)
        answer = self._next()
        assert answer is None or isinstance(answer, str)
        return answer

    # pylint: disable-next=too-many-arguments
    def ask_int(self, question: str, re_ask_reason: Optional[str] = None, *,
                nullable: bool = False, min_value: Optional[int] = None,
                max_value: Optional[int] = None,
                default: Optional[int] = None) -> Optional[int]:
        """Return the next scripted integer answer."""
        self.asked.append(question)
        answer = self._next()
        assert answer is None or isinstance(answer, int)
        return answer

    def ask_path(self, question: str, re_ask_reason: Optional[str] = None, *,
                 options: Optional[PathAskOptions] = None) -> Optional[Path]:
        """Return the next scripted path answer."""
        self.asked.append(question)
        answer = self._next()
        assert answer is None or isinstance(answer, Path)
        return answer

    def ask_yes_no(self, question: str, default: bool,
                   re_ask_reason: Optional[str] = None) -> bool:
        """Return the next scripted yes/no answer."""
        self.asked.append(question)
        answer = self._next()
        assert isinstance(answer, bool)
        return answer

    def ask_choice(self, question: str, *, choices: Sequence[str],
                   default: Optional[str] = None,
                   re_ask_reason: Optional[str] = None) -> str:
        """Return the next scripted choice answer."""
        self.asked.append(question)
        answer = self._next()
        assert isinstance(answer, str)
        return answer

    # pylint: disable-next=too-many-arguments
    def ask_multi(self, question: str, *, choices: Sequence[str],
                  default: Optional[Sequence[str]] = None, min_select: int = 0,
                  max_select: Optional[int] = None,
                  re_ask_reason: Optional[str] = None) -> list[str]:
        """Return the next scripted multi-choice answer."""
        self.asked.append(question)
        answer = self._next()
        assert isinstance(answer, list)
        return answer


def _all_fields() -> tuple[AskTextField, AskIntField, AskYesNoField,
                           AskChoiceField, AskMultiChoiceField]:
    """Return one field of each kind, in a fixed order."""
    return (AskTextField('Name', None),
            AskIntField('Age', None, default=30),
            AskYesNoField('Sub?', None, True),
            AskChoiceField('Color', None, choices=('red', 'green', 'blue')),
            AskMultiChoiceField('Tags', None, choices=('a', 'b', 'c')))


def test_int_bad_range() -> None:
    """An integer field with min greater than max is rejected."""
    with pytest.raises(ValueError, match='min_value'):
        AskIntField('N', None, min_value=5, max_value=1)


@pytest.mark.parametrize('default', [-1, 11])
def test_int_bad_default(default: int) -> None:
    """An integer field default outside the bounds is rejected."""
    with pytest.raises(ValueError, match='range'):
        AskIntField('N', None, min_value=0, max_value=10, default=default)


def test_int_good_default() -> None:
    """An integer field default within the bounds is accepted."""
    field = AskIntField('N', None, min_value=0, max_value=10, default=5)
    assert field.default == 5


def test_text_secret_default() -> None:
    """A sensitive text field cannot carry a default."""
    with pytest.raises(ValueError, match='default'):
        AskTextField('P', None, default='x', sensitive=True)


def test_choice_nullable() -> None:
    """A choice answer accepts None to signal a not-yet-answered choice."""
    field = AskChoiceField('C', None, choices=('x',))
    assert AnswerChoiceField(field, None).value is None


def test_initial_answers() -> None:
    """initial_answer returns each field's default as its start value."""
    text, integer, yes_no, choice, multi = _all_fields()
    assert initial_answer(text) == AnswerTextField(text, None)
    assert initial_answer(integer) == AnswerIntField(integer, 30)
    assert initial_answer(yes_no) == AnswerYesNoField(yes_no, True)
    assert initial_answer(choice) == AnswerChoiceField(choice, None)
    assert initial_answer(multi) == AnswerMultiChoiceField(multi, [])


def test_initial_path_default(tmp_path: Path) -> None:
    """A path field starts from the default kept in its path options."""
    field = AskPathField('P', None, PathAskOptions(default=tmp_path))
    assert initial_answer(field) == AnswerPathField(field, tmp_path)


def test_initial_multi() -> None:
    """A multi-choice field starts from a copy of its default values."""
    field = AskMultiChoiceField('T', None, choices=('a', 'b'), default=('a',))
    assert initial_answer(field) == AnswerMultiChoiceField(field, ['a'])


def test_form_in_order() -> None:
    """ask_form returns one answer per field, in field order."""
    fields = _all_fields()
    bridge = _FormBridge(['Tom', 42, False, 'green', ['a', 'c']])
    answers = bridge.ask_form('Fill this', fields)
    assert [answer.value for answer in answers] == \
        ['Tom', 42, False, 'green', ['a', 'c']]
    assert [answer.asking for answer in answers] == list(fields)


def test_form_shows_prompt() -> None:
    """ask_form shows the long question and the re-ask reason first."""
    bridge = _FormBridge(['Tom'])
    bridge.ask_form('Please fill', [AskTextField('Name', None)],
                    re_ask_reason='try again')
    assert bridge.shown[:2] == ['Please fill', 'try again']


def test_form_shows_help() -> None:
    """ask_form shows a field's help text before asking it."""
    bridge = _FormBridge(['Tom'])
    bridge.ask_form('Q', [AskTextField('Name', 'your full name')])
    assert 'your full name' in bridge.shown


def test_form_partial_message() -> None:
    """A not-valid partial result shows its message to the user."""
    def validator(answers: Sequence[object],
                  index: int) -> PartFormValidationResult:
        _ = (answers, index)
        return PartFormValidationResult(False, 'looks wrong')
    bridge = _FormBridge(['Tom'])
    bridge.ask_form('Q', [AskTextField('Name', None)],
                    partial_validator=validator)
    assert 'looks wrong' in bridge.shown


def test_form_partial_disable(toggle_fields: list[AskField],
                              toggle_validator: PartialFormValidator) -> None:
    """A disabled field is not asked and keeps its start value."""
    bridge = _FormBridge([False])
    answers = bridge.ask_form('Q', toggle_fields,
                              partial_validator=toggle_validator)
    assert bridge.asked == ['Color?']
    assert answers[1].value is None


def test_form_back_steps() -> None:
    """A back request from a field re-asks the previous field."""
    fields = [AskTextField('A', None), AskTextField('B', None)]
    bridge = _FormBridge(['first', WizardBack(), 'again', 'second'])
    answers = bridge.ask_form('Q', fields)
    assert [answer.value for answer in answers] == ['again', 'second']
    assert bridge.asked == ['A', 'B', 'A', 'B']


def test_form_back_first_out() -> None:
    """A back request at the first field propagates out of ask_form."""
    bridge = _FormBridge([WizardBack()])
    with pytest.raises(WizardBack):
        bridge.ask_form('Q', [AskTextField('A', None)])


def test_form_empty() -> None:
    """An empty form returns no answers but still shows the prompt."""
    bridge = _FormBridge([])
    assert not bridge.ask_form('Nothing here', [])
    assert bridge.shown == ['Nothing here']
