# Table of Contents

* [tableio\_cfg\_json.config](#tableio_cfg_json.config)
  * [\_choices](#tableio_cfg_json.config._choices)
  * [\_choice\_validator](#tableio_cfg_json.config._choice_validator)
  * [\_optional\_choice](#tableio_cfg_json.config._optional_choice)
  * [\_optional\_string](#tableio_cfg_json.config._optional_string)
  * [\_optional\_int\_at\_least](#tableio_cfg_json.config._optional_int_at_least)
  * [\_TioWholeValidator](#tableio_cfg_json.config._TioWholeValidator)
    * [validate](#tableio_cfg_json.config._TioWholeValidator.validate)
  * [\_issue\_message](#tableio_cfg_json.config._issue_message)
  * [\_optional\_one\_char](#tableio_cfg_json.config._optional_one_char)
  * [\_optional\_non\_empty](#tableio_cfg_json.config._optional_non_empty)
  * [TioJsonCsvConfig](#tableio_cfg_json.config.TioJsonCsvConfig)
    * [\_\_init\_\_](#tableio_cfg_json.config.TioJsonCsvConfig.__init__)
    * [\_omit\_none\_from\_json](#tableio_cfg_json.config.TioJsonCsvConfig._omit_none_from_json)
    * [parse\_converters](#tableio_cfg_json.config.TioJsonCsvConfig.parse_converters)
    * [get\_validation\_plan](#tableio_cfg_json.config.TioJsonCsvConfig.get_validation_plan)
  * [TioJsonHtmlConfig](#tableio_cfg_json.config.TioJsonHtmlConfig)
    * [\_\_init\_\_](#tableio_cfg_json.config.TioJsonHtmlConfig.__init__)
    * [\_omit\_none\_from\_json](#tableio_cfg_json.config.TioJsonHtmlConfig._omit_none_from_json)
    * [get\_validation\_plan](#tableio_cfg_json.config.TioJsonHtmlConfig.get_validation_plan)
  * [TioJsonLatexConfig](#tableio_cfg_json.config.TioJsonLatexConfig)
    * [\_\_init\_\_](#tableio_cfg_json.config.TioJsonLatexConfig.__init__)
    * [\_omit\_none\_from\_json](#tableio_cfg_json.config.TioJsonLatexConfig._omit_none_from_json)
    * [get\_validation\_plan](#tableio_cfg_json.config.TioJsonLatexConfig.get_validation_plan)
  * [TioJsonConfig](#tableio_cfg_json.config.TioJsonConfig)
    * [\_\_init\_\_](#tableio_cfg_json.config.TioJsonConfig.__init__)
    * [capabilities](#tableio_cfg_json.config.TioJsonConfig.capabilities)
    * [file\_access](#tableio_cfg_json.config.TioJsonConfig.file_access)
    * [\_omit\_none\_from\_json](#tableio_cfg_json.config.TioJsonConfig._omit_none_from_json)
    * [nested\_configs](#tableio_cfg_json.config.TioJsonConfig.nested_configs)
    * [get\_validation\_plan](#tableio_cfg_json.config.TioJsonConfig.get_validation_plan)
  * [tio\_json\_config\_default](#tableio_cfg_json.config.tio_json_config_default)

<a id="tableio_cfg_json.config"></a>

# tableio\_cfg\_json.config

JSON-backed configuration classes for TableIO settings.

The module adapts tableio's framework-neutral configuration data classes to
config-as-json. The public classes keep tableio's durable values while adding
JSON reading, writing, nested-section handling and validation.

<a id="tableio_cfg_json.config._choices"></a>

#### \_choices

```python
def _choices(name: str) -> tuple[str, ...]
```

Return tableio choices for one configuration member.

TableIO owns the accepted values. Looking them up here keeps this bridge
aligned with currently registered formats, implementations and options.

**Arguments**:

- `name` - Dotted tableio configuration member name.

**Raises**:

- `KeyError` - The member name is not known by tableio.
- `AssertionError` - The tableio member has no finite choices.

**Returns**:

  Accepted string values for the requested member.

<a id="tableio_cfg_json.config._choice_validator"></a>

#### \_choice\_validator

```python
def _choice_validator(name: str) -> StrValidator
```

Return a validator for one required tableio choice member.

**Arguments**:

- `name` - Dotted tableio configuration member name.

**Raises**:

- `KeyError` - The member name is not known by tableio.
- `AssertionError` - The tableio member has no finite choices.

**Returns**:

  A string validator that accepts and normalizes tableio choices.

<a id="tableio_cfg_json.config._optional_choice"></a>

#### \_optional\_choice

```python
def _optional_choice(name: str) -> OptionalMemberValidator
```

Return a validator for one optional tableio choice member.

**Arguments**:

- `name` - Dotted tableio configuration member name.

**Raises**:

- `KeyError` - The member name is not known by tableio.
- `AssertionError` - The tableio member has no finite choices.

**Returns**:

  A validator that accepts ``None`` or a normalized tableio choice.

<a id="tableio_cfg_json.config._optional_string"></a>

#### \_optional\_string

```python
def _optional_string() -> OptionalMemberValidator
```

Return a validator for an optional plain string member.

**Returns**:

  A validator that accepts ``None`` or a string.

<a id="tableio_cfg_json.config._optional_int_at_least"></a>

#### \_optional\_int\_at\_least

```python
def _optional_int_at_least(min_value: int) -> OptionalMemberValidator
```

Return a validator for an optional strict integer lower bound.

The numeric validator checks the range, and the strict type validator
rejects bools and floats that Python would otherwise treat as numbers.

**Arguments**:

- `min_value` - Inclusive lower bound accepted for non-``None`` values.

**Returns**:

  A validator that accepts ``None`` or a strict integer at least
  ``min_value``.

<a id="tableio_cfg_json.config._TioWholeValidator"></a>

## \_TioWholeValidator Objects

```python
class _TioWholeValidator(WholeConfigValidator)
```

Run tableio whole-configuration validation for TioJsonConfig.

Member validators check individual JSON values. This validator asks
tableio to validate relationships between values, including selected
format, implementation, runtime capabilities and file access.

<a id="tableio_cfg_json.config._TioWholeValidator.validate"></a>

#### validate

```python
@override
def validate(config: Config, stderr_file: TextIO = sys.stderr) -> None
```

Validate one complete TioJsonConfig instance.

**Arguments**:

- `config` - Configuration object to validate.
- `stderr_file` - Stream receiving user-facing validation messages.

**Raises**:

- `AssertionError` - ``config`` is not a TioJsonConfig.
- `InvalidConfiguration` - The tableio whole-configuration rules
  reject the selected values, capabilities or file access.

**Returns**:

  None when validation succeeds.

<a id="tableio_cfg_json.config._issue_message"></a>

#### \_issue\_message

```python
def _issue_message(error: ConfigError) -> str
```

Return one compact config-as-json message from tableio issues.

**Arguments**:

- `error` - TableIO configuration error containing one or more issues.

**Returns**:

  A newline-separated message suitable for InvalidConfiguration.

<a id="tableio_cfg_json.config._optional_one_char"></a>

#### \_optional\_one\_char

```python
def _optional_one_char() -> OptionalMemberValidator
```

Return a validator for optional one-character strings.

**Returns**:

  A validator that accepts ``None`` or a one-character string.

<a id="tableio_cfg_json.config._optional_non_empty"></a>

#### \_optional\_non\_empty

```python
def _optional_non_empty() -> OptionalMemberValidator
```

Return a validator for optional non-empty strings.

**Returns**:

  A validator that accepts ``None`` or a non-empty string.

<a id="tableio_cfg_json.config.TioJsonCsvConfig"></a>

## TioJsonCsvConfig Objects

```python
class TioJsonCsvConfig(CsvConfigData, Config)
```

JSON-backed CSV configuration section for TableIO.

The class stores the same durable CSV values as CsvConfigData and adds
config-as-json support for the optional nested ``csv`` section in
TioJsonConfig.

<a id="tableio_cfg_json.config.TioJsonCsvConfig.__init__"></a>

#### \_\_init\_\_

```python
def __init__(dialect: Optional[CsvDialect] = None,
             delimiter: Optional[str] = None,
             quoting: Optional[str] = None,
             quotechar: Optional[str] = None,
             lineterminator: Optional[str] = None,
             escapechar: Optional[str] = None,
             from_json_data_text: Optional[str] = None,
             from_json_filename: Optional[PathOrStr] = None,
             stderr_file: TextIO = sys.stderr) -> None
```

Create CSV settings or read them from a JSON source.

Constructor arguments provide defaults. If JSON text or a filename is
supplied, config-as-json applies the JSON values over those defaults.

**Arguments**:

- `dialect` - Optional CSV dialect template.
- `delimiter` - Optional one-character CSV delimiter.
- `quoting` - Optional CSV quoting style.
- `quotechar` - Optional one-character CSV quote character.
- `lineterminator` - Optional non-empty CSV line terminator.
- `escapechar` - Optional one-character CSV escape character.
- `from_json_data_text` - Optional JSON text to parse.
- `from_json_filename` - Optional JSON file to read.
- `stderr_file` - Stream receiving user-facing diagnostics.

**Raises**:

- `ValueError` - Both JSON text and a JSON filename were supplied.
- `SystemExit` - The JSON filename does not exist.
- `OSError` - The JSON file cannot be read.
- `KeyError` - Parsed JSON has missing, unknown or misplaced keys.
- `ConfigBadJson` - The JSON text or file content is not usable as
  configuration JSON.
- `InvalidConfiguration` - Parsed or default values fail validation.
- `NotImplementedError` - A required config-as-json override is
  missing.

<a id="tableio_cfg_json.config.TioJsonCsvConfig._omit_none_from_json"></a>

#### \_omit\_none\_from\_json

```python
@override
def _omit_none_from_json() -> list[str]
```

Return optional CSV keys omitted from JSON while set to None.

**Returns**:

  CSV member names omitted during JSON serialization when their
  value is ``None``.

<a id="tableio_cfg_json.config.TioJsonCsvConfig.parse_converters"></a>

#### parse\_converters

```python
@override
def parse_converters() -> dict[str, ParseConverter]
```

Return JSON converters for CSV members.

``dialect`` is a CsvDialect enum member in tableio and a string name
in JSON.

**Returns**:

  Conversion rules used after reading JSON.

<a id="tableio_cfg_json.config.TioJsonCsvConfig.get_validation_plan"></a>

#### get\_validation\_plan

```python
@override
def get_validation_plan(stderr_file: TextIO) -> ValidationPlan
```

Return validation for CSV-only JSON values.

Missing values are accepted as ``None``. Delimiter, quote character
and escape character must be single-character strings, while line
terminator only needs to be a non-empty string.

**Arguments**:

- `stderr_file` - Stream available for validators that need
  diagnostics while building the plan.

**Raises**:

- `KeyError` - A tableio choice member is not known.
- `AssertionError` - A tableio choice member has no finite choices.

**Returns**:

  Validation steps for CSV-specific members.

<a id="tableio_cfg_json.config.TioJsonHtmlConfig"></a>

## TioJsonHtmlConfig Objects

```python
class TioJsonHtmlConfig(HtmlConfigData, Config)
```

JSON-backed HTML configuration section for TableIO.

The class stores the same durable HTML values as HtmlConfigData and adds
config-as-json support for the optional nested ``html`` section in
TioJsonConfig.

<a id="tableio_cfg_json.config.TioJsonHtmlConfig.__init__"></a>

#### \_\_init\_\_

```python
def __init__(css_file: Optional[str] = None,
             from_json_data_text: Optional[str] = None,
             from_json_filename: Optional[PathOrStr] = None,
             stderr_file: TextIO = sys.stderr) -> None
```

Create HTML settings or read them from a JSON source.

Constructor arguments provide defaults. If JSON text or a filename is
supplied, config-as-json applies the JSON values over those defaults.

**Arguments**:

- `css_file` - Optional CSS file path or URL.
- `from_json_data_text` - Optional JSON text to parse.
- `from_json_filename` - Optional JSON file to read.
- `stderr_file` - Stream receiving user-facing diagnostics.

**Raises**:

- `ValueError` - Both JSON text and a JSON filename were supplied.
- `SystemExit` - The JSON filename does not exist.
- `OSError` - The JSON file cannot be read.
- `KeyError` - Parsed JSON has missing, unknown or misplaced keys.
- `ConfigBadJson` - The JSON text or file content is not usable as
  configuration JSON.
- `InvalidConfiguration` - Parsed or default values fail validation.
- `NotImplementedError` - A required config-as-json override is
  missing.

<a id="tableio_cfg_json.config.TioJsonHtmlConfig._omit_none_from_json"></a>

#### \_omit\_none\_from\_json

```python
@override
def _omit_none_from_json() -> list[str]
```

Return optional HTML keys omitted from JSON while set to None.

**Returns**:

  HTML member names omitted during JSON serialization when their
  value is ``None``.

<a id="tableio_cfg_json.config.TioJsonHtmlConfig.get_validation_plan"></a>

#### get\_validation\_plan

```python
@override
def get_validation_plan(stderr_file: TextIO) -> ValidationPlan
```

Return validation for HTML-only JSON values.

**Arguments**:

- `stderr_file` - Stream available for validators that need
  diagnostics while building the plan.

**Returns**:

  Validation steps for HTML-specific members.

<a id="tableio_cfg_json.config.TioJsonLatexConfig"></a>

## TioJsonLatexConfig Objects

```python
class TioJsonLatexConfig(LatexConfigData, Config)
```

JSON-backed LaTeX configuration section for TableIO.

The class stores the same durable LaTeX values as LatexConfigData and
adds config-as-json support for the optional nested ``latex`` section in
TioJsonConfig.

<a id="tableio_cfg_json.config.TioJsonLatexConfig.__init__"></a>

#### \_\_init\_\_

```python
def __init__(document_class: Optional[str] = None,
             preamble: Optional[str] = None,
             from_json_data_text: Optional[str] = None,
             from_json_filename: Optional[PathOrStr] = None,
             stderr_file: TextIO = sys.stderr) -> None
```

Create LaTeX settings or read them from a JSON source.

Constructor arguments provide defaults. If JSON text or a filename is
supplied, config-as-json applies the JSON values over those defaults.

**Arguments**:

- `document_class` - Optional LaTeX document class.
- `preamble` - Optional extra LaTeX preamble text.
- `from_json_data_text` - Optional JSON text to parse.
- `from_json_filename` - Optional JSON file to read.
- `stderr_file` - Stream receiving user-facing diagnostics.

**Raises**:

- `ValueError` - Both JSON text and a JSON filename were supplied.
- `SystemExit` - The JSON filename does not exist.
- `OSError` - The JSON file cannot be read.
- `KeyError` - Parsed JSON has missing, unknown or misplaced keys.
- `ConfigBadJson` - The JSON text or file content is not usable as
  configuration JSON.
- `InvalidConfiguration` - Parsed or default values fail validation.
- `NotImplementedError` - A required config-as-json override is
  missing.

<a id="tableio_cfg_json.config.TioJsonLatexConfig._omit_none_from_json"></a>

#### \_omit\_none\_from\_json

```python
@override
def _omit_none_from_json() -> list[str]
```

Return optional LaTeX keys omitted from JSON while set to None.

**Returns**:

  LaTeX member names omitted during JSON serialization when their
  value is ``None``.

<a id="tableio_cfg_json.config.TioJsonLatexConfig.get_validation_plan"></a>

#### get\_validation\_plan

```python
@override
def get_validation_plan(stderr_file: TextIO) -> ValidationPlan
```

Return validation for LaTeX-only JSON values.

**Arguments**:

- `stderr_file` - Stream available for validators that need
  diagnostics while building the plan.

**Raises**:

- `KeyError` - A tableio choice member is not known.
- `AssertionError` - A tableio choice member has no finite choices.

**Returns**:

  Validation steps for LaTeX-specific members.

<a id="tableio_cfg_json.config.TioJsonConfig"></a>

## TioJsonConfig Objects

```python
class TioJsonConfig(ConfigData, Config)
```

Complete JSON-backed TableIO configuration.

Instances are both tableio ConfigData objects and config-as-json Config
objects. Runtime capabilities and file access are used for default
selection and validation, but they are private runtime context rather
than durable JSON configuration values.

<a id="tableio_cfg_json.config.TioJsonConfig.__init__"></a>

#### \_\_init\_\_

```python
def __init__(capabilities: Capabilities,
             file_access: FileAccess,
             format_name: Optional[str] = None,
             implementation: Optional[str] = None,
             include_all_options: bool = False,
             from_json_data_text: Optional[str] = None,
             from_json_filename: Optional[PathOrStr] = None,
             auto_ch_hook: Optional[ConfigAutoChangeHook] = None,
             stderr_file: TextIO = sys.stderr) -> None
```

Create TableIO settings or read them from a JSON source.

Default values come from tableio's recommended configuration for the
supplied capabilities and file access. If JSON text or a filename is
supplied, config-as-json applies the JSON values over those defaults.

**Arguments**:

- `capabilities` - Runtime capabilities requested by the application.
- `file_access` - Runtime file access requested by the application.
- `format_name` - Optional preferred tableio format name.
- `implementation` - Optional preferred tableio implementation name.
- `include_all_options` - Include explicit non-``None`` defaults for
  template-style configuration output.
- `from_json_data_text` - Optional JSON text to parse.
- `from_json_filename` - Optional JSON file to read.
- `auto_ch_hook` - Hook receiving config-as-json automatic changes
  while reading old configuration files.
- `stderr_file` - Stream receiving user-facing diagnostics.

**Raises**:

- `ConfigError` - TableIO cannot select or validate default data from
  the supplied runtime values.
- `TypeError` - File access or capabilities have invalid types in
  tableio access-capability validation.
- `ValueError` - Both JSON text and a JSON filename were supplied, or
  tableio rejects the requested file access value.
- `SystemExit` - The JSON filename does not exist.
- `OSError` - The JSON file cannot be read.
- `KeyError` - Parsed JSON has missing, unknown or misplaced keys.
- `ConfigBadJson` - The JSON text or file content is not usable as
  configuration JSON.
- `InvalidConfiguration` - Parsed or default values fail validation.
- `NotImplementedError` - A required config-as-json override is
  missing.

<a id="tableio_cfg_json.config.TioJsonConfig.capabilities"></a>

#### capabilities

```python
@property
def capabilities() -> Capabilities
```

Return capabilities used to choose and validate the backend.

**Returns**:

  Runtime capabilities with file access requirements included.

<a id="tableio_cfg_json.config.TioJsonConfig.file_access"></a>

#### file\_access

```python
@property
def file_access() -> FileAccess
```

Return file access used to choose and validate the backend.

**Returns**:

  Runtime file access supplied when the configuration was created.

<a id="tableio_cfg_json.config.TioJsonConfig._omit_none_from_json"></a>

#### \_omit\_none\_from\_json

```python
@override
def _omit_none_from_json() -> list[str]
```

Return optional top-level keys omitted while set to None.

**Returns**:

  Top-level member names omitted during JSON serialization when
  their value is ``None``.

<a id="tableio_cfg_json.config.TioJsonConfig.nested_configs"></a>

#### nested\_configs

```python
@override
def nested_configs() -> NestedConfigs
```

Return declarations for optional format-specific sections.

**Returns**:

  Nested config declarations for ``csv``, ``html`` and ``latex``.

<a id="tableio_cfg_json.config.TioJsonConfig.get_validation_plan"></a>

#### get\_validation\_plan

```python
@override
def get_validation_plan(stderr_file: TextIO) -> ValidationPlan
```

Return validation for top-level JSON values.

Member validation checks value shapes and normalizes tableio choices.
The final whole-config step lets tableio validate combinations that
depend on capabilities, file access, format and implementation.

**Arguments**:

- `stderr_file` - Stream available for validators that need
  diagnostics while building the plan.

**Raises**:

- `KeyError` - A tableio choice member is not known.
- `AssertionError` - A tableio choice member has no finite choices.

**Returns**:

  Validation steps for top-level and whole-configuration values.

<a id="tableio_cfg_json.config.tio_json_config_default"></a>

#### tio\_json\_config\_default

```python
def tio_json_config_default(capabilities: Capabilities,
                            file_access: FileAccess,
                            format_name: Optional[str] = None,
                            implementation: Optional[str] = None,
                            include_all_options: bool = False,
                            stderr_file: TextIO = sys.stderr) -> TioJsonConfig
```

Return a TioJsonConfig with tableio's recommended defaults.

The returned object can be used directly as a tableio ConfigData object
and can also read or write the same settings as JSON through
config-as-json.

**Arguments**:

- `capabilities` - Runtime capabilities requested by the application.
- `file_access` - Runtime file access requested by the application.
- `format_name` - Optional preferred tableio format name.
- `implementation` - Optional preferred tableio implementation name.
- `include_all_options` - Include explicit non-``None`` defaults for
  template-style configuration output.
- `stderr_file` - Stream receiving user-facing diagnostics.

**Raises**:

- `ConfigError` - TableIO cannot select or validate default data from the
  supplied runtime values.
- `TypeError` - File access or capabilities have invalid types in tableio
  access-capability validation.
- `ValueError` - TableIO rejects the requested file access value.
- `InvalidConfiguration` - The resulting default configuration does not
  pass validation.

**Returns**:

  A JSON-backed tableio configuration object.

