"""Interactive helpers for creating TableIO JSON configuration.

The public helper in this module is intentionally scoped to one TableIO
endpoint. Application code can call it once for each input or output it wants
to configure, and then place the returned TioJsonConfig objects inside its own
larger config-as-json configuration class.
"""

import json
from dataclasses import dataclass, field
from io import StringIO
from typing import Literal, Optional, Sequence, TextIO

from config_as_json import ConfigBadJson, InvalidConfiguration
from tableio import Capabilities, ConfigError, ConfigSpec, FileAccess, \
    add_access_capabilities, list_implementations_tableio, \
    list_registered_tableio, tio_config_specs
from tableio_cfg_json.config import TioJsonConfig
from tableio_cfg_json.wizard_ui_bridge_arg_types import WizardBack, \
    WizardCancelLevel
from tableio_cfg_json.wizard_ui_bridge import WizardUiBridge
from tableio_cfg_json.wizard_ui_bridge_form_defs import AskField, \
    AnswerField, AnswerFields, AskTextField, AskIntField, AskChoiceField, \
    AnswerTextField, AnswerIntField, AnswerChoiceField, \
    PartFormValidationResult, PartialFormValidator
from tableio_cfg_json._wizard_ui_bridge_helpers import CHOICE_ERROR, \
    match_token

_AUTO_IMPL = 'let TableIO choose (recommended)'
_AUTO_MEMBER = 'use the default'


@dataclass
class _WizardRun:
    """Mutable state shared by the steps of one wizard run."""

    bridge: WizardUiBridge
    caps: Capabilities
    file_access: FileAccess
    match_caps: Capabilities
    stderr: TextIO
    data: dict[str, object]


@dataclass(frozen=True)
class _Step:
    """One navigable question or grouped option form in a wizard run."""

    kind: Literal['format', 'impl', 'options']
    specs: tuple[ConfigSpec, ...] = field(default_factory=tuple)


def tio_json_config_wizard(capabilities: Capabilities, file_access: FileAccess,
                           ui_bridge: WizardUiBridge, *,
                           default: Optional[TioJsonConfig] = None,
                           backward: bool = False) -> TioJsonConfig:
    """Interactively create one TableIO JSON endpoint configuration.

    Use this function when an application wants to ask a user which TableIO
    format and options should be stored for one input or output endpoint. The
    function first offers only formats that match the supplied capabilities and
    file access. If the selected format has several matching implementations,
    it asks which one to use, offering "let TableIO choose (recommended)" as
    the default choice that keeps the runtime behavior where TableIO selects
    the implementation. It then asks for the optional members that can affect
    the selected backend and validates each entered value by constructing a
    TioJsonConfig.

    The user can navigate the questions of this one endpoint through the bridge
    by asking to go back to the previous question or to cancel the current
    level. Navigation that reaches past the first question of this endpoint is
    raised out of this function so the application can navigate its own flow.

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
        default: Default values to pre-fill the wizard. This can be what the
            what a configuration file already contains, what the user already
            answered before going back in an enclosing wizard, or what the
            application wants to suggest as a starting point.
        backward: When True, the wizard starts at the last question instead of
            the first. This will be set to True when the user asked to go back
            from a later question in an enclosing wizard.
    Raises:
        EOFError: Scripted input ends before all required answers are read.
        TableIOFactoryNoCapabilityMatch: No registered backend matches the
            supplied capabilities and file access.
        InvalidConfiguration: The selected values fail final validation.
        WizardBack: The user asked to go back from the first question.
        WizardCancelLevel: The user cancelled this endpoint level.
        WizardAbort: The user abandoned the whole configuration.
    Returns:
        A validated TableIO JSON config for the one endpoint.
    """
    stderr_file = ui_bridge.error_file()
    match_caps = add_access_capabilities(file_access, capabilities,
                                         error_file=stderr_file)
    data = _default_data(default, stderr_file)
    run = _WizardRun(bridge=ui_bridge, caps=capabilities,
                     file_access=file_access, match_caps=match_caps,
                     stderr=stderr_file, data=data)
    return _drive(run, backward)


def _default_data(default: Optional[TioJsonConfig],
                  stderr_file: TextIO) -> dict[str, object]:
    """Return compact JSON data copied from a default config."""
    if default is None:
        return {}
    data = json.loads(default.as_json_string(stderr_file=stderr_file))
    assert isinstance(data, dict)
    return data


