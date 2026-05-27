"""Interactive helpers for creating TableIO JSON configuration.

The public helper in this module is intentionally scoped to one TableIO
endpoint. Application code can call it once for each input or output it wants
to configure, and then place the returned TioJsonConfig objects inside its own
larger config-as-json configuration class.
"""

import json
import sys
from copy import deepcopy
from typing import Optional, Sequence, TextIO

from config_as_json import ConfigBadJson, InvalidConfiguration
from tableio import Capabilities, ConfigError, ConfigSpec, FileAccess, \
    add_access_capabilities, list_implementations_tableio, \
    list_registered_tableio, tio_config_specs
from tableio_cfg_json.config import TioJsonConfig


def tio_json_config_wizard(capabilities: Capabilities, file_access: FileAccess,
                           stdin_file: TextIO = sys.stdin,
                           stdout_file: TextIO = sys.stdout,
                           stderr_file: TextIO = sys.stderr) -> TioJsonConfig:
    """Interactively create one TableIO JSON endpoint configuration.

    Use this function when an application wants to ask a user which TableIO
    format and options should be stored for one input or output endpoint. The
    function first offers only formats that match the supplied capabilities and
    file access. If the selected format has several matching implementations,
    it asks whether to lock one down; a blank answer keeps the recommended
    runtime behavior where TableIO chooses the implementation. It then asks
    for the optional members that can affect the selected backend and validates
    each entered value by constructing a TioJsonConfig.

    The returned object is a validated TioJsonConfig. Compact JSON written from
    that object contains only the durable choices entered by the user; omitted
    optional values stay omitted so TableIO can use backend defaults later.

    Args:
        capabilities: Capabilities needed by this application endpoint. Pass
            the capabilities for the one input or output being configured, not
            for the whole application.
        file_access: File access for this endpoint, such as READ for an input
            file or CREATE for an output file. This controls which formats and
            implementations can be offered.
        stdin_file: Stream to read user answers from. Tests can pass a
            StringIO with scripted answers.
        stdout_file: Stream receiving prompts and retry messages.
        stderr_file: Stream receiving validation diagnostics from TableIO and
            config-as-json.
    Raises:
        EOFError: Scripted input ends before all required answers are read.
        TableIOFactoryNoCapabilityMatch: No registered backend matches the
            supplied capabilities and file access.
        InvalidConfiguration: The selected values fail final validation.
    Returns:
        A validated TableIO JSON config for the one endpoint.
    """
    match_caps = add_access_capabilities(file_access, capabilities,
                                         error_file=stderr_file)
    format_name = _ask_format(match_caps, stdin_file, stdout_file)
    impl_names = _impl_names(format_name, match_caps)
    implementation = _ask_implementation(impl_names, stdin_file, stdout_file)
    data = _start_data(format_name, implementation)
    _config_from_data(data, capabilities, file_access, stderr_file)
    selected_impls = impl_names
    if implementation is not None:
        selected_impls = (implementation,)
    for spec in tio_config_specs().values():
        if _ask_member(spec, format_name, selected_impls):
            _ask_config_member(spec, data, capabilities, file_access,
                               stdin_file, stdout_file, stderr_file)
    return _config_from_data(data, capabilities, file_access, stderr_file)


def _ask_format(capabilities: Capabilities, stdin_file: TextIO,
                stdout_file: TextIO) -> str:
    """Ask the user to select one format that matches the endpoint."""
    format_names = list_registered_tableio(capabilities=capabilities)
    return _ask_menu('Select TableIO format:', format_names, False, '',
                     stdin_file, stdout_file)


def _impl_names(format_name: str, capabilities: Capabilities
                ) -> tuple[str, ...]:
    """Return matching implementations for the selected format."""
    impl_names = list_implementations_tableio(format_name=format_name,
                                              capabilities=capabilities)
    return tuple(impl_names)


def _ask_implementation(impl_names: Sequence[str], stdin_file: TextIO,
                        stdout_file: TextIO) -> Optional[str]:
    """Ask for an implementation only when TableIO exposes a choice."""
    if len(impl_names) < 2:
        return None
    blank_text = 'let TableIO choose (recommended)'
    implementation = _ask_menu('Select implementation:', impl_names, True,
                               blank_text, stdin_file, stdout_file)
    if implementation == '':
        return None
    return implementation


def _start_data(format_name: str,
                implementation: Optional[str]) -> dict[str, object]:
    """Create the first JSON object used by the wizard."""
    data: dict[str, object] = {'format_name': format_name}
    if implementation is not None:
        data['implementation'] = implementation
    return data


def _ask_member(spec: ConfigSpec, format_name: str,
                impl_names: Sequence[str]) -> bool:
    """Return True when the wizard should ask for this config member."""
    if spec.name in ('format_name', 'implementation'):
        return False
    return (_matches(spec.relevant_formats, (format_name,))
            and _matches(spec.relevant_impls, impl_names))


