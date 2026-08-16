#! /usr/local/bin/python3
"""What the TableIO configuration members mean, for a configuration editor.

An application that hands its own configuration class to one of the
edit-cfg-json editors describes the members it declares in an
``edit_cfg_json.Descriptions`` mapping, because a member has no docstring at
runtime. The members that come from this package are this package's to
describe, so an application that nests a TioJsonConfig gets that text from
here instead of writing the TableIO configuration down a second time.

What the editor works out for itself is deliberately absent. It reads the
docstring of every configuration class, it says what kind of value each
member holds, it says which members may be left out of the file, and where a
member holds an enum it lists the names of that enum. What it never reads is
a validator, so the values a plain string member accepts are listed here, and
what those values mean is written here as well.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Collection

from config_as_json import ConfigPath
from edit_cfg_json import Descriptions
from tableio import ConfigSpec, tio_config_specs
from tableio_cfg_json.spec_text import CHOICES_LABEL, DEFAULT_LABEL, \
    FORMATS_LABEL, IMPLS_LABEL, end_sentence, value_list

STRING_TYPES = ('str', 'Optional[str]')
"""The member types whose accepted values the editor cannot work out.

A member that holds an enum is one the editor lists the names of itself,
because the parse converter of the configuration class names the enum class.
A member that holds a plain string has its values in a validator instead, and
a validator is what the editor never reads.
"""

SECTION_TEXT = 'These settings are used only by the formats named below.'
"""What is said about one optional format-specific section as a whole."""

VALUE_MEANINGS: dict[str, dict[str, str]] = {
    'table_alignment': {
        'RIGHT': 'Every value is put at the right edge of its column.',
        'LEFT': 'Every value is put at the left edge of its column.',
        'LEFT_BUT_DIGITS_RIGHT': 'At the left edge, except a value written '
                                 'with only digits, dots and commas, which '
                                 'goes to the right edge.',
        'CENTER': 'Every value is centered in its column.',
        'CENTER_BUT_DIGITS_RIGHT': 'Centered, except a value written with '
                                   'only digits, dots and commas, which goes '
                                   'to the right edge.'},
    'csv.dialect': {
        'EXCEL': 'What Microsoft Excel reads and writes: comma separated, '
                 'carriage return and line feed at the end of a line, and '
                 'quotes only where they are needed.',
        'UNIX': 'Comma separated, line feed at the end of a line, and every '
                'field quoted.'},
    'csv.quoting': {
        'all': 'Quote every field.',
        'minimal': 'Quote only a field holding the delimiter, the quote '
                   'character or a line break.',
        'nonnumeric': 'Quote every field that is not a number.',
        'none': 'Quote nothing, and write the escape character before a '
                'character that would need quoting.',
        'strings': 'Quote every field that is text, and write no value at '
                   'all as an empty unquoted field.',
        'notnull': 'Quote every field that has a value, and write no value '
                   'at all as an empty unquoted field.'},
    'latex.document_class': {
        'Article': 'Headings start at section. There are no chapters.',
        'Report': 'Headings start at chapter.',
        'Book': 'Headings start at part, and the next level is chapter.',
        'Letter': 'The LaTeX letter class. Headings start at section.'}}
"""What each value of a member means, where the name does not say it.

