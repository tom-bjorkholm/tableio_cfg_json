"""Interactive helpers for creating TableIO JSON configuration.

The public helper in this module is intentionally scoped to one TableIO
endpoint. Application code can call it once for each input or output it wants
to configure, and then place the returned TioJsonConfig objects inside its own
larger config-as-json configuration class.
"""

import json
from copy import deepcopy
from dataclasses import dataclass, field
from io import StringIO
from typing import Literal, Optional, Sequence, TextIO

from config_as_json import ConfigBadJson, InvalidConfiguration
from tableio import Capabilities, ConfigError, ConfigSpec, FileAccess, \
    add_access_capabilities, list_implementations_tableio, \
    list_registered_tableio, tio_config_specs
from tableio_cfg_json.config import TioJsonConfig
from tableio_cfg_json.wizard_ui_bridge import PartialCheck, TableCell, \
    TableColumn, WizardBack, WizardCancelLevel, WizardUiBridge, \
    _CHOICE_ERROR, _match_token

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
    """One navigable question or grouped table in a wizard run."""

    kind: Literal['format', 'impl', 'scalar', 'section']
    spec: Optional[ConfigSpec] = None
    section: Optional[str] = None
    specs: tuple[ConfigSpec, ...] = field(default_factory=tuple)


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
    run = _WizardRun(bridge=ui_bridge, caps=capabilities,
                     file_access=file_access, match_caps=match_caps,
                     stderr=stderr_file, data={})
    return _drive(run)


def _drive(run: _WizardRun) -> TioJsonConfig:
    """Run wizard steps with back navigation until the config validates."""
    history: list[dict[str, object]] = []
    index = 0
    while True:
        steps = _build_steps(run)
        if index >= len(steps):
            return _config_from_data(run.data, run.caps, run.file_access,
                                     run.stderr)
        before = deepcopy(run.data)
        try:
            _run_step(run, steps[index])
        except WizardBack:
            if index == 0:
                raise
            index -= 1
            run.data = history.pop()
            continue
        history.append(before)
        index += 1


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
    steps.extend(_member_steps(format_name, selected))
    return steps


def _member_steps(format_name: str,
                  selected_impls: Sequence[str]) -> list[_Step]:
    """Return scalar and section steps for the relevant config members."""
    steps: list[_Step] = []
    seen_sections: set[str] = set()
    for spec in tio_config_specs().values():
        if not _ask_member(spec, format_name, selected_impls):
            continue
        if '.' not in spec.name:
            steps.append(_Step(kind='scalar', spec=spec))
            continue
        section = spec.name.split('.', maxsplit=1)[0]
        if section in seen_sections:
            continue
        seen_sections.add(section)
        specs = _section_specs(section, format_name, selected_impls)
        steps.append(_Step(kind='section', section=section, specs=specs))
    return steps


def _section_specs(section: str, format_name: str,
                   selected_impls: Sequence[str]) -> tuple[ConfigSpec, ...]:
    """Return the relevant config specs that belong to one section."""
    prefix = f'{section}.'
    return tuple(spec for spec in tio_config_specs().values()
                 if spec.name.startswith(prefix)
                 and _ask_member(spec, format_name, selected_impls))


def _run_step(run: _WizardRun, step: _Step) -> None:
    """Dispatch one step to the function that asks its question."""
    if step.kind == 'format':
        _run_format_step(run)
    elif step.kind == 'impl':
        _run_impl_step(run)
    elif step.kind == 'scalar':
        assert step.spec is not None
        _ask_config_member(step.spec, run.data, run.caps, run.file_access,
                           run.bridge, run.stderr)
    else:
        assert step.section is not None
        _run_section_step(run, step.section, step.specs)


def _run_format_step(run: _WizardRun) -> None:
    """Ask for the format and store it in the wizard data."""
    run.data['format_name'] = _ask_format(run.match_caps, run.bridge)


def _run_impl_step(run: _WizardRun) -> None:
    """Ask for the implementation and store or clear it in the data."""
    format_name = run.data['format_name']
    assert isinstance(format_name, str)
    impl_names = _impl_names(format_name, run.match_caps)
    implementation = _ask_implementation(impl_names, run.bridge)
    if implementation is None:
        run.data.pop('implementation', None)
    else:
        run.data['implementation'] = implementation


def _run_section_step(run: _WizardRun, section: str,
                      specs: tuple[ConfigSpec, ...]) -> None:
    """Ask one table of section members and store the entered values."""
    columns = (TableColumn('Parameter', read_only=True), TableColumn('Value'))
    question = _section_question(section)
    check = _section_check(run, section, specs)
    reason: Optional[str] = None
    while True:
        cells = _section_cells(run, section, specs)
        try:
            result = run.bridge.ask_table(columns, cells, question,
                                          re_ask_reason=reason,
                                          partial_check=check)
        except WizardCancelLevel:
            return
        try:
            new_data = _resolve_section(run.data, section, specs, result)
        except (ConfigBadJson, ConfigError, InvalidConfiguration,
                ValueError) as error:
            reason = f'Invalid value: {error}\nPlease try again.'
            continue
        reason = _commit(run.data, new_data, run.caps, run.file_access,
                         run.stderr)
        if reason is None:
            return


