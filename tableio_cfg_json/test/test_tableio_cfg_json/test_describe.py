#! /usr/bin/env python3
"""Tests for generated tableio-cfg-json format descriptions."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

# pylint: disable=protected-access

import json
import sys
from typing import Optional

import pytest

from tableio import CAP_NEEDED, Capabilities, ConfigSpec, FileAccess, \
    list_registered_tableio
from tableio.factory import TableIOFactoryNoCapabilityMatch
from tableio_cfg_json import describe_config, describe_config_example, \
    describe_config_members, describe_config_reference, \
    get_config_member_names, get_general_cfg_info, tio_json_config_default
import tableio_cfg_json.describe as describe_module


def _assert_line_limit(text: str) -> None:
    """Assert that generated documentation respects the line limit."""
    long_lines = [line for line in text.splitlines() if len(line) > 79]
    assert long_lines == []


def _json_after(text: str, heading: str) -> dict[str, object]:
    """Return the JSON object following a heading in generated text."""
    heading_pos = text.index(heading)
    json_pos = text.index('{', heading_pos)
    value, _ = json.JSONDecoder().raw_decode(text[json_pos:])
    assert isinstance(value, dict)
    return value


def test_public_api_exports() -> None:
    """Documentation helpers are exported from the package root."""
    assert callable(describe_config)
    assert callable(describe_config_example)
    assert callable(describe_config_members)
    assert callable(describe_config_reference)
    assert callable(get_config_member_names)
    assert callable(get_general_cfg_info)


def test_general_info_lines() -> None:
    """General information explains JSON structure and nested use."""
    text = get_general_cfg_info()
    _assert_line_limit(text)
    assert 'JSON object' in text
    assert 'nested' in text
    assert 'larger config-as-json' in text
    assert 'TableIO' not in text
    assert 'TioJsonConfig' not in text
    assert 'Members' not in text


def test_describe_all_formats() -> None:
    """The unrestricted description lists every registered format."""
    text = describe_config(include_compact_example=False)
    _assert_line_limit(text)
    for format_name in list_registered_tableio():
        assert format_name in text
    assert get_general_cfg_info().splitlines()[0] not in text


def test_read_filtering() -> None:
    """Read access limits documented formats and implementations."""
    text = describe_config(file_access=FileAccess.READ,
                           include_compact_example=False)
    _assert_line_limit(text)
    assert 'Choices: CSV, Excel, ODS.' in text
    assert 'Excel: OpenPyXL, pylightxl.' in text
    assert 'XlsxWriter' not in text


def test_csv_member_filter() -> None:
    """A selected format limits the member documentation."""
    text = describe_config(format_name='CSV', include_compact_example=False)
    _assert_line_limit(text)
    assert 'Choices: CSV.' in text
    assert 'csv.dialect' in text
    assert 'html.css_file' not in text
    assert 'latex.document_class' not in text


def test_config_member_names() -> None:
    """Relevant member names are returned in metadata order."""
    names = get_config_member_names(format_name='CSV')
    assert names[:2] == ('format_name', 'implementation')
    assert 'character_encoding' in names
    assert 'csv.delimiter' in names
    assert 'html.css_file' not in names


def test_member_names_impl() -> None:
    """An implementation filter limits formats and member names."""
    names = get_config_member_names(implementation='csv')
    assert names == get_config_member_names(format_name='CSV')


def test_impl_filter_no_match() -> None:
    """An implementation filter must match the remaining formats."""
    with pytest.raises(TableIOFactoryNoCapabilityMatch) as exc_info:
        get_config_member_names(format_name='CSV', implementation='OpenPyXL')
    assert 'Implementation "OpenPyXL"' in str(exc_info.value)


def test_config_members() -> None:
    """A compact endpoint summary lists choices and relevant names."""
    text = describe_config_members(file_access=FileAccess.READ)
    _assert_line_limit(text)
    assert 'format_name choices: CSV, Excel, ODS.' in text
    assert 'implementation choices' in text
    assert 'Excel: OpenPyXL, pylightxl.' in text
    assert 'Relevant members' in text
    assert '  format_name' in text


def test_members_filter_impl() -> None:
    """Implementation filtering narrows the compact summary."""
    text = describe_config_members(format_name='Excel',
                                   implementation='OpenPyXL')
    _assert_line_limit(text)
    assert 'format_name choices: Excel.' in text
    assert 'Excel: OpenPyXL.' in text
    assert 'pylightxl' not in text


def test_compact_example() -> None:
    """The compact example is the single best TableIO default."""
    text = describe_config()
    compact = _json_after(text, 'Compact example')
    config = tio_json_config_default(Capabilities(), FileAccess.CREATE)
    expected = json.loads(config.as_json_string(stderr_file=sys.stderr))
    assert compact == expected
    assert 'Compact example (CREATE)' in text
    assert 'Full example' not in text


@pytest.mark.parametrize(
    ('capabilities', 'heading'),
    [pytest.param(Capabilities(can_read=CAP_NEEDED, can_write=CAP_NEEDED),
                  'Compact example (UPDATE)', id='read-write'),
     pytest.param(Capabilities(can_read=CAP_NEEDED), 'Compact example (READ)',
                  id='read'),
     pytest.param(Capabilities(can_write=CAP_NEEDED),
                  'Compact example (CREATE)', id='write')])
def test_example_access_caps(capabilities: Capabilities, heading: str) -> None:
    """Example access is inferred from read/write capabilities."""
    text = describe_config(capabilities=capabilities)
    _assert_line_limit(text)
    assert heading in text


def test_config_example() -> None:
    """A standalone example contains only formatted JSON text."""
    text = describe_config_example(format_name='CSV')
    _assert_line_limit(text)
    assert text.startswith('{')
    assert 'Compact example' not in text
    assert json.loads(text) == {'format_name': 'CSV'}


def test_example_complete() -> None:
    """A standalone complete example contains all config fields."""
    text = describe_config_example(format_name='CSV', complete=True)
    data = json.loads(text)
    assert 'character_encoding' in data
    assert isinstance(data['csv'], dict)


def test_example_impl() -> None:
    """An explicit implementation is included in the example JSON."""
    text = describe_config_example(format_name='CSV', implementation='csv')
    data = json.loads(text)
    assert data == {'format_name': 'CSV', 'implementation': 'csv'}


def test_no_default_example() -> None:
    """Example generation reports when no default backend can be selected."""
    with pytest.raises(TableIOFactoryNoCapabilityMatch) as exc_info:
        describe_config_example(file_access=FileAccess.READ,
                                format_name='HTML')
    assert 'No default configuration matches' in str(exc_info.value)


def test_reference_selected() -> None:
    """Selected member references preserve metadata order."""
    text = describe_config_reference(
        member_names=('csv.delimiter', 'format_name'))
    _assert_line_limit(text)
    assert text.index('format_name') < text.index('csv.delimiter')
    assert 'The TableIO format name to use.' in text
    assert 'The one-character CSV delimiter.' in text
    assert 'html.css_file' not in text


def test_ref_empty() -> None:
    """An empty explicit reference selection returns empty text."""
    assert describe_config_reference(member_names=()) == ''


def test_reference_all() -> None:
    """Omitting member names describes all known members."""
    text = describe_config_reference()
    _assert_line_limit(text)
    assert 'format_name' in text
    assert 'latex.preamble' in text


def test_reference_unknown() -> None:
    """Unknown member names are reported as KeyError."""
    with pytest.raises(KeyError):
        describe_config_reference(member_names=('missing',))


def test_full_example_all() -> None:
    """The full example includes all TioJsonConfig fields."""
    text = describe_config(format_name='CSV', include_full_example=True)
    full = _json_after(text, 'Full example')
    assert set(full) == {
        'format_name', 'implementation', 'character_encoding', 'language',
        'title', 'paper_size', 'line_length', 'table_max_line_length',
        'table_alignment', 'csv', 'html', 'latex'
    }
    assert isinstance(full['csv'], dict)
    assert isinstance(full['html'], dict)
    assert isinstance(full['latex'], dict)


def test_both_examples() -> None:
    """Both compact and full examples can be requested together."""
    text = describe_config(format_name='CSV', include_full_example=True)
    compact = _json_after(text, 'Compact example')
    full = _json_after(text, 'Full example')
    assert compact == {'format_name': 'CSV'}
    assert 'character_encoding' in full


def test_no_matching_format() -> None:
    """No matching format raises the documented factory error."""
    caps = Capabilities(can_write_borders=CAP_NEEDED)
    with pytest.raises(TableIOFactoryNoCapabilityMatch):
        describe_config(capabilities=caps, file_access=FileAccess.CREATE,
                        format_name='CSV')


def test_unrestricted_overlap() -> None:
    """Metadata without restrictions matches every requested choice."""
    assert describe_module._overlaps(None, []) is True


def test_format_lookup_guard(monkeypatch: pytest.MonkeyPatch) -> None:
    """The impossible unknown-format fall-through has a guard error."""
    def fake_registered(
            capabilities: Optional[Capabilities] = None) -> list[str]:
        """Return no registered formats."""
        _ = capabilities
        return []

    def fake_impls(format_name: str,
                   capabilities: Optional[Capabilities] = None) -> list[str]:
        """Pretend the implementation lookup unexpectedly succeeded."""
        _ = format_name
        _ = capabilities
        return []
    monkeypatch.setattr(describe_module, 'list_registered_tableio',
                        fake_registered)
    monkeypatch.setattr(describe_module, 'list_implementations_tableio',
                        fake_impls)
    with pytest.raises(AssertionError, match='Unreachable'):
        describe_module._format_names(None, 'missing')


def test_format_caps_skip() -> None:
    """A capability-mismatched later format is reported after a skip."""
    caps = Capabilities(can_write_borders=CAP_NEEDED)
    with pytest.raises(TableIOFactoryNoCapabilityMatch) as exc_info:
        describe_config(capabilities=caps, file_access=FileAccess.CREATE,
                        format_name='HTML')
    assert 'does not match the capabilities' in str(exc_info.value)


def test_member_no_default() -> None:
    """A member without a default omits the default line."""
    spec = ConfigSpec(name='member_x', description='A member.',
                      value_type='str')
    lines: list[str] = []
    describe_module._add_member(lines, spec, [], [])
    assert 'member_x' in lines
    assert not any('Default' in line for line in lines)


def test_ref_no_default() -> None:
    """A reference member without a default omits the default line."""
    spec = ConfigSpec(name='member_y', description='A member.',
                      value_type='str')
    lines: list[str] = []
    describe_module._add_ref_member(lines, spec)
    assert 'member_y' in lines
    assert not any('Default' in line for line in lines)


def test_example_all_fail() -> None:
    """When every candidate access fails the first error is the cause."""
    caps = Capabilities(can_read=CAP_NEEDED, can_write=CAP_NEEDED)
    with pytest.raises(TableIOFactoryNoCapabilityMatch) as exc_info:
        describe_config_example(capabilities=caps, format_name='HTML')
    assert exc_info.value.__cause__ is not None
