#! /usr/local/bin/python3
"""User interface bridge for the TableIO JSON configuration wizard.

This module defines the abstract bridge between the wizard and a user
interface, the navigation requests a bridge raises to steer wizard flow,
and the column and cell descriptors used by table questions. Concrete
console and graphical bridges derive from WizardUiBridge.

An application that drives the wizard is responsible for implementing
the typed ask methods of its bridge, together with show(). The typed
methods are ask_text() for free text, ask_choice() for one choice,
ask_multi() for several choices, ask_yes_no() for a boolean and
ask_table() for a table. The low-level ask() is deprecated: it warns
when called and when a bridge overrides it. To give application bridge
authors time to migrate, the base class keeps temporary fallback
implementations of the typed methods written in terms of ask(), so a
bridge that still overrides ask() keeps working while it is adjusted to
implement the typed methods directly. These fallbacks are a temporary
compatibility aid that warns on use and will be withdrawn once bridges
implement the typed methods directly.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
import warnings
from dataclasses import dataclass
from io import StringIO
from typing import Callable, Optional, Sequence, TextIO
from config_as_json import InvalidConfiguration, string_best_match

type PartialCheck = Callable[
    [list[list[Optional[str]]], tuple[int, int]], tuple[bool, str]]
"""Callback for early per-cell feedback while a table is filled.

It receives the whole table as it currently stands and the 0-based
(row, column) position of the changed cell, and returns whether the
value is accepted together with a message to show the user.
"""

type AskReader = Callable[
    [str, Optional[str], Optional[Sequence[str]]], str | int]
"""An ask-like reader used by the temporary table fallback machinery.

