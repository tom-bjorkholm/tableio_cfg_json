#! /usr/local/bin/python3
"""JSON-backed configuration classes for TableIO settings.

The module adapts tableio's framework-neutral configuration data classes to
config-as-json. The public classes keep tableio's durable values while adding
JSON reading, writing, nested-section handling and validation.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
from typing import Optional, TextIO, override

from config_as_json import CharEncodingValidator, Config, \
    ConfigAutoChangeHook, ConfigNesting, ConfigNestingKind, \
    InvalidConfiguration, IntFloatValidator, MemberValidationStep, \
    MemberValidatorSequence, \
    NestedConfigs, OptionalMemberValidator, ParseConverter, PathOrStr, \
    StrLenValidator, StrValidator, ValidationPlan, \
    ValueTypeValidator, WholeConfigValidationStep, WholeConfigValidator
from tableio import Capabilities, ConfigData, ConfigError, CsvConfigData, \
    CsvDialect, FileAccess, HtmlConfigData, LatexConfigData, \
    add_access_capabilities, tio_config_default, tio_config_specs, \
    tio_config_validate


def _choices(name: str) -> tuple[str, ...]:
    """Return tableio choices for one configuration member.

    TableIO owns the accepted values. Looking them up here keeps this bridge
    aligned with currently registered formats, implementations and options.

    Args:
        name: Dotted tableio configuration member name.
    Raises:
        KeyError: The member name is not known by tableio.
        AssertionError: The tableio member has no finite choices.
    Returns:
        Accepted string values for the requested member.
    """
    choices = tio_config_specs()[name].choices
    assert choices is not None
    return choices


def _choice_validator(name: str) -> StrValidator:
    """Return a validator for one required tableio choice member.

    Args:
        name: Dotted tableio configuration member name.
    Raises:
        KeyError: The member name is not known by tableio.
        AssertionError: The tableio member has no finite choices.
    Returns:
        A string validator that accepts and normalizes tableio choices.
    """
    return StrValidator(_choices(name), ignore_case=True, normalize=True)


def _optional_choice(name: str) -> OptionalMemberValidator:
    """Return a validator for one optional tableio choice member.

    Args:
        name: Dotted tableio configuration member name.
    Raises:
        KeyError: The member name is not known by tableio.
        AssertionError: The tableio member has no finite choices.
    Returns:
        A validator that accepts ``None`` or a normalized tableio choice.
    """
    return OptionalMemberValidator(_choice_validator(name))


def _optional_string() -> OptionalMemberValidator:
    """Return a validator for an optional plain string member.

    Returns:
        A validator that accepts ``None`` or a string.
    """
    return OptionalMemberValidator(ValueTypeValidator(str))


def _optional_int_at_least(min_value: int) -> OptionalMemberValidator:
    """Return a validator for an optional strict integer lower bound.

    The numeric validator checks the range, and the strict type validator
    rejects bools and floats that Python would otherwise treat as numbers.

    Args:
        min_value: Inclusive lower bound accepted for non-``None`` values.
    Returns:
        A validator that accepts ``None`` or a strict integer at least
        ``min_value``.
    """
    validator1 = IntFloatValidator(min_value=min_value, max_value=None,
                                   allowed_values=None)
    validator2 = ValueTypeValidator(value_type=int, strict=True)
    validators = MemberValidatorSequence(validators=[validator1, validator2])
    return OptionalMemberValidator(validators)


# pylint: disable=too-few-public-methods
class _TioWholeValidator(WholeConfigValidator):
    """Run tableio whole-configuration validation for TioJsonConfig.

    Member validators check individual JSON values. This validator asks
    tableio to validate relationships between values, including selected
    format, implementation, runtime capabilities and file access.
    """

    @override
    def validate(self, config: Config,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Validate one complete TioJsonConfig instance.

        Args:
            config: Configuration object to validate.
            stderr_file: Stream receiving user-facing validation messages.
        Raises:
            AssertionError: ``config`` is not a TioJsonConfig.
            InvalidConfiguration: The tableio whole-configuration rules
                reject the selected values, capabilities or file access.
        Returns:
            None when validation succeeds.
        """
        assert isinstance(config, TioJsonConfig)
        try:
            tio_config_validate(config, capabilities=config.capabilities,
                                file_access=config.file_access)
        except ConfigError as err:
            message = _issue_message(err)
            print(message, file=stderr_file)
            raise InvalidConfiguration(message) from err


