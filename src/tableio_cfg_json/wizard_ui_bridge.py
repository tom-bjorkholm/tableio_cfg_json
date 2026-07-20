#! /usr/local/bin/python3
"""User interface bridge for the TableIO JSON configuration wizard.

This module defines the abstract bridge between the wizard and a user
interface, the navigation requests a bridge raises to steer wizard flow,
and the column and cell descriptors used by table questions. Concrete
console and graphical bridges derive from WizardUiBridge.

An application that drives the wizard is responsible for implementing
the typed ask methods of its bridge, together with show(). A concrete
bridge implements ask_text(), ask_choice(), ask_multi(), ask_yes_no()
and ask_table(); ask_path() has a permanent base implementation that a
bridge may override for a native file or directory picker. The low-level
ask() is deprecated: it warns when called and when a bridge overrides
it. The base class keeps temporary fallback implementations of the typed
methods written in terms of ask(), so a bridge that still overrides
ask() keeps working while it is adjusted to implement the typed methods
directly.

A GUI, textual, curses or web application should override ask_form() to show
the whole form at once, so the user sees every question together and answers
them in any order. The base implementation is permanent and suitable for a
console text interface.

A GUI, textual, curses or web application should also override ask_path() to
provide a native file or directory picker. The base implementation asks for
text and validates the path.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
import warnings
from pathlib import Path
from typing import Optional, Sequence, TextIO
from tableio_cfg_json.wizard_ui_bridge_arg_types import PartialCheck, \
    PathAskOptions, TableColumn, TableCell, WizardBack
from tableio_cfg_json._wizard_ui_bridge_helpers import check_text_args, \
    text_answer, question_with_default, ask_yes_no, ask_one, \
    ask_many, run_table, int_text, out_of_range, range_error, path_answer
from tableio_cfg_json._wizard_ui_bridge_form import initial_answer, \
    valid_prefills, prefilled_field
from tableio_cfg_json.wizard_ui_bridge_form_defs import AskField, AskFields, \
    AnswerField, AnswerFields, PartialFormValidator, AskTextField, \
    AskIntField, AskPathField, AskYesNoField, AskChoiceField, \
    AskMultiChoiceField, AnswerTextField, AnswerIntField, AnswerPathField, \
    AnswerYesNoField, AnswerChoiceField, AnswerMultiChoiceField, \
    PrefillValueType


_INT_ERROR = 'Please enter an integer.'


class WizardUiBridge:
    """Bridge between the wizard and the user interface.

    This is an abstract base class for a bridge between the wizard and
    the user interface. Provide concrete classes of this bridge to allow
    the wizard to use a console text user interface or a graphical user
    interface.

    A concrete bridge implements ask_text(), ask_choice(), ask_multi(),
    ask_yes_no(), ask_table() and show(). It may override ask_path() for
    a native file or directory picker; otherwise the base implementation
    asks for text and validates the path. It may override ask_form() to
    show the whole form at once, so the user sees every question together
    and answers them in any order. Overriding ask_form() and ask_path()
    is strongly recommended for a GUI, textual, curses or web application.

    The low-level ask() is deprecated: it warns when called and when a bridge
    overrides it. As a temporary migration aid the base class implements
    typed methods via the deprecated ask(), so a bridge that still overrides
    ask() keeps working while it is adjusted; each fallback warns that the
    typed method should be overridden instead. These fallbacks are temporary
    and will be withdrawn once bridges implement the typed methods
    directly.

    Any ask method may raise a WizardNavigation subclass to request back,
    cancel-level or abort instead of returning an answer.
    """

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Warn when a subclass overrides the deprecated ask()."""
        super().__init_subclass__(**kwargs)
        if 'ask' in cls.__dict__:
            warnings.warn(
                'Overriding WizardUiBridge.ask() is deprecated; override '
                'ask_text(), ask_choice(), ask_multi(), ask_yes_no() and '
                'ask_table() in the bridge instead.',
                DeprecationWarning, stacklevel=2)

    def ask(self, question: str, re_ask_reason: Optional[str] = None,
            choices: Optional[Sequence[str]] = None) -> str | int:
        """Ask a question and return the user's answer.

        Deprecated. Call ask_text() for free text or ask_choice() for a
        single choice instead. This base implementation is temporary
        plumbing: it warns and then dispatches to ask_text() when no
        choices are given and to ask_choice() otherwise, so existing
        callers keep working against a bridge that implements the typed
        methods.

        Args:
            question: The question to ask the user.
            re_ask_reason: The reason for re-asking the question, for
                           instance that the user's answer was invalid.
            choices: The choices to offer the user as a sequence of
                     strings.

        Returns:
            The user's answer: the entered text when no choices are
            given, otherwise the chosen one of choices.
        Raises:
            WizardBack: The user asked to return to the previous question.
            WizardCancelLevel: The user cancelled the current level.
            WizardAbort: The user abandoned the whole configuration.
        """
        warnings.warn(
            'WizardUiBridge.ask() is deprecated; call ask_text() for free '
            'text or ask_choice() for a single choice instead.',
            DeprecationWarning, stacklevel=2)
        if choices is None:
            text = self.ask_text(question, re_ask_reason)
            return '' if text is None else text
        return self.ask_choice(question, choices=choices,
                               re_ask_reason=re_ask_reason)

    def ask_text(self, question: str, re_ask_reason: Optional[str] = None,
                 nullable: bool = False, *, default: Optional[str] = None,
                 sensitive: bool = False) -> Optional[str]:
        """Ask a free-text question and return the entered text.

        The application is responsible for implementing this method with
        a real text-entry control. As a temporary migration aid the base
        class provides a fallback in terms of the deprecated ask(), so a
        bridge that still overrides ask() keeps working for non-sensitive
        questions.

        Args:
            question: The question to ask the user.
            re_ask_reason: The reason for re-asking the question, for
                           instance that the user's answer was invalid.
            nullable: When True an empty answer with no default is
                      reported as None. When False an empty answer with
                      no default is the empty string.
            default: The value returned by an empty answer, or None for
                     no default.
            sensitive: True when the bridge must avoid echoing the
                       entered text, such as for passwords. A default is
                       not allowed for a sensitive question.

        Returns:
            The entered text, default for an empty answer with a default,
            or None for an empty answer when nullable.
        Raises:
            ValueError: default is given together with sensitive.
            NotImplementedError: The deprecated ask() fallback is used
                                 for sensitive input.
            WizardBack: The user asked to return to the previous question.
            WizardCancelLevel: The user cancelled the current level.
            WizardAbort: The user abandoned the whole configuration.
        """
        check_text_args(default, sensitive)
        if sensitive:
            raise NotImplementedError('ask_text() sensitive input not '
                                      'implemented')
        self._guard_fallback('ask_text')
        prompt = question_with_default(question, default)
        answer = self.ask(prompt, re_ask_reason)
        text = answer if isinstance(answer, str) else str(answer)
        return text_answer(text, nullable, default)

    # pylint: disable-next=too-many-arguments
    def ask_int(self, question: str, re_ask_reason: Optional[str] = None, *,
                nullable: bool = False, min_value: Optional[int] = None,
                max_value: Optional[int] = None,
                default: Optional[int] = None) -> Optional[int]:
        """Ask for an integer, optionally within inclusive bounds.

        The base implementation uses ask_text() and re-asks until the
        answer is empty when allowed or parses as an integer in range. A
        derived bridge may override it with a direct numeric control.

        Args:
            question: The question to ask the user.
            re_ask_reason: The reason for re-asking the question, for
                           instance that the user's answer was invalid.
            nullable: When True an empty answer is reported as None, so
                      the caller can treat it as a request to use the
                      default. When False an empty answer will be re-asked
                      until a valid answer is entered.
            min_value: The minimum allowed value, or None for no lower bound.
                       The min value is inclusive.
            max_value: The maximum allowed value, or None for no upper bound.
                       The max value is inclusive.
            default: The value returned by an empty answer, or None for
                     no default.

        Returns:
            The entered integer, default for an empty answer with a
            default, or None for an empty answer when nullable.
        Raises:
            WizardBack: The user asked to return to the previous question.
            WizardCancelLevel: The user cancelled the current level.
            WizardAbort: The user abandoned the whole configuration.
        """
        assert (min_value is None or max_value is None
                or min_value <= max_value)
        assert default is None or not out_of_range(default, min_value,
                                                   max_value)
        reason = re_ask_reason
        default_text = None if default is None else str(default)
        while True:
            text = self.ask_text(question, reason, nullable,
                                 default=default_text)
            if text is None:
                return None
            value = int_text(text)
            if value is None:
                reason = _INT_ERROR
            elif out_of_range(value, min_value, max_value):
                reason = range_error(min_value, max_value)
            else:
                return value

    def ask_path(self, question: str, re_ask_reason: Optional[str] = None, *,
                 options: Optional[PathAskOptions] = None) -> Optional[Path]:
        """Ask a question for a path and return the accepted path.

        A derived bridge may override this method to provide a native file
        or directory picker. The base implementation is permanent and
        asks for text through ask_text(), then validates the answer.

        Args:
            question: The question to ask the user.
            re_ask_reason: The reason for re-asking the question.
            options: Path options. None only rejects existing directories.

        Returns:
            The accepted path, a default path, or None when nullable.
        Raises:
            WizardBack: The user asked to return to the previous question.
            WizardCancelLevel: The user cancelled the current level.
            WizardAbort: The user abandoned the whole configuration.
        """
        path_options = PathAskOptions() if options is None else options
        reason = re_ask_reason
        default = path_options.default
        default_text = None if default is None else str(default)
        while True:
            text = self.ask_text(question, reason, path_options.nullable,
                                 default=default_text)
            done, path, reason = path_answer(text, path_options)
            if done:
                return path

    def ask_yes_no(self, question: str, default: bool,
                   re_ask_reason: Optional[str] = None) -> bool:
        """Ask a yes/no question and return the chosen boolean.

        Yes/no questions are asked through this method, and the
        application is responsible for implementing it with a real yes/no
        interface, such as a pair of yes and no buttons in a graphical
        bridge or a y/n prompt in a console bridge. As a temporary
        migration aid the base class provides a fallback in terms of the
        deprecated ask() with the choices ('yes', 'no'): an empty answer
        selects default, an index or matching text selects the boolean,
        and any other answer is re-asked.

        Args:
            question: The yes/no question to ask.
            default: The value to use when the user makes no explicit
                     choice.
            re_ask_reason: The reason for re-asking the question, for
                           instance that the user's answer was invalid.

        Returns:
            The user's choice as a boolean.
        Raises:
            WizardBack: The user asked to return to the previous question.
            WizardCancelLevel: The user cancelled the current level.
            WizardAbort: The user abandoned the whole configuration.
        """
        self._guard_fallback('ask_yes_no')

        def reader(reason: Optional[str]) -> str | int:
            return self.ask(question, reason, choices=('yes', 'no'))
        return ask_yes_no(reader, default, re_ask_reason)

    def ask_choice(self, question: str, *, choices: Sequence[str],
                   default: Optional[str] = None,
                   re_ask_reason: Optional[str] = None) -> str:
        """Ask the user to pick exactly one of choices and return it.

        The return value is always one of choices. An empty answer
        selects default, so default must name one of choices; when
        default is None an empty answer counts as no choice and the
        question is re-asked.

        The application is responsible for implementing this method with
        a real single-choice control, such as a drop-down or a set of
        radio buttons in a graphical bridge. As a temporary migration aid
        the base class provides a fallback in terms of the deprecated
        ask().

        Args:
            question: The question to ask the user.
            choices: The choices to offer, in display order.
            default: The choice selected by an empty answer, or None to
                     require an explicit choice.
            re_ask_reason: The reason for re-asking, shown before the
                           first question when not None.

        Returns:
            The chosen value, one of choices.
        Raises:
            WizardBack: The user asked to return to the previous question.
            WizardCancelLevel: The user cancelled the current level.
            WizardAbort: The user abandoned the whole configuration.
        """
        self._guard_fallback('ask_choice')

        def reader(reason: Optional[str]) -> str | int:
            return self.ask(question, reason, choices)
        return ask_one(reader, choices, default, re_ask_reason)

    # pylint: disable-next=too-many-arguments
    def ask_multi(self, question: str, *, choices: Sequence[str],
                  default: Optional[Sequence[str]] = None, min_select: int = 0,
                  max_select: Optional[int] = None,
                  re_ask_reason: Optional[str] = None) -> list[str]:
        """Ask the user to pick several of choices and return them.

        The result holds the chosen values in the order of choices, with
        a count between min_select and max_select; max_select None means
        no upper bound. An empty answer selects default, or selects
        nothing when default is None.

        The application is responsible for implementing this method with
        a real multi-selection control, such as a list of check boxes or
        a multi-select list in a graphical bridge. As a temporary
        migration aid the base class provides a fallback in terms of the
        deprecated ask() that reads one comma-separated answer of menu
        indexes or names.

        Args:
            question: The question to ask the user.
            choices: The choices to offer, in display order.
            default: The values pre-selected by an empty answer, or None.
            min_select: The smallest acceptable number of choices.
            max_select: The largest acceptable number of choices, or None
                        for no upper bound.
            re_ask_reason: The reason for re-asking, shown before the
                           first question when not None.

        Returns:
            The chosen values, each one of choices, in choices order.
        Raises:
            WizardBack: The user asked to return to the previous question.
            WizardCancelLevel: The user cancelled the current level.
            WizardAbort: The user abandoned the whole configuration.
        """
        self._guard_fallback('ask_multi')

        def reader(reason: Optional[str]) -> str | int:
            return self.ask(question, reason, choices)
        return ask_many(reader, choices, default, min_select, max_select,
                        re_ask_reason, one_based=False)

    # pylint: disable-next=too-many-arguments
    def ask_table(self, columns: Sequence[TableColumn],
                  cells: list[list[TableCell]], question: str, *,
                  re_ask_reason: Optional[str] = None,
                  partial_check: Optional[PartialCheck] = None,
                  min_rows: Optional[int] = None,
                  max_rows: Optional[int] = None) -> list[list[Optional[str]]]:
        """Ask the user to fill in a table and return its cells.

        The bridge shows a table whose columns are described by columns
        and whose rows start from cells. Each row in cells holds one
        TableCell per column. Read-only columns show the fixed text in
        each cell, such as a column of parameter names, while editable
        columns show pre-filled or empty values the user may change.

        The application is responsible for implementing this method with
        a real table widget. As a temporary migration aid the base class
        provides a fallback in terms of the deprecated ask(), asking once
        per editable cell and folding the read-only cells of the row into
        the prompt, so a bridge that still overrides ask() keeps working.
        The fallback only fills the rows given in cells, so it ignores
        min_rows and max_rows and cannot add or remove rows. In that
        fallback an empty answer keeps the cell's current value and a
        reserved erase token empties the cell, which is how a console
        user replaces a pre-filled default with an empty cell.

        How an empty editable cell is reported follows its TableCell: a
        nullable cell reports None, a free-text cell reports an empty
        string, and a cell with choices treats empty as not yet a valid
        value.

        When partial_check is given, the bridge calls it after the user
        changes a cell, passing the whole table as it currently stands
        and the (row, column) position of the changed cell, both 0-based.
        The callback returns (accepted, message); the bridge uses message
        to give early feedback. The callback must tolerate empty or partly
        filled cells, and it gives advisory feedback only: the wizard
        still validates the final table.

        Args:
            columns: Description of each column, in left-to-right order.
            cells: Starting rows, each a list of one TableCell per column.
            question: The question or instruction shown above the table.
            re_ask_reason: The reason for re-asking, for instance that a
                           value failed validation.
            partial_check: Optional callback for early per-cell feedback.
                           It receives the current table and the changed
                           (row, column) position and returns an accepted
                           flag and a message.
            min_rows: Minimum number of rows the user must leave in the
                      table, or None when rows are fixed to the rows in
                      cells. A variable number of rows requires both
                      min_rows and max_rows to be non-None.
            max_rows: Maximum number of rows the user may add the table
                      to, or None when rows are fixed to the rows in
                      cells. A variable number of rows requires both
                      min_rows and max_rows to be non-None.

        Returns:
            The complete table as rows of cells, including the read-only
            columns, with one cell per column in each row. Each cell is
            the final string the user left, or None for an empty cell.
        Raises:
            WizardBack: The user asked to return to the previous question.
            WizardCancelLevel: The user cancelled the current level.
            WizardAbort: The user abandoned the whole configuration.
        """
        self._guard_fallback('ask_table')
        _ = (min_rows, max_rows)  # the fallback fills the fixed rows in cells
        return run_table(self.ask, self.show, columns, cells, question,
                         re_ask_reason, partial_check)

    def ask_form(self, long_question: str, ask_fields: AskFields, *,
                 re_ask_reason: Optional[str] = None,
                 partial_validator: Optional[PartialFormValidator] = None) \
            -> AnswerFields:
        """Ask the user to fill in a form and return the answers.

        The bridge shows a form whose fields are described by ask_fields.
        The base implementation is permanent and suitable for a console
        text interface: it shows long_question, then asks each field in
        turn with the typed ask methods ask_text(), ask_int(),
        ask_yes_no(), ask_path(), ask_choice() and ask_multi(), and
        returns one AnswerField per field in the same order.

        Any serious application or library using GUI, textual, curses or
        web interfaces should override this method to show the whole form
        at once, so the user sees every question together and answers them
        in any order. In such an implementation ask_form is typically a
        dialog or form window with long_question and re_ask_reason shown
        above a grid with two columns: the left column a label with the
        field's short question, and the right column an input widget.

        See wizard_ui_bridge_form_defs.py for the AskFields, and the
        description of how each field type is typically implemented in a GUI
        or textual interface.

        When partial_validator is given, the base implementation calls it
        after each field is answered, passing the current answers and the
        index of the field just answered. It shows the returned message and
        skips asking the fields listed in disable_row_idxs, filling them
        with their default or not-yet-answered value instead. WizardBack
        steps to the previous asked field; from the first field it
        propagates so the wizard steps to the previous question.

        Args:
            long_question: The main question or instruction to the user,
                           typically shown above the form. It may be long
                           string that the UI bridge is responsible for
                           wrapping and displaying nicely.
            ask_fields: Description of each field in the form.
            re_ask_reason: The reason for re-asking, for instance how a
                           value failed validation.
            partial_validator: Optional callback for early per-field
                               feedback. It receives the current answers
                               and the changed field index, and returns a
                               PartFormValidationResult.

        Returns:
            One AnswerField per AskField, in the order of ask_fields.
        Raises:
            WizardBack: The user asked to return to the previous question.
            WizardCancelLevel: The user cancelled the current level.
            WizardAbort: The user abandoned the whole configuration.
        """
        self.show(long_question)
        if re_ask_reason is not None:
            self.show(re_ask_reason)
        answers = [initial_answer(field) for field in ask_fields]
        self._fill_form(ask_fields, answers, partial_validator)
        return answers

    def _fill_form(self, ask_fields: AskFields, answers: list[AnswerField],
                   validator: Optional[PartialFormValidator]) -> None:
        """Ask each enabled field in turn, stepping back on WizardBack.

        A prefill returned by the validator for a not-yet-asked row is kept
        in pending and offered as that row's default when it is asked.
        """
        disabled: set[int] = set()
        pending: dict[int, PrefillValueType] = {}
        position = 0
        while position < len(ask_fields):
            if position in disabled:
                position += 1
                continue
            try:
                answers[position] = self._ask_field(
                    ask_fields[position], pending.pop(position, None))
            except WizardBack:
                position = self._prev_field(position, disabled)
                continue
            disabled = self._form_feedback(ask_fields, answers, position,
                                           validator, pending)
            position += 1

    @staticmethod
    def _prev_field(position: int, disabled: set[int]) -> int:
        """Return the previous enabled field index, or re-raise WizardBack."""
        prev = position - 1
        while prev >= 0 and prev in disabled:
            prev -= 1
        if prev < 0:
            raise WizardBack()
        return prev

    # pylint: disable-next=too-many-arguments
    def _form_feedback(self, ask_fields: AskFields, answers: list[AnswerField],
                       position: int,
                       validator: Optional[PartialFormValidator],
                       pending: dict[int, PrefillValueType]) -> set[int]:
        """Run the validator, show its message, store prefills, return rows.

        Prefills for other rows are validated and kept in pending, so a
        later row is offered the value as its default when it is asked.
        """
        if validator is None:
            return set()
        result = validator(answers, position)
        if not result.is_valid and result.message:
            self.show(result.message)
        for index, value in valid_prefills(ask_fields, position,
                                           result.prefill_values):
            pending[index] = value
        return set(result.disable_row_idxs)

    def _ask_field(self, field: AskField,
                   prefill: Optional[PrefillValueType] = None) -> AnswerField:
        """Ask one form field with the matching typed ask method.

        When prefill is given it replaces the field's default, so the value
        is offered as the starting answer the user can accept or edit.
        """
        if prefill is not None:
            field = prefilled_field(field, prefill)
        if field.help_text is not None:
            self.show(field.help_text)
        if isinstance(field, AskTextField):
            return AnswerTextField(field, self.ask_text(
                field.short_question, nullable=field.nullable,
                default=field.default, sensitive=field.sensitive))
        if isinstance(field, AskIntField):
            return AnswerIntField(field, self.ask_int(
                field.short_question, nullable=field.nullable,
                min_value=field.min_value, max_value=field.max_value,
                default=field.default))
        if isinstance(field, AskPathField):
            return AnswerPathField(field, self.ask_path(
                field.short_question, options=field.path_options))
        if isinstance(field, AskYesNoField):
            return AnswerYesNoField(field, self.ask_yes_no(
                field.short_question, field.default))
        if isinstance(field, AskChoiceField):
            return AnswerChoiceField(field, self.ask_choice(
                field.short_question, choices=field.choices,
                default=field.default))
        assert isinstance(field, AskMultiChoiceField)
        return AnswerMultiChoiceField(field, self.ask_multi(
            field.short_question, choices=field.choices, default=field.default,
            min_select=field.min_select, max_select=field.max_select))

    def _guard_fallback(self, method_name: str) -> None:
        """Guard a deprecated fallback and warn that it is temporary.

        The base typed-method fallbacks work only while a bridge still
        overrides the deprecated ask(). A bridge that overrides neither
        ask() nor method_name has no implementation for it, so this
        raises NotImplementedError; otherwise it warns that method_name
        should be overridden instead of relying on the fallback.
        """
        if type(self).ask is WizardUiBridge.ask:
            raise NotImplementedError(f'{method_name}() not implemented')
        warnings.warn(
            f'WizardUiBridge.{method_name}() relies on temporary backward '
            f'compatibility code; override {method_name}() in the bridge '
            'instead of the deprecated ask().',
            DeprecationWarning, stacklevel=3)

    def error_file(self) -> TextIO:
        """Return the stream used for validation diagnostics."""
        return sys.stderr

    def show(self, message: str) -> None:
        """Show a message to the user.

        If implementing a graphical user interface, this method should
        display the message in a dialog or a message box. If implementing
        a console text user interface, this method should print the
        message to the console.

        Args:
            message: The message to show the user.
        """
        raise NotImplementedError('show() not implemented')
