#! /usr/local/bin/python3
"""Describe the configuration file format of tableio-cfg-json."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
from textwrap import wrap
from typing import Optional

from tableio import Capabilities, ConfigError, ConfigSpec, FileAccess, \
    add_access_capabilities, list_implementations_tableio, \
    list_registered_tableio, tio_config_specs
from tableio.factory import TableIOFactoryNoCapabilityMatch
from tableio_cfg_json.config import tio_json_config_default

_WIDTH = 79
_BASE_NAMES = ('format_name', 'implementation')


def _wrapped(text: str, initial: str = '',
             subsequent: Optional[str] = None) -> list[str]:
    """Return text wrapped to the module line width.

    Args:
        text: Text to wrap.
        initial: Prefix for the first returned line.
        subsequent: Prefix for following returned lines.
    Returns:
        Wrapped lines.
    """
    next_prefix = initial if subsequent is None else subsequent
    return wrap(text, width=_WIDTH, initial_indent=initial,
                subsequent_indent=next_prefix)


def _add_wrapped(lines: list[str], text: str, initial: str = '',
                 subsequent: Optional[str] = None) -> None:
    """Append wrapped text to a line list.

    Args:
        lines: Lines to extend.
        text: Text to wrap and append.
        initial: Prefix for the first appended line.
        subsequent: Prefix for following appended lines.
    Returns:
        None.
    """
    lines.extend(_wrapped(text, initial=initial, subsequent=subsequent))


def _paragraph(text: str) -> str:
    """Return one wrapped paragraph.

    Args:
        text: Paragraph text to wrap.
    Returns:
        A wrapped paragraph string.
    """
    return '\n'.join(_wrapped(text))


def _matching_caps(capabilities: Optional[Capabilities],
                   file_access: Optional[FileAccess]) -> \
        Optional[Capabilities]:
    """Return capabilities used for backend filtering.

    Args:
        capabilities: Application capability requirements.
        file_access: Optional file access that adds read/write requirements.
    Returns:
        Capabilities with access requirements added, or None when no filter
        was supplied.
    """
    if file_access is None:
        return capabilities
    base_caps = capabilities if capabilities is not None else Capabilities()
    return add_access_capabilities(file_access, base_caps)


def _format_names(match_caps: Optional[Capabilities],
                  format_name: Optional[str]) -> list[str]:
    """Return matching format names with TableIO casing.

    Args:
        match_caps: Capabilities used for TableIO filtering.
        format_name: Optional requested format name.
    Raises:
        TableIOFactoryNoCapabilityMatch: The requested filters match no
            registered format.
    Returns:
        Matching format names.
    """
    matching = list_registered_tableio(capabilities=match_caps)
    if format_name is None:
        return matching
    for name in matching:
        if name.lower() == format_name.lower():
            return [name]
    for name in list_registered_tableio():
        if name.lower() == format_name.lower():
            msg = f'Format "{format_name}" does not match the capabilities.'
            raise TableIOFactoryNoCapabilityMatch(msg)
    list_implementations_tableio(format_name)
    raise AssertionError('Unreachable format lookup failure.')


def _impls_by_format(format_names: list[str],
                     match_caps: Optional[Capabilities]) -> \
        dict[str, list[str]]:
    """Return matching implementation names keyed by format.

    Args:
        format_names: Matching format names.
        match_caps: Capabilities used for TableIO filtering.
    Returns:
        Matching implementation names for each format.
    """
    return {
        name: list_implementations_tableio(name, capabilities=match_caps)
        for name in format_names
    }


def _unique_impls(impls_by_fmt: dict[str, list[str]]) -> list[str]:
    """Return implementation names without duplicates.

    Args:
        impls_by_fmt: Implementation names keyed by format.
    Returns:
        Implementation names in first-seen order.
    """
    ret: list[str] = []
    for impls in impls_by_fmt.values():
        for impl in impls:
            if impl not in ret:
                ret.append(impl)
    return ret


def _overlaps(values: Optional[tuple[str, ...]], choices: list[str]) -> bool:
    """Return whether optional metadata values overlap choices.

    Args:
        values: Optional metadata values from TableIO.
        choices: Matching choices from the current request.
    Returns:
        True when no metadata restriction exists or at least one choice
        overlaps.
    """
    if values is None:
        return True
    return any(value in choices for value in values)


def _spec_matches(spec: ConfigSpec, format_names: list[str],
                  impl_names: list[str]) -> bool:
    """Return whether a TableIO config spec is relevant.

    Args:
        spec: TableIO configuration specification.
        format_names: Matching format names.
        impl_names: Matching implementation names.
    Returns:
        True when the spec can affect at least one matching backend.
    """
    if spec.name in _BASE_NAMES:
        return True
    return _overlaps(spec.relevant_formats, format_names) and \
        _overlaps(spec.relevant_impls, impl_names)


def _relevant_specs(format_names: list[str],
                    impls_by_fmt: dict[str, list[str]]) -> list[ConfigSpec]:
    """Return TableIO specs relevant to the matching backends.

    Args:
        format_names: Matching format names.
        impls_by_fmt: Matching implementation names keyed by format.
    Returns:
        Relevant specs in TableIO metadata order.
    """
    impl_names = _unique_impls(impls_by_fmt)
    return [
        spec for spec in tio_config_specs().values()
        if _spec_matches(spec, format_names, impl_names)
    ]


def _member_choices(spec: ConfigSpec, format_names: list[str],
                    impl_names: list[str]) -> Optional[tuple[str, ...]]:
    """Return filtered choice values for one member.

    Args:
        spec: TableIO configuration specification.
        format_names: Matching format names.
        impl_names: Matching implementation names.
    Returns:
        Choice values for the member, or None when it has no finite choices.
    """
    if spec.name == 'format_name':
        return tuple(format_names)
    if spec.name == 'implementation':
        return tuple(impl_names)
    return spec.choices


def _filtered(values: Optional[tuple[str, ...]],
              choices: list[str]) -> Optional[tuple[str, ...]]:
    """Return values filtered to matching choices.

    Args:
        values: Optional metadata values from TableIO.
        choices: Matching choices from the current request.
    Returns:
        Matching metadata values, or None when no metadata restriction exists.
    """
    if values is None:
        return None
    return tuple(value for value in values if value in choices)


def _add_value_list(lines: list[str], label: str,
                    values: Optional[tuple[str, ...]]) -> None:
    """Append a labelled comma-separated value list when present.

    Args:
        lines: Lines to extend.
        label: Label to prepend.
        values: Values to show.
    Returns:
        None.
    """
    if values:
        _add_wrapped(lines, f'{label}: {", ".join(values)}.', '  ', '  ')


def _end_sentence(text: str) -> str:
    """Return text with sentence-ending punctuation.

    Args:
        text: Text that may already end with punctuation.
    Returns:
        Text ending with a sentence punctuation mark.
    """
    if text.endswith(('.', '!', '?')):
        return text
    return text + '.'


def _add_member(lines: list[str], spec: ConfigSpec, format_names: list[str],
                impl_names: list[str]) -> None:
    """Append documentation for one configuration member.

    Args:
        lines: Lines to extend.
        spec: TableIO configuration specification.
        format_names: Matching format names.
        impl_names: Matching implementation names.
    Returns:
        None.
    """
    lines.append(spec.name)
    _add_wrapped(lines, spec.description, '  ', '  ')
    _add_wrapped(lines, f'Type: {spec.value_type}.', '  ', '  ')
    if spec.default_text is not None:
        _add_wrapped(lines, f'Default: {_end_sentence(spec.default_text)}',
                     '  ', '  ')
    _add_value_list(lines, 'Choices',
                    _member_choices(spec, format_names, impl_names))
    _add_value_list(lines, 'Relevant formats',
                    _filtered(spec.relevant_formats, format_names))
    _add_value_list(lines, 'Relevant implementations',
                    _filtered(spec.relevant_impls, impl_names))


def _uses_read_caps(capabilities: Capabilities) -> bool:
    """Return whether capabilities imply a read-oriented example.

    Args:
        capabilities: Application capability requirements.
    Returns:
        True when the capabilities request reading behavior.
    """
    return capabilities.can_read.supported or \
        capabilities.can_read_box.supported or \
        capabilities.can_find_value_position.supported


def _uses_write_caps(capabilities: Capabilities) -> bool:
    """Return whether capabilities imply a write-oriented example.

    Args:
        capabilities: Application capability requirements.
    Returns:
        True when the capabilities request writing behavior.
    """
    return capabilities.can_write.supported or \
        capabilities.can_fmt_row.supported or \
        capabilities.can_fmt_value.supported or \
        capabilities.filtered_data_range.supported or \
        capabilities.can_write_box.supported or \
        capabilities.can_write_highlight.supported or \
        capabilities.multi_sheet.supported or \
        capabilities.can_write_borders.supported


def _example_accesses(capabilities: Capabilities,
                      file_access: Optional[FileAccess]) -> list[FileAccess]:
    """Return file accesses to try for example generation.

    Args:
        capabilities: Application capability requirements.
        file_access: Optional file access supplied by the caller.
    Returns:
        Candidate file accesses in preference order.
    """
    if file_access is not None:
        return [file_access]
    uses_read = _uses_read_caps(capabilities)
    uses_write = _uses_write_caps(capabilities)
    if uses_read and uses_write:
        return [FileAccess.UPDATE, FileAccess.READ, FileAccess.CREATE]
    if uses_read:
        return [FileAccess.READ, FileAccess.UPDATE, FileAccess.CREATE]
    if uses_write:
        return [FileAccess.CREATE, FileAccess.UPDATE, FileAccess.READ]
    return [FileAccess.CREATE, FileAccess.READ, FileAccess.UPDATE]


def _example_text(capabilities: Optional[Capabilities],
                  file_access: Optional[FileAccess],
                  format_name: Optional[str],
                  include_all_options: bool) -> tuple[FileAccess, str]:
    """Return one example JSON document and the access used for it.

    Args:
        capabilities: Application capability requirements.
        file_access: Optional file access supplied by the caller.
        format_name: Optional requested format name.
        include_all_options: Whether all options should be visible.
    Raises:
        TableIOFactoryNoCapabilityMatch: No default example can be selected.
    Returns:
        The file access and JSON document selected by TableIO defaults.
    """
    caps = capabilities if capabilities is not None else Capabilities()
    first_error: Optional[ConfigError] = None
    for access in _example_accesses(caps, file_access):
        try:
            config = tio_json_config_default(
                capabilities=caps, file_access=access, format_name=format_name,
                include_all_options=include_all_options)
            return access, config.as_json_string(stderr_file=sys.stderr)
        except ConfigError as error:
            if first_error is None:
                first_error = error
    msg = 'No default configuration matches the requested filters.'
    raise TableIOFactoryNoCapabilityMatch(msg) from first_error


def _add_example(lines: list[str], title: str,
                 example: tuple[FileAccess, str]) -> None:
    """Append one JSON example.

    Args:
        lines: Lines to extend.
        title: Example title.
        example: File access and JSON document to append.
    Returns:
        None.
    """
    access, text = example
    lines.append('')
    lines.append(f'{title} ({access.name})')
    lines.extend(text.splitlines())


def get_general_cfg_info() -> str:
    """Get a description of the general configuration file format.

    Returns:
        A description of the general configuration file format.
        This is a string suitable as introduction text in a plain
        text file that later will describe the
        specific configuration options for a use case in
        more detail. This description concentrates on the syntax
        of the JSON configuration file, how values are represented
        and how the configuration file is structured, including
        that many values are optional.
        The line length in the returned string is limited
        to 79 characters.
    """
    paragraphs = [
        'The configuration is stored as a JSON object. If this object is '
        'nested inside a larger config-as-json configuration file, it appears '
        'as the value of the application member that owns these settings.',
        'JSON object keys are public configuration member names. Required '
        'members must be present. Optional members may be omitted when their '
        'value is not set.',
        'Related settings may be grouped in optional nested JSON objects. '
        'Nested objects may be omitted when no value in the group is set.',
        'String values use JSON strings, integers use JSON numbers without a '
        'fractional part, and unset optional values use null when present. '
        'Compact configuration output omits null optional values.'
    ]
    return '\n\n'.join(_paragraph(text) for text in paragraphs)


# pylint: disable=too-many-arguments,too-many-positional-arguments
def describe_config(capabilities: Optional[Capabilities] = None,
                    file_access: Optional[FileAccess] = None,
                    format_name: Optional[str] = None,
                    include_compact_example: bool = True,
                    include_full_example: bool = False) -> str:
    """Get a description of the configuration file format of tableio-cfg-json.

    Args:
        capabilities: The capabilities of the application. If provided the
                      description will be limited to the configuration options
                      that are relevant for the given capabilities. If not
                      provided the description will include all configuration
                      options that are relevant for the given file access.
        file_access: The file access of the application. If provided the
                      description will be limited to the configuration options
                      that are relevant for the given file access. If not
                      provided the description will include all configuration
                      options that are relevant for the given capabilities.
                      For instance if the file access is READ, only
                      format_name values that are READ-capable will be
                      included.
        format_name: The name of the format to describe. If provided the
                      description will be limited to the configuration options
                      that are relevant for the given format name. If not
                      provided the description will include all configuration
                      options that are relevant for the given capabilities and
                      file access.
        include_compact_example: Whether to include a compact configuration
                      example (that is JSON string produced by the
                      configuration that is described), with the default
                      values omitted to keep the example compact.
        include_full_example: Whether to include a full configuration example
                      (that is JSON string produced by the configuration
                      that is described), with all values (also default values)
                      included. Both include_compact_example and
                      include_full_example can be True, in which case both
                      examples are included.

    Returns:
        A description of the configuration file format of tableio-cfg-json.
        The returned string is suitable as a section in a plain text file
        that describes the configuration file format of tableio-cfg-json.
        The line length in the returned string is limited to 79 characters.
        It is assumed that the string returned by get_general_cfg_info()
        has been added to the plain text file before the return value of
        this function.

    Raises:
        TableIOFactoryNoCapabilityMatch: The requested capabilities cannot be
        matched to any available implementation.
    """
    match_caps = _matching_caps(capabilities, file_access)
    format_names = _format_names(match_caps, format_name)
    impls_by_fmt = _impls_by_format(format_names, match_caps)
    impl_names = _unique_impls(impls_by_fmt)
    lines = ['File formats', '']
    _add_value_list(lines, 'Matching formats', tuple(format_names))
    lines.append('')
    lines.append('Possible implementations for each file format')
    lines.append('')
    for fmt_name, impls in impls_by_fmt.items():
        _add_value_list(lines, fmt_name, tuple(impls))
    lines.append('')
    lines.append('Configuration options')
    for spec in _relevant_specs(format_names, impls_by_fmt):
        lines.append('')
        _add_member(lines, spec, format_names, impl_names)
    if include_compact_example:
        example = _example_text(capabilities, file_access, format_name,
                                include_all_options=False)
        _add_example(lines, 'Compact example', example)
    if include_full_example:
        example = _example_text(capabilities, file_access, format_name,
                                include_all_options=True)
        _add_example(lines, 'Full example', example)
    return '\n'.join(lines)
