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
from typing import Any, Callable, NamedTuple, Optional, Protocol, Sequence, \
    TypeVar, Union
from pathlib import Path
from datetime import datetime, date, time, timedelta
from tableio_cfg_json.wizard_ui_bridge_arg_types import PathAskOptions


class _OrderedValue(Protocol):
    """A value comparable to values of its own type with < and >.

    Float, date, time, datetime and timedelta all satisfy this, so a
    single helper can range-check every ordered form field. The other
    operand is Any because each concrete type only compares with itself,
    which is exactly how the standard library types are annotated.
    """

    def __lt__(self, other: Any) -> bool:
        """Return whether this value sorts before other."""

    def __gt__(self, other: Any) -> bool:
        """Return whether this value sorts after other."""


_OrderedT = TypeVar('_OrderedT', bound=_OrderedValue)


def value_out_of_range(value: _OrderedT, minimum: Optional[_OrderedT],
                       maximum: Optional[_OrderedT]) -> bool:
    """Return whether value lies outside the inclusive bounds."""
    below = minimum is not None and value < minimum
    above = maximum is not None and value > maximum
    return below or above


def _check_bounds(minimum: Optional[_OrderedValue],
                  maximum: Optional[_OrderedValue],
                  default: Optional[_OrderedValue]) -> None:
    """Raise ValueError when ordered bounds or the default disagree."""
    if minimum is not None and maximum is not None and minimum > maximum:
        raise ValueError('min_value must not exceed max_value')
    if default is not None and value_out_of_range(default, minimum, maximum):
        raise ValueError('default is out of the allowed range')


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


@dataclass
class AskFloatField(AskFieldCommon):
    """A float field in a form.

    Attributes:
        nullable: When True an empty answer with no default is reported
                  as None. When False an empty answer with no default will
                  be re-asked until the user fills in a valid number.
        default: The value returned when user fills in nothing, or None for
                 no default. In a GUI implementation this is typically shown
                 as the starting value in the input field, and the user can
                 change it.
        min_value: The minimum allowed value, or None for no minimum.
                   The min value is inclusive.
        max_value: The maximum allowed value, or None for no maximum.
                   The max value is inclusive.
    """

    nullable: bool = False
    default: Optional[float] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None

    def __post_init__(self) -> None:
        """Check that the float bounds and default agree."""
        _check_bounds(self.min_value, self.max_value, self.default)


@dataclass
class AskDateField(AskFieldCommon):
    """A date field in a form.

    In a GUI implementation this is typically displayed as a text input field
    with a button next to it that opens a date chooser dialog.

    Attributes:
        nullable: When True an empty answer with no default is reported
                  as None. When False an empty answer with no default will
                  be re-asked until the user fills in a valid date.
        default: The value returned when user fills in nothing, or None for
                 no default. In a GUI implementation this is typically shown
                 as the starting value in the input field, and the user can
                 change it.
        min_value: The minimum allowed value, or None for no minimum.
                   The min value is inclusive.
        max_value: The maximum allowed value, or None for no maximum.
                   The max value is inclusive.
    """

    nullable: bool = False
    default: Optional[date] = None
    min_value: Optional[date] = None
    max_value: Optional[date] = None

    def __post_init__(self) -> None:
        """Check that the date bounds and default agree."""
        _check_bounds(self.min_value, self.max_value, self.default)


@dataclass
class AskTimeField(AskFieldCommon):
    """A time field in a form.

    Attributes:
        nullable: When True an empty answer with no default is reported
                  as None. When False an empty answer with no default will
                  be re-asked until the user fills in a valid time.
        default: The value returned when user fills in nothing, or None for
                 no default. In a GUI implementation this is typically shown
                 as the starting value in the input field, and the user can
                 change it.
        min_value: The minimum allowed value, or None for no minimum.
                   The min value is inclusive.
        max_value: The maximum allowed value, or None for no maximum.
                   The max value is inclusive.
    """

    nullable: bool = False
    default: Optional[time] = None
    min_value: Optional[time] = None
    max_value: Optional[time] = None

    def __post_init__(self) -> None:
        """Check that the time bounds and default agree."""
        _check_bounds(self.min_value, self.max_value, self.default)


@dataclass
class AskDateTimeField(AskFieldCommon):
    """A date-time field in a form.

    In a GUI implementation this is typically displayed as a text input field
    with a button next to it that opens a date-time chooser dialog for the
    date part.

    Attributes:
        nullable: When True an empty answer with no default is reported
                  as None. When False an empty answer with no default will
                  be re-asked until the user fills in a valid date-time.
        default: The value returned when user fills in nothing, or None for
                 no default. In a GUI implementation this is typically shown
                 as the starting value in the input field, and the user can
                 change it.
        min_value: The minimum allowed value, or None for no minimum.
                   The min value is inclusive.
        max_value: The maximum allowed value, or None for no maximum.
                   The max value is inclusive.
    """

    nullable: bool = False
    default: Optional[datetime] = None
    min_value: Optional[datetime] = None
    max_value: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Check that the date-time bounds and default agree."""
        _check_bounds(self.min_value, self.max_value, self.default)


@dataclass
class AskDurationField(AskFieldCommon):
    """A duration field in a form.

    Attributes:
        nullable: When True an empty answer with no default is reported
                  as None. When False an empty answer with no default will
                  be re-asked until the user fills in a valid duration.
        default: The value returned when user fills in nothing, or None for
                 no default. In a GUI implementation this is typically shown
                 as the starting value in the input field, and the user can
                 change it.
        min_value: The minimum allowed value, or None for no minimum.
                   The min value is inclusive.
        max_value: The maximum allowed value, or None for no maximum.
                   The max value is inclusive.
    """

    nullable: bool = False
    default: Optional[timedelta] = None
    min_value: Optional[timedelta] = None
    max_value: Optional[timedelta] = None

    def __post_init__(self) -> None:
        """Check that the duration bounds and default agree."""
        _check_bounds(self.min_value, self.max_value, self.default)


type AskField = Union[AskTextField, AskIntField, AskPathField, AskYesNoField,
                      AskChoiceField, AskMultiChoiceField, AskFloatField,
                      AskDateField, AskTimeField, AskDateTimeField,
                      AskDurationField]
"""An AskField is the question asked in a row in a form in a wizard UI bridge.

   The AskField is one of the Ask*Field dataclasses. It holds the actual
   question text, help text, and other attributes of the question.
