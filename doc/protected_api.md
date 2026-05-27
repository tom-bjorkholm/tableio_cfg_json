# Table of Contents

* [tableio\_cfg\_json.describe](#tableio_cfg_json.describe)
  * [\_DescriptionContext](#tableio_cfg_json.describe._DescriptionContext)
  * [\_wrapped](#tableio_cfg_json.describe._wrapped)
  * [\_add\_wrapped](#tableio_cfg_json.describe._add_wrapped)
  * [\_paragraph](#tableio_cfg_json.describe._paragraph)
  * [\_matching\_caps](#tableio_cfg_json.describe._matching_caps)
  * [\_format\_names](#tableio_cfg_json.describe._format_names)
  * [\_impls\_by\_format](#tableio_cfg_json.describe._impls_by_format)
  * [\_filtered\_impls](#tableio_cfg_json.describe._filtered_impls)
  * [\_unique\_impls](#tableio_cfg_json.describe._unique_impls)
  * [\_overlaps](#tableio_cfg_json.describe._overlaps)
  * [\_spec\_matches](#tableio_cfg_json.describe._spec_matches)
  * [\_relevant\_specs](#tableio_cfg_json.describe._relevant_specs)
  * [\_description\_context](#tableio_cfg_json.describe._description_context)
  * [\_member\_choices](#tableio_cfg_json.describe._member_choices)
  * [\_filtered](#tableio_cfg_json.describe._filtered)
  * [\_add\_value\_list](#tableio_cfg_json.describe._add_value_list)
  * [\_end\_sentence](#tableio_cfg_json.describe._end_sentence)
  * [\_add\_member](#tableio_cfg_json.describe._add_member)
  * [\_add\_ref\_member](#tableio_cfg_json.describe._add_ref_member)
  * [\_reference\_specs](#tableio_cfg_json.describe._reference_specs)
  * [\_uses\_read\_caps](#tableio_cfg_json.describe._uses_read_caps)
  * [\_uses\_write\_caps](#tableio_cfg_json.describe._uses_write_caps)
  * [\_example\_accesses](#tableio_cfg_json.describe._example_accesses)
  * [\_example\_text](#tableio_cfg_json.describe._example_text)
  * [\_add\_example](#tableio_cfg_json.describe._add_example)
  * [get\_general\_cfg\_info](#tableio_cfg_json.describe.get_general_cfg_info)
  * [get\_config\_member\_names](#tableio_cfg_json.describe.get_config_member_names)
  * [describe\_config\_members](#tableio_cfg_json.describe.describe_config_members)
  * [describe\_config\_reference](#tableio_cfg_json.describe.describe_config_reference)
  * [describe\_config\_example](#tableio_cfg_json.describe.describe_config_example)
  * [describe\_config](#tableio_cfg_json.describe.describe_config)
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
* [tableio\_cfg\_json.wizard](#tableio_cfg_json.wizard)
  * [tio\_json\_config\_wizard](#tableio_cfg_json.wizard.tio_json_config_wizard)
  * [\_ask\_format](#tableio_cfg_json.wizard._ask_format)
  * [\_impl\_names](#tableio_cfg_json.wizard._impl_names)
  * [\_ask\_implementation](#tableio_cfg_json.wizard._ask_implementation)
  * [\_start\_data](#tableio_cfg_json.wizard._start_data)
  * [\_ask\_member](#tableio_cfg_json.wizard._ask_member)
  * [\_matches](#tableio_cfg_json.wizard._matches)
  * [\_ask\_config\_member](#tableio_cfg_json.wizard._ask_config_member)
  * [\_ask\_member\_value](#tableio_cfg_json.wizard._ask_member_value)
  * [\_parse\_member\_value](#tableio_cfg_json.wizard._parse_member_value)
  * [\_print\_member\_prompt](#tableio_cfg_json.wizard._print_member_prompt)
  * [\_ask\_menu](#tableio_cfg_json.wizard._ask_menu)
  * [\_read\_answer](#tableio_cfg_json.wizard._read_answer)
  * [\_set\_json\_member](#tableio_cfg_json.wizard._set_json_member)
  * [\_config\_from\_data](#tableio_cfg_json.wizard._config_from_data)

<a id="tableio_cfg_json.describe"></a>

# tableio\_cfg\_json.describe

Describe the configuration file format of tableio-cfg-json.

<a id="tableio_cfg_json.describe._DescriptionContext"></a>

## \_DescriptionContext Objects

```python
class _DescriptionContext(NamedTuple)
```

Matched TableIO metadata used by description helpers.

<a id="tableio_cfg_json.describe._wrapped"></a>

#### \_wrapped

```python
def _wrapped(text: str,
             initial: str = '',
             subsequent: Optional[str] = None) -> list[str]
```

Return text wrapped to the module line width.

**Arguments**:

- `text` - Text to wrap.
- `initial` - Prefix for the first returned line.
- `subsequent` - Prefix for following returned lines.

**Returns**:

  Wrapped lines.

<a id="tableio_cfg_json.describe._add_wrapped"></a>

#### \_add\_wrapped

```python
def _add_wrapped(lines: list[str],
                 text: str,
                 initial: str = '',
                 subsequent: Optional[str] = None) -> None
```

Append wrapped text to a line list.

**Arguments**:

- `lines` - Lines to extend.
- `text` - Text to wrap and append.
- `initial` - Prefix for the first appended line.
- `subsequent` - Prefix for following appended lines.

**Returns**:

  None.

<a id="tableio_cfg_json.describe._paragraph"></a>

#### \_paragraph

```python
def _paragraph(text: str) -> str
```

Return one wrapped paragraph.

**Arguments**:

- `text` - Paragraph text to wrap.

**Returns**:

  A wrapped paragraph string.

<a id="tableio_cfg_json.describe._matching_caps"></a>

#### \_matching\_caps

```python
def _matching_caps(
        capabilities: Optional[Capabilities],
        file_access: Optional[FileAccess]) -> Optional[Capabilities]
```

Return capabilities used for backend filtering.

**Arguments**:

- `capabilities` - Application capability requirements.
- `file_access` - Optional file access that adds read/write requirements.

**Returns**:

  Capabilities with access requirements added, or None when no filter
  was supplied.

<a id="tableio_cfg_json.describe._format_names"></a>

#### \_format\_names

```python
def _format_names(match_caps: Optional[Capabilities],
                  format_name: Optional[str]) -> list[str]
```

Return matching format names with TableIO casing.

**Arguments**:

- `match_caps` - Capabilities used for TableIO filtering.
- `format_name` - Optional requested format name.

**Raises**:

- `TableIOFactoryNoCapabilityMatch` - The requested filters match no
  registered format.

**Returns**:

  Matching format names.

<a id="tableio_cfg_json.describe._impls_by_format"></a>

#### \_impls\_by\_format

```python
def _impls_by_format(
        format_names: list[str],
        match_caps: Optional[Capabilities]) -> dict[str, list[str]]
```

Return matching implementation names keyed by format.

**Arguments**:

- `format_names` - Matching format names.
- `match_caps` - Capabilities used for TableIO filtering.

**Returns**:

  Matching implementation names for each format.

<a id="tableio_cfg_json.describe._filtered_impls"></a>

#### \_filtered\_impls

```python
def _filtered_impls(impls_by_fmt: dict[str, list[str]],
                    implementation: Optional[str]) -> dict[str, list[str]]
```

Return implementations limited to one requested implementation.

**Arguments**:

- `impls_by_fmt` - Matching implementation names keyed by format.
- `implementation` - Optional requested implementation name.

**Raises**:

- `TableIOFactoryNoCapabilityMatch` - No matching implementation exists.

**Returns**:

  Implementation names keyed by matching format.

<a id="tableio_cfg_json.describe._unique_impls"></a>

#### \_unique\_impls

```python
def _unique_impls(impls_by_fmt: dict[str, list[str]]) -> list[str]
```

Return implementation names without duplicates.

**Arguments**:

- `impls_by_fmt` - Implementation names keyed by format.

**Returns**:

  Implementation names in first-seen order.

<a id="tableio_cfg_json.describe._overlaps"></a>

#### \_overlaps

```python
def _overlaps(values: Optional[tuple[str, ...]], choices: list[str]) -> bool
```

Return whether optional metadata values overlap choices.

**Arguments**:

- `values` - Optional metadata values from TableIO.
- `choices` - Matching choices from the current request.

**Returns**:

  True when no metadata restriction exists or at least one choice
  overlaps.

<a id="tableio_cfg_json.describe._spec_matches"></a>

#### \_spec\_matches

```python
def _spec_matches(spec: ConfigSpec, format_names: list[str],
                  impl_names: list[str]) -> bool
```

Return whether a TableIO config spec is relevant.

**Arguments**:

- `spec` - TableIO configuration specification.
- `format_names` - Matching format names.
- `impl_names` - Matching implementation names.

**Returns**:

  True when the spec can affect at least one matching backend.

<a id="tableio_cfg_json.describe._relevant_specs"></a>

#### \_relevant\_specs

```python
def _relevant_specs(format_names: list[str],
                    impls_by_fmt: dict[str, list[str]]) -> list[ConfigSpec]
```

Return TableIO specs relevant to the matching backends.

**Arguments**:

- `format_names` - Matching format names.
- `impls_by_fmt` - Matching implementation names keyed by format.

**Returns**:

  Relevant specs in TableIO metadata order.

<a id="tableio_cfg_json.describe._description_context"></a>

#### \_description\_context

```python
def _description_context(capabilities: Optional[Capabilities],
                         file_access: Optional[FileAccess],
                         format_name: Optional[str],
                         implementation: Optional[str]) -> _DescriptionContext
```

Return matched TableIO metadata for one endpoint description.

**Arguments**:

- `capabilities` - Application capability requirements.
- `file_access` - Optional file access that adds read/write requirements.
- `format_name` - Optional requested format name.
- `implementation` - Optional requested implementation name.

**Raises**:

- `TableIOFactoryNoCapabilityMatch` - The requested filters match no
  registered format or implementation.

**Returns**:

  Matched metadata shared by the public description helpers.

<a id="tableio_cfg_json.describe._member_choices"></a>

#### \_member\_choices

```python
def _member_choices(spec: ConfigSpec, format_names: list[str],
                    impl_names: list[str]) -> Optional[tuple[str, ...]]
```

Return filtered choice values for one member.

**Arguments**:

- `spec` - TableIO configuration specification.
- `format_names` - Matching format names.
- `impl_names` - Matching implementation names.

**Returns**:

  Choice values for the member, or None when it has no finite choices.

<a id="tableio_cfg_json.describe._filtered"></a>

#### \_filtered

```python
def _filtered(values: Optional[tuple[str, ...]],
              choices: list[str]) -> Optional[tuple[str, ...]]
```

Return values filtered to matching choices.

**Arguments**:

- `values` - Optional metadata values from TableIO.
- `choices` - Matching choices from the current request.

**Returns**:

  Matching metadata values, or None when no metadata restriction exists.

<a id="tableio_cfg_json.describe._add_value_list"></a>

#### \_add\_value\_list

```python
def _add_value_list(lines: list[str], label: str,
                    values: Optional[tuple[str, ...]]) -> None
```

Append a labelled comma-separated value list when present.

**Arguments**:

- `lines` - Lines to extend.
- `label` - Label to prepend.
- `values` - Values to show.

**Returns**:

  None.

<a id="tableio_cfg_json.describe._end_sentence"></a>

#### \_end\_sentence

```python
def _end_sentence(text: str) -> str
```

Return text with sentence-ending punctuation.

**Arguments**:

- `text` - Text that may already end with punctuation.

**Returns**:

  Text ending with a sentence punctuation mark.

<a id="tableio_cfg_json.describe._add_member"></a>

#### \_add\_member

```python
def _add_member(lines: list[str], spec: ConfigSpec, format_names: list[str],
                impl_names: list[str]) -> None
```

Append documentation for one configuration member.

**Arguments**:

- `lines` - Lines to extend.
- `spec` - TableIO configuration specification.
- `format_names` - Matching format names.
- `impl_names` - Matching implementation names.

**Returns**:

  None.

<a id="tableio_cfg_json.describe._add_ref_member"></a>

#### \_add\_ref\_member

```python
def _add_ref_member(lines: list[str], spec: ConfigSpec) -> None
```

Append unfiltered documentation for one configuration member.

**Arguments**:

- `lines` - Lines to extend.
- `spec` - TableIO configuration specification.

**Returns**:

  None.

<a id="tableio_cfg_json.describe._reference_specs"></a>

#### \_reference\_specs

```python
def _reference_specs(
        member_names: Optional[Sequence[str]]) -> list[ConfigSpec]
```

Return specs selected for a one-time member reference.

**Arguments**:

- `member_names` - Optional member names to describe. None means all
  known members.

**Raises**:

- `KeyError` - A requested member name is unknown.

**Returns**:

  Selected specs in TableIO metadata order.

<a id="tableio_cfg_json.describe._uses_read_caps"></a>

#### \_uses\_read\_caps

```python
def _uses_read_caps(capabilities: Capabilities) -> bool
```

Return whether capabilities imply a read-oriented example.

**Arguments**:

- `capabilities` - Application capability requirements.

**Returns**:

  True when the capabilities request reading behavior.

<a id="tableio_cfg_json.describe._uses_write_caps"></a>

#### \_uses\_write\_caps

```python
def _uses_write_caps(capabilities: Capabilities) -> bool
```

Return whether capabilities imply a write-oriented example.

**Arguments**:

- `capabilities` - Application capability requirements.

**Returns**:

  True when the capabilities request writing behavior.

<a id="tableio_cfg_json.describe._example_accesses"></a>

#### \_example\_accesses

```python
def _example_accesses(capabilities: Capabilities,
                      file_access: Optional[FileAccess]) -> list[FileAccess]
```

Return file accesses to try for example generation.

**Arguments**:

- `capabilities` - Application capability requirements.
- `file_access` - Optional file access supplied by the caller.

**Returns**:

  Candidate file accesses in preference order.

<a id="tableio_cfg_json.describe._example_text"></a>

#### \_example\_text

```python
def _example_text(capabilities: Optional[Capabilities],
                  file_access: Optional[FileAccess],
                  format_name: Optional[str], implementation: Optional[str],
                  include_all_options: bool) -> tuple[FileAccess, str]
```

Return one example JSON document and the access used for it.

**Arguments**:

- `capabilities` - Application capability requirements.
- `file_access` - Optional file access supplied by the caller.
- `format_name` - Optional requested format name.
- `implementation` - Optional requested implementation name.
- `include_all_options` - Whether all options should be visible.

**Raises**:

- `TableIOFactoryNoCapabilityMatch` - No default example can be selected.

**Returns**:

  The file access and JSON document selected by TableIO defaults.

<a id="tableio_cfg_json.describe._add_example"></a>

#### \_add\_example

```python
def _add_example(lines: list[str], title: str, example: tuple[FileAccess,
                                                              str]) -> None
```

Append one JSON example.

**Arguments**:

- `lines` - Lines to extend.
- `title` - Example title.
- `example` - File access and JSON document to append.

**Returns**:

  None.

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
                           stdin_file: TextIO = sys.stdin,
                           stdout_file: TextIO = sys.stdout,
                           stderr_file: TextIO = sys.stderr) -> TioJsonConfig
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
- `stdin_file` - Stream to read user answers from. Tests can pass a
  StringIO with scripted answers.
- `stdout_file` - Stream receiving prompts and retry messages.
- `stderr_file` - Stream receiving validation diagnostics from TableIO and
  config-as-json.

**Raises**:

- `EOFError` - Scripted input ends before all required answers are read.
- `TableIOFactoryNoCapabilityMatch` - No registered backend matches the
  supplied capabilities and file access.
- `InvalidConfiguration` - The selected values fail final validation.

**Returns**:

  A validated TableIO JSON config for the one endpoint.

<a id="tableio_cfg_json.wizard._ask_format"></a>

#### \_ask\_format

```python
def _ask_format(capabilities: Capabilities, stdin_file: TextIO,
                stdout_file: TextIO) -> str
```

Ask the user to select one format that matches the endpoint.

<a id="tableio_cfg_json.wizard._impl_names"></a>

#### \_impl\_names

```python
def _impl_names(format_name: str,
                capabilities: Capabilities) -> tuple[str, ...]
```

Return matching implementations for the selected format.

<a id="tableio_cfg_json.wizard._ask_implementation"></a>

#### \_ask\_implementation

```python
def _ask_implementation(impl_names: Sequence[str], stdin_file: TextIO,
                        stdout_file: TextIO) -> Optional[str]
```

Ask for an implementation only when TableIO exposes a choice.

<a id="tableio_cfg_json.wizard._start_data"></a>

#### \_start\_data

```python
def _start_data(format_name: str,
                implementation: Optional[str]) -> dict[str, object]
```

Create the first JSON object used by the wizard.

<a id="tableio_cfg_json.wizard._ask_member"></a>

#### \_ask\_member

```python
def _ask_member(spec: ConfigSpec, format_name: str,
                impl_names: Sequence[str]) -> bool
```

Return True when the wizard should ask for this config member.

<a id="tableio_cfg_json.wizard._matches"></a>

#### \_matches

```python
def _matches(spec_values: Optional[Sequence[str]],
             wanted_values: Sequence[str]) -> bool
```

Return True when metadata values overlap or are unrestricted.

<a id="tableio_cfg_json.wizard._ask_config_member"></a>

#### \_ask\_config\_member

```python
def _ask_config_member(spec: ConfigSpec, data: dict[str, object],
                       caps: Capabilities, file_access: FileAccess,
                       stdin_file: TextIO, stdout_file: TextIO,
                       stderr_file: TextIO) -> None
```

Ask for one optional member and keep retrying until it validates.

<a id="tableio_cfg_json.wizard._ask_member_value"></a>

#### \_ask\_member\_value

```python
def _ask_member_value(spec: ConfigSpec, stdin_file: TextIO,
                      stdout_file: TextIO) -> Optional[object]
```

Ask for one optional value and convert simple scalar types.

<a id="tableio_cfg_json.wizard._parse_member_value"></a>

#### \_parse\_member\_value

```python
def _parse_member_value(spec: ConfigSpec, answer: str) -> object
```

Convert a free-text answer to the type expected by TableIO.

<a id="tableio_cfg_json.wizard._print_member_prompt"></a>

#### \_print\_member\_prompt

```python
def _print_member_prompt(spec: ConfigSpec, stdout_file: TextIO) -> None
```

Print the explanatory prompt for one free-text member.

<a id="tableio_cfg_json.wizard._ask_menu"></a>

#### \_ask\_menu

```python
def _ask_menu(title: str, choices: Sequence[str], allow_blank: bool,
              blank_text: str, stdin_file: TextIO, stdout_file: TextIO) -> str
```

Ask for a numbered menu choice and reject unknown answers.

<a id="tableio_cfg_json.wizard._read_answer"></a>

#### \_read\_answer

```python
def _read_answer(prompt_name: str, stdin_file: TextIO,
                 stdout_file: TextIO) -> str
```

Read one line and fail clearly if scripted input ends too early.

<a id="tableio_cfg_json.wizard._set_json_member"></a>

#### \_set\_json\_member

```python
def _set_json_member(data: dict[str, object], member_name: str,
                     value: object) -> None
```

Set a top-level or dotted member in the JSON data being built.

<a id="tableio_cfg_json.wizard._config_from_data"></a>

#### \_config\_from\_data

```python
def _config_from_data(data: dict[str, object], capabilities: Capabilities,
                      file_access: FileAccess,
                      stderr_file: TextIO) -> TioJsonConfig
```

Validate JSON data and return it as a TableIO JSON config.