def _drive(run: _WizardRun, backward: bool) -> TioJsonConfig:
    """Run the endpoint steps until the configuration validates.

    Back steps to the previous question and keeps the previous answers
    available as defaults. Cancel-level returns to the first step, the
    format question that opened the later option questions, and discards
    dependent option values. Raised at the format question it propagates
    out, so the application can handle the level enclosing this endpoint.
    """
    index = _start_index(run, backward)
    while True:
        steps = _build_steps(run)
        if index >= len(steps):
            return _config_from_data(run.data, run.caps, run.file_access,
                                     run.stderr)
        try:
            _run_step(run, steps[index])
        except WizardBack:
            if index == 0:
                raise
            index -= 1
            continue
        except WizardCancelLevel:
            if index == 0:
                raise
            _clear_after_format(run.data)
            index = 0
            continue
        index += 1


def _start_index(run: _WizardRun, backward: bool) -> int:
    """Return the first step index for the requested direction."""
    if not backward:
        return 0
    return max(0, len(_build_steps(run)) - 1)


def _build_steps(run: _WizardRun) -> list[_Step]:
    """Return the ordered steps implied by the answers collected so far."""
    steps = [_Step(kind='format')]
    format_name = run.data.get('format_name')
    if not isinstance(format_name, str):
        return steps
    impl_names = _impl_names(format_name, run.match_caps)
    if len(impl_names) >= 2:
        steps.append(_Step(kind='impl'))
    implementation = run.data.get('implementation')
    selected = (implementation,) if isinstance(implementation, str) \
        else impl_names
    specs = _relevant_specs(format_name, selected)
    if specs:
        steps.append(_Step(kind='options', specs=specs))
    return steps


def _relevant_specs(format_name: str,
                    selected_impls: Sequence[str]) -> tuple[ConfigSpec, ...]:
    """Return the config specs the option form should ask for."""
    return tuple(spec for spec in tio_config_specs().values()
                 if _ask_member(spec, format_name, selected_impls))


def _run_step(run: _WizardRun, step: _Step) -> None:
    """Dispatch one step to the function that asks its question."""
    if step.kind == 'format':
        _run_format_step(run)
    elif step.kind == 'impl':
        _run_impl_step(run)
    else:
        _run_options_step(run, step.specs)


def _run_format_step(run: _WizardRun) -> None:
    """Ask for the format and store it in the wizard data."""
    old = run.data.get('format_name')
    new = _ask_format(run.match_caps, run.bridge, old)
    if old != new:
        run.data.clear()
    run.data['format_name'] = new


def _run_impl_step(run: _WizardRun) -> None:
    """Ask for the implementation and store or clear it in the data."""
    format_name = run.data['format_name']
    assert isinstance(format_name, str)
    impl_names = _impl_names(format_name, run.match_caps)
    old = run.data.get('implementation')
    implementation = _ask_implementation(impl_names, run.bridge, old)
    if old != implementation:
        _clear_after_format(run.data)
    if implementation is None:
        run.data.pop('implementation', None)
    else:
        run.data['implementation'] = implementation


def _clear_after_format(data: dict[str, object]) -> None:
    """Keep the selected format and discard dependent option values."""
    format_name = data.get('format_name')
    data.clear()
    if isinstance(format_name, str):
        data['format_name'] = format_name


def _run_options_step(run: _WizardRun, specs: tuple[ConfigSpec, ...]) -> None:
    """Ask one form of all optional members and store the answers."""
    question = _options_question(run.data)
    validator = _options_validator(run, specs)
    reason: Optional[str] = None
    values = _current_values(run.data, specs)
    while True:
        answers = run.bridge.ask_form(question, _option_fields(specs, values),
                                      re_ask_reason=reason,
                                      partial_validator=validator)
        values = _answer_values(specs, answers)
        reason = _apply_options(run, specs, values)
        if reason is None:
            return


def _options_question(data: dict[str, object]) -> str:
    """Return the instruction shown above the option form."""
    format_name = data.get('format_name')
    assert isinstance(format_name, str)
    return (f'Configure options for {format_name}.\n'
            'Leave a field blank or choose "use the default" to keep the '
            'backend default.')


