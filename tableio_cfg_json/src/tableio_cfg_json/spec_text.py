#! /usr/local/bin/python3
"""Text fragments built from one TableIO configuration specification.

TableIO owns the metadata about its configuration members, and this package
turns that metadata into text in two places: the plain text guides of
describe.py and the editor descriptions of descriptions.py. The labels and
the small formatting rules are shared here so that one member reads the same
way whichever of the two a user meets it in.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional

CHOICES_LABEL = 'Choices'
"""Label of the list of values that one member accepts."""

DEFAULT_LABEL = 'Default'
"""Label of what one member holds when nothing is stored for it."""

FORMATS_LABEL = 'Relevant formats'
"""Label of the formats that one member has an effect for."""

IMPLS_LABEL = 'Relevant implementations'
"""Label of the implementations that one member has an effect for."""


def value_list(label: str, values: Optional[tuple[str, ...]]) -> Optional[str]:
    """Return one labelled comma-separated value list.

    Args:
        label: Label to prepend.
        values: Values to list. ``None`` and an empty tuple both mean that
            there is no restriction worth stating.
    Returns:
        The labelled list as one sentence, or ``None`` when there is nothing
        to list.
    """
    if not values:
        return None
    return f'{label}: {", ".join(values)}.'


def end_sentence(text: str) -> str:
    """Return text with sentence-ending punctuation.

    Args:
        text: Text that may already end with punctuation.
    Returns:
        Text ending with a sentence punctuation mark.
    """
    if text.endswith(('.', '!', '?')):
        return text
    return text + '.'
