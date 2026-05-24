#! /usr/local/bin/python3
"""Config-as-json bridge for framework-neutral tableio configuration."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
from typing import Callable, NoReturn, Optional, TextIO, override

from config_as_json import CharEncodingValidator, Config, \
    ConfigAutoChangeHook, ConfigNesting, ConfigNestingKind, \
    InvalidConfiguration, MemberValidationStep, MemberValidatorSequence, \
    IntFloatValidator, \
    NestedConfigs, OptionalMemberValidator, ParseConverter, PathOrStr, \
    StrLenValidator, StrValidator, ValidationPlan, \
    ValueTypeValidator, WholeConfigValidationStep, WholeConfigValidator
from tableio import Capabilities, ConfigData, ConfigError, CsvConfigData, \
    CsvDialect, FileAccess, HtmlConfigData, LatexConfigData, \
    add_access_capabilities, tio_config_default, tio_config_specs, \
    tio_config_validate


def _choices(name: str) -> tuple[str, ...]:
    """Return advertised choices for one tableio configuration member."""
    choices = tio_config_specs()[name].choices
    assert choices is not None
    return choices


def _format_choices() -> tuple[str, ...]:
    """Return currently registered tableio format names."""
    return _choices('format_name')


def _impl_choices() -> tuple[str, ...]:
    """Return currently registered tableio implementation names."""
    return _choices('implementation')


def _paper_choices() -> tuple[str, ...]:
    """Return advertised paper size values."""
    return _choices('paper_size')


def _align_choices() -> tuple[str, ...]:
    """Return advertised text table alignment values."""
    return _choices('table_alignment')


def _quoting_choices() -> tuple[str, ...]:
    """Return advertised CSV quoting values."""
    return _choices('csv.quoting')


def _latex_doc_choices() -> tuple[str, ...]:
    """Return advertised LaTeX document class values."""
    return _choices('latex.document_class')


def _raise_invalid(message: str, stderr_file: TextIO) -> NoReturn:
    """Write one validation message and raise InvalidConfiguration."""
    print(message, file=stderr_file)
    raise InvalidConfiguration(message)


def _optional_string() -> OptionalMemberValidator:
    """Return a validator for an optional string member."""
    return OptionalMemberValidator(ValueTypeValidator(str))


def _optional_choice(
        choices: Callable[[], tuple[str, ...]]) -> OptionalMemberValidator:
    """Return a validator for an optional string with known choices."""
    return OptionalMemberValidator(
        StrValidator(choices, ignore_case=True, normalize=True))


def _optional_int_at_least(min_value: int) -> OptionalMemberValidator:
    """Return a validator for an optional integer lower bound."""
    validator1 = IntFloatValidator(min_value=min_value, max_value=None,
                                   allowed_values=None)
    validator2 = ValueTypeValidator(value_type=int, strict=True)
    validators = MemberValidatorSequence(validators=[validator1, validator2])
    return OptionalMemberValidator(validators)


def _none_members(config: object, names: list[str]) -> list[str]:
    """Return member names whose current value is None."""
    return [name for name in names if getattr(config, name) is None]


# pylint: disable=too-few-public-methods
class TioWholeValidator(WholeConfigValidator):
    """Validate the complete bridge object with tableio rules."""

    def validate(self, config: Config,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Validate one complete tableio JSON configuration."""
        assert isinstance(config, TioJsonConfig)
        try:
            tio_config_validate(config, capabilities=config.capabilities,
                                file_access=config.file_access)
        except ConfigError as err:
            message = _issue_message(err)
            _raise_invalid(message, stderr_file)


def _issue_message(error: ConfigError) -> str:
    """Return one compact config-as-json message from tableio issues."""
    return '\n'.join(
        f'{issue.name}: {issue.message}' for issue in error.issues)


def _one_char_validator() -> OptionalMemberValidator:
    """Return a validator for optional one-character strings."""
    return OptionalMemberValidator(StrLenValidator(min_length=1, max_length=1))