def _apply_options(run: _WizardRun, specs: tuple[ConfigSpec, ...],
                   values: dict[str, object]) -> Optional[str]:
    """Build data from the answers, validate it and commit on success."""
    try:
        new_data = _data_from_values(run.data, specs, values)
    except (ConfigBadJson, ConfigError, InvalidConfiguration,
            ValueError) as error:
        return f'Invalid value: {error}\nPlease try again.'
    return _commit(run.data, new_data, run.caps, run.file_access, run.stderr)


def _options_validator(run: _WizardRun,
                       specs: tuple[ConfigSpec, ...]) -> PartialFormValidator:
    """Return a partial-form validator for the option form."""
    def validator(answers: AnswerFields,
                  _index: int) -> PartFormValidationResult:
        values = _answer_values(specs, answers)
        capture = StringIO()
        try:
            trial = _data_from_values(run.data, specs, values)
            _config_from_data(trial, run.caps, run.file_access, capture)
        except (ConfigBadJson, ConfigError, InvalidConfiguration,
                ValueError) as error:
            return PartFormValidationResult(False, f'Invalid value: {error}')
        return PartFormValidationResult(True, '')
    return validator


def _current_values(data: dict[str, object],
                    specs: tuple[ConfigSpec, ...]) -> dict[str, object]:
    """Return the members already set in the data, keyed by member name."""
    values: dict[str, object] = {}
    for spec in specs:
        value = _get_json_member(data, spec.name)
        if value is not None:
            values[spec.name] = value
    return values


def _answer_values(specs: tuple[ConfigSpec, ...],
                   answers: AnswerFields) -> dict[str, object]:
    """Return the answered members, dropping omitted ones, by member name."""
    values: dict[str, object] = {}
    for spec, answer in zip(specs, answers):
        value = _answer_value(answer)
        if value is not None:
            values[spec.name] = value
    return values


def _answer_value(answer: AnswerField) -> Optional[object]:
    """Return one member value from a form answer, or None when omitted."""
    if isinstance(answer, AnswerChoiceField):
        chosen = answer.value
        return None if chosen in (None, _AUTO_MEMBER) else chosen
    if isinstance(answer, AnswerIntField):
        return answer.value
    assert isinstance(answer, AnswerTextField)
    return None if answer.value in (None, '') else answer.value


def _option_fields(specs: tuple[ConfigSpec, ...],
                   values: dict[str, object]) -> list[AskField]:
    """Return one form field per config member, pre-filled from values."""
    return [_option_field(spec, values.get(spec.name)) for spec in specs]


def _option_field(spec: ConfigSpec, current: Optional[object]) -> AskField:
    """Return the form field that asks for one config member."""
    if spec.choices is not None:
        return _choice_field(spec, current)
    if spec.value_type == 'Optional[int]':
        return AskIntField(spec.name, spec.description, nullable=True,
                           default=_int_default(spec, current))
    return AskTextField(spec.name, spec.description, nullable=True,
                        default=_text_default(spec, current))


def _choice_field(spec: ConfigSpec, current: Optional[object]) \
        -> AskChoiceField:
    """Return a choice field with a leading use-the-default option."""
    real = _spec_choices(spec)
    assert real is not None
    choices = (_AUTO_MEMBER,) + real
    default = str(current) if current is not None and str(current) in real \
        else _AUTO_MEMBER
    return AskChoiceField(spec.name, spec.description, choices=choices,
                          default=default)


def _int_default(spec: ConfigSpec, current: Optional[object]) -> Optional[int]:
    """Return the pre-filled integer default for one member."""
    if isinstance(current, int):
        return current
    text = _member_default(spec)
    return None if text is None else int(text)


def _text_default(spec: ConfigSpec,
                  current: Optional[object]) -> Optional[str]:
    """Return the pre-filled text default for one member."""
    if current is not None:
        return str(current)
    return _member_default(spec)


def _spec_choices(spec: ConfigSpec) -> Optional[tuple[str, ...]]:
    """Return the advertised choices of one config member as strings."""
    if spec.choices is None:
        return None
    return tuple(str(choice) for choice in spec.choices)


