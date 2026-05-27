#! /usr/local/bin/python3
"""Describe the configuration file format of tableio-cfg-json."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
from textwrap import wrap
from typing import NamedTuple, Optional, Sequence

from tableio import Capabilities, ConfigError, ConfigSpec, FileAccess, \
    add_access_capabilities, list_implementations_tableio, \
    list_registered_tableio, tio_config_specs
from tableio.factory import TableIOFactoryNoCapabilityMatch
from tableio_cfg_json.config import tio_json_config_default

_WIDTH = 79
_BASE_NAMES = ('format_name', 'implementation')


class _DescriptionContext(NamedTuple):
    """Matched TableIO metadata used by description helpers."""

    format_names: list[str]
    impls_by_fmt: dict[str, list[str]]
    impl_names: list[str]
    specs: list[ConfigSpec]


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


def _filtered_impls(impls_by_fmt: dict[str, list[str]],
                    implementation: Optional[str]) -> dict[str, list[str]]:
    """Return implementations limited to one requested implementation.

    Args:
        impls_by_fmt: Matching implementation names keyed by format.
        implementation: Optional requested implementation name.
    Raises:
        TableIOFactoryNoCapabilityMatch: No matching implementation exists.
    Returns:
        Implementation names keyed by matching format.
    """
    if implementation is None:
        return impls_by_fmt
    ret: dict[str, list[str]] = {}
    for fmt_name, impls in impls_by_fmt.items():
        for impl_name in impls:
            if impl_name.lower() == implementation.lower():
                ret[fmt_name] = [impl_name]
    if ret:
        return ret
    msg = f'Implementation "{implementation}" does not match the filters.'
    raise TableIOFactoryNoCapabilityMatch(msg)


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


def _description_context(capabilities: Optional[Capabilities],
                         file_access: Optional[FileAccess],
                         format_name: Optional[str],
                         implementation: Optional[str]) -> \
        _DescriptionContext:
    """Return matched TableIO metadata for one endpoint description.

    Args:
        capabilities: Application capability requirements.
        file_access: Optional file access that adds read/write requirements.
        format_name: Optional requested format name.
        implementation: Optional requested implementation name.
    Raises:
        TableIOFactoryNoCapabilityMatch: The requested filters match no
            registered format or implementation.
    Returns:
        Matched metadata shared by the public description helpers.
    """
    match_caps = _matching_caps(capabilities, file_access)
    format_names = _format_names(match_caps, format_name)
    impls_by_fmt = _impls_by_format(format_names, match_caps)
    impls_by_fmt = _filtered_impls(impls_by_fmt, implementation)
    format_names = [
        name for name in format_names
        if name in impls_by_fmt
    ]
    impl_names = _unique_impls(impls_by_fmt)
    specs = _relevant_specs(format_names, impls_by_fmt)
    return _DescriptionContext(format_names=format_names,
                               impls_by_fmt=impls_by_fmt,
                               impl_names=impl_names, specs=specs)


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


def _add_ref_member(lines: list[str], spec: ConfigSpec) -> None:
    """Append unfiltered documentation for one configuration member.

    Args:
        lines: Lines to extend.
        spec: TableIO configuration specification.
    Returns:
        None.
    """
    lines.append(spec.name)
    _add_wrapped(lines, spec.description, '  ', '  ')
    _add_wrapped(lines, f'Type: {spec.value_type}.', '  ', '  ')
    if spec.default_text is not None:
        _add_wrapped(lines, f'Default: {_end_sentence(spec.default_text)}',
                     '  ', '  ')
    _add_value_list(lines, 'Choices', spec.choices)
    _add_value_list(lines, 'Relevant formats', spec.relevant_formats)
    _add_value_list(lines, 'Relevant implementations', spec.relevant_impls)


def _reference_specs(member_names: Optional[Sequence[str]],
                     include_all_members: bool) -> list[ConfigSpec]:
    """Return specs selected for a one-time member reference.

    Args:
        member_names: Optional member names to describe.
        include_all_members: Whether to describe all known members.
    Raises:
        ValueError: The selection arguments are ambiguous or missing.
        KeyError: A requested member name is unknown.
    Returns:
        Selected specs in TableIO metadata order.
    """
    if member_names is None and not include_all_members:
        msg = 'member_names or include_all_members must be supplied.'
        raise ValueError(msg)
    if member_names is not None and include_all_members:
        msg = 'member_names and include_all_members cannot both be supplied.'
        raise ValueError(msg)
    specs = tio_config_specs()
    if member_names is None:
        return list(specs.values())
    missing = [name for name in member_names if name not in specs]
    if missing:
        raise KeyError(missing[0])
    selected = set(member_names)
    return [
        spec for spec in specs.values()
        if spec.name in selected
    ]


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
                  format_name: Optional[str], implementation: Optional[str],
                  include_all_options: bool) -> tuple[FileAccess, str]:
    """Return one example JSON document and the access used for it.

    Args:
        capabilities: Application capability requirements.
        file_access: Optional file access supplied by the caller.
        format_name: Optional requested format name.
        implementation: Optional requested implementation name.
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
                implementation=implementation,
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