def _matches(spec_values: Optional[Sequence[str]],
             wanted_values: Sequence[str]) -> bool:
    """Return True when metadata values overlap or are unrestricted."""
    if spec_values is None:
        return True
    return any(value in spec_values for value in wanted_values)


# pylint: disable-next=too-many-arguments,too-many-positional-arguments
def _ask_config_member(spec: ConfigSpec, data: dict[str, object],
                       caps: Capabilities, file_access: FileAccess,
                       stdin_file: TextIO, stdout_file: TextIO,
                       stderr_file: TextIO) -> None:
    """Ask for one optional member and keep retrying until it validates."""
    while True:
        value = _ask_member_value(spec, stdin_file, stdout_file)
        if value is None:
            return
        new_data = deepcopy(data)
        _set_json_member(new_data, spec.name, value)
        try:
            _config_from_data(new_data, caps, file_access, stderr_file)
        except (ConfigBadJson, ConfigError, InvalidConfiguration,
                ValueError) as error:
            print(f'Invalid value: {error}', file=stdout_file)
            print('Please try again.', file=stdout_file)
            continue
        data.clear()
        data.update(new_data)
        return


def _ask_member_value(spec: ConfigSpec, stdin_file: TextIO,
                      stdout_file: TextIO) -> Optional[object]:
    """Ask for one optional value and convert simple scalar types."""
    if spec.choices is not None:
        choices = tuple(str(choice) for choice in spec.choices)
        choice = _ask_menu(f'Select value for {spec.name}:', choices, True,
                           'use the default', stdin_file, stdout_file)
        if choice == '':
            return None
        return choice
    _print_member_prompt(spec, stdout_file)
    answer = _read_answer(spec.name, stdin_file, stdout_file)
    if answer == '':
        return None
    try:
        return _parse_member_value(spec, answer)
    except ValueError as error:
        print(f'Invalid value: {error}', file=stdout_file)
        print('Please try again.', file=stdout_file)
        return _ask_member_value(spec, stdin_file, stdout_file)


def _parse_member_value(spec: ConfigSpec, answer: str) -> object:
    """Convert a free-text answer to the type expected by TableIO."""
    if spec.value_type == 'Optional[int]':
        return int(answer)
    return answer


def _print_member_prompt(spec: ConfigSpec, stdout_file: TextIO) -> None:
    """Print the explanatory prompt for one free-text member."""
    print('', file=stdout_file)
    print(f'{spec.name}:', file=stdout_file)
    print(spec.description, file=stdout_file)
    print(f'Type: {spec.value_type}', file=stdout_file)
    print('Press Enter to use the default.', file=stdout_file)


# pylint: disable-next=too-many-arguments,too-many-positional-arguments
def _ask_menu(title: str, choices: Sequence[str], allow_blank: bool,
              blank_text: str, stdin_file: TextIO, stdout_file: TextIO) -> str:
    """Ask for a numbered menu choice and reject unknown answers."""
    while True:
        print('', file=stdout_file)
        print(title, file=stdout_file)
        if allow_blank:
            print(f'Enter: {blank_text}', file=stdout_file)
        for index, choice in enumerate(choices, start=1):
            print(f'{index}: {choice}', file=stdout_file)
        answer = _read_answer(title, stdin_file, stdout_file)
        if answer == '' and allow_blank:
            return ''
        try:
            choice_index = int(answer)
        except ValueError:
            print('Please enter one of the menu numbers.', file=stdout_file)
            continue
        if 1 <= choice_index <= len(choices):
            return choices[choice_index - 1]
        print('Please enter one of the menu numbers.', file=stdout_file)


def _read_answer(prompt_name: str, stdin_file: TextIO,
                 stdout_file: TextIO) -> str:
    """Read one line and fail clearly if scripted input ends too early."""
    print('> ', end='', file=stdout_file)
    answer = stdin_file.readline()
    if answer == '':
        raise EOFError(f'No answer supplied for {prompt_name}.')
    return answer.rstrip('\n')


def _set_json_member(data: dict[str, object], member_name: str,
                     value: object) -> None:
    """Set a top-level or dotted member in the JSON data being built."""
    if '.' not in member_name:
        data[member_name] = value
        return
    section_name, child_name = member_name.split('.', maxsplit=1)
    section = data.get(section_name)
    if section is None:
        section = {}
        data[section_name] = section
    if not isinstance(section, dict):
        raise ValueError(f'{section_name} is not a JSON object.')
    section[child_name] = value


def _config_from_data(data: dict[str, object], capabilities: Capabilities,
                      file_access: FileAccess,
                      stderr_file: TextIO) -> TioJsonConfig:
    """Validate JSON data and return it as a TableIO JSON config."""
    return TioJsonConfig(capabilities=capabilities, file_access=file_access,
                         from_json_data_text=json.dumps(data),
                         stderr_file=stderr_file)
