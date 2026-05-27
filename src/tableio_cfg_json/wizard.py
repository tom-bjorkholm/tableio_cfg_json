"""Interactive helpers for creating TableIO JSON configuration.

The public helper in this module is intentionally scoped to one TableIO
endpoint. Application code can call it once for each input or output it wants
to configure, and then place the returned TioJsonConfig objects inside its own
larger config-as-json configuration class.
"""

import json
import sys
from copy import deepcopy
from enum import Enum
from typing import Optional, Sequence, TextIO

import tableio
from config_as_json import ConfigBadJson, InvalidConfiguration, \
    string_best_match, string_to_enum_best_match
from tableio import Capabilities, ConfigError, ConfigSpec, FileAccess, \
    add_access_capabilities, list_implementations_tableio, \
    list_registered_tableio, tio_config_specs
from tableio_cfg_json.config import TioJsonConfig


class WizardUiBridge:
    """Bridge between the wizard and the user interface.

    This is an abstract base class for a bridge between the wizard and
    the user interface. Provide concrete classes of this bridge to
    allow the wizard to use console text user interface or a graphical
    user interface.
    """

    def ask(self, question: str, re_ask_reason: Optional[str] = None,
            choices: Optional[Sequence[str]] = None) -> str | int:
        """Ask a question and return the user's answer.

        Args:
            question: The question to ask the user.
            re_ask_reason: The reason for re-asking the question for
                           instance that the user's answer was invalid.
            choices: The choices to offer the user as a sequence of strings.

        Returns:
            The user's answer. If the user's answer is one of the choices,
            then the return value can be either the matching string or the
            index of what the user selected. If integer index is used it is
            0-based.
            The bridge is not required to validate the user's answer in
            any way. It is the responsibility of the caller to validate the
            user's answer.
            If the user entered/selected an empty string as answer, then the
            return value should be an empty string. The caller may interpret
            this as a request to use the default value.
        """
        raise NotImplementedError('ask() not implemented')

    def error_file(self) -> TextIO:
        """Return the stream used for validation diagnostics."""
        return sys.stderr

    def show(self, message: str) -> None:
        """Show a message to the user.

        If implementing a graphical user interface, this method should
        display the message in a dialog or a message box. If implementing
        a console text user interface, this method should print the message
        to the console.
        Args:
            message: The message to show the user.
        """
        raise NotImplementedError('show() not implemented')


class WizardUiBridgeConsole(WizardUiBridge):
    """Bridge between the wizard and the console text user interface."""

    def __init__(self, stdout_file: TextIO, stdin_file: TextIO,
                 stderr_file: TextIO) -> None:
        """Initialize the bridge.

        Args:
            stdout_file: Stream to print messages to.
            stdin_file: Stream to read user answers from.
            stderr_file: Stream to print errors to.
        """
        self.stdout_file = stdout_file
        self.stdin_file = stdin_file
        self.stderr_file = stderr_file

    def ask(self, question: str, re_ask_reason: Optional[str] = None,
            choices: Optional[Sequence[str]] = None) -> str | int:
        """Ask a question and return the user's answer.

        Args:
            question: The question to ask the user.
            re_ask_reason: The reason for re-asking the question for
                           instance that the user's answer was invalid.
            choices: The choices to offer the user as a sequence of strings.

        Returns:
            The user's answer. If the user's answer is one of the choices,
            then the return value can be either the matching string or the
            index of what the user selected. If integer index is used it is
            0-based.
            The bridge is not required to validate the user's answer in
            any way. It is the responsibility of the caller to validate the
            user's answer.
            If the user entered/selected an empty string as answer, then the
            return value should be an empty string. The caller may interpret
            this as a request to use the default value.
        """
        if re_ask_reason is not None:
            print(re_ask_reason, file=self.stderr_file)
        print('', file=self.stdout_file)
        print(question, file=self.stdout_file)
        if choices is not None:
            for index, choice in enumerate(choices, start=1):
                print(f'{index}: {choice}', file=self.stdout_file)
        print('> ', end='', file=self.stdout_file)
        answer = self.stdin_file.readline()
        if answer == '':
            raise EOFError(f'No answer supplied for {question}.')
        text_answer = answer.rstrip('\n')
        if choices is not None:
            choice_index = _int_text(text_answer)
            if choice_index is not None:
                return choice_index - 1
        return text_answer

    def error_file(self) -> TextIO:
        """Return the stream used for validation diagnostics."""
        return self.stderr_file

    def show(self, message: str) -> None:
        """Show a message to the user.

        This method prints the message to the console.
        Args:
            message: The message to show the user.
        """
        print(message, file=self.stdout_file)


