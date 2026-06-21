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
* [tableio\_cfg\_json.wizard\_ui\_bridge](#tableio_cfg_json.wizard_ui_bridge)
  * [WizardNavigation](#tableio_cfg_json.wizard_ui_bridge.WizardNavigation)
  * [WizardBack](#tableio_cfg_json.wizard_ui_bridge.WizardBack)
  * [WizardCancelLevel](#tableio_cfg_json.wizard_ui_bridge.WizardCancelLevel)
  * [WizardAbort](#tableio_cfg_json.wizard_ui_bridge.WizardAbort)
  * [TableColumn](#tableio_cfg_json.wizard_ui_bridge.TableColumn)
  * [TableCell](#tableio_cfg_json.wizard_ui_bridge.TableCell)
  * [WizardUiBridge](#tableio_cfg_json.wizard_ui_bridge.WizardUiBridge)
    * [ask](#tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.ask)
    * [ask\_yes\_no](#tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.ask_yes_no)
    * [ask\_choice](#tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.ask_choice)
    * [ask\_multi](#tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.ask_multi)
    * [ask\_table](#tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.ask_table)
    * [error\_file](#tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.error_file)
    * [show](#tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.show)
* [tableio\_cfg\_json.wizard\_ui\_bridge\_textual](#tableio_cfg_json.wizard_ui_bridge_textual)
  * [WizardUiBridgeTextual](#tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual)
    * [\_\_init\_\_](#tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual.__init__)
    * [ask](#tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual.ask)
    * [ask\_yes\_no](#tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual.ask_yes_no)
    * [ask\_choice](#tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual.ask_choice)
    * [ask\_multi](#tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual.ask_multi)
    * [ask\_table](#tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual.ask_table)
    * [error\_file](#tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual.error_file)
    * [show](#tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual.show)
* [tableio\_cfg\_json.wizard\_ui\_bridge\_console](#tableio_cfg_json.wizard_ui_bridge_console)
  * [WizardUiBridgeConsole](#tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole)
    * [\_\_init\_\_](#tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole.__init__)
    * [ask](#tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole.ask)
    * [ask\_choice](#tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole.ask_choice)
    * [ask\_multi](#tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole.ask_multi)
    * [error\_file](#tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole.error_file)
    * [show](#tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole.show)
* [tableio\_cfg\_json.wizard](#tableio_cfg_json.wizard)
  * [tio\_json\_config\_wizard](#tableio_cfg_json.wizard.tio_json_config_wizard)
* [tableio\_cfg\_json.wizard\_ui\_factory](#tableio_cfg_json.wizard_ui_factory)
  * [make\_text\_ui\_bridge](#tableio_cfg_json.wizard_ui_factory.make_text_ui_bridge)

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

<a id="tableio_cfg_json.wizard_ui_bridge"></a>

# tableio\_cfg\_json.wizard\_ui\_bridge

User interface bridge for the TableIO JSON configuration wizard.

This module defines the abstract bridge between the wizard and a user
interface, the navigation requests a bridge raises to steer wizard flow,
and the column and cell descriptors used by table questions. Concrete
console and graphical bridges derive from WizardUiBridge.

An application that drives the wizard is responsible for implementing
all the public ask methods of its bridge, together with show(). To give
application bridge authors time to migrate to the full API, the base
class provides temporary fallback implementations of ask_yes_no(),
ask_choice(), ask_multi() and ask_table() written in terms of ask(), so
a bridge that has not yet overridden one of them keeps working. These
fallbacks are a temporary compatibility aid and will be withdrawn in a
future release once bridges implement the methods directly.

<a id="tableio_cfg_json.wizard_ui_bridge.WizardNavigation"></a>

## WizardNavigation Objects

```python
class WizardNavigation(Exception)
```

Base class for wizard navigation requests raised by a bridge.

A user interface raises a subclass of this exception from an ask
method when the user wants to move within the wizard instead of
answering the current question. The wizard keeps these distinct from
validation errors, so its retry loops never catch them and they
reach the navigation driver unchanged.

<a id="tableio_cfg_json.wizard_ui_bridge.WizardBack"></a>

## WizardBack Objects

```python
class WizardBack(WizardNavigation)
```

Request to return to the previous wizard question.

A bridge raises this when the user chooses "back". The wizard
restores the data collected before the previous question and asks
that question again. Raised at the first question of one wizard call
it has no earlier question within that call, so the wizard lets it
propagate out to the application. The application can then step back
in its own outer navigation, for instance to the previous endpoint.

<a id="tableio_cfg_json.wizard_ui_bridge.WizardCancelLevel"></a>

## WizardCancelLevel Objects

```python
class WizardCancelLevel(WizardNavigation)
```

Request to leave the current level and change what opened it.

A bridge raises this when the user asks to step out of the current
configuration level, such as a table of format-specific parameters or
a group of questions that exist only because of an earlier choice.
Unlike WizardBack, which moves to the previous question at the same
level, this asks to return to the question one level out whose answer
opened the current level, so the user can change that answer. The
answers collected at the current level are discarded.

Each level's driver catches this from the level it opened and re-asks
the opening question. When the current level has no enclosing level,
the outermost driver cannot step out; following this contract it
re-asks the current question and tells the user there is no outer
level. Nesting may be arbitrarily deep: each driver either handles the
request for the level it opened or lets it propagate further out.

<a id="tableio_cfg_json.wizard_ui_bridge.WizardAbort"></a>

## WizardAbort Objects

```python
class WizardAbort(WizardNavigation)
```

Request to abandon the whole configuration.

A bridge raises this when the user abandons configuration entirely.
The wizard does not catch it; it propagates out of the wizard call so
the application can stop the configuration session.

<a id="tableio_cfg_json.wizard_ui_bridge.TableColumn"></a>

## TableColumn Objects

```python
@dataclass(frozen=True)
class TableColumn()
```

Header and editability for one whole column of a table question.

A table question describes its columns once. Read-only columns show
fixed text the user cannot edit, such as a column of parameter names.
Per-cell values and value constraints are described by TableCell.

**Attributes**:

- `header` - Column heading shown to the user.
- `read_only` - True when the whole column shows fixed text the user
  cannot edit.

<a id="tableio_cfg_json.wizard_ui_bridge.TableCell"></a>

## TableCell Objects

```python
@dataclass(frozen=True)
class TableCell()
```

Initial content and value constraints for one table cell.

A table question holds one TableCell per column in each row, so each
row of an editable column can offer its own finite value set. This
suits a table whose rows are different parameters that each accept
different values, such as the format-specific options of a config.

**Attributes**:

- `value` - The initial text shown in the cell. For a read-only column
  this is the fixed text. For an editable column it is the
  pre-filled value, or None for an empty cell.
- `choices` - The finite set of values this cell accepts, or None for
  free text. A graphical bridge can render choices as a
  drop-down.
- `nullable` - True when the user may leave the cell empty, which the
  table reports as None. False when an empty cell is not
  interpreted as None: with choices None an empty cell is
  an empty string the validation may or may not accept,
  and with choices given an empty editable cell is not yet
  a valid final value.

<a id="tableio_cfg_json.wizard_ui_bridge.WizardUiBridge"></a>

## WizardUiBridge Objects

```python
class WizardUiBridge()
```

Bridge between the wizard and the user interface.

This is an abstract base class for a bridge between the wizard and
the user interface. Provide concrete classes of this bridge to allow
the wizard to use a console text user interface or a graphical user
interface.

An application is responsible for implementing every public ask method
of its bridge, together with show(). At minimum a concrete bridge must
implement ask() and show(), which have no fallback. As a temporary
migration aid the base class implements ask_yes_no(), ask_choice(),
ask_multi() and ask_table() in terms of ask(), so a bridge that has
not yet overridden one of them keeps working while it is adjusted to
implement these methods directly. These fallbacks are temporary and
will be withdrawn once bridges implement them directly. Any ask
method may raise a WizardNavigation subclass to request back,
cancel-level or abort instead of returning an answer.

<a id="tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.ask"></a>

#### ask

```python
def ask(question: str,
        re_ask_reason: Optional[str] = None,
        choices: Optional[Sequence[str]] = None) -> str | int
```

Ask a question and return the user's answer.

**Arguments**:

- `question` - The question to ask the user.
- `re_ask_reason` - The reason for re-asking the question, for
  instance that the user's answer was invalid.
- `choices` - The choices to offer the user as a sequence of
  strings.
  

**Returns**:

  The user's answer. If the user's answer is one of the
  choices, then the return value can be either the matching
  string or the index of what the user selected. If integer
  index is used it is 0-based. The bridge is not required to
  validate the user's answer in any way. It is the
  responsibility of the caller to validate the user's answer.
  If the user entered/selected an empty string as answer, then
  the return value should be an empty string. The caller may
  interpret this as a request to use the default value.

**Raises**:

- `WizardBack` - The user asked to return to the previous question.
- `WizardCancelLevel` - The user cancelled the current level.
- `WizardAbort` - The user abandoned the whole configuration.

<a id="tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.ask_yes_no"></a>

#### ask\_yes\_no

```python
def ask_yes_no(question: str,
               default: bool,
               re_ask_reason: Optional[str] = None) -> bool
```

Ask a yes/no question and return the chosen boolean.

Yes/no questions are asked through this method, and the
application is responsible for implementing it with a real yes/no
interface, such as a pair of yes and no buttons in a graphical
bridge or a y/n prompt in a console bridge. As a temporary
migration aid the base class provides a fallback in terms of ask()
with the choices ('yes', 'no'), so a bridge that has not yet
overridden this method keeps working: an empty answer selects
default, an index or matching text selects the boolean, and any
other answer is re-asked.

**Arguments**:

- `question` - The yes/no question to ask.
- `default` - The value to use when the user makes no explicit
  choice.
- `re_ask_reason` - The reason for re-asking the question, for
  instance that the user's answer was invalid.
  

**Returns**:

  The user's choice as a boolean.

**Raises**:

- `WizardBack` - The user asked to return to the previous question.
- `WizardCancelLevel` - The user cancelled the current level.
- `WizardAbort` - The user abandoned the whole configuration.

<a id="tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.ask_choice"></a>

#### ask\_choice

```python
def ask_choice(question: str,
               *,
               choices: Sequence[str],
               default: Optional[str] = None,
               re_ask_reason: Optional[str] = None) -> str
```

Ask the user to pick exactly one of choices and return it.

The return value is always one of choices. An empty answer
selects default, so default must name one of choices; when
default is None an empty answer counts as no choice and the
question is re-asked.

The application is responsible for implementing this method with
a real single-choice control, such as a drop-down or a set of
radio buttons in a graphical bridge. As a temporary migration aid
the base class provides a fallback in terms of ask().

**Arguments**:

- `question` - The question to ask the user.
- `choices` - The choices to offer, in display order.
- `default` - The choice selected by an empty answer, or None to
  require an explicit choice.
- `re_ask_reason` - The reason for re-asking, shown before the
  first question when not None.
  

**Returns**:

  The chosen value, one of choices.

**Raises**:

- `WizardBack` - The user asked to return to the previous question.
- `WizardCancelLevel` - The user cancelled the current level.
- `WizardAbort` - The user abandoned the whole configuration.

<a id="tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.ask_multi"></a>

#### ask\_multi

```python
def ask_multi(question: str,
              *,
              choices: Sequence[str],
              default: Optional[Sequence[str]] = None,
              min_select: int = 0,
              max_select: Optional[int] = None,
              re_ask_reason: Optional[str] = None) -> list[str]
```

Ask the user to pick several of choices and return them.

The result holds the chosen values in the order of choices, with
a count between min_select and max_select; max_select None means
no upper bound. An empty answer selects default, or selects
nothing when default is None.

The application is responsible for implementing this method with
a real multi-selection control, such as a list of check boxes or
a multi-select list in a graphical bridge. As a temporary
migration aid the base class provides a fallback in terms of
ask() that reads one comma-separated answer of menu indexes or
names.

**Arguments**:

- `question` - The question to ask the user.
- `choices` - The choices to offer, in display order.
- `default` - The values pre-selected by an empty answer, or None.
- `min_select` - The smallest acceptable number of choices.
- `max_select` - The largest acceptable number of choices, or None
  for no upper bound.
- `re_ask_reason` - The reason for re-asking, shown before the
  first question when not None.
  

**Returns**:

  The chosen values, each one of choices, in choices order.

**Raises**:

- `WizardBack` - The user asked to return to the previous question.
- `WizardCancelLevel` - The user cancelled the current level.
- `WizardAbort` - The user abandoned the whole configuration.

<a id="tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.ask_table"></a>

#### ask\_table

```python
def ask_table(columns: Sequence[TableColumn],
              cells: list[list[TableCell]],
              question: str,
              *,
              re_ask_reason: Optional[str] = None,
              partial_check: Optional[PartialCheck] = None,
              min_rows: Optional[int] = None,
              max_rows: Optional[int] = None) -> list[list[Optional[str]]]
```

Ask the user to fill in a table and return its cells.

The bridge shows a table whose columns are described by columns
and whose rows start from cells. Each row in cells holds one
TableCell per column. Read-only columns show the fixed text in
each cell, such as a column of parameter names, while editable
columns show pre-filled or empty values the user may change.

The application is responsible for implementing this method with
a real table widget. As a temporary migration aid the base class
provides a fallback in terms of ask(), asking once per editable
cell and folding the read-only cells of the row into the prompt,
so a bridge that has not yet overridden this method keeps
working. The fallback only fills the rows given in cells, so it
ignores min_rows and max_rows and cannot add or remove rows. In
that fallback an empty answer keeps the cell's
current value and a reserved erase token empties the cell, which
is how a console user replaces a pre-filled default with an empty
cell.

How an empty editable cell is reported follows its TableCell: a
nullable cell reports None, a free-text cell reports an empty
string, and a cell with choices treats empty as not yet a valid
value.

When partial_check is given, the bridge calls it after the user
changes a cell, passing the whole table as it currently stands
and the (row, column) position of the changed cell, both 0-based.
The callback returns (accepted, message); the bridge uses message
to give early feedback. The callback must tolerate empty or partly
filled cells, and it gives advisory feedback only: the wizard
still validates the final table.

**Arguments**:

- `columns` - Description of each column, in left-to-right order.
- `cells` - Starting rows, each a list of one TableCell per column.
- `question` - The question or instruction shown above the table.
- `re_ask_reason` - The reason for re-asking, for instance that a
  value failed validation.
- `partial_check` - Optional callback for early per-cell feedback.
  It receives the current table and the changed
  (row, column) position and returns an accepted
  flag and a message.
- `min_rows` - Minimum number of rows the user must leave in the
  table, or None when rows are fixed to the rows in
  cells. A variable number of rows requires both
  min_rows and max_rows to be non-None.
- `max_rows` - Maximum number of rows the user may add the table
  to, or None when rows are fixed to the rows in
  cells. A variable number of rows requires both
  min_rows and max_rows to be non-None.
  

**Returns**:

  The complete table as rows of cells, including the read-only
  columns, with one cell per column in each row. Each cell is
  the final string the user left, or None for an empty cell.

**Raises**:

- `WizardBack` - The user asked to return to the previous question.
- `WizardCancelLevel` - The user cancelled the current level.
- `WizardAbort` - The user abandoned the whole configuration.

<a id="tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.error_file"></a>

#### error\_file

```python
def error_file() -> TextIO
```

Return the stream used for validation diagnostics.

<a id="tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.show"></a>

#### show

```python
def show(message: str) -> None
```

Show a message to the user.

If implementing a graphical user interface, this method should
display the message in a dialog or a message box. If implementing
a console text user interface, this method should print the
message to the console.

**Arguments**:

- `message` - The message to show the user.

<a id="tableio_cfg_json.wizard_ui_bridge_textual"></a>

# tableio\_cfg\_json.wizard\_ui\_bridge\_textual

Textual full-screen user interface bridge for the wizard.

This module provides the concrete Textual bridge used when the wizard
talks to a user through a real terminal. Each ask method runs a short
lived Textual application for one question and returns its result, which
keeps the one-question-at-a-time contract of WizardUiBridge while giving
the user a full-screen interface with selectable lists, check boxes and
editable tables.

Navigation keys exit a screen with no value and record which
WizardNavigation request to raise, so the bridge re-raises it after the
screen closes. Messages passed to show() and diagnostics written to
error_file() are buffered and rendered in the header of the next
screen, so nothing is written straight to the terminal where it would
corrupt the Textual display.

<a id="tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual"></a>

## WizardUiBridgeTextual Objects

```python
class WizardUiBridgeTextual(WizardUiBridge)
```

Bridge between the wizard and a Textual terminal interface.

Each ask method runs a short-lived Textual application for one
question and returns its result. Validation diagnostics written to
error_file() and messages passed to show() are buffered and rendered
in the header of the next question's screen, so nothing reaches the
terminal directly where it would corrupt the Textual display.

This bridge draws on the controlling terminal itself, so it takes no
streams. Use make_text_ui_bridge() to obtain this bridge when a
terminal is available and a console bridge otherwise.

<a id="tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual.__init__"></a>

#### \_\_init\_\_

```python
def __init__() -> None
```

Start with an empty diagnostics buffer and message list.

<a id="tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual.ask"></a>

#### ask

```python
def ask(question: str,
        re_ask_reason: Optional[str] = None,
        choices: Optional[Sequence[str]] = None) -> str | int
```

Ask one question; see WizardUiBridge.ask.

<a id="tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual.ask_yes_no"></a>

#### ask\_yes\_no

```python
def ask_yes_no(question: str,
               default: bool,
               re_ask_reason: Optional[str] = None) -> bool
```

Ask a yes/no question; see WizardUiBridge.ask_yes_no.

<a id="tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual.ask_choice"></a>

#### ask\_choice

```python
def ask_choice(question: str,
               *,
               choices: Sequence[str],
               default: Optional[str] = None,
               re_ask_reason: Optional[str] = None) -> str
```

Ask the user to pick one choice; see ask_choice.

<a id="tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual.ask_multi"></a>

#### ask\_multi

```python
def ask_multi(question: str,
              *,
              choices: Sequence[str],
              default: Optional[Sequence[str]] = None,
              min_select: int = 0,
              max_select: Optional[int] = None,
              re_ask_reason: Optional[str] = None) -> list[str]
```

Ask the user to pick several choices; see ask_multi.

<a id="tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual.ask_table"></a>

#### ask\_table

```python
def ask_table(columns: Sequence[TableColumn],
              cells: list[list[TableCell]],
              question: str,
              *,
              re_ask_reason: Optional[str] = None,
              partial_check: Optional[PartialCheck] = None,
              min_rows: Optional[int] = None,
              max_rows: Optional[int] = None) -> list[list[Optional[str]]]
```

Ask the user to fill a table; see WizardUiBridge.ask_table.

<a id="tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual.error_file"></a>

#### error\_file

```python
def error_file() -> StringIO
```

Return the in-memory stream shown on the next screen.

<a id="tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual.show"></a>

#### show

```python
def show(message: str) -> None
```

Buffer a message for the next question's screen.

A message shown when no further question follows is not
displayed, because only a Textual screen renders it.

<a id="tableio_cfg_json.wizard_ui_bridge_console"></a>

# tableio\_cfg\_json.wizard\_ui\_bridge\_console

Console text user interface bridge for the configuration wizard.

This module provides the concrete console bridge used when the wizard
talks to a user through plain text streams. It recognises reserved
navigation tokens so a console user can step back, cancel the current
level or abandon the whole configuration.

<a id="tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole"></a>

## WizardUiBridgeConsole Objects

```python
class WizardUiBridgeConsole(WizardUiBridge)
```

Bridge between the wizard and the console text user interface.

<a id="tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole.__init__"></a>

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

<a id="tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole.ask"></a>

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

**Raises**:

- `EOFError` - The input stream ended before an answer was read.
- `WizardBack` - The user asked to return to the previous question.
- `WizardCancelLevel` - The user cancelled the current level.
- `WizardAbort` - The user abandoned the whole configuration.

<a id="tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole.ask_choice"></a>

#### ask\_choice

```python
def ask_choice(question: str,
               *,
               choices: Sequence[str],
               default: Optional[str] = None,
               re_ask_reason: Optional[str] = None) -> str
```

Ask one choice on the console; see WizardUiBridge.ask_choice.

<a id="tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole.ask_multi"></a>

#### ask\_multi

```python
def ask_multi(question: str,
              *,
              choices: Sequence[str],
              default: Optional[Sequence[str]] = None,
              min_select: int = 0,
              max_select: Optional[int] = None,
              re_ask_reason: Optional[str] = None) -> list[str]
```

Ask several choices on the console; see WizardUiBridge.ask_multi.

<a id="tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole.error_file"></a>

#### error\_file

```python
def error_file() -> TextIO
```

Return the stream used for validation diagnostics.

<a id="tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole.show"></a>

#### show

```python
def show(message: str) -> None
```

Show a message to the user.

This method prints the message to the console.

**Arguments**:

- `message` - The message to show the user.

<a id="tableio_cfg_json.wizard"></a>

# tableio\_cfg\_json.wizard

Interactive helpers for creating TableIO JSON configuration.

The public helper in this module is intentionally scoped to one TableIO
endpoint. Application code can call it once for each input or output it wants
to configure, and then place the returned TioJsonConfig objects inside its own
larger config-as-json configuration class.

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

The user can navigate the questions of this one endpoint through the bridge
by asking to go back to the previous question or to cancel the current
level. Navigation that reaches past the first question of this endpoint is
raised out of this function so the application can navigate its own flow.

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
- `WizardBack` - The user asked to go back from the first question.
- `WizardCancelLevel` - The user cancelled this endpoint level.
- `WizardAbort` - The user abandoned the whole configuration.

**Returns**:

  A validated TableIO JSON config for the one endpoint.

<a id="tableio_cfg_json.wizard_ui_factory"></a>

# tableio\_cfg\_json.wizard\_ui\_factory

Factory selecting a text-mode user interface bridge.

The wizard talks to the user through a WizardUiBridge. This factory
returns a Textual full-screen bridge when Textual is installed and the
streams are a real terminal, and falls back to the console bridge
otherwise, such as when output is redirected, when running under tests,
or where Textual is not available. The fallback keeps the library
importable and usable even if Textual has been uninstalled.

This factory chooses between text-mode bridges only. An application
with a graphical user interface should provide and use its own
graphical bridge instead.

<a id="tableio_cfg_json.wizard_ui_factory.make_text_ui_bridge"></a>

#### make\_text\_ui\_bridge

```python
def make_text_ui_bridge(stdout_file: TextIO, stdin_file: TextIO,
                        stderr_file: TextIO) -> WizardUiBridge
```

Return a Textual bridge for a terminal, else a console bridge.

**Arguments**:

- `stdout_file` - Stream the console bridge prints to, also checked
  for being a terminal.
- `stdin_file` - Stream the console bridge reads from, also checked
  for being a terminal.
- `stderr_file` - Stream the console bridge prints errors to.
  

**Returns**:

  A Textual bridge when Textual is installed and both streams are
  a terminal, otherwise a console bridge.