def _issue_message(error: ConfigError) -> str:
    """Return one compact config-as-json message from tableio issues.

    Args:
        error: TableIO configuration error containing one or more issues.
    Returns:
        A newline-separated message suitable for InvalidConfiguration.
    """
    return '\n'.join(
        f'{issue.name}: {issue.message}' for issue in error.issues)


def _optional_one_char() -> OptionalMemberValidator:
    """Return a validator for optional one-character strings.

    Returns:
        A validator that accepts ``None`` or a one-character string.
    """
    return OptionalMemberValidator(StrLenValidator(min_length=1, max_length=1))


def _optional_non_empty() -> OptionalMemberValidator:
    """Return a validator for optional non-empty strings.

    Returns:
        A validator that accepts ``None`` or a non-empty string.
    """
    validator = StrLenValidator(min_length=1, max_length=None)
    return OptionalMemberValidator(validator)


class TioJsonCsvConfig(CsvConfigData, Config):
    """JSON-backed CSV configuration section for TableIO.

    The class stores the same durable CSV values as CsvConfigData and adds
    config-as-json support for the optional nested ``csv`` section in
    TioJsonConfig.
    """

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
        """Create CSV settings or read them from a JSON source.

        Constructor arguments provide defaults. If JSON text or a filename is
        supplied, config-as-json applies the JSON values over those defaults.

        Args:
            dialect: Optional CSV dialect template.
            delimiter: Optional one-character CSV delimiter.
            quoting: Optional CSV quoting style.
            quotechar: Optional one-character CSV quote character.
            lineterminator: Optional non-empty CSV line terminator.
            escapechar: Optional one-character CSV escape character.
            from_json_data_text: Optional JSON text to parse.
            from_json_filename: Optional JSON file to read.
            stderr_file: Stream receiving user-facing diagnostics.
        Raises:
            ValueError: Both JSON text and a JSON filename were supplied.
            SystemExit: The JSON filename does not exist.
            OSError: The JSON file cannot be read.
            KeyError: Parsed JSON has missing, unknown or misplaced keys.
            ConfigBadJson: The JSON text or file content is not usable as
                configuration JSON.
            InvalidConfiguration: Parsed or default values fail validation.
            NotImplementedError: A required config-as-json override is
                missing.
        """
        CsvConfigData.__init__(self, dialect=dialect, delimiter=delimiter,
                               quoting=quoting, quotechar=quotechar,
                               lineterminator=lineterminator,
                               escapechar=escapechar)
        Config.__init__(self, from_json_data_text=from_json_data_text,
                        from_json_filename=from_json_filename,
                        stderr_file=stderr_file)

    @override
    def _omit_none_from_json(self) -> list[str]:
        """Return optional CSV keys omitted from JSON while set to None.

        Returns:
            CSV member names omitted during JSON serialization when their
            value is ``None``.
        """
        return ['dialect', 'delimiter', 'quoting', 'quotechar',
                'lineterminator', 'escapechar']

    @override
    def parse_converters(self) -> dict[str, ParseConverter]:
        """Return JSON converters for CSV members.

        ``dialect`` is a CsvDialect enum member in tableio and a string name
        in JSON.

        Returns:
            Conversion rules used after reading JSON.
        """
        return {'dialect': self.get_converter_dict(CsvDialect)}

    @override
    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return validation for CSV-only JSON values.

        Missing values are accepted as ``None``. Delimiter, quote character
        and escape character must be single-character strings, while line
        terminator only needs to be a non-empty string.

        Args:
            stderr_file: Stream available for validators that need
                diagnostics while building the plan.
        Raises:
            KeyError: A tableio choice member is not known.
            AssertionError: A tableio choice member has no finite choices.
        Returns:
            Validation steps for CSV-specific members.
        """
        _ = stderr_file
        return [
            MemberValidationStep(member_names=['delimiter'],
                                 validator=_optional_one_char()),
            MemberValidationStep(member_names=['quoting'],
                                 validator=_optional_choice('csv.quoting')),
            MemberValidationStep(member_names=['quotechar'],
                                 validator=_optional_one_char()),
            MemberValidationStep(member_names=['lineterminator'],
                                 validator=_optional_non_empty()),
            MemberValidationStep(member_names=['escapechar'],
                                 validator=_optional_one_char())
        ]


class TioJsonHtmlConfig(HtmlConfigData, Config):
    """JSON-backed HTML configuration section for TableIO.

    The class stores the same durable HTML values as HtmlConfigData and adds
    config-as-json support for the optional nested ``html`` section in
    TioJsonConfig.
    """

    def __init__(self, css_file: Optional[str] = None,
                 from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Create HTML settings or read them from a JSON source.

        Constructor arguments provide defaults. If JSON text or a filename is
        supplied, config-as-json applies the JSON values over those defaults.

        Args:
            css_file: Optional CSS file path or URL.
            from_json_data_text: Optional JSON text to parse.
            from_json_filename: Optional JSON file to read.
            stderr_file: Stream receiving user-facing diagnostics.
        Raises:
            ValueError: Both JSON text and a JSON filename were supplied.
            SystemExit: The JSON filename does not exist.
            OSError: The JSON file cannot be read.
            KeyError: Parsed JSON has missing, unknown or misplaced keys.
            ConfigBadJson: The JSON text or file content is not usable as
                configuration JSON.
            InvalidConfiguration: Parsed or default values fail validation.
            NotImplementedError: A required config-as-json override is
                missing.
        """
        HtmlConfigData.__init__(self, css_file=css_file)
        Config.__init__(self, from_json_data_text=from_json_data_text,
                        from_json_filename=from_json_filename,
                        stderr_file=stderr_file)

    @override
    def _omit_none_from_json(self) -> list[str]:
        """Return optional HTML keys omitted from JSON while set to None.

        Returns:
            HTML member names omitted during JSON serialization when their
            value is ``None``.
        """
        return ['css_file']

    @override
    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return validation for HTML-only JSON values.

        Args:
            stderr_file: Stream available for validators that need
                diagnostics while building the plan.
        Returns:
            Validation steps for HTML-specific members.
        """
        _ = stderr_file
        return [
            MemberValidationStep(member_names=['css_file'],
                                 validator=_optional_string())
        ]


class TioJsonLatexConfig(LatexConfigData, Config):
    """JSON-backed LaTeX configuration section for TableIO.

    The class stores the same durable LaTeX values as LatexConfigData and
    adds config-as-json support for the optional nested ``latex`` section in
    TioJsonConfig.
    """

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, document_class: Optional[str] = None,
                 preamble: Optional[str] = None,
                 from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Create LaTeX settings or read them from a JSON source.

        Constructor arguments provide defaults. If JSON text or a filename is
        supplied, config-as-json applies the JSON values over those defaults.

        Args:
            document_class: Optional LaTeX document class.
            preamble: Optional extra LaTeX preamble text.
            from_json_data_text: Optional JSON text to parse.
            from_json_filename: Optional JSON file to read.
            stderr_file: Stream receiving user-facing diagnostics.
        Raises:
            ValueError: Both JSON text and a JSON filename were supplied.
            SystemExit: The JSON filename does not exist.
            OSError: The JSON file cannot be read.
            KeyError: Parsed JSON has missing, unknown or misplaced keys.
            ConfigBadJson: The JSON text or file content is not usable as
                configuration JSON.
            InvalidConfiguration: Parsed or default values fail validation.
            NotImplementedError: A required config-as-json override is
                missing.
        """
        LatexConfigData.__init__(self, document_class=document_class,
                                 preamble=preamble)
        Config.__init__(self, from_json_data_text=from_json_data_text,
                        from_json_filename=from_json_filename,
                        stderr_file=stderr_file)

    @override
    def _omit_none_from_json(self) -> list[str]:
        """Return optional LaTeX keys omitted from JSON while set to None.

        Returns:
            LaTeX member names omitted during JSON serialization when their
            value is ``None``.
        """
        return ['document_class', 'preamble']

    @override
    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return validation for LaTeX-only JSON values.

        Args:
            stderr_file: Stream available for validators that need
                diagnostics while building the plan.
        Raises:
            KeyError: A tableio choice member is not known.
            AssertionError: A tableio choice member has no finite choices.
        Returns:
            Validation steps for LaTeX-specific members.
        """
        _ = stderr_file
        return [
            MemberValidationStep(member_names=['document_class'],
                                 validator=_optional_choice(
                                     'latex.document_class')),
            MemberValidationStep(member_names=['preamble'],
                                 validator=_optional_string())
        ]


class TioJsonConfig(ConfigData, Config):  # pylint: disable=too-many-ancestors
    """Complete JSON-backed TableIO configuration.

    Instances are both tableio ConfigData objects and config-as-json Config
    objects. Runtime capabilities and file access are used for default
    selection and validation, but they are private runtime context rather
    than durable JSON configuration values.
    """

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
        """Create TableIO settings or read them from a JSON source.

        Default values come from tableio's recommended configuration for the
        supplied capabilities and file access. If JSON text or a filename is
        supplied, config-as-json applies the JSON values over those defaults.

        Args:
            capabilities: Runtime capabilities requested by the application.
            file_access: Runtime file access requested by the application.
            format_name: Optional preferred tableio format name.
            implementation: Optional preferred tableio implementation name.
            include_all_options: Include explicit non-``None`` defaults for
                template-style configuration output.
            from_json_data_text: Optional JSON text to parse.
            from_json_filename: Optional JSON file to read.
            auto_ch_hook: Hook receiving config-as-json automatic changes
                while reading old configuration files.
            stderr_file: Stream receiving user-facing diagnostics.
        Raises:
            ConfigError: TableIO cannot select or validate default data from
                the supplied runtime values.
            TypeError: File access or capabilities have invalid types in
                tableio access-capability validation.
            ValueError: Both JSON text and a JSON filename were supplied, or
                tableio rejects the requested file access value.
            SystemExit: The JSON filename does not exist.
            OSError: The JSON file cannot be read.
            KeyError: Parsed JSON has missing, unknown or misplaced keys.
            ConfigBadJson: The JSON text or file content is not usable as
                configuration JSON.
            InvalidConfiguration: Parsed or default values fail validation.
            NotImplementedError: A required config-as-json override is
                missing.
        """
        data = tio_config_default(capabilities, file_access,
                                  format_name=format_name,
                                  implementation=implementation,
                                  include_all_options=include_all_options)
        # Compact output should not lock the runtime implementation unless
        # the caller explicitly requested one.
        if implementation is None and not include_all_options:
            data.implementation = None
        self._capabilities = add_access_capabilities(file_access, capabilities,
                                                     error_file=stderr_file)
        self._file_access = file_access
        Config.copy_initial_data(data, self)
        Config.__init__(self, from_json_data_text=from_json_data_text,
                        from_json_filename=from_json_filename,
                        auto_ch_hook=auto_ch_hook, stderr_file=stderr_file)

    @property
    def capabilities(self) -> Capabilities:
        """Return capabilities used to choose and validate the backend.

        Returns:
            Runtime capabilities with file access requirements included.
        """
        return self._capabilities

    @property
    def file_access(self) -> FileAccess:
        """Return file access used to choose and validate the backend.

        Returns:
            Runtime file access supplied when the configuration was created.
        """
        return self._file_access

    @override
    def _omit_none_from_json(self) -> list[str]:
        """Return optional top-level keys omitted while set to None.

        Returns:
            Top-level member names omitted during JSON serialization when
            their value is ``None``.
        """
        return ['implementation', 'character_encoding', 'language', 'title',
                'paper_size', 'line_length', 'table_max_line_length',
                'table_alignment', 'csv', 'html', 'latex']

    @override
    def nested_configs(self) -> NestedConfigs:
        """Return declarations for optional format-specific sections.

        Returns:
            Nested config declarations for ``csv``, ``html`` and ``latex``.
        """
        return {
            'csv': ConfigNesting(kind=ConfigNestingKind.OPTIONAL_MEMBER,
                                 config_type=TioJsonCsvConfig),
            'html': ConfigNesting(kind=ConfigNestingKind.OPTIONAL_MEMBER,
                                  config_type=TioJsonHtmlConfig),
            'latex': ConfigNesting(kind=ConfigNestingKind.OPTIONAL_MEMBER,
                                   config_type=TioJsonLatexConfig)
        }

    @override
    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return validation for top-level JSON values.

        Member validation checks value shapes and normalizes tableio choices.
        The final whole-config step lets tableio validate combinations that
        depend on capabilities, file access, format and implementation.

        Args:
            stderr_file: Stream available for validators that need
                diagnostics while building the plan.
        Raises:
            KeyError: A tableio choice member is not known.
            AssertionError: A tableio choice member has no finite choices.
        Returns:
            Validation steps for top-level and whole-configuration values.
        """
        _ = stderr_file
        return [
            MemberValidationStep(member_names=['format_name'],
                                 validator=_choice_validator('format_name')),
            MemberValidationStep(member_names=['implementation'],
                                 validator=_optional_choice('implementation')),
            MemberValidationStep(member_names=['character_encoding'],
                                 validator=OptionalMemberValidator(
                                     CharEncodingValidator())),
            MemberValidationStep(member_names=['language', 'title'],
                                 validator=_optional_string()),
            MemberValidationStep(member_names=['paper_size'],
                                 validator=_optional_choice('paper_size')),
            MemberValidationStep(member_names=['line_length'],
                                 validator=_optional_int_at_least(11)),
            MemberValidationStep(member_names=['table_max_line_length'],
                                 validator=_optional_int_at_least(10)),
            MemberValidationStep(member_names=['table_alignment'],
                                 validator=_optional_choice(
                                     'table_alignment')),
            WholeConfigValidationStep(validator=_TioWholeValidator())
        ]


