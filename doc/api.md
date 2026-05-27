# Table of Contents

* [tableio\_cfg\_json.describe](#tableio_cfg_json.describe)
  * [get\_general\_cfg\_info](#tableio_cfg_json.describe.get_general_cfg_info)
  * [get\_config\_member\_names](#tableio_cfg_json.describe.get_config_member_names)
  * [describe\_config\_members](#tableio_cfg_json.describe.describe_config_members)
  * [describe\_config\_reference](#tableio_cfg_json.describe.describe_config_reference)
  * [describe\_config\_example](#tableio_cfg_json.describe.describe_config_example)
  * [describe\_config](#tableio_cfg_json.describe.describe_config)
* [tableio\_cfg\_json.config](#tableio_cfg_json.config)
  * [TioJsonCsvConfig](#tableio_cfg_json.config.TioJsonCsvConfig)
    * [\_\_init\_\_](#tableio_cfg_json.config.TioJsonCsvConfig.__init__)
    * [parse\_converters](#tableio_cfg_json.config.TioJsonCsvConfig.parse_converters)
    * [get\_validation\_plan](#tableio_cfg_json.config.TioJsonCsvConfig.get_validation_plan)
  * [TioJsonHtmlConfig](#tableio_cfg_json.config.TioJsonHtmlConfig)
    * [\_\_init\_\_](#tableio_cfg_json.config.TioJsonHtmlConfig.__init__)
    * [get\_validation\_plan](#tableio_cfg_json.config.TioJsonHtmlConfig.get_validation_plan)
  * [TioJsonLatexConfig](#tableio_cfg_json.config.TioJsonLatexConfig)
    * [\_\_init\_\_](#tableio_cfg_json.config.TioJsonLatexConfig.__init__)
    * [get\_validation\_plan](#tableio_cfg_json.config.TioJsonLatexConfig.get_validation_plan)
  * [TioJsonConfig](#tableio_cfg_json.config.TioJsonConfig)
    * [\_\_init\_\_](#tableio_cfg_json.config.TioJsonConfig.__init__)
    * [capabilities](#tableio_cfg_json.config.TioJsonConfig.capabilities)
    * [file\_access](#tableio_cfg_json.config.TioJsonConfig.file_access)
    * [nested\_configs](#tableio_cfg_json.config.TioJsonConfig.nested_configs)
    * [get\_validation\_plan](#tableio_cfg_json.config.TioJsonConfig.get_validation_plan)
  * [tio\_json\_config\_default](#tableio_cfg_json.config.tio_json_config_default)
* [tableio\_cfg\_json.wizard](#tableio_cfg_json.wizard)
  * [WizardUiBridge](#tableio_cfg_json.wizard.WizardUiBridge)
    * [ask](#tableio_cfg_json.wizard.WizardUiBridge.ask)
    * [error\_file](#tableio_cfg_json.wizard.WizardUiBridge.error_file)
    * [show](#tableio_cfg_json.wizard.WizardUiBridge.show)
  * [WizardUiBridgeConsole](#tableio_cfg_json.wizard.WizardUiBridgeConsole)
    * [\_\_init\_\_](#tableio_cfg_json.wizard.WizardUiBridgeConsole.__init__)
    * [ask](#tableio_cfg_json.wizard.WizardUiBridgeConsole.ask)
    * [error\_file](#tableio_cfg_json.wizard.WizardUiBridgeConsole.error_file)
    * [show](#tableio_cfg_json.wizard.WizardUiBridgeConsole.show)
  * [tio\_json\_config\_wizard](#tableio_cfg_json.wizard.tio_json_config_wizard)

<a id="tableio_cfg_json.describe"></a>

# tableio\_cfg\_json.describe

Describe the configuration file format of tableio-cfg-json.

<a id="tableio_cfg_json.describe.get_general_cfg_info"></a>

#### get\_general\_cfg\_info

```python
def get_general_cfg_info() -> str
```

Get a description of the general configuration file format.

**Returns**:

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

<a id="tableio_cfg_json.describe.get_config_member_names"></a>

#### get\_config\_member\_names

```python
def get_config_member_names(
        capabilities: Optional[Capabilities] = None,
        file_access: Optional[FileAccess] = None,
        format_name: Optional[str] = None,
        implementation: Optional[str] = None) -> tuple[str, ...]
```

Get relevant configuration member names for one TableIO endpoint.

Use this helper when an application wants to compose its own
documentation text instead of using the complete text returned by
describe_config(). It is especially useful for larger application
configuration files with several TableIO endpoints: call it once for each
endpoint, combine the names, and pass the result to
describe_config_reference() so the long parameter descriptions appear
only once.

**Arguments**:

- `capabilities` - Capabilities needed by the application endpoint.
  Passing this filters the result to formats and options that can
  satisfy those capabilities.
- `file_access` - File access for the endpoint, for example READ for an
  input endpoint or CREATE for an output endpoint. Passing this
  filters the result to backends that support that access.
- `format_name` - Optional TableIO format name. Passing this narrows the
  result to members relevant for that format.
- `implementation` - Optional TableIO implementation name. Passing this
  narrows the result to members relevant for that implementation.

**Raises**:

- `TableIOFactoryNoCapabilityMatch` - The requested filters match no
  registered format or implementation.

**Returns**:

  Relevant member names in TableIO metadata order.

<a id="tableio_cfg_json.describe.describe_config_members"></a>

#### describe\_config\_members

```python
def describe_config_members(capabilities: Optional[Capabilities] = None,
                            file_access: Optional[FileAccess] = None,
                            format_name: Optional[str] = None,
                            implementation: Optional[str] = None) -> str
```

Get a compact member summary for one TableIO endpoint.

Use this helper when the surrounding application already explains what
the endpoint means, and only needs a short list of the TableIO choices
and member names that are editable for that endpoint. It deliberately
avoids the longer per-member descriptions so that an application can show
this section once for each input or output, and then use
describe_config_reference() once for the shared detailed reference.

**Arguments**:

- `capabilities` - Capabilities needed by the application endpoint.
  Passing this filters format choices, implementation choices and
  members to what the endpoint can actually use.
- `file_access` - File access for the endpoint. For example, READ limits
  the listed formats to read-capable formats.
- `format_name` - Optional TableIO format name. Passing this is useful
  when documenting one already-selected format.
- `implementation` - Optional TableIO implementation name. Passing this
  is useful when documenting one already-selected backend.

**Raises**:

- `TableIOFactoryNoCapabilityMatch` - The requested filters match no
  registered format or implementation.

**Returns**:

  A compact text listing format choices, implementation choices and
  relevant configuration members. The returned line length is limited
  to 79 characters.

<a id="tableio_cfg_json.describe.describe_config_reference"></a>

#### describe\_config\_reference

```python
def describe_config_reference(
        member_names: Optional[Sequence[str]] = None) -> str
```

Get unfiltered reference text for selected configuration members.

Use this helper for the detailed reference section in user-facing syntax
text. In a simple single-endpoint program, describe_config() may be
enough. In a larger application config, prefer describing each endpoint
with describe_config_members(), collect the relevant names with
get_config_member_names(), and call this function once so each parameter
description is not repeated for every endpoint.

**Arguments**:

- `member_names` - Optional names of members to describe. Pass None, or
  omit the argument, to describe all known TableIO configuration
  members. Pass a sequence from get_config_member_names() to limit
  the reference to members relevant for one or more endpoints. Pass
  an empty sequence to get an empty string. Unknown names raise
  ``KeyError`` and output order follows TableIO metadata order.

**Raises**:

- `KeyError` - A requested member name is unknown.

**Returns**:

  A long-form member reference. The returned line length is limited
  to 79 characters.

<a id="tableio_cfg_json.describe.describe_config_example"></a>

#### describe\_config\_example

```python
def describe_config_example(capabilities: Optional[Capabilities] = None,
                            file_access: Optional[FileAccess] = None,
                            format_name: Optional[str] = None,
                            implementation: Optional[str] = None,
                            complete: bool = False) -> str
```

Get one formatted JSON example for one TableIO endpoint.

Use this helper when the application wants to decide where example JSON
belongs in its own text. The return value is only the indented JSON
document, with no heading or explanation. Use the compact default for a
realistic hand-editable example, and ``complete=True`` when the goal is a
template that shows optional defaults.

**Arguments**:

- `capabilities` - Capabilities needed by the application endpoint.
  These capabilities influence which default TableIO backend can be
  selected for the example.
- `file_access` - File access for the endpoint. If omitted, the helper
  tries a sensible access mode based on the capabilities.
- `format_name` - Optional TableIO format name to use in the example.
- `implementation` - Optional TableIO implementation name to use in the
  example.
- `complete` - Whether all options should be visible in the example.

**Raises**:

- `TableIOFactoryNoCapabilityMatch` - No default example can be selected.

**Returns**:

  A formatted JSON document string without any heading text.

<a id="tableio_cfg_json.describe.describe_config"></a>

#### describe\_config

```python
def describe_config(capabilities: Optional[Capabilities] = None,
                    file_access: Optional[FileAccess] = None,
                    format_name: Optional[str] = None,
                    include_compact_example: bool = True,
                    include_full_example: bool = False,
                    implementation: Optional[str] = None) -> str
```

Get a description of the configuration file format of tableio-cfg-json.

Use this function for a simple program where one configuration file
mainly describes one TableIO endpoint. It returns a complete section with
matching formats, implementations, relevant members, detailed member
descriptions and optional JSON examples. For a larger application config
with several TableIO inputs or outputs, prefer composing the text from
get_general_cfg_info(), describe_config_members(),
get_config_member_names(), describe_config_reference() and
describe_config_example() so the application can explain each endpoint in
its own words and avoid repeating the long member reference.

**Arguments**:

- `capabilities` - The capabilities of the application. If provided the
  description will be limited to the configuration options
  that are relevant for the given capabilities. If not
  provided the description will include all configuration
  options that are relevant for the given file access.
- `file_access` - The file access of the application. If provided the
  description will be limited to the configuration options
  that are relevant for the given file access. If not
  provided the description will include all configuration
  options that are relevant for the given capabilities.
  For instance if the file access is READ, only
  format_name values that are READ-capable will be
  included.
- `format_name` - The name of the format to describe. If provided the
  description will be limited to the configuration options
  that are relevant for the given format name. If not
  provided the description will include all configuration
  options that are relevant for the given capabilities and
  file access.
- `include_compact_example` - Whether to include a compact configuration
  example (that is JSON string produced by the
  configuration that is described), with the default
  values omitted to keep the example compact.
- `include_full_example` - Whether to include a full configuration example
  (that is JSON string produced by the configuration
  that is described), with all values (also default values)
  included. Both include_compact_example and
  include_full_example can be True, in which case both
  examples are included.
- `implementation` - The implementation name to describe. If provided the
  description will be limited to the configuration options
  that are relevant for that implementation.
  

**Returns**:

  A description of the configuration file format of tableio-cfg-json.
  The returned string is suitable as a section in a plain text file
  that describes the configuration file format of tableio-cfg-json.
  The line length in the returned string is limited to 79 characters.
  It is assumed that the string returned by get_general_cfg_info()
  has been added to the plain text file before the return value of
  this function.
  

**Raises**:

- `TableIOFactoryNoCapabilityMatch` - The requested capabilities cannot be
  matched to any available implementation.

<a id="tableio_cfg_json.config"></a>

# tableio\_cfg\_json.config

JSON-backed configuration classes for TableIO settings.

The module adapts tableio's framework-neutral configuration data classes to
config-as-json. The public classes keep tableio's durable values while adding
JSON reading, writing, nested-section handling and validation.

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

<a id="tableio_cfg_json.wizard"></a>

# tableio\_cfg\_json.wizard

Interactive helpers for creating TableIO JSON configuration.

The public helper in this module is intentionally scoped to one TableIO
endpoint. Application code can call it once for each input or output it wants
to configure, and then place the returned TioJsonConfig objects inside its own
larger config-as-json configuration class.

<a id="tableio_cfg_json.wizard.WizardUiBridge"></a>

## WizardUiBridge Objects

```python
class WizardUiBridge()
```

Bridge between the wizard and the user interface.

This is an abstract base class for a bridge between the wizard and
the user interface. Provide concrete classes of this bridge to
allow the wizard to use console text user interface or a graphical
user interface.

<a id="tableio_cfg_json.wizard.WizardUiBridge.ask"></a>

#### ask

```python
def ask(question: str,
        re_ask_reason: Optional[str] = None,
        choices: Optional[Sequence[str]] = None) -> str | int
```

Ask a question and return the user's answer.

**Arguments**:

- `question` - The question to ask the user.
- `re_ask_reason` - The reason for re-asking the question for
  instance that the user's answer was invalid.
- `choices` - The choices to offer the user as a sequence of strings.
  

**Returns**:

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

<a id="tableio_cfg_json.wizard.WizardUiBridge.error_file"></a>

#### error\_file

```python
def error_file() -> TextIO
```

Return the stream used for validation diagnostics.

<a id="tableio_cfg_json.wizard.WizardUiBridge.show"></a>

#### show

```python
def show(message: str) -> None
```

Show a message to the user.

If implementing a graphical user interface, this method should
display the message in a dialog or a message box. If implementing
a console text user interface, this method should print the message
to the console.

**Arguments**:

- `message` - The message to show the user.

<a id="tableio_cfg_json.wizard.WizardUiBridgeConsole"></a>

## WizardUiBridgeConsole Objects

```python
class WizardUiBridgeConsole(WizardUiBridge)
```

Bridge between the wizard and the console text user interface.

<a id="tableio_cfg_json.wizard.WizardUiBridgeConsole.__init__"></a>

#### \_\_init\_\_

```python
def __init__(stdout_file: TextIO, stdin_file: TextIO,
             stderr_file: TextIO) -> None
```

Initialize the bridge.

**Arguments**:

- `stdout_file` - Stream to print messages to.
- `stdin_file` - Stream to read user answers from.
- `stderr_file` - Stream to print errors to.

<a id="tableio_cfg_json.wizard.WizardUiBridgeConsole.ask"></a>

#### ask

```python
def ask(question: str,
        re_ask_reason: Optional[str] = None,
        choices: Optional[Sequence[str]] = None) -> str | int
```

Ask a question and return the user's answer.

**Arguments**:

- `question` - The question to ask the user.
- `re_ask_reason` - The reason for re-asking the question for
  instance that the user's answer was invalid.
- `choices` - The choices to offer the user as a sequence of strings.
  

**Returns**:

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

<a id="tableio_cfg_json.wizard.WizardUiBridgeConsole.error_file"></a>

#### error\_file

```python
def error_file() -> TextIO
```

Return the stream used for validation diagnostics.

<a id="tableio_cfg_json.wizard.WizardUiBridgeConsole.show"></a>

#### show

```python
def show(message: str) -> None
```

Show a message to the user.

This method prints the message to the console.

**Arguments**:

- `message` - The message to show the user.

<a id="tableio_cfg_json.wizard.tio_json_config_wizard"></a>

#### tio\_json\_config\_wizard

```python
def tio_json_config_wizard(capabilities: Capabilities, file_access: FileAccess,
                           ui_bridge: WizardUiBridge) -> TioJsonConfig
```

Interactively create one TableIO JSON endpoint configuration.

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

**Arguments**:

- `capabilities` - Capabilities needed by this application endpoint. Pass
  the capabilities for the one input or output being configured, not
  for the whole application.
- `file_access` - File access for this endpoint, such as READ for an input
  file or CREATE for an output file. This controls which formats and
  implementations can be offered.
- `ui_bridge` - Bridge between the wizard and the user interface.

**Raises**:

- `EOFError` - Scripted input ends before all required answers are read.
- `TableIOFactoryNoCapabilityMatch` - No registered backend matches the
  supplied capabilities and file access.
- `InvalidConfiguration` - The selected values fail final validation.

**Returns**:

  A validated TableIO JSON config for the one endpoint.