def _non_empty_validator() -> OptionalMemberValidator:
    """Return a validator for optional non-empty strings."""
    validator = StrLenValidator(min_length=1, max_length=None)
    return OptionalMemberValidator(validator)


class TioJsonCsvConfig(CsvConfigData, Config):
    """CSV tableio configuration section backed by config-as-json."""

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, dialect: Optional[CsvDialect] = None,
                 delimiter: Optional[str] = None,
                 quoting: Optional[str] = None,
                 quotechar: Optional[str] = None,
                 lineterminator: Optional[str] = None,
                 escapechar: Optional[str] = None,
                 from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Initialize the CSV configuration section."""
        CsvConfigData.__init__(self, dialect=dialect, delimiter=delimiter,
                               quoting=quoting, quotechar=quotechar,
                               lineterminator=lineterminator,
                               escapechar=escapechar)
        Config.__init__(self, from_json_data_text=from_json_data_text,
                        from_json_filename=from_json_filename,
                        stderr_file=stderr_file)

    @override
    def _omit_none_from_json(self) -> list[str]:
        """Return optional CSV members omitted while set to None."""
        return _none_members(
            self, ['dialect', 'delimiter', 'quoting', 'quotechar',
                   'lineterminator', 'escapechar'])

    @override
    def parse_converters(self) -> dict[str, ParseConverter]:
        """Return JSON read conversions for CSV values."""
        return {'dialect': self.get_converter_dict(CsvDialect)}

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return config-as-json validation steps for CSV values."""
        _ = stderr_file
        quoting_validator = _optional_choice(_quoting_choices)
        return [
            MemberValidationStep(member_names=['delimiter'],
                                 validator=_one_char_validator()),
            MemberValidationStep(member_names=['quoting'],
                                 validator=quoting_validator),
            MemberValidationStep(member_names=['quotechar'],
                                 validator=_one_char_validator()),
            MemberValidationStep(member_names=['lineterminator'],
                                 validator=_non_empty_validator()),
            MemberValidationStep(member_names=['escapechar'],
                                 validator=_one_char_validator())
        ]