# pylint: disable=too-many-arguments,too-many-positional-arguments
def tio_json_config_default(capabilities: Capabilities,
                            file_access: FileAccess,
                            format_name: Optional[str] = None,
                            implementation: Optional[str] = None,
                            include_all_options: bool = False,
                            stderr_file: TextIO = sys.stderr) -> TioJsonConfig:
    """Return a TioJsonConfig with tableio's recommended defaults.

    The returned object can be used directly as a tableio ConfigData object
    and can also read or write the same settings as JSON through
    config-as-json.

    Args:
        capabilities: Runtime capabilities requested by the application.
        file_access: Runtime file access requested by the application.
        format_name: Optional preferred tableio format name.
        implementation: Optional preferred tableio implementation name.
        include_all_options: Include explicit non-``None`` defaults for
            template-style configuration output.
        stderr_file: Stream receiving user-facing diagnostics.
    Raises:
        ConfigError: TableIO cannot select or validate default data from the
            supplied runtime values.
        TypeError: File access or capabilities have invalid types in tableio
            access-capability validation.
        ValueError: TableIO rejects the requested file access value.
        InvalidConfiguration: The resulting default configuration does not
            pass validation.
    Returns:
        A JSON-backed tableio configuration object.
    """
    return TioJsonConfig(capabilities=capabilities, file_access=file_access,
                         format_name=format_name,
                         implementation=implementation,
                         include_all_options=include_all_options,
                         stderr_file=stderr_file)
