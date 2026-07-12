#! /usr/local/bin/python3
"""Definitions of types for wizard UI bridge forms.

Wizard UI bridge forms are used when a number of questions should preferably
be asked on a single form (in a GUI, textual or curses implementation).
For a good user experience the user should see all questions at the same time,
and the user should be able to fill in the answers in any order, and change
them before submitting the form.

In a GUI, curses or textual implementation, the form is typically displayed
in a single window, in something like a grid layout, with 2 columns and
2 - 10 rows. The left column contains the questions, and the right column
contains the input fields. Above the grid there is typically a longer question
or instruction, that explains to the user what the form is about. Below the
grid there are typically buttons for submitting the form, canceling the form,
and possibly for going back to a previous form step in a multi-step wizard.

This file defines the data types used to describe the questions and answers of
a form, and the validation callback function that is used to validate the
answers of a partly filled form.
"""

from dataclasses import dataclass
from typing import Callable, NamedTuple, Optional, Sequence, Union
from pathlib import Path
from tableio_cfg_json.wizard_ui_bridge_arg_types import PathAskOptions


@dataclass
class AskFieldCommon:
    """Common attributes of a field in a form.

    Each concrete field is one of the Ask*Field subclasses, so its Python
    type already tells the bridge which kind of input to show. There is no
    separate kind attribute to keep in sync.

    Attributes:
        short_question: A short question to be displayed to the user.
                        In a GUI implementation this is typically displayed
                        as a label in a left column next to the input field.
        help_text: Optional help text to be displayed to the user. Could be
                   used as tooltip text in a GUI implementation, or as a
                   popup message in a in response to a help button click
                   or similar user action.
    """

    short_question: str
    help_text: Optional[str]


@dataclass
class AskTextField(AskFieldCommon):
    """A text field in a form.

    Attributes:
        nullable: When True an empty answer with no default is reported
                  as None. When False an empty answer with no default is
                  the empty string.
        default: The value returned when user fills in nothing, or None for
                 no default. In a GUI implementation this is typically shown
                 as the starting value in the input field, and the user can
                 change it.
        sensitive: True when the bridge must avoid echoing the entered text,
                   such as for passwords. A default is not allowed for a
                   sensitive question.
    """

    nullable: bool = False
    default: Optional[str] = None
    sensitive: bool = False

    def __post_init__(self) -> None:
        """Check that the text field arguments are valid."""
        if self.sensitive and self.default is not None:
            raise ValueError('Sensitive text field cannot have a default')


@dataclass
class AskIntField(AskFieldCommon):
    """An integer field in a form.

    Attributes:
        nullable: When True an empty answer with no default is reported
                  as None. When False an empty answer with no default will
                  be re-asked until the user fills in a valid integer.
        default: The value returned when user fills in nothing, or None for
                 no default. In a GUI implementation this is typically shown
                 as the starting value in the input field, and the user can
                 change it.
        min_value: The minimum allowed value, or None for no minimum.
        max_value: The maximum allowed value, or None for no maximum.
    """

    nullable: bool = False
    default: Optional[int] = None
    min_value: Optional[int] = None
    max_value: Optional[int] = None

    def __post_init__(self) -> None:
        """Check that the integer bounds and default agree."""
        if (self.min_value is not None and self.max_value is not None
                and self.min_value > self.max_value):
            raise ValueError('min_value must not exceed max_value')
        if self.default is not None and (
                (self.min_value is not None and self.default < self.min_value)
                or (self.max_value is not None
                    and self.default > self.max_value)):
            raise ValueError('default is out of the allowed range')


@dataclass
class AskPathField(AskFieldCommon):
    """A path field in a form.

    In a GUI implementation this is typically displayed as a text input field
    with a button next to it that opens a file/directory chooser dialog.

    Attributes:
        path_options: Options for how the path question is asked, including
                      whether the path must exist, whether it must be a file
                      or a directory.
    """

    path_options: PathAskOptions


@dataclass
class AskYesNoField(AskFieldCommon):
    """A yes/no field in a form.

    In a GUI implementation this is typically displayed as a checkbox or a
    toggle button.

    Attributes:
        default: The boolean value used when the user makes no explicit
                 choice. In a GUI implementation this is typically shown as
                 the starting value in the checkbox or toggle, and the user
                 can change it.
    """

    default: bool


@dataclass
class AskChoiceField(AskFieldCommon):
    """A choice field in a form.

    In a GUI implementation this is typically displayed as a dropdown list
    or a set of radio buttons.

    Attributes:
        choices: The allowed choices for the answer.
        default: The value returned when user fills in nothing, or None for
                 no default. In a GUI implementation this is typically shown
                 as the starting value in the input field, and the user can
                 change it.
    """

    choices: Sequence[str]
    default: Optional[str] = None