def get_config_member_names(capabilities: Optional[Capabilities] = None,
                            file_access: Optional[FileAccess] = None,
                            format_name: Optional[str] = None,
                            implementation: Optional[str] = None) -> \
        tuple[str, ...]:
    """Get relevant configuration member names for one TableIO endpoint.

    Use this helper when an application wants to compose its own
    documentation text instead of using the complete text returned by
    describe_config(). It is especially useful for larger application
    configuration files with several TableIO endpoints: call it once for each
    endpoint, combine the names, and pass the result to
    describe_config_reference() so the long parameter descriptions appear
    only once.

    Args:
        capabilities: Capabilities needed by the application endpoint.
            Passing this filters the result to formats and options that can
            satisfy those capabilities.
        file_access: File access for the endpoint, for example READ for an
            input endpoint or CREATE for an output endpoint. Passing this
            filters the result to backends that support that access.
        format_name: Optional TableIO format name. Passing this narrows the
            result to members relevant for that format.
        implementation: Optional TableIO implementation name. Passing this
            narrows the result to members relevant for that implementation.
    Raises:
        TableIOFactoryNoCapabilityMatch: The requested filters match no
            registered format or implementation.
    Returns:
        Relevant member names in TableIO metadata order.
    """
    context = _description_context(capabilities, file_access, format_name,
                                   implementation)
    return tuple(spec.name for spec in context.specs)


def describe_config_members(capabilities: Optional[Capabilities] = None,
                            file_access: Optional[FileAccess] = None,
                            format_name: Optional[str] = None,
                            implementation: Optional[str] = None) -> str:
    """Get a compact member summary for one TableIO endpoint.

    Use this helper when the surrounding application already explains what
    the endpoint means, and only needs a short list of the TableIO choices
    and member names that are editable for that endpoint. It deliberately
    avoids the longer per-member descriptions so that an application can show
    this section once for each input or output, and then use
    describe_config_reference() once for the shared detailed reference.

    Args:
        capabilities: Capabilities needed by the application endpoint.
            Passing this filters format choices, implementation choices and
            members to what the endpoint can actually use.
        file_access: File access for the endpoint. For example, READ limits
            the listed formats to read-capable formats.
        format_name: Optional TableIO format name. Passing this is useful
            when documenting one already-selected format.
        implementation: Optional TableIO implementation name. Passing this
            is useful when documenting one already-selected backend.
    Raises:
        TableIOFactoryNoCapabilityMatch: The requested filters match no
            registered format or implementation.
    Returns:
        A compact text listing format choices, implementation choices and
        relevant configuration members. The returned line length is limited
        to 79 characters.
    """
    context = _description_context(capabilities, file_access, format_name,
                                   implementation)
    lines: list[str] = []
    _add_value_list(lines, 'format_name choices', tuple(context.format_names))
    lines.append('')
    lines.append('implementation choices')
    for fmt_name, impls in context.impls_by_fmt.items():
        _add_value_list(lines, fmt_name, tuple(impls))
    lines.append('')
    lines.append('Relevant members')
    for spec in context.specs:
        lines.append(f'  {spec.name}')
    return '\n'.join(lines)


