#! /usr/local/bin/python3
"""Types used as arguments to the WizardUIBridge class."""

from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Callable, Optional, Sequence


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


class WizardPathKind(Enum):
    """Expected path type and existence for a path question."""

    EXISTING_FILE = auto()
    NON_EXISTING_FILE = auto()
    FILE = auto()
    EXISTING_DIR = auto()
    NON_EXISTING_DIR = auto()
    DIR = auto()


@dataclass(frozen=True)
class PathAskOptions:
    """Options for a path question."""

    kind: WizardPathKind = WizardPathKind.FILE
    nullable: bool = False
    default: Optional[Path] = None


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