@dataclass
class AskMultiChoiceField(AskFieldCommon):
    """A multi-choice field in a form.

    In a GUI implementation this is typically displayed as a list of checkboxes
    or a list of items with multiple selection enabled.

    Attributes:
        choices: The allowed choices for the answer.
        default: The values returned when user fills in nothing, or None for
                 no default. In a GUI implementation this is typically shown
                 as the starting value in the input field, and the user can
                 change it.
        min_select: The minimum number of choices that must be selected.
        max_select: The maximum number of choices that can be selected,
                    or None for no maximum.
    """

    choices: Sequence[str]
    default: Optional[Sequence[str]] = None
    min_select: int = 0
    max_select: Optional[int] = None


type AskField = Union[AskTextField, AskIntField, AskPathField, AskYesNoField,
                      AskChoiceField, AskMultiChoiceField]
"""An AskField is the question asked in a row in a form in a wizard UI bridge.

   The AskField is one of the Ask*Field dataclasses. It holds the actual
   question text, help text, and other attributes of the question.
"""

type AskFields = Sequence[AskField]
"""AskFields is a sequence of AskField objects, one for each row in a form."""


@dataclass
class AnswerTextField:
    """An answer to a text field in a form.

    Attributes:
        asking: How the question was asked, including the question text, help
                text, and other attributes of the question.
        value: The value of the answer, or None when the user did not fill in
               anything and the field is nullable.
    """

    asking: AskTextField
    value: Optional[str]


@dataclass
class AnswerIntField:
    """An answer to an integer field in a form.

    Attributes:
        asking: How the question was asked, including the question text, help
                text, and other attributes of the question.
        value: The value of the answer, or None when the user did not fill in
               anything and the field is nullable.
    """

    asking: AskIntField
    value: Optional[int]


@dataclass
class AnswerPathField:
    """An answer to a path field in a form.

    Attributes:
        asking: How the question was asked, including the question text, help
                text, and other attributes of the question.
        value: The value of the answer, or None when the user did not fill in
               anything and the field is nullable.
    """

    asking: AskPathField
    value: Optional[Path]


@dataclass
class AnswerYesNoField:
    """An answer to a yes/no field in a form.

    Attributes:
        asking: How the question was asked, including the question text, help
                text, and other attributes of the question.
        value: The value of the answer.
    """

    asking: AskYesNoField
    value: bool


@dataclass
class AnswerChoiceField:
    """An answer to a choice field in a form.

    Attributes:
        asking: How the question was asked, including the question text, help
                text, and other attributes of the question.
        value: The chosen value, one of the choices. It is None only to
               tell a partial validator that a choice with no default has
               not been answered yet. A bridge never returns None as a final
               choice answer: it makes sure a choice with no default is
               answered before the form is submitted for final validation,
               unless the choice is disabled by a partial validator because
               it is irrelevant given the current state of the form.
    """

    asking: AskChoiceField
    value: Optional[str]


@dataclass
class AnswerMultiChoiceField:
    """An answer to a multi-choice field in a form.

    Attributes:
        asking: How the question was asked, including the question text, help
                text, and other attributes of the question.
        value: The values of the answer.
    """

    asking: AskMultiChoiceField
    value: Sequence[str]


type AnswerField = Union[AnswerTextField, AnswerIntField, AnswerPathField,
                         AnswerYesNoField, AnswerChoiceField,
                         AnswerMultiChoiceField]
"""An AnswerField is the answer to a question in a row in a form.

   The AnswerField is one of the Answer*Field dataclasses. It holds the actual
   answer value, and the AskField that was asked.
   """


type AnswerFields = Sequence[AnswerField]
"""AnswerFields is a sequence of AnswerField objects.

   It holds one AnswerField for each row in a form.
   """


class PartFormValidationResult(NamedTuple):
    """Result of validating a partly filled form.

    Attributes:
        is_valid: True when the form is valid, False when it is not valid.
        message: A message to be displayed to the user, explaining why the
                 form is not valid. Empty string when the form is valid.
        disable_row_idxs: A tuple of row indexes that should be disabled in the
                          form, because what has been filled in so far makes
                          these rows irrelevant. For example if ouput format
                          is set to some binary format, then the row(s) that
                          ask for character encoding can be disabled, because
                          they are irrelevant for the chosen output format.
                          Actually disabling these rows is not strictly
                          necessary, but it is a good user experience to do so.
    """

    is_valid: bool
    message: str
    disable_row_idxs: tuple[int, ...] = ()


type PartialFormValidator = Callable[[AnswerFields, int],
                                     PartFormValidationResult]
"""Callback for early per-row feedback while a form is filled.

   The callback receives the current state of the form as AnswerFields,
   and the index of the row most recently filled in.
   It returns a PartFormValidationResult, which indicates whether the form is
   valid, and if not valid, a message to be displayed to the user, and a tuple
   of row indexes that should be disabled in the form because they are
   irrelevant given the current state of the form.
"""