class TioJsonHtmlConfig(HtmlConfigData, Config):
    """HTML tableio configuration section backed by config-as-json."""

    def __init__(self, css_file: Optional[str] = None,
                 from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Initialize the HTML configuration section."""
        HtmlConfigData.__init__(self, css_file=css_file)
        Config.__init__(self, from_json_data_text=from_json_data_text,
                        from_json_filename=from_json_filename,
                        stderr_file=stderr_file)

    @override
    def _omit_none_from_json(self) -> list[str]:
        """Return optional HTML members omitted while set to None."""
        return _none_members(self, ['css_file'])

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return config-as-json validation steps for HTML values."""
        _ = stderr_file
        return [
            MemberValidationStep(member_names=['css_file'],
                                 validator=_optional_string())
        ]


class TioJsonLatexConfig(LatexConfigData, Config):
    """LaTeX tableio configuration section backed by config-as-json."""

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, document_class: Optional[str] = None,
                 preamble: Optional[str] = None,
                 from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Initialize the LaTeX configuration section."""
        LatexConfigData.__init__(self, document_class=document_class,
                                 preamble=preamble)
        Config.__init__(self, from_json_data_text=from_json_data_text,
                        from_json_filename=from_json_filename,
                        stderr_file=stderr_file)

    @override
    def _omit_none_from_json(self) -> list[str]:
        """Return optional LaTeX members omitted while set to None."""
        return _none_members(self, ['document_class', 'preamble'])

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return config-as-json validation steps for LaTeX values."""
        _ = stderr_file
        return [
            MemberValidationStep(member_names=['document_class'],
                                 validator=_optional_choice(
                                     _latex_doc_choices)),
            MemberValidationStep(member_names=['preamble'],
                                 validator=_optional_string())
        ]


class TioJsonConfig(ConfigData, Config):  # pylint: disable=too-many-ancestors
    """Complete tableio configuration backed by config-as-json."""

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    # pylint: disable=super-init-not-called
    def __init__(self, capabilities: Capabilities, file_access: FileAccess,
                 format_name: Optional[str] = None,
                 implementation: Optional[str] = None,
                 include_all_options: bool = False,
                 from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 auto_ch_hook: Optional[ConfigAutoChangeHook] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Initialize a tableio JSON configuration."""
        data = tio_config_default(capabilities, file_access,
                                  format_name=format_name,
                                  implementation=implementation,
                                  include_all_options=include_all_options)
        self._capabilities = add_access_capabilities(file_access, capabilities)
        self._file_access = file_access
        Config.copy_initial_data(data, self)
        Config.__init__(self, from_json_data_text=from_json_data_text,
                        from_json_filename=from_json_filename,
                        auto_ch_hook=auto_ch_hook, stderr_file=stderr_file)

    @property
    def capabilities(self) -> Capabilities:
        """Return runtime capabilities used for validation."""
        return self._capabilities

    @property
    def file_access(self) -> FileAccess:
        """Return runtime file access used for validation."""
        return self._file_access

    @override
    def _omit_none_from_json(self) -> list[str]:
        """Return optional top-level members omitted while set to None."""
        return _none_members(
            self, ['implementation', 'character_encoding', 'language',
                   'title', 'paper_size', 'line_length',
                   'table_max_line_length', 'table_alignment', 'csv', 'html',
                   'latex'])

    @override
    def nested_configs(self) -> NestedConfigs:
        """Return nested tableio configuration section declarations."""
        return {
            'csv': ConfigNesting(kind=ConfigNestingKind.OPTIONAL_MEMBER,
                                 config_type=TioJsonCsvConfig),
            'html': ConfigNesting(kind=ConfigNestingKind.OPTIONAL_MEMBER,
                                  config_type=TioJsonHtmlConfig),
            'latex': ConfigNesting(kind=ConfigNestingKind.OPTIONAL_MEMBER,
                                   config_type=TioJsonLatexConfig)
        }

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return config-as-json validation steps for top-level values."""
        _ = stderr_file
        paper_validator = _optional_choice(_paper_choices)
        align_validator = _optional_choice(_align_choices)
        return [
            MemberValidationStep(member_names=['format_name'],
                                 validator=StrValidator(_format_choices,
                                                        ignore_case=True,
                                                        normalize=True)),
            MemberValidationStep(member_names=['implementation'],
                                 validator=_optional_choice(_impl_choices)),
            MemberValidationStep(member_names=['character_encoding'],
                                 validator=OptionalMemberValidator(
                                     CharEncodingValidator())),
            MemberValidationStep(member_names=['language', 'title'],
                                 validator=_optional_string()),
            MemberValidationStep(member_names=['paper_size'],
                                 validator=paper_validator),
            MemberValidationStep(member_names=['line_length'],
                                 validator=_optional_int_at_least(11)),
            MemberValidationStep(member_names=['table_max_line_length'],
                                 validator=_optional_int_at_least(10)),
            MemberValidationStep(member_names=['table_alignment'],
                                 validator=align_validator),
            WholeConfigValidationStep(validator=TioWholeValidator())
        ]


# pylint: disable=too-many-arguments,too-many-positional-arguments
def tio_json_config_default(capabilities: Capabilities,
                            file_access: FileAccess,
                            format_name: Optional[str] = None,
                            implementation: Optional[str] = None,
                            include_all_options: bool = False,
                            stderr_file: TextIO = sys.stderr) -> TioJsonConfig:
    """Return a default tableio configuration backed by config-as-json."""
    return TioJsonConfig(
        capabilities=capabilities, file_access=file_access,
        format_name=format_name, implementation=implementation,
        include_all_options=include_all_options, stderr_file=stderr_file)