def _section_question(section: str) -> str:
    """Return the instruction shown above one section table."""
    return f'Configure {section} options (one row per setting):'


def _section_cells(run: _WizardRun, section: str,
                   specs: tuple[ConfigSpec, ...]) -> list[list[TableCell]]:
    """Return the table rows for one section, pre-filled from the data."""
    current = run.data.get(section)
    values = current if isinstance(current, dict) else {}
    rows: list[list[TableCell]] = []
    for spec in specs:
        child = spec.name.split('.', maxsplit=1)[1]
        value = values.get(child)
        value_str = None if value is None else str(value)
        rows.append([TableCell(value=child),
                     TableCell(value=value_str, choices=_spec_choices(spec),
                               nullable=True)])
    return rows


def _spec_choices(spec: ConfigSpec) -> Optional[tuple[str, ...]]:
    """Return the advertised choices of one config member as strings."""
    if spec.choices is None:
        return None
    return tuple(str(choice) for choice in spec.choices)


def _resolve_section(data: dict[str, object], section: str,
                     specs: tuple[ConfigSpec, ...],
                     result: list[list[Optional[str]]]) -> dict[str, object]:
    """Return data with one section rebuilt from a filled-in table."""
    new_data = deepcopy(data)
    new_data.pop(section, None)
    for index, spec in enumerate(specs):
        raw = result[index][1]
        if raw is None or raw == '':
            continue
        value = _resolve_member_value(spec, raw)
        _set_json_member(new_data, spec.name, value)
    return new_data


def _resolve_member_value(spec: ConfigSpec, raw: str) -> object:
    """Convert one entered table value to the type TableIO expects."""
    if spec.choices is not None:
        choices = tuple(str(choice) for choice in spec.choices)
        resolved = _match_token(raw, choices, False)
        if resolved is None:
            raise ValueError(_CHOICE_ERROR)
        return resolved
    return _parse_member_value(spec, raw)


def _section_check(run: _WizardRun, section: str,
                   specs: tuple[ConfigSpec, ...]) -> PartialCheck:
    """Return a partial-check callback for one section table."""
    def check(table: list[list[Optional[str]]],
              _position: tuple[int, int]) -> tuple[bool, str]:
        capture = StringIO()
        try:
            trial = _resolve_section(run.data, section, specs, table)
            _config_from_data(trial, run.caps, run.file_access, capture)
        except (ConfigBadJson, ConfigError, InvalidConfiguration,
                ValueError) as error:
            return (False, f'Invalid value: {error}')
        return (True, '')
    return check


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


def _ask_format(capabilities: Capabilities, ui_bridge: WizardUiBridge) -> str:
    """Ask the user to select one format that matches the endpoint."""
    format_names = list_registered_tableio(capabilities=capabilities)
    return ui_bridge.ask_choice('Select TableIO format:',
                                choices=tuple(format_names))


def _impl_names(format_name: str, capabilities: Capabilities
                ) -> tuple[str, ...]:
    """Return matching implementations for the selected format."""
    impl_names = list_implementations_tableio(format_name=format_name,
                                              capabilities=capabilities)
    return tuple(impl_names)


def _ask_implementation(impl_names: Sequence[str],
                        ui_bridge: WizardUiBridge) -> Optional[str]:
    """Ask for an implementation only when TableIO exposes a choice."""
    if len(impl_names) < 2:
        return None
    choices = (_AUTO_IMPL,) + tuple(impl_names)
    chosen = ui_bridge.ask_choice('Select implementation:', choices=choices,
                                  default=_AUTO_IMPL)
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


# pylint: disable-next=too-many-arguments,too-many-positional-arguments
def _ask_config_member(spec: ConfigSpec, data: dict[str, object],
                       caps: Capabilities, file_access: FileAccess,
                       ui_bridge: WizardUiBridge, stderr_file: TextIO) -> None:
    """Ask for one optional member and keep retrying until it validates."""
    re_ask_reason = None
    while True:
        value = _ask_member_value(spec, ui_bridge, re_ask_reason)
        if value is None:
            return
        new_data = deepcopy(data)
        _set_json_member(new_data, spec.name, value)
        re_ask_reason = _commit(data, new_data, caps, file_access, stderr_file)
        if re_ask_reason is None:
            return


def _ask_member_value(spec: ConfigSpec, ui_bridge: WizardUiBridge,
                      re_ask_reason: Optional[str]) -> Optional[object]:
    """Ask for one optional value and convert simple scalar types."""
    if spec.choices is not None:
        real = tuple(str(choice) for choice in spec.choices)
        choices = (_AUTO_MEMBER,) + real
        chosen = ui_bridge.ask_choice(f'Select value for {spec.name}:',
                                      choices=choices, default=_AUTO_MEMBER,
                                      re_ask_reason=re_ask_reason)
        return None if chosen == _AUTO_MEMBER else chosen
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