def tio_json_config_wizard(capabilities: Capabilities, file_access: FileAccess,
                           ui_bridge: WizardUiBridge) -> TioJsonConfig:
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
        ui_bridge: Bridge between the wizard and the user interface.
    Raises:
        EOFError: Scripted input ends before all required answers are read.
        TableIOFactoryNoCapabilityMatch: No registered backend matches the
            supplied capabilities and file access.
        InvalidConfiguration: The selected values fail final validation.
    Returns:
        A validated TableIO JSON config for the one endpoint.
    """
    stderr_file = ui_bridge.error_file()
    match_caps = add_access_capabilities(file_access, capabilities,
                                         error_file=stderr_file)
    format_name = _ask_format(match_caps, ui_bridge, stderr_file)
    impl_names = _impl_names(format_name, match_caps)
    implementation = _ask_implementation(impl_names, ui_bridge, stderr_file)
    data = _start_data(format_name, implementation)
    _config_from_data(data, capabilities, file_access, stderr_file)
    selected_impls = impl_names
    if implementation is not None:
        selected_impls = (implementation,)
    for spec in tio_config_specs().values():
        if _ask_member(spec, format_name, selected_impls):
            _ask_config_member(spec, data, capabilities, file_access,
                               ui_bridge, stderr_file)
    return _config_from_data(data, capabilities, file_access, stderr_file)


def _ask_format(capabilities: Capabilities, ui_bridge: WizardUiBridge,
                stderr_file: TextIO) -> str:
    """Ask the user to select one format that matches the endpoint."""
    format_names = list_registered_tableio(capabilities=capabilities)
    return _ask_choice('Select TableIO format:', 'format_name', format_names,
                       False, '', ui_bridge, stderr_file)


def _impl_names(format_name: str, capabilities: Capabilities
                ) -> tuple[str, ...]:
    """Return matching implementations for the selected format."""
    impl_names = list_implementations_tableio(format_name=format_name,
                                              capabilities=capabilities)
    return tuple(impl_names)


def _ask_implementation(impl_names: Sequence[str], ui_bridge: WizardUiBridge,
                        stderr_file: TextIO) -> Optional[str]:
    """Ask for an implementation only when TableIO exposes a choice."""
    if len(impl_names) < 2:
        return None
    blank_text = 'let TableIO choose (recommended)'
    implementation = _ask_choice('Select implementation:', 'implementation',
                                 impl_names, True, blank_text, ui_bridge,
                                 stderr_file)
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
                       ui_bridge: WizardUiBridge, stderr_file: TextIO) -> None:
    """Ask for one optional member and keep retrying until it validates."""
    re_ask_reason = None
    while True:
        value = _ask_member_value(spec, ui_bridge, stderr_file, re_ask_reason)
        if value is None:
            return
        new_data = deepcopy(data)
        _set_json_member(new_data, spec.name, value)
        try:
            _config_from_data(new_data, caps, file_access, stderr_file)
        except (ConfigBadJson, ConfigError, InvalidConfiguration,
                ValueError) as error:
            re_ask_reason = f'Invalid value: {error}\nPlease try again.'
            continue
        data.clear()
        data.update(new_data)
        return


def _ask_member_value(spec: ConfigSpec, ui_bridge: WizardUiBridge,
                      stderr_file: TextIO,
                      re_ask_reason: Optional[str]) -> Optional[object]:
    """Ask for one optional value and convert simple scalar types."""
    if spec.choices is not None:
        choices = tuple(str(choice) for choice in spec.choices)
        enum_type = _enum_type(spec)
        choice = _ask_choice(f'Select value for {spec.name}:', spec.name,
                             choices, True, 'use the default', ui_bridge,
                             stderr_file, enum_type, re_ask_reason)
        if choice == '':
            return None
        return choice
    return _ask_text_member_value(spec, ui_bridge, re_ask_reason)


def _ask_text_member_value(spec: ConfigSpec, ui_bridge: WizardUiBridge,
                           re_ask_reason: Optional[str]) -> Optional[object]:
    """Ask for one free-text optional value."""
    question = _member_question(spec)
    while True:
        answer = ui_bridge.ask(question, re_ask_reason)
        if not isinstance(answer, str):
            re_ask_reason = 'Please enter a text value.'
            continue
        if answer == '':
            return None
        try:
            return _parse_member_value(spec, answer)
        except ValueError as error:
            re_ask_reason = f'Invalid value: {error}\nPlease try again.'


def _parse_member_value(spec: ConfigSpec, answer: str) -> object:
    """Convert a free-text answer to the type expected by TableIO."""
    if spec.value_type == 'Optional[int]':
        return int(answer)
    return answer


def _member_question(spec: ConfigSpec) -> str:
    """Return the explanatory question for one free-text member."""
    return (
        f'{spec.name}:\n'
        f'{spec.description}\n'
        f'Type: {spec.value_type}\n'
        'Press Enter to use the default.')


# pylint: disable-next=too-many-arguments,too-many-positional-arguments
def _ask_choice(title: str, member_name: str, choices: Sequence[str],
                allow_blank: bool, blank_text: str, ui_bridge: WizardUiBridge,
                stderr_file: TextIO, enum_type: Optional[type[Enum]] = None,
                first_re_ask: Optional[str] = None) -> str:
    """Ask for one answer from a list of choices."""
    question = _choice_question(title, allow_blank, blank_text)
    re_ask_reason = first_re_ask
    while True:
        answer = ui_bridge.ask(question, re_ask_reason, choices)
        try:
            return _choice_from_answer(answer, choices, allow_blank,
                                       member_name, stderr_file, enum_type)
        except (InvalidConfiguration, ValueError) as error:
            re_ask_reason = str(error)


def _choice_question(title: str, allow_blank: bool, blank_text: str) -> str:
    """Return the question text for one list choice."""
    if allow_blank:
        return f'{title}\nEnter: {blank_text}'
    return title


# pylint: disable-next=too-many-arguments,too-many-positional-arguments
def _choice_from_answer(answer: str | int, choices: Sequence[str],
                        allow_blank: bool, member_name: str,
                        stderr_file: TextIO,
                        enum_type: Optional[type[Enum]]) -> str:
    """Return a validated choice selected by an answer."""
    if answer == '' and allow_blank:
        return ''
    if isinstance(answer, int) and not isinstance(answer, bool):
        return _choice_from_index(answer, choices)
    if not isinstance(answer, str):
        raise ValueError('Please enter one of the listed choices.')
    index = _int_text(answer)
    if index is not None:
        return _choice_from_index(index, choices)
    if enum_type is not None:
        return _choice_from_enum(answer, choices, enum_type)
    return string_best_match(answer, choices, member_name, stderr_file)


def _choice_from_index(index: int, choices: Sequence[str]) -> str:
    """Return the choice at a 0-based index."""
    if 0 <= index < len(choices):
        return choices[index]
    raise ValueError('Please enter one of the listed choices.')


def _choice_from_enum(answer: str, choices: Sequence[str],
                      enum_type: type[Enum]) -> str:
    """Return the enum choice whose name best matches the answer."""
    try:
        enum_value = string_to_enum_best_match(answer, enum_type)
    except (AssertionError, KeyError) as error:
        raise ValueError('Please enter one of the listed choices.') from error
    if enum_value.name in choices:
        return enum_value.name
    raise ValueError('Please enter one of the listed choices.')


def _enum_type(spec: ConfigSpec) -> Optional[type[Enum]]:
    """Return the enum type used by a config member choice list."""
    type_name = _optional_type_name(spec.value_type)
    if type_name is None:
        return None
    enum_type: object = getattr(tableio, type_name, None)
    if isinstance(enum_type, type) and issubclass(enum_type, Enum):
        return enum_type
    return None


def _optional_type_name(value_type: str) -> Optional[str]:
    """Return the inner type name from an Optional type description."""
    prefix = 'Optional['
    suffix = ']'
    if value_type.startswith(prefix) and value_type.endswith(suffix):
        return value_type[len(prefix):-len(suffix)]
    return None


def _int_text(text: str) -> Optional[int]:
    """Return an integer from text, or None when text is not an integer."""
    try:
        return int(text)
    except ValueError:
        return None


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
