# Table of Contents

* [tableio\_cfg\_json.describe](#tableio_cfg_json.describe)
  * [get\_general\_cfg\_info](#tableio_cfg_json.describe.get_general_cfg_info)
  * [get\_config\_member\_names](#tableio_cfg_json.describe.get_config_member_names)
  * [describe\_config\_members](#tableio_cfg_json.describe.describe_config_members)
  * [describe\_config\_reference](#tableio_cfg_json.describe.describe_config_reference)
  * [describe\_config\_example](#tableio_cfg_json.describe.describe_config_example)
  * [describe\_config](#tableio_cfg_json.describe.describe_config)
* [tableio\_cfg\_json.spec\_text](#tableio_cfg_json.spec_text)
  * [CHOICES\_LABEL](#tableio_cfg_json.spec_text.CHOICES_LABEL)
  * [DEFAULT\_LABEL](#tableio_cfg_json.spec_text.DEFAULT_LABEL)
  * [FORMATS\_LABEL](#tableio_cfg_json.spec_text.FORMATS_LABEL)
  * [IMPLS\_LABEL](#tableio_cfg_json.spec_text.IMPLS_LABEL)
  * [value\_list](#tableio_cfg_json.spec_text.value_list)
  * [end\_sentence](#tableio_cfg_json.spec_text.end_sentence)
* [tableio\_cfg\_json.\_moved](#tableio_cfg_json._moved)
  * [STRICT\_ENV](#tableio_cfg_json._moved.STRICT_ENV)
  * [REMOVED\_IN](#tableio_cfg_json._moved.REMOVED_IN)
  * [MOVED\_NAMES](#tableio_cfg_json._moved.MOVED_NAMES)
  * [WizardUiBridgeMoved](#tableio_cfg_json._moved.WizardUiBridgeMoved)
  * [moved\_attr](#tableio_cfg_json._moved.moved_attr)
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
  * [tio\_json\_config\_wizard](#tableio_cfg_json.wizard.tio_json_config_wizard)
* [tableio\_cfg\_json.loader](#tableio_cfg_json.loader)
  * [NO\_FILE\_NAME](#tableio_cfg_json.loader.NO_FILE_NAME)
  * [tio\_json\_loader](#tableio_cfg_json.loader.tio_json_loader)
  * [tio\_json\_read\_loader](#tableio_cfg_json.loader.tio_json_read_loader)
  * [tio\_json\_create\_loader](#tableio_cfg_json.loader.tio_json_create_loader)
  * [tio\_json\_update\_loader](#tableio_cfg_json.loader.tio_json_update_loader)
* [tableio\_cfg\_json.descriptions](#tableio_cfg_json.descriptions)
  * [STRING\_TYPES](#tableio_cfg_json.descriptions.STRING_TYPES)
  * [SECTION\_TEXT](#tableio_cfg_json.descriptions.SECTION_TEXT)
  * [VALUE\_MEANINGS](#tableio_cfg_json.descriptions.VALUE_MEANINGS)
  * [EXTRA\_NOTES](#tableio_cfg_json.descriptions.EXTRA_NOTES)
  * [tio\_json\_descriptions](#tableio_cfg_json.descriptions.tio_json_descriptions)
  * [TIO\_JSON\_DESCRIPTIONS](#tableio_cfg_json.descriptions.TIO_JSON_DESCRIPTIONS)

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

<a id="tableio_cfg_json.spec_text"></a>

# tableio\_cfg\_json.spec\_text

Text fragments built from one TableIO configuration specification.

TableIO owns the metadata about its configuration members, and this package
turns that metadata into text in two places: the plain text guides of
describe.py and the editor descriptions of descriptions.py. The labels and
the small formatting rules are shared here so that one member reads the same
way whichever of the two a user meets it in.

<a id="tableio_cfg_json.spec_text.CHOICES_LABEL"></a>

#### CHOICES\_LABEL

Label of the list of values that one member accepts.

<a id="tableio_cfg_json.spec_text.DEFAULT_LABEL"></a>

#### DEFAULT\_LABEL

Label of what one member holds when nothing is stored for it.

<a id="tableio_cfg_json.spec_text.FORMATS_LABEL"></a>

#### FORMATS\_LABEL

Label of the formats that one member has an effect for.

<a id="tableio_cfg_json.spec_text.IMPLS_LABEL"></a>

#### IMPLS\_LABEL

Label of the implementations that one member has an effect for.

<a id="tableio_cfg_json.spec_text.value_list"></a>

#### value\_list

```python
def value_list(label: str, values: Optional[tuple[str, ...]]) -> Optional[str]
```

Return one labelled comma-separated value list.

**Arguments**:

- `label` - Label to prepend.
- `values` - Values to list. ``None`` and an empty tuple both mean that
  there is no restriction worth stating.

**Returns**:

  The labelled list as one sentence, or ``None`` when there is nothing
  to list.

<a id="tableio_cfg_json.spec_text.end_sentence"></a>

#### end\_sentence

```python
def end_sentence(text: str) -> str
```

Return text with sentence-ending punctuation.

**Arguments**:

- `text` - Text that may already end with punctuation.

**Returns**:

  Text ending with a sentence punctuation mark.

<a id="tableio_cfg_json._moved"></a>

# tableio\_cfg\_json.\_moved

Support for names that moved to the wizard_ui_bridge package.

The wizard user interface bridge used to be part of tableio_cfg_json.
It is now the separate package wizard_ui_bridge, which does not depend
on TableIO. The old names still work here, so applications keep
running, but each use warns so that maintainers know to change the
import.

The warning is a DeprecationWarning subclass, which Python hides from
end users by default while pytest and unittest show it by default. A
maintainer who wants the stale imports to fail instead of warn can set
the environment variable named by STRICT_ENV to any non-empty value.

<a id="tableio_cfg_json._moved.STRICT_ENV"></a>

#### STRICT\_ENV

Set this environment variable to make a moved name raise ImportError.

<a id="tableio_cfg_json._moved.REMOVED_IN"></a>

#### REMOVED\_IN

The release that removes the deprecated re-exports named here.

<a id="tableio_cfg_json._moved.MOVED_NAMES"></a>

#### MOVED\_NAMES

The wizard UI bridge names this package used to define itself.

<a id="tableio_cfg_json._moved.WizardUiBridgeMoved"></a>

## WizardUiBridgeMoved Objects

```python
class WizardUiBridgeMoved(DeprecationWarning)
```

Warns that a name moved to the wizard_ui_bridge package.

Being its own category lets a maintainer turn just these warnings
into errors, by running pytest with
`-W error::tableio_cfg_json.WizardUiBridgeMoved`. The interpreter's
own -W and PYTHONWARNINGS cannot name this category, because they
are resolved before this package can be imported; STRICT_ENV works
there instead.

<a id="tableio_cfg_json._moved.moved_attr"></a>

#### moved\_attr

```python
def moved_attr(old_module: str, new_module: str, name: str) -> object
```

Return name from new_module, warning that it moved there.

Dunder names are rejected without warning, so that attribute
lookups made by the interpreter and by tools do not import the new
module and do not warn.

**Arguments**:

- `old_module` - Deprecated module the name was looked up in.
- `new_module` - Module the name lives in now.
- `name` - Name that was looked up.
  

**Raises**:

- `AttributeError` - If name is a dunder name.
- `ImportError` - If strict mode is on, see STRICT_ENV.

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
             stderr_file: TextIO = sys.stderr,
             *,
             member_name: Optional[str] = None) -> None
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
- `member_name` - Path for reaching this section from the top
  level of the complete configuration, or ``None`` when this
  section is that top level and not a member of anything.

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
             stderr_file: TextIO = sys.stderr,
             *,
             member_name: Optional[str] = None) -> None
```

Create HTML settings or read them from a JSON source.

Constructor arguments provide defaults. If JSON text or a filename is
supplied, config-as-json applies the JSON values over those defaults.

**Arguments**:

- `css_file` - Optional CSS file path or URL.
- `from_json_data_text` - Optional JSON text to parse.
- `from_json_filename` - Optional JSON file to read.
- `stderr_file` - Stream receiving user-facing diagnostics.
- `member_name` - Path for reaching this section from the top
  level of the complete configuration, or ``None`` when this
  section is that top level and not a member of anything.

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
             stderr_file: TextIO = sys.stderr,
             *,
             member_name: Optional[str] = None) -> None
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
- `member_name` - Path for reaching this section from the top
  level of the complete configuration, or ``None`` when this
  section is that top level and not a member of anything.

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
             stderr_file: TextIO = sys.stderr,
             *,
             member_name: Optional[str] = None) -> None
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
- `member_name` - Path for reaching this configuration from the top
  level of a larger configuration, or ``None`` when this
  object is that top level and not a member of anything. An
  application nesting one endpoint per member names each of
  them, so that a diagnostic says which endpoint it is about.

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
def tio_json_config_default(
        capabilities: Capabilities,
        file_access: FileAccess,
        format_name: Optional[str] = None,
        implementation: Optional[str] = None,
        include_all_options: bool = False,
        stderr_file: TextIO = sys.stderr,
        *,
        member_name: Optional[str] = None) -> TioJsonConfig
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
- `member_name` - Path for reaching the returned configuration from the
  top level of a larger configuration, or ``None`` when it is that
  top level and not a member of anything.

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

<a id="tableio_cfg_json.wizard.tio_json_config_wizard"></a>

#### tio\_json\_config\_wizard

```python
def tio_json_config_wizard(capabilities: Capabilities,
                           file_access: FileAccess,
                           ui_bridge: WizardUiBridge,
                           *,
                           default: Optional[TioJsonConfig] = None,
                           backward: bool = False) -> TioJsonConfig
```

Interactively create one TableIO JSON endpoint configuration.

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

**Arguments**:

- `capabilities` - Capabilities needed by this application endpoint. Pass
  the capabilities for the one input or output being configured, not
  for the whole application.
- `file_access` - File access for this endpoint, such as READ for an input
  file or CREATE for an output file. This controls which formats and
  implementations can be offered.
- `ui_bridge` - Bridge between the wizard and the user interface.
- `default` - Default values to pre-fill the wizard. This can be what a
  configuration file already contains, what the user already
  answered before going back in an enclosing wizard, or what the
  application wants to suggest as a starting point.
- `backward` - When True, the wizard starts at the last question instead of
  the first. This will be set to True when the user asked to go back
  from a later question in an enclosing wizard.

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

<a id="tableio_cfg_json.loader"></a>

# tableio\_cfg\_json.loader

How a configuration editor constructs a TioJsonConfig.

An edit-cfg-json editor constructs the configuration class itself, from the
keyword arguments config-as-json documents. TioJsonConfig takes two more than
that: the runtime capabilities and the file access of the endpoint, which are
the application's and which nothing in a configuration file could supply. An
``edit_cfg_json.ConfigLoader`` is how an application says how its class is
built, and this module is that loader for TioJsonConfig.

The defaults TableIO recommends depend on the chosen format, so the format
and the implementation are read out of the JSON text before the defaults are
asked for. Without that, a file selecting CSV would be built on the defaults
of another format and refused for an implementation the user never wrote.

A ready-made loader is offered for each file access, for a program that needs
a name to point at rather than a call to make, which is what the ``--loader``
option of ``python3 -m edit_cfg_json.dump`` takes. There are three of them and
not one, because the file access is not in the configuration file and picking
the wrong one is not harmless: READ matches only the formats that can be read,
while CREATE matches every registered format, and the implementation that the
defaults fill in for one access is not the one the other access would choose.

<a id="tableio_cfg_json.loader.NO_FILE_NAME"></a>

#### NO\_FILE\_NAME

Message of the refusal of a file name given to this loader.

<a id="tableio_cfg_json.loader.tio_json_loader"></a>

#### tio\_json\_loader

```python
def tio_json_loader(capabilities: Capabilities,
                    file_access: FileAccess,
                    format_name: Optional[str] = None,
                    implementation: Optional[str] = None,
                    include_all_options: bool = True,
                    *,
                    member_name: Optional[str] = None) -> ConfigLoader
```

Get a loader that constructs a TioJsonConfig for a config editor.

Pass the result as the ``loader`` argument of ``edit_cfg_json.edit()``,
``editor_model()`` or ``load_config()``. An application that edits its own
configuration class needs no loader from here: it is the class holding the
TioJsonConfig members that the editor is given, and constructing that one
is the application's own to describe.

``include_all_options`` is what decides how much of a TableIO
configuration an editing session can reach. A configuration file normally
stores only the durable choices that have to be fixed, and an option that
is not in the file is not a row in the editor, so the default here is to
build on a complete set of defaults and let the editor mark every value
the file did not hold. The cost is that saving then writes all of them,
which turns a compact configuration file into a full one and fixes the
implementation that TableIO would otherwise choose at runtime. Pass False
to keep an edited file as compact as it was.

**Arguments**:

- `capabilities` - Runtime capabilities requested by the application.
- `file_access` - Runtime file access requested by the application.
- `format_name` - Optional preferred TableIO format name, used only when
  the edited JSON text does not select one.
- `implementation` - Optional preferred TableIO implementation name, used
  only when the edited JSON text does not select one.
- `include_all_options` - Whether the editor should offer every option as
  a row rather than only the options the file holds.
- `member_name` - Path for reaching the loaded configuration from the
  top level of a larger one, or ``None`` when it is that top level.
  An editor asks a loader for a whole configuration, so an editing
  session leaves this ``None``. It is here for an application that
  loads one nested endpoint itself, which the loader and not
  ``TioJsonConfig`` is the door to, because only a load decides
  whether the defaults may fill in what the text leaves out.

**Returns**:

  A loader for TioJsonConfig, satisfying ``edit_cfg_json.ConfigLoader``.

<a id="tableio_cfg_json.loader.tio_json_read_loader"></a>

#### tio\_json\_read\_loader

Ready-made loader for a configuration of an endpoint that is read.

<a id="tableio_cfg_json.loader.tio_json_create_loader"></a>

#### tio\_json\_create\_loader

Ready-made loader for a configuration of an endpoint that is written.

<a id="tableio_cfg_json.loader.tio_json_update_loader"></a>

#### tio\_json\_update\_loader

Ready-made loader for an endpoint that is both read and written.

The three ready-made loaders ask for no capability beyond the access itself,
so they match every backend that can do that access. An application that needs
more than that, or that wants an edited file to stay as compact as it was,
calls ``tio_json_loader()`` with what it needs.

<a id="tableio_cfg_json.descriptions"></a>

# tableio\_cfg\_json.descriptions

What the TableIO configuration members mean, for a configuration editor.

An application that hands its own configuration class to one of the
edit-cfg-json editors describes the members it declares in an
``edit_cfg_json.Descriptions`` mapping, because a member has no docstring at
runtime. The members that come from this package are this package's to
describe, so an application that nests a TioJsonConfig gets that text from
here instead of writing the TableIO configuration down a second time.

What the editor works out for itself is deliberately absent. It reads the
docstring of every configuration class, it says what kind of value each
member holds, it says which members may be left out of the file, and where a
member holds an enum it lists the names of that enum. What it never reads is
a validator, so the values a plain string member accepts are listed here, and
what those values mean is written here as well.

<a id="tableio_cfg_json.descriptions.STRING_TYPES"></a>

#### STRING\_TYPES

The member types whose accepted values the editor cannot work out.

A member that holds an enum is one the editor lists the names of itself,
because the parse converter of the configuration class names the enum class.
A member that holds a plain string has its values in a validator instead, and
a validator is what the editor never reads.

<a id="tableio_cfg_json.descriptions.SECTION_TEXT"></a>

#### SECTION\_TEXT

What is said about one optional format-specific section as a whole.

<a id="tableio_cfg_json.descriptions.VALUE_MEANINGS"></a>

#### VALUE\_MEANINGS

What each value of a member means, where the name does not say it.

Only the members whose values need explaining are here. A format name, an
implementation name and a paper size are listed without a sentence each,
because the name is the whole of what there is to say about it.

<a id="tableio_cfg_json.descriptions.EXTRA_NOTES"></a>

#### EXTRA\_NOTES

Rules between members that no single member validator can state.

<a id="tableio_cfg_json.descriptions.tio_json_descriptions"></a>

#### tio\_json\_descriptions

```python
def tio_json_descriptions(prefix: ConfigPath = ()) -> Descriptions
```

Get what each TioJsonConfig member means, for a config editor.

Pass the result to ``edit_cfg_json.edit()``, ``editor_model()`` or one of
the edit-cfg-json editor backends, so that a user editing a TableIO
configuration is told what the members are for. An application that
declares a TioJsonConfig as one member of its own configuration class
passes the path of that member as the prefix, because a description
addresses the whole path to the member it is about. An application with
several TableIO endpoints calls this once per endpoint and merges the
results.

The text follows the TableIO metadata, so it names the formats,
implementations and values that are registered when this is called.

**Arguments**:

- `prefix` - Path of the member holding the TioJsonConfig, which is
  ``('input',)`` for a member called ``input`` and ``()`` for a
  TioJsonConfig that is the whole configuration being edited.

**Returns**:

  What each member of a TioJsonConfig and of its optional ``csv``,
  ``html`` and ``latex`` sections means, under the absolute path of
  that member.

<a id="tableio_cfg_json.descriptions.TIO_JSON_DESCRIPTIONS"></a>

#### TIO\_JSON\_DESCRIPTIONS

What each member means, for a TioJsonConfig that is the whole config.

This is the value of ``tio_json_descriptions()`` as the formats and
implementations were registered when this module was imported, offered as a
constant for a program that needs a name to point at rather than a call to
make. An application that registers a TableIO format of its own after
importing this module calls ``tio_json_descriptions()`` instead.