It takes a prompt, an optional re-ask reason and optional choices and
returns the raw user answer as text or a 0-based choice index, exactly
like the deprecated WizardUiBridge.ask(). The shared table helpers take
one so the console bridge and the deprecated base fallback share code.
"""

_ERASE_TOKEN = ':e'  # empties an editable cell in the ask_table fallback
_CHOICE_ERROR = 'Please enter one of the listed choices.'
_INT_ERROR = 'Please enter an integer.'


class WizardNavigation(Exception):
    """Base class for wizard navigation requests raised by a bridge.

    A user interface raises a subclass of this exception from an ask
    method when the user wants to move within the wizard instead of
    answering the current question. The wizard keeps these distinct from
    validation errors, so its retry loops never catch them and they
    reach the navigation driver unchanged.
    """


class WizardBack(WizardNavigation):
    """Request to return to the previous wizard question.

    A bridge raises this when the user chooses "back". The wizard
    restores the data collected before the previous question and asks
    that question again. Raised at the first question of one wizard call
    it has no earlier question within that call, so the wizard lets it
    propagate out to the application. The application can then step back
    in its own outer navigation, for instance to the previous endpoint.
    """


class WizardCancelLevel(WizardNavigation):
    """Request to leave the current level and change what opened it.

    A bridge raises this when the user asks to step out of the current
    configuration level, such as a table of format-specific parameters or
    a group of questions that exist only because of an earlier choice.
    Unlike WizardBack, which moves to the previous question at the same
    level, this asks to return to the question one level out whose answer
    opened the current level, so the user can change that answer. The
    answers collected at the current level are discarded.

    Each level's driver catches this from the level it opened and re-asks
    the opening question. When the current level has no enclosing level,
    the outermost driver cannot step out; following this contract it
    re-asks the current question and tells the user there is no outer
    level. Nesting may be arbitrarily deep: each driver either handles the
    request for the level it opened or lets it propagate further out.
    """


class WizardAbort(WizardNavigation):
    """Request to abandon the whole configuration.

    A bridge raises this when the user abandons configuration entirely.
    The wizard does not catch it; it propagates out of the wizard call so
    the application can stop the configuration session.
    """


@dataclass(frozen=True)
class TableColumn:
    """Header and editability for one whole column of a table question.

    A table question describes its columns once. Read-only columns show
    fixed text the user cannot edit, such as a column of parameter names.
    Per-cell values and value constraints are described by TableCell.

    Attributes:
        header: Column heading shown to the user.
        read_only: True when the whole column shows fixed text the user
                   cannot edit.
    """

    header: str
    read_only: bool = False


@dataclass(frozen=True)
class TableCell:
    """Initial content and value constraints for one table cell.

    A table question holds one TableCell per column in each row, so each
    row of an editable column can offer its own finite value set. This
    suits a table whose rows are different parameters that each accept
    different values, such as the format-specific options of a config.

    Attributes:
        value: The initial text shown in the cell. For a read-only column
               this is the fixed text. For an editable column it is the
               pre-filled value, or None for an empty cell.
        choices: The finite set of values this cell accepts, or None for
                 free text. A graphical bridge can render choices as a
                 drop-down.
        nullable: True when the user may leave the cell empty, which the
                  table reports as None. False when an empty cell is not
                  interpreted as None: with choices None an empty cell is
                  an empty string the validation may or may not accept,
                  and with choices given an empty editable cell is not yet
                  a valid final value.
    """

    value: Optional[str] = None
    choices: Optional[tuple[str, ...]] = None
    nullable: bool = False


class WizardUiBridge:
    """Bridge between the wizard and the user interface.

    This is an abstract base class for a bridge between the wizard and
    the user interface. Provide concrete classes of this bridge to allow
    the wizard to use a console text user interface or a graphical user
    interface.

    A concrete bridge implements the typed ask methods, ask_text(),
    ask_choice(), ask_multi(), ask_yes_no() and ask_table(), together
    with show(). The low-level ask() is deprecated: it warns when called
    and when a bridge overrides it. As a temporary migration aid the base
    class implements the typed methods in terms of the deprecated ask(),
    so a bridge that still overrides ask() keeps working while it is
    adjusted; each fallback warns that the typed method should be
    overridden instead. These fallbacks are temporary and will be
    withdrawn once bridges implement the typed methods directly. Any ask
    method may raise a WizardNavigation subclass to request back,
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
                 nullable: bool = False) -> Optional[str]:
        """Ask a free-text question and return the entered text.

        The application is responsible for implementing this method with
        a real text-entry control. As a temporary migration aid the base
        class provides a fallback in terms of the deprecated ask(), so a
        bridge that still overrides ask() keeps working.

        Args:
            question: The question to ask the user.
            re_ask_reason: The reason for re-asking the question, for
                           instance that the user's answer was invalid.
            nullable: When True an empty answer is reported as None, so
                      the caller can treat it as a request to use the
                      default. When False an empty answer is the empty
                      string.

        Returns:
            The entered text, or None for an empty answer when nullable.
        Raises:
            WizardBack: The user asked to return to the previous question.
            WizardCancelLevel: The user cancelled the current level.
            WizardAbort: The user abandoned the whole configuration.
        """
        self._guard_fallback('ask_text')
        answer = self.ask(question, re_ask_reason)
        text = answer if isinstance(answer, str) else str(answer)
        return None if (nullable and text == '') else text

    def ask_int(self, question: str, re_ask_reason: Optional[str] = None, *,
                nullable: bool = False, min_value: Optional[int] = None,
                max_value: Optional[int] = None) -> Optional[int]:
        """Ask a question for an integer and return the entered integer.

        The method asks the user for an integer value (optionally
        within a range) and returns it. The range is inclusive.
        If the answer is invalid, the method re-asks the question
        internally, until a valid answer is entered.

        This method is implemented by the base class using ask_text(),
        but a derived bridge can override it to implement something
        that is more efficient or more user-friendly.

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

        Returns:
            The entered integer, or None for an empty answer when nullable.
        Raises:
            WizardBack: The user asked to return to the previous question.
            WizardCancelLevel: The user cancelled the current level.
            WizardAbort: The user abandoned the whole configuration.
        """
        assert (min_value is None or max_value is None
                or min_value <= max_value)
        reason = re_ask_reason
        while True:
            text = self.ask_text(question, reason, nullable)
            if text is None:
                return None
            value = _int_text(text)
            if value is None:
                reason = _INT_ERROR
            elif _out_of_range(value, min_value, max_value):
                reason = _range_error(min_value, max_value)
            else:
                return value

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
        return _ask_yes_no(reader, default, re_ask_reason)

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
        return _ask_one(reader, choices, default, re_ask_reason)

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
        return _ask_many(reader, choices, default, min_select, max_select,
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
        return _run_table(self.ask, self.show, columns, cells, question,
                          re_ask_reason, partial_check)

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


def _interpret_yes_no(answer: str | int, default: bool) -> Optional[bool]:
    """Map a bridge answer to a yes/no boolean, or None to re-ask."""
    if answer == '':
        return default
    if isinstance(answer, bool):
        return answer
    if isinstance(answer, int):
        return _yes_no_from_index(answer)
    return _yes_no_from_text(answer)


def _yes_no_from_index(index: int) -> Optional[bool]:
    """Map a 0-based ('yes', 'no') index to a boolean, or None."""
    if index == 0:
        return True
    if index == 1:
        return False
    return None


def _yes_no_from_text(text: str) -> Optional[bool]:
    """Map yes/no free text to a boolean, or None when unrecognised."""
    cleaned = text.strip().lower()
    if cleaned in ('y', 'yes', 'true'):
        return True
    if cleaned in ('n', 'no', 'false'):
        return False
    return None


def _ask_yes_no(reader: Callable[[Optional[str]], str | int], default: bool,
                re_ask_reason: Optional[str]) -> bool:
    """Re-ask through reader until a yes/no answer is understood."""
    reason = re_ask_reason
    while True:
        choice = _interpret_yes_no(reader(reason), default)
        if choice is not None:
            return choice
        reason = 'Please answer yes or no.'


# pylint: disable-next=too-many-arguments,too-many-positional-arguments
def _run_table(ask: AskReader, show: Callable[[str], None],
               columns: Sequence[TableColumn], cells: list[list[TableCell]],
               question: str, re_ask_reason: Optional[str],
               partial_check: Optional[PartialCheck]
               ) -> list[list[Optional[str]]]:
    """Show one table question and fill its editable cells via ask.

    The read-only cells stay fixed and only the editable cells are asked,
    one at a time, through the ask reader. This is the shared core of the
    console table interface and the deprecated base-class table fallback.
    """
    show(question)
    if re_ask_reason is not None:
        show(re_ask_reason)
    table: list[list[Optional[str]]] = [
        [cell.value for cell in row] for row in cells]
    _fill_table(ask, columns, cells, table, partial_check)
    return table


def _fill_table(ask: AskReader, columns: Sequence[TableColumn],
                cells: list[list[TableCell]], table: list[list[Optional[str]]],
                partial_check: Optional[PartialCheck]) -> None:
    """Fill the editable cells, stepping back one cell on WizardBack.

    WizardBack from the first editable cell has no earlier cell to
    return to, so it propagates and the wizard steps to the previous
    question. Cells already filled stay in the table while the user
    moves between cells.
    """
    spots = [(row, col) for row in range(len(cells))
             for col in range(len(columns)) if not columns[col].read_only]
    position = 0
    while position < len(spots):
        row, col = spots[position]
        check = _cell_checker(table, (row, col), partial_check)
        try:
            table[row][col] = _fill_cell(ask, columns, cells[row], col,
                                         table[row][col], check)
        except WizardBack:
            if position == 0:
                raise
            position -= 1
            continue
        position += 1


# pylint: disable-next=too-many-arguments,too-many-positional-arguments
def _fill_cell(ask: AskReader, columns: Sequence[TableColumn],
               row: list[TableCell], col: int, current: Optional[str],
               check: Callable[[Optional[str]], Optional[str]]
               ) -> Optional[str]:
    """Ask one editable cell until its value is accepted.

    Args:
        ask: The ask reader used to read the cell value.
        columns: The table columns, used to build the prompt.
        row: The cells of the row being filled.
        col: The index of the cell being filled.
        current: The cell's current value, kept when the user presses
                 enter and shown in the prompt.
        check: Records a candidate in the table and returns an error
               message, or None when the candidate is accepted.

    Returns:
        The accepted cell value, or None for an empty nullable cell.
    Raises:
        WizardBack: The user asked to return to the previous cell.
        WizardCancelLevel: The user cancelled the current level.
        WizardAbort: The user abandoned the whole configuration.
    """
    cell = row[col]
    prompt = _cell_prompt(columns, row, col, current)
    reason: Optional[str] = None
    while True:
        answer = ask(prompt, reason, cell.choices)
        valid, candidate = _cell_value(answer, cell, current)
        if not valid:
            reason = 'Please enter a value.'
            continue
        error = check(candidate)
        if error is None:
            return candidate
        reason = error


def _cell_prompt(columns: Sequence[TableColumn], row: list[TableCell],
                 col_index: int, current: Optional[str]) -> str:
    """Return the console prompt for one editable cell."""
    labels = [str(row[i].value) for i in range(len(columns))
              if columns[i].read_only and i != col_index
              and row[i].value is not None]
    prefix = ' / '.join(labels)
    lead = f'{prefix} - ' if prefix else ''
    shown = '' if current is None else current
    header = columns[col_index].header
    return f'{lead}{header} [{shown}] (enter=keep, :e=erase)'


def _cell_checker(table: list[list[Optional[str]]], position: tuple[int, int],
                  partial_check: Optional[PartialCheck]
                  ) -> Callable[[Optional[str]], Optional[str]]:
    """Return a per-cell check that records a candidate and validates it."""
    def check(candidate: Optional[str]) -> Optional[str]:
        table[position[0]][position[1]] = candidate
        if partial_check is None:
            return None
        accepted, message = partial_check(table, position)
        return None if accepted else message
    return check


def _cell_value(answer: str | int, cell: TableCell,
                current: Optional[str]) -> tuple[bool, Optional[str]]:
    """Map a bridge answer to a cell value and whether it is usable."""
    if answer == '':
        return (True, current)
    if isinstance(answer, str) and answer.strip().lower() == _ERASE_TOKEN:
        return _erased_value(cell)
    if isinstance(answer, bool):
        return (False, None)
    if isinstance(answer, int):
        return _indexed_value(answer, cell)
    return (True, answer)


def _erased_value(cell: TableCell) -> tuple[bool, Optional[str]]:
    """Map an erase request to a cell value and whether it is usable."""
    if cell.nullable:
        return (True, None)
    if cell.choices is None:
        return (True, '')
    return (False, None)


def _indexed_value(index: int, cell: TableCell) -> tuple[bool, Optional[str]]:
    """Map a 0-based choice index to a cell value, or mark it unusable."""
    if cell.choices is not None and 0 <= index < len(cell.choices):
        return (True, cell.choices[index])
    return (False, None)


def _int_text(text: str) -> Optional[int]:
    """Return an integer from text, or None when text is not an integer."""
    try:
        return int(text)
    except ValueError:
        return None


def _out_of_range(value: int, min_value: Optional[int],
                  max_value: Optional[int]) -> bool:
    """Return whether value lies outside the inclusive bounds."""
    below = min_value is not None and value < min_value
    above = max_value is not None and value > max_value
    return below or above


def _range_error(min_value: Optional[int], max_value: Optional[int]) -> str:
    """Return the message shown when an integer is out of range."""
    if min_value is None:
        return f'Please enter an integer at most {max_value}.'
    if max_value is None:
        return f'Please enter an integer at least {min_value}.'
    return f'Please enter an integer between {min_value} and {max_value}.'


def _ask_one(reader: Callable[[Optional[str]], str | int],
             choices: Sequence[str], default: Optional[str],
             re_ask_reason: Optional[str]) -> str:
    """Re-ask through reader until one valid choice is selected."""
    reason = re_ask_reason
    while True:
        chosen = _resolve_choice(reader(reason), choices, default)
        if chosen is not None:
            return chosen
        reason = _CHOICE_ERROR


# pylint: disable-next=too-many-arguments,too-many-positional-arguments
def _ask_many(reader: Callable[[Optional[str]], str | int],
              choices: Sequence[str], default: Optional[Sequence[str]],
              min_select: int, max_select: Optional[int],
              re_ask_reason: Optional[str], one_based: bool) -> list[str]:
    """Re-ask through reader until a valid set of choices is selected."""
    reason = re_ask_reason
    while True:
        chosen, error = _resolve_multi(reader(reason), choices, default,
                                       min_select, max_select, one_based)
        if chosen is not None:
            return chosen
        reason = error


def _resolve_choice(answer: str | int, choices: Sequence[str],
                    default: Optional[str]) -> Optional[str]:
    """Map a single-choice answer to a choice, or None to re-ask."""
    if answer == '':
        return default
    if isinstance(answer, bool):
        return None
    if isinstance(answer, int):
        return _choice_at_index(answer, choices)
    return _match_token(answer, choices, False)


# pylint: disable-next=too-many-arguments,too-many-positional-arguments
def _resolve_multi(answer: str | int, choices: Sequence[str],
                   default: Optional[Sequence[str]], min_select: int,
                   max_select: Optional[int],
                   one_based: bool) -> tuple[Optional[list[str]], str]:
    """Map a multi-choice answer to choices and an error to re-ask."""
    labels = _multi_labels(answer, choices, default, one_based)
    if labels is None:
        return (None, _CHOICE_ERROR)
    chosen = [choice for choice in choices if choice in set(labels)]
    too_few = len(chosen) < min_select
    too_many = max_select is not None and len(chosen) > max_select
    if too_few or too_many:
        return (None, _multi_count_error(min_select, max_select))
    return (chosen, '')


def _multi_labels(answer: str | int, choices: Sequence[str],
                  default: Optional[Sequence[str]],
                  one_based: bool) -> Optional[list[str]]:
    """Map a multi-choice answer to chosen labels, or None to re-ask."""
    if answer == '':
        return [] if default is None else list(default)
    if isinstance(answer, bool):
        return None
    if isinstance(answer, int):
        one = _choice_at_index(answer, choices)
        return None if one is None else [one]
    return _tokens_to_labels(answer, choices, one_based)


def _tokens_to_labels(text: str, choices: Sequence[str],
                      one_based: bool) -> Optional[list[str]]:
    """Map a comma-separated answer to labels, or None to re-ask."""
    labels: list[str] = []
    for raw in text.split(','):
        token = raw.strip()
        if token == '':
            continue
        one = _match_token(token, choices, one_based)
        if one is None:
            return None
        labels.append(one)
    return labels


def _match_token(token: str, choices: Sequence[str],
                 one_based: bool) -> Optional[str]:
    """Map one menu index or name to a choice, or None when no match."""
    index = _int_text(token)
    if index is not None:
        return _choice_at_index(index - 1 if one_based else index, choices)
    return _best_match(token, choices)


def _best_match(token: str, choices: Sequence[str]) -> Optional[str]:
    """Return the unique best name match for token, or None."""
    try:
        return string_best_match(token, choices, 'choice', StringIO())
    except InvalidConfiguration:
        return None


def _choice_at_index(index: int, choices: Sequence[str]) -> Optional[str]:
    """Return the choice at a 0-based index, or None when out of range."""
    if 0 <= index < len(choices):
        return choices[index]
    return None


def _multi_count_error(min_select: int, max_select: Optional[int]) -> str:
    """Return the message shown when the selected count is not allowed."""
    if max_select is None:
        return f'Please select at least {min_select}.'
    if min_select == max_select:
        return f'Please select exactly {min_select}.'
    return f'Please select between {min_select} and {max_select}.'
