#! /usr/bin/env python3
"""Tests for generated tableio-cfg-json format descriptions."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import json
import sys

import pytest

from tableio import CAP_NEEDED, Capabilities, FileAccess, \
    list_registered_tableio
from tableio.factory import TableIOFactoryNoCapabilityMatch
from tableio_cfg_json import describe_config, get_general_cfg_info, \
    tio_json_config_default


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


def test_compact_example() -> None:
    """The compact example is the single best TableIO default."""
    text = describe_config()
    compact = _json_after(text, 'Compact example')
    config = tio_json_config_default(Capabilities(), FileAccess.CREATE)
    expected = json.loads(config.as_json_string(stderr_file=sys.stderr))
    assert compact == expected
    assert 'Compact example (CREATE)' in text
    assert 'Full example' not in text


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
