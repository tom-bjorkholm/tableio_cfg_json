#! /usr/bin/env python3
"""Tests for the editor descriptions of the TableIO configuration."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from enum import Enum
from typing import Optional

import pytest

from config_as_json import Config, ConfigPath, ParseConverter
from tableio import tio_config_specs
from tableio_cfg_json import TIO_JSON_DESCRIPTIONS, TioJsonCsvConfig, \
    TioJsonHtmlConfig, TioJsonLatexConfig, tio_json_descriptions
from tableio_cfg_json.descriptions import EXTRA_NOTES, VALUE_MEANINGS

SECTIONS = ('csv', 'html', 'latex')


def _spec_paths() -> list[ConfigPath]:
    """Return the path of every member TableIO declares."""
    return [tuple(name.split('.')) for name in tio_config_specs()]


def _converters(config: Config) -> dict[str, ParseConverter]:
    """Return the parse converters of one configuration object."""
    declared = config.parse_converters()
    return {} if declared is None else declared


def _enum_members() -> set[str]:
    """Return the dotted names of members that the editor sees as enums.

    The parse converters of the configuration classes are what the editor
    reads the names of an enum from, so they decide which members must not
    have their values listed a second time in a description. A converter for
    a member the class does not declare is left out, because config-as-json
    declares one of those for every class.
    """
    sections: list[tuple[str, Config]] = [
        ('csv', TioJsonCsvConfig()), ('html', TioJsonHtmlConfig()),
        ('latex', TioJsonLatexConfig())]
    return {f'{section}.{member}' for section, config in sections
            for member, converter in _converters(config).items()
            if member in vars(config)
            and issubclass(converter.result_type, Enum)}


def test_every_member_said() -> None:
    """Every member TableIO declares has a description of its own."""
    described = tio_json_descriptions()
    for path in _spec_paths():
        assert path in described
        assert described[path]


def test_sections_described() -> None:
    """The optional format-specific sections are described as a whole."""
    described = tio_json_descriptions()
    for section in SECTIONS:
        assert 'used only by the formats' in described[(section,)]
    assert 'Relevant formats: CSV.' in described[('csv',)]
    assert 'Relevant formats: HTML.' in described[('html',)]
    assert 'Relevant formats: LaTeX.' in described[('latex',)]


def test_paths_are_real() -> None:
    """Nothing is described that is not a member or a section."""
    known = set(_spec_paths()) | {(name,) for name in SECTIONS}
    assert set(tio_json_descriptions()) <= known


def test_constant_matches() -> None:
    """The constant is what the function answers with no prefix."""
    assert dict(TIO_JSON_DESCRIPTIONS) == dict(tio_json_descriptions())


@pytest.mark.parametrize('prefix', [(), ('input',), ('outputs', '['),
                                    ('a', 'b', 'c')])
def test_prefix_moves_paths(prefix: ConfigPath) -> None:
    """A prefix puts every description below the named member."""
    described = tio_json_descriptions(prefix)
    plain = tio_json_descriptions()
    assert set(described) == {prefix + path for path in plain}
    for path, text in plain.items():
        assert described[prefix + path] == text


@pytest.mark.parametrize('name', sorted(VALUE_MEANINGS))
def test_meanings_are_choices(name: str) -> None:
    """Each explained value is a value that TableIO accepts."""
    choices = tio_config_specs()[name].choices
    assert choices is not None
    assert set(VALUE_MEANINGS[name]) == set(choices)


@pytest.mark.parametrize('name', sorted(EXTRA_NOTES))
def test_notes_name_members(name: str) -> None:
    """Each extra note is about a member that TableIO declares."""
    assert name in tio_config_specs()


def test_str_choices_listed() -> None:
    """A plain string member lists the values its validator accepts."""
    described = tio_json_descriptions()
    for spec in tio_config_specs().values():
        text = described[tuple(spec.name.split('.'))]
        wanted = spec.choices is not None and \
            spec.name not in _enum_members()
        assert ('Choices: ' in text) == wanted, spec.name


def test_enum_choices_absent() -> None:
    """A member holding an enum leaves the value list to the editor."""
    described = tio_json_descriptions()
    for name in _enum_members():
        assert 'Choices: ' not in described[tuple(name.split('.'))]


def test_enum_meaning_given() -> None:
    """The meaning of each enum value is what the description adds."""
    text = tio_json_descriptions()[('csv', 'dialect')]
    assert 'EXCEL: ' in text
    assert 'UNIX: ' in text
    assert 'Microsoft Excel' in text


def test_no_type_information() -> None:
    """No description repeats the value kind that the editor derives."""
    for text in tio_json_descriptions().values():
        assert 'Type: ' not in text
        assert 'may be left out' not in text


@pytest.mark.parametrize('name,expected', [
    ('character_encoding', 'Relevant formats: CSV, HTML, LaTeX, md, reST, '
                           'txt.'),
    ('line_length', 'Relevant implementations: mformat.'),
    ('csv.quoting', 'minimal: Quote only a field holding the delimiter'),
    ('latex.preamble', '\\documentclass'),
    ('table_alignment', 'CENTER_BUT_DIGITS_RIGHT: Centered')])
def test_member_text_content(name: str, expected: str) -> None:
    """A member description carries what the editor cannot work out."""
    assert expected in tio_json_descriptions()[tuple(name.split('.'))]


@pytest.mark.parametrize('name', ['format_name', 'implementation'])
def test_base_member_no_scope(name: str) -> None:
    """A member that every format uses names no format and no backend."""
    text = tio_json_descriptions()[(name,)]
    assert 'Relevant formats' not in text
    assert 'Relevant implementations' not in text


def _default_line(name: str) -> Optional[str]:
    """Return the default line of one member description."""
    text = tio_json_descriptions()[tuple(name.split('.'))]
    for line in text.splitlines():
        if line.startswith('Default: '):
            return line
    return None


@pytest.mark.parametrize('name', ['format_name', 'implementation',
                                  'paper_size', 'csv.dialect'])
def test_default_is_stated(name: str) -> None:
    """A member whose metadata states a default says what it is."""
    line = _default_line(name)
    assert line is not None
    assert line.endswith('.')
