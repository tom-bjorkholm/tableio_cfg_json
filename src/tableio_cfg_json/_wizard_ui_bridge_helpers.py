#! /usr/local/bin/python3
"""Helpers for the WizardUiBridge base class."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from io import StringIO
from pathlib import Path
from typing import Callable, Optional, Sequence
from config_as_json import InvalidConfiguration, string_best_match
from tableio_cfg_json.wizard_ui_bridge_arg_types import PartialCheck, \
    AskReader, WizardBack, WizardPathKind, PathAskOptions, TableColumn, \
    TableCell


_ERASE_TOKEN = ':e'  # empties an editable cell in the ask_table fallback
CHOICE_ERROR = 'Please enter one of the listed choices.'
_PATH_REQUIRED = 'Please enter a path.'


def check_text_args(default: Optional[str], sensitive: bool) -> None:
    """Raise when text-question arguments are inconsistent."""
    if sensitive and default is not None:
        raise ValueError('default is not allowed for sensitive input')


def question_with_default(question: str, default: Optional[str]) -> str:
    """Return question with a bracketed default when one is given."""
    if default is None:
        return question
    return f'{question} [{default}]'


def text_answer(text: str, nullable: bool,
                default: Optional[str]) -> Optional[str]:
    """Return the public text answer for raw text from a bridge."""
    if text == '' and default is not None:
        return default
    if text == '' and nullable:
        return None
    return text


def path_answer(text: Optional[str], options: PathAskOptions
                ) -> tuple[bool, Optional[Path], Optional[str]]:
    """Return whether a path answer is final, its value, and retry reason."""
    if text is None:
        return (True, None, None)
    if text == '' and options.default is not None:
        return (True, options.default, None)
    if text == '' and options.nullable:
        return (True, None, None)
    if text == '':
        return (False, None, _PATH_REQUIRED)
    path = Path(text)
    reason = _path_error(path, options.kind)
    return (reason is None, path if reason is None else None, reason)


def _path_error(path: Path, kind: WizardPathKind) -> Optional[str]:
    """Return the validation error for path, or None when accepted."""
    exists, error = _path_exists(path)
    if error is not None:
        return error
    if _path_must_not_exist(kind) and exists:
        return 'Path already exists.'
    if _path_must_exist(kind) and not exists:
        return 'Path does not exist.'
    if exists and _path_must_be_file(kind) and not path.is_file():
        return 'Path is not a file.'
    if exists and _path_must_be_dir(kind) and not path.is_dir():
        return 'Path is not a directory.'
    return None


def _path_exists(path: Path) -> tuple[bool, Optional[str]]:
    """Return whether path exists, or an error for an unusable path."""
    try:
        return (path.exists(), None)
    except OSError as error:
        return (False, f'Invalid path: {error}.')


def _path_must_exist(kind: WizardPathKind) -> bool:
    """Return whether kind requires an existing path."""
    return kind in (WizardPathKind.EXISTING_FILE, WizardPathKind.EXISTING_DIR)


def _path_must_not_exist(kind: WizardPathKind) -> bool:
    """Return whether kind requires a path that does not exist."""
    return kind in (
        WizardPathKind.NON_EXISTING_FILE, WizardPathKind.NON_EXISTING_DIR)


def _path_must_be_file(kind: WizardPathKind) -> bool:
    """Return whether kind rejects existing directories."""
    return kind in (WizardPathKind.EXISTING_FILE, WizardPathKind.FILE)


def _path_must_be_dir(kind: WizardPathKind) -> bool:
    """Return whether kind rejects existing files."""
    return kind in (WizardPathKind.EXISTING_DIR, WizardPathKind.DIR)


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


def ask_yes_no(reader: Callable[[Optional[str]], str | int], default: bool,
               re_ask_reason: Optional[str]) -> bool:
    """Re-ask through reader until a yes/no answer is understood."""
    reason = re_ask_reason
    while True:
        choice = _interpret_yes_no(reader(reason), default)
        if choice is not None:
            return choice
        reason = 'Please answer yes or no.'


# pylint: disable-next=too-many-arguments,too-many-positional-arguments
def run_table(ask: AskReader, show: Callable[[str], None],
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
        check = cell_checker(table, (row, col), partial_check)
        try:
            table[row][col] = fill_cell(ask, columns, cells[row], col,
                                        table[row][col], check)
        except WizardBack:
            if position == 0:
                raise
            position -= 1
            continue
        position += 1


# pylint: disable-next=too-many-arguments,too-many-positional-arguments
def fill_cell(ask: AskReader, columns: Sequence[TableColumn],
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


def cell_checker(table: list[list[Optional[str]]], position: tuple[int, int],
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


def int_text(text: str) -> Optional[int]:
    """Return an integer from text, or None when text is not an integer."""
    try:
        return int(text)
    except ValueError:
        return None


def out_of_range(value: int, min_value: Optional[int],
                 max_value: Optional[int]) -> bool:
    """Return whether value lies outside the inclusive bounds."""
    below = min_value is not None and value < min_value
    above = max_value is not None and value > max_value
    return below or above


def range_error(min_value: Optional[int], max_value: Optional[int]) -> str:
    """Return the message shown when an integer is out of range."""
    if min_value is None:
        return f'Please enter an integer at most {max_value}.'
    if max_value is None:
        return f'Please enter an integer at least {min_value}.'
    return f'Please enter an integer between {min_value} and {max_value}.'


def ask_one(reader: Callable[[Optional[str]], str | int],
            choices: Sequence[str], default: Optional[str],
            re_ask_reason: Optional[str]) -> str:
    """Re-ask through reader until one valid choice is selected."""
    reason = re_ask_reason
    while True:
        chosen = _resolve_choice(reader(reason), choices, default)
        if chosen is not None:
            return chosen
        reason = CHOICE_ERROR


# pylint: disable-next=too-many-arguments,too-many-positional-arguments
def ask_many(reader: Callable[[Optional[str]], str | int],
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
    return match_token(answer, choices, False)


# pylint: disable-next=too-many-arguments,too-many-positional-arguments
def _resolve_multi(answer: str | int, choices: Sequence[str],
                   default: Optional[Sequence[str]], min_select: int,
                   max_select: Optional[int],
                   one_based: bool) -> tuple[Optional[list[str]], str]:
    """Map a multi-choice answer to choices and an error to re-ask."""
    labels = _multi_labels(answer, choices, default, one_based)
    if labels is None:
        return (None, CHOICE_ERROR)
    chosen = [choice for choice in choices if choice in set(labels)]
    too_few = len(chosen) < min_select
    too_many = max_select is not None and len(chosen) > max_select
    if too_few or too_many:
        return (None, multi_count_error(min_select, max_select))
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
        one = match_token(token, choices, one_based)
        if one is None:
            return None
        labels.append(one)
    return labels


def match_token(token: str, choices: Sequence[str],
                one_based: bool) -> Optional[str]:
    """Map one menu index or name to a choice, or None when no match."""
    index = int_text(token)
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


def multi_count_error(min_select: int, max_select: Optional[int]) -> str:
    """Return the message shown when the selected count is not allowed."""
    if max_select is None:
        return f'Please select at least {min_select}.'
    if min_select == max_select:
        return f'Please select exactly {min_select}.'
    return f'Please select between {min_select} and {max_select}.'