"""

type AskFields = Sequence[AskField]
"""AskFields is a sequence of AskField objects, one for each row in a form."""


ALL_ASK_FIELD_TYPES = (AskTextField, AskIntField, AskPathField, AskYesNoField,
                       AskChoiceField, AskMultiChoiceField, AskFloatField,
                       AskDateField, AskTimeField, AskDateTimeField,
                       AskDurationField)
"""Every concrete AskField class, in the order of the AskField union.

A bridge that shows all field types checks membership against this tuple
in supports_form_field(), so a field type added later is reported as
unsupported until this tuple and the bridge are extended together.
"""


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


@dataclass
class AnswerFloatField:
    """An answer to a float field in a form.

    Attributes:
        asking: How the question was asked, including the question text, help
                text, and other attributes of the question.
        value: The value of the answer, or None when the user did not fill in
               anything and the field is nullable.
    """

    asking: AskFloatField
    value: Optional[float]


@dataclass
class AnswerDateField:
    """An answer to a date field in a form.

    Attributes:
        asking: How the question was asked, including the question text, help
                text, and other attributes of the question.
        value: The value of the answer, or None when the user did not fill in
               anything and the field is nullable.
    """

    asking: AskDateField
    value: Optional[date]


@dataclass
class AnswerTimeField:
    """An answer to a time field in a form.

    Attributes:
        asking: How the question was asked, including the question text, help
                text, and other attributes of the question.
        value: The value of the answer, or None when the user did not fill in
               anything and the field is nullable.
    """

    asking: AskTimeField
    value: Optional[time]


@dataclass
class AnswerDateTimeField:
    """An answer to a date-time field in a form.

    Attributes:
        asking: How the question was asked, including the question text, help
                text, and other attributes of the question.
        value: The value of the answer, or None when the user did not fill in
               anything and the field is nullable.
    """

    asking: AskDateTimeField
    value: Optional[datetime]


@dataclass
class AnswerDurationField:
    """An answer to a duration field in a form.

    Attributes:
        asking: How the question was asked, including the question text, help
                text, and other attributes of the question.
        value: The value of the answer, or None when the user did not fill in
               anything and the field is nullable.
    """

    asking: AskDurationField
    value: Optional[timedelta]


type AnswerField = Union[AnswerTextField, AnswerIntField, AnswerPathField,
                         AnswerYesNoField, AnswerChoiceField,
                         AnswerMultiChoiceField, AnswerFloatField,
                         AnswerDateField, AnswerTimeField,
                         AnswerDateTimeField, AnswerDurationField]
"""An AnswerField is the answer to a question in a row in a form.

   The AnswerField is one of the Answer*Field dataclasses. It holds the actual
   answer value, and the AskField that was asked.
   """


type AnswerFields = Sequence[AnswerField]
"""AnswerFields is a sequence of AnswerField objects.

   It holds one AnswerField for each row in a form.
   """


type PrefillValueType = Union[str, int, Path, bool, Sequence[str], float, date,
                              time, datetime, timedelta]
"""The type of a value a partial validator may prefill into a field.

The value must match the answer type of the target field: a str for a
text or choice field, an int for an integer field, a Path for a path
field, a bool for a yes/no field, a sequence of str for a multi-choice
field, a float for a float field, and a date, time, datetime or
timedelta for a date, time, date-time or duration field respectively.
"""


type PrefillValues = tuple[tuple[int, PrefillValueType], ...]
"""Prefill requests returned by a partial form validator.

Each pair is (row_index, value): a request to place value into the input
of the row at row_index, as if the user had typed it. See
PartFormValidationResult.prefill_values for the rules a bridge follows
when it applies these requests.
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
        prefill_values: Values the validator asks the bridge to place into
                        other rows' inputs, as a tuple of (row_index, value)
                        pairs. Each value must match the answer type of the
                        field in that row. A bridge applies each request
                        during live editing as if the user had typed the
                        value; setting a value equal to the one already there
                        is a no-op, so a validator that emits a stable value
                        does not loop. The validator owns idempotency: it
                        should emit a prefill only when it means to fill or
                        overwrite the target. A prefill aimed at the row that
                        just changed is ignored, so writing back never fights
                        the user's current edit. A prefill aimed at a disabled
                        row is still applied, so the value shows in the greyed
                        row and takes effect if the row is later enabled. A
                        row index outside the form, or a value whose type does
                        not match the field, raises an exception, since both
                        are validator bugs. A choice or multi-choice value not
                        among the field's choices, and any prefill of a
                        sensitive field, are ignored. prefill_values is a
                        live-editing convenience only and is ignored when the
                        form is submitted, so an application must still apply
                        the same default on submit.
    """

    is_valid: bool
    message: str
    disable_row_idxs: tuple[int, ...] = ()
    prefill_values: PrefillValues = ()


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