def _data_from_values(data: dict[str, object], specs: tuple[ConfigSpec, ...],
                      values: dict[str, object]) -> dict[str, object]:
    """Return fresh data from the chosen format and the answered members."""
    new_data: dict[str, object] = {}
    format_name = data.get('format_name')
    assert isinstance(format_name, str)
    new_data['format_name'] = format_name
    implementation = data.get('implementation')
    if isinstance(implementation, str):
        new_data['implementation'] = implementation
    for spec in specs:
        if spec.name in values:
            _set_json_member(new_data, spec.name,
                             _resolve_member_value(spec, values[spec.name]))
    return new_data


def _resolve_member_value(spec: ConfigSpec, raw: object) -> object:
    """Convert one answered value to the type TableIO expects."""
    if spec.choices is not None:
        choices = tuple(str(choice) for choice in spec.choices)
        resolved = match_token(str(raw), choices, False)
        if resolved is None:
            raise ValueError(CHOICE_ERROR)
        return resolved
    if isinstance(raw, int):
        return raw
    return _parse_member_value(spec, str(raw))


def _commit(data: dict[str, object], new_data: dict[str, object],
            caps: Capabilities, file_access: FileAccess,
            stderr_file: TextIO) -> Optional[str]:
    """Validate new_data; on success copy it into data and return None.

    Returns an error reason to show the user when validation fails, so the
    caller can re-ask. On success the data is updated in place.
    """
    try:
        _config_from_data(new_data, caps, file_access, stderr_file)
    except (ConfigBadJson, ConfigError, InvalidConfiguration,
            ValueError) as error:
        return f'Invalid value: {error}\nPlease try again.'
    data.clear()
    data.update(new_data)
    return None


def _ask_format(capabilities: Capabilities, ui_bridge: WizardUiBridge,
                default: object) -> str:
    """Ask the user to select one format that matches the endpoint."""
    format_names = list_registered_tableio(capabilities=capabilities)
    default_name = default if isinstance(default, str) else None
    if default_name not in format_names:
        default_name = None
    return ui_bridge.ask_choice('Select TableIO format:',
                                choices=tuple(format_names),
                                default=default_name)


def _impl_names(format_name: str, capabilities: Capabilities
                ) -> tuple[str, ...]:
    """Return matching implementations for the selected format."""
    impl_names = list_implementations_tableio(format_name=format_name,
                                              capabilities=capabilities)
    return tuple(impl_names)


def _ask_implementation(impl_names: Sequence[str], ui_bridge: WizardUiBridge,
                        default: object) -> Optional[str]:
    """Ask for an implementation only when TableIO exposes a choice."""
    if len(impl_names) < 2:
        return None
    choices = (_AUTO_IMPL,) + tuple(impl_names)
    default_name = default if isinstance(default, str) else _AUTO_IMPL
    if default_name not in choices:
        default_name = _AUTO_IMPL
    chosen = ui_bridge.ask_choice('Select implementation:', choices=choices,
                                  default=default_name)
    return None if chosen == _AUTO_IMPL else chosen


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


def _parse_member_value(spec: ConfigSpec, answer: str) -> object:
    """Convert a free-text answer to the type expected by TableIO."""
    if spec.value_type == 'Optional[int]':
        return int(answer)
    return answer


def _member_default(spec: ConfigSpec) -> Optional[str]:
    """Return a concrete default text value for one spec, if available."""
    if spec.default_text is None:
        return None
    if spec.default_text.strip().lower().startswith('none means '):
        return None
    try:
        _parse_member_value(spec, spec.default_text)
    except ValueError:
        return None
    return spec.default_text


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


def _get_json_member(data: dict[str, object], member_name: str) -> object:
    """Return a top-level or dotted member from JSON data, or None."""
    if '.' not in member_name:
        return data.get(member_name)
    section_name, child_name = member_name.split('.', maxsplit=1)
    section = data.get(section_name)
    if not isinstance(section, dict):
        return None
    return section.get(child_name)


def _config_from_data(data: dict[str, object], capabilities: Capabilities,
                      file_access: FileAccess,
                      stderr_file: TextIO) -> TioJsonConfig:
    """Validate JSON data and return it as a TableIO JSON config."""
    return TioJsonConfig(capabilities=capabilities, file_access=file_access,
                         from_json_data_text=json.dumps(data),
                         stderr_file=stderr_file)