def describe_config_reference(member_names: Optional[Sequence[str]] = None,
                              include_all_members: bool = False) -> str:
    """Get unfiltered reference text for selected configuration members.

    Use this helper for the detailed reference section in user-facing syntax
    text. In a simple single-endpoint program, describe_config() may be
    enough. In a larger application config, prefer describing each endpoint
    with describe_config_members(), collect the relevant names with
    get_config_member_names(), and call this function once so each parameter
    description is not repeated for every endpoint.

    Args:
        member_names: Optional names of members to describe. When supplied,
            unknown names raise ``KeyError`` and output order follows TableIO
            metadata order.
        include_all_members: Whether to describe all known TableIO
            configuration members.
    Raises:
        ValueError: Neither selection argument was supplied, or both were.
        KeyError: A requested member name is unknown.
    Returns:
        A long-form member reference. The returned line length is limited
        to 79 characters.
    """
    lines: list[str] = []
    for spec in _reference_specs(member_names, include_all_members):
        if lines:
            lines.append('')
        _add_ref_member(lines, spec)
    return '\n'.join(lines)


def describe_config_example(capabilities: Optional[Capabilities] = None,
                            file_access: Optional[FileAccess] = None,
                            format_name: Optional[str] = None,
                            implementation: Optional[str] = None,
                            complete: bool = False) -> str:
    """Get one formatted JSON example for one TableIO endpoint.

    Use this helper when the application wants to decide where example JSON
    belongs in its own text. The return value is only the indented JSON
    document, with no heading or explanation. Use the compact default for a
    realistic hand-editable example, and ``complete=True`` when the goal is a
    template that shows optional defaults.

    Args:
        capabilities: Capabilities needed by the application endpoint.
            These capabilities influence which default TableIO backend can be
            selected for the example.
        file_access: File access for the endpoint. If omitted, the helper
            tries a sensible access mode based on the capabilities.
        format_name: Optional TableIO format name to use in the example.
        implementation: Optional TableIO implementation name to use in the
            example.
        complete: Whether all options should be visible in the example.
    Raises:
        TableIOFactoryNoCapabilityMatch: No default example can be selected.
    Returns:
        A formatted JSON document string without any heading text.
    """
    _access, text = _example_text(capabilities, file_access, format_name,
                                  implementation, complete)
    return text


# pylint: disable=too-many-arguments,too-many-positional-arguments
def describe_config(capabilities: Optional[Capabilities] = None,
                    file_access: Optional[FileAccess] = None,
                    format_name: Optional[str] = None,
                    include_compact_example: bool = True,
                    include_full_example: bool = False,
                    implementation: Optional[str] = None) -> str:
    """Get a description of the configuration file format of tableio-cfg-json.

    Use this function for a simple program where one configuration file
    mainly describes one TableIO endpoint. It returns a complete section with
    matching formats, implementations, relevant members, detailed member
    descriptions and optional JSON examples. For a larger application config
    with several TableIO inputs or outputs, prefer composing the text from
    get_general_cfg_info(), describe_config_members(),
    get_config_member_names(), describe_config_reference() and
    describe_config_example() so the application can explain each endpoint in
    its own words and avoid repeating the long member reference.

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
        implementation: The implementation name to describe. If provided the
                      description will be limited to the configuration options
                      that are relevant for that implementation.

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
    context = _description_context(capabilities, file_access, format_name,
                                   implementation)
    lines = ['File formats', '']
    _add_value_list(lines, 'Matching formats', tuple(context.format_names))
    lines.append('')
    lines.append('Possible implementations for each file format')
    lines.append('')
    for fmt_name, impls in context.impls_by_fmt.items():
        _add_value_list(lines, fmt_name, tuple(impls))
    lines.append('')
    lines.append('Configuration options')
    for spec in context.specs:
        lines.append('')
        _add_member(lines, spec, context.format_names, context.impl_names)
    if include_compact_example:
        example = _example_text(capabilities, file_access, format_name,
                                implementation, include_all_options=False)
        _add_example(lines, 'Compact example', example)
    if include_full_example:
        example = _example_text(capabilities, file_access, format_name,
                                implementation, include_all_options=True)
        _add_example(lines, 'Full example', example)
    return '\n'.join(lines)