Only the members whose values need explaining are here. A format name, an
implementation name and a paper size are listed without a sentence each,
because the name is the whole of what there is to say about it.
"""

EXTRA_NOTES: dict[str, str] = {
    'latex.preamble': 'A preamble holding a \\documentclass command cannot '
                      'be combined with paper_size.'}
"""Rules between members that no single member validator can state."""


def _choice_lines(spec: ConfigSpec) -> list[str]:
    """Return the lines saying which values one member accepts.

    Args:
        spec: TableIO configuration specification.
    Returns:
        The list of accepted values where the editor cannot show it, followed
        by one line per value that needs explaining.
    """
    choices = spec.choices if spec.choices is not None else ()
    meanings = VALUE_MEANINGS.get(spec.name, {})
    listed = value_list(CHOICES_LABEL, spec.choices) \
        if spec.value_type in STRING_TYPES else None
    explained = [f'{value}: {meanings[value]}'
                 for value in choices if value in meanings]
    return ([listed] if listed is not None else []) + explained


def _member_lines(spec: ConfigSpec) -> list[str]:
    """Return everything this package says about one member.

    Args:
        spec: TableIO configuration specification.
    Returns:
        The lines of the description of that member, most important first.
    """
    lines = [spec.description] + _choice_lines(spec)
    note = EXTRA_NOTES.get(spec.name)
    if note is not None:
        lines.append(note)
    if spec.default_text is not None:
        lines.append(f'{DEFAULT_LABEL}: {end_sentence(spec.default_text)}')
    return lines + _relevance_lines(spec)


def _relevance_lines(spec: ConfigSpec) -> list[str]:
    """Return the lines saying where one member has an effect.

    Args:
        spec: TableIO configuration specification.
    Returns:
        The formats and the implementations the member matters for, leaving
        out whichever of the two TableIO does not restrict.
    """
    listed = [value_list(FORMATS_LABEL, spec.relevant_formats),
              value_list(IMPLS_LABEL, spec.relevant_impls)]
    return [line for line in listed if line is not None]


def _section_formats(specs: Collection[ConfigSpec]) -> dict[str, list[str]]:
    """Return the formats that each optional nested section belongs to.

    A section is described by what its own members are relevant for, so a
    section added to TableIO later is described without being named here.

    Args:
        specs: TableIO configuration specifications.
    Returns:
        The relevant format names of each section, in metadata order and
        without duplicates, keyed by the section member name.
    """
    found: dict[str, list[str]] = {}
    for spec in specs:
        section, _, member = spec.name.partition('.')
        if not member:
            continue
        formats = found.setdefault(section, [])
        formats.extend(name for name in (spec.relevant_formats or ())
                       if name not in formats)
    return found


def _section_lines(formats: list[str]) -> list[str]:
    """Return the description lines of one optional nested section.

    Args:
        formats: Format names that the members of the section matter for.
    Returns:
        The lines of the description, and nothing at all when TableIO
        restricts the section to no particular format.
    """
    listed = value_list(FORMATS_LABEL, tuple(formats))
    return [] if listed is None else [SECTION_TEXT, listed]


def _described(specs: Collection[ConfigSpec]) -> dict[ConfigPath, str]:
    """Return the description of every member and every nested section.

    Args:
        specs: TableIO configuration specifications.
    Returns:
        One description per member of the TioJsonConfig tree, under the path
        that addresses it inside a TioJsonConfig.
    """
    described = {tuple(spec.name.split('.')): '\n'.join(_member_lines(spec))
                 for spec in specs}
    for name, formats in _section_formats(specs).items():
        lines = _section_lines(formats)
        if lines:
            described[(name,)] = '\n'.join(lines)
    return described


def tio_json_descriptions(prefix: ConfigPath = ()) -> Descriptions:
    """Get what each TioJsonConfig member means, for a config editor.

    Pass the result to ``edit_cfg_json.edit()``, ``editor_model()`` or one of
    the edit-cfg-json editor backends, so that a user editing a TableIO
    configuration is told what the members are for. An application that
    declares a TioJsonConfig as one member of its own configuration class
    passes the path of that member as the prefix, because a description
    addresses the whole path to the member it is about. An application with
    several TableIO endpoints calls this once per endpoint and merges the
    results.

    The text follows the TableIO metadata, so it names the formats,
    implementations and values that are registered when this is called.

    Args:
        prefix: Path of the member holding the TioJsonConfig, which is
            ``('input',)`` for a member called ``input`` and ``()`` for a
            TioJsonConfig that is the whole configuration being edited.
    Returns:
        What each member of a TioJsonConfig and of its optional ``csv``,
        ``html`` and ``latex`` sections means, under the absolute path of
        that member.
    """
    return {prefix + path: text
            for path, text in _described(tio_config_specs().values()).items()}


TIO_JSON_DESCRIPTIONS: Descriptions = tio_json_descriptions()
"""What each member means, for a TioJsonConfig that is the whole config.

This is the value of ``tio_json_descriptions()`` as the formats and
implementations were registered when this module was imported, offered as a
constant for a program that needs a name to point at rather than a call to
make. An application that registers a TableIO format of its own after
importing this module calls ``tio_json_descriptions()`` instead.
"""
