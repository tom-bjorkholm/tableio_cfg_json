# Table of Contents

* [tableio\_cfg\_json](#tableio_cfg_json)
  * [\_\_getattr\_\_](#tableio_cfg_json.__getattr__)
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
  * [\_add\_default](#tableio_cfg_json.describe._add_default)
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
* [tableio\_cfg\_json.wizard\_ui\_bridge](#tableio_cfg_json.wizard_ui_bridge)
  * [\_\_getattr\_\_](#tableio_cfg_json.wizard_ui_bridge.__getattr__)
* [tableio\_cfg\_json.wizard\_ui\_bridge\_textual](#tableio_cfg_json.wizard_ui_bridge_textual)
  * [\_\_getattr\_\_](#tableio_cfg_json.wizard_ui_bridge_textual.__getattr__)
* [tableio\_cfg\_json.wizard\_ui\_bridge\_console](#tableio_cfg_json.wizard_ui_bridge_console)
  * [\_\_getattr\_\_](#tableio_cfg_json.wizard_ui_bridge_console.__getattr__)
* [tableio\_cfg\_json.wizard\_ui\_bridge\_arg\_types](#tableio_cfg_json.wizard_ui_bridge_arg_types)
  * [\_\_getattr\_\_](#tableio_cfg_json.wizard_ui_bridge_arg_types.__getattr__)
* [tableio\_cfg\_json.wizard](#tableio_cfg_json.wizard)
  * [\_WizardRun](#tableio_cfg_json.wizard._WizardRun)
  * [\_Step](#tableio_cfg_json.wizard._Step)
  * [tio\_json\_config\_wizard](#tableio_cfg_json.wizard.tio_json_config_wizard)
  * [\_default\_data](#tableio_cfg_json.wizard._default_data)
  * [\_drive](#tableio_cfg_json.wizard._drive)
  * [\_start\_index](#tableio_cfg_json.wizard._start_index)
  * [\_build\_steps](#tableio_cfg_json.wizard._build_steps)
  * [\_relevant\_specs](#tableio_cfg_json.wizard._relevant_specs)
  * [\_run\_step](#tableio_cfg_json.wizard._run_step)
  * [\_run\_format\_step](#tableio_cfg_json.wizard._run_format_step)
  * [\_run\_impl\_step](#tableio_cfg_json.wizard._run_impl_step)
  * [\_clear\_after\_format](#tableio_cfg_json.wizard._clear_after_format)
  * [\_run\_options\_step](#tableio_cfg_json.wizard._run_options_step)
  * [\_options\_question](#tableio_cfg_json.wizard._options_question)
  * [\_apply\_options](#tableio_cfg_json.wizard._apply_options)
  * [\_options\_validator](#tableio_cfg_json.wizard._options_validator)
  * [\_current\_values](#tableio_cfg_json.wizard._current_values)
  * [\_answer\_values](#tableio_cfg_json.wizard._answer_values)
  * [\_answer\_value](#tableio_cfg_json.wizard._answer_value)
  * [\_option\_fields](#tableio_cfg_json.wizard._option_fields)
  * [\_option\_field](#tableio_cfg_json.wizard._option_field)
  * [\_choice\_field](#tableio_cfg_json.wizard._choice_field)
  * [\_int\_default](#tableio_cfg_json.wizard._int_default)
  * [\_text\_default](#tableio_cfg_json.wizard._text_default)
  * [\_spec\_choices](#tableio_cfg_json.wizard._spec_choices)
  * [\_data\_from\_values](#tableio_cfg_json.wizard._data_from_values)
  * [\_resolve\_member\_value](#tableio_cfg_json.wizard._resolve_member_value)
  * [\_commit](#tableio_cfg_json.wizard._commit)
  * [\_ask\_format](#tableio_cfg_json.wizard._ask_format)
  * [\_impl\_names](#tableio_cfg_json.wizard._impl_names)
  * [\_ask\_implementation](#tableio_cfg_json.wizard._ask_implementation)
  * [\_ask\_member](#tableio_cfg_json.wizard._ask_member)
  * [\_matches](#tableio_cfg_json.wizard._matches)
  * [\_parse\_member\_value](#tableio_cfg_json.wizard._parse_member_value)
  * [\_member\_default](#tableio_cfg_json.wizard._member_default)
  * [\_set\_json\_member](#tableio_cfg_json.wizard._set_json_member)
  * [\_get\_json\_member](#tableio_cfg_json.wizard._get_json_member)
  * [\_config\_from\_data](#tableio_cfg_json.wizard._config_from_data)
* [tableio\_cfg\_json.loader](#tableio_cfg_json.loader)
  * [NO\_FILE\_NAME](#tableio_cfg_json.loader.NO_FILE_NAME)
  * [\_json\_member](#tableio_cfg_json.loader._json_member)
  * [tio\_json\_loader](#tableio_cfg_json.loader.tio_json_loader)
  * [tio\_json\_read\_loader](#tableio_cfg_json.loader.tio_json_read_loader)
  * [tio\_json\_create\_loader](#tableio_cfg_json.loader.tio_json_create_loader)
  * [tio\_json\_update\_loader](#tableio_cfg_json.loader.tio_json_update_loader)
* [tableio\_cfg\_json.wizard\_ui\_bridge\_table](#tableio_cfg_json.wizard_ui_bridge_table)
  * [\_\_getattr\_\_](#tableio_cfg_json.wizard_ui_bridge_table.__getattr__)
* [tableio\_cfg\_json.wizard\_ui\_bridge\_form\_defs](#tableio_cfg_json.wizard_ui_bridge_form_defs)
  * [\_\_getattr\_\_](#tableio_cfg_json.wizard_ui_bridge_form_defs.__getattr__)
* [tableio\_cfg\_json.wizard\_ui\_factory](#tableio_cfg_json.wizard_ui_factory)
  * [\_\_getattr\_\_](#tableio_cfg_json.wizard_ui_factory.__getattr__)
* [tableio\_cfg\_json.descriptions](#tableio_cfg_json.descriptions)
  * [STRING\_TYPES](#tableio_cfg_json.descriptions.STRING_TYPES)
  * [SECTION\_TEXT](#tableio_cfg_json.descriptions.SECTION_TEXT)
  * [VALUE\_MEANINGS](#tableio_cfg_json.descriptions.VALUE_MEANINGS)
  * [EXTRA\_NOTES](#tableio_cfg_json.descriptions.EXTRA_NOTES)
  * [\_choice\_lines](#tableio_cfg_json.descriptions._choice_lines)
  * [\_member\_lines](#tableio_cfg_json.descriptions._member_lines)
  * [\_relevance\_lines](#tableio_cfg_json.descriptions._relevance_lines)
  * [\_section\_formats](#tableio_cfg_json.descriptions._section_formats)
  * [\_section\_lines](#tableio_cfg_json.descriptions._section_lines)
  * [\_described](#tableio_cfg_json.descriptions._described)
  * [tio\_json\_descriptions](#tableio_cfg_json.descriptions.tio_json_descriptions)
  * [TIO\_JSON\_DESCRIPTIONS](#tableio_cfg_json.descriptions.TIO_JSON_DESCRIPTIONS)

<a id="tableio_cfg_json"></a>

# tableio\_cfg\_json

Public API for the tableio config-as-json bridge.

The wizard user interface bridge that used to be part of this package
is now the separate package wizard_ui_bridge, which does not depend on
TableIO. Its names are still available from here, deprecated, so that
applications keep working while their maintainers change the imports.
See tableio_cfg_json._moved for how the deprecation is reported.

<a id="tableio_cfg_json.__getattr__"></a>

#### \_\_getattr\_\_

```python
def __getattr__(name: str) -> object
```

Return a moved wizard UI bridge name, warning that it moved.

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

<a id="tableio_cfg_json.describe._add_default"></a>

#### \_add\_default

```python
def _add_default(lines: list[str], spec: ConfigSpec) -> None
```

Append the default of one member when the metadata states one.

**Arguments**:

- `lines` - Lines to extend.
- `spec` - TableIO configuration specification.

**Returns**:

  None.

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

<a id="tableio_cfg_json.wizard_ui_bridge"></a>

# tableio\_cfg\_json.wizard\_ui\_bridge

Deprecated location of the WizardUiBridge base class.

This module moved to wizard_ui_bridge.bridge. Importing from here still
works and warns, see tableio_cfg_json._moved for how to make it fail
instead.

<a id="tableio_cfg_json.wizard_ui_bridge.__getattr__"></a>

#### \_\_getattr\_\_

```python
def __getattr__(name: str) -> object
```

Return name from its new module, warning that it moved.

<a id="tableio_cfg_json.wizard_ui_bridge_textual"></a>

# tableio\_cfg\_json.wizard\_ui\_bridge\_textual

Deprecated location of the Textual wizard UI bridge.

This module moved to wizard_ui_bridge.textual_bridge. Importing from here still
works and warns, see tableio_cfg_json._moved for how to make it fail
instead.

<a id="tableio_cfg_json.wizard_ui_bridge_textual.__getattr__"></a>

#### \_\_getattr\_\_

```python
def __getattr__(name: str) -> object
```

Return name from its new module, warning that it moved.

<a id="tableio_cfg_json.wizard_ui_bridge_console"></a>

# tableio\_cfg\_json.wizard\_ui\_bridge\_console

Deprecated location of the console wizard UI bridge.

This module moved to wizard_ui_bridge.console. Importing from here still
works and warns, see tableio_cfg_json._moved for how to make it fail
instead.

<a id="tableio_cfg_json.wizard_ui_bridge_console.__getattr__"></a>

#### \_\_getattr\_\_

```python
def __getattr__(name: str) -> object
```

Return name from its new module, warning that it moved.

<a id="tableio_cfg_json.wizard_ui_bridge_arg_types"></a>

# tableio\_cfg\_json.wizard\_ui\_bridge\_arg\_types

Deprecated location of the wizard UI bridge argument types.

This module moved to wizard_ui_bridge.arg_types. Importing from here still
works and warns, see tableio_cfg_json._moved for how to make it fail
instead.

<a id="tableio_cfg_json.wizard_ui_bridge_arg_types.__getattr__"></a>

#### \_\_getattr\_\_

```python
def __getattr__(name: str) -> object
```

Return name from its new module, warning that it moved.

<a id="tableio_cfg_json.wizard"></a>

# tableio\_cfg\_json.wizard

Interactive helpers for creating TableIO JSON configuration.

The public helper in this module is intentionally scoped to one TableIO
endpoint. Application code can call it once for each input or output it wants
to configure, and then place the returned TioJsonConfig objects inside its own
larger config-as-json configuration class.

<a id="tableio_cfg_json.wizard._WizardRun"></a>

## \_WizardRun Objects

```python
@dataclass
class _WizardRun()
```

Mutable state shared by the steps of one wizard run.

<a id="tableio_cfg_json.wizard._Step"></a>

## \_Step Objects

```python
@dataclass(frozen=True)
class _Step()
```

One navigable question or grouped option form in a wizard run.

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

<a id="tableio_cfg_json.wizard._default_data"></a>

#### \_default\_data

```python
def _default_data(default: Optional[TioJsonConfig],
                  stderr_file: TextIO) -> dict[str, object]
```

Return compact JSON data copied from a default config.

<a id="tableio_cfg_json.wizard._drive"></a>

#### \_drive

```python
def _drive(run: _WizardRun, backward: bool) -> TioJsonConfig
```

Run the endpoint steps until the configuration validates.

Back steps to the previous question and keeps the previous answers
available as defaults. Cancel-level returns to the first step, the
format question that opened the later option questions, and discards
dependent option values. Raised at the format question it propagates
out, so the application can handle the level enclosing this endpoint.

<a id="tableio_cfg_json.wizard._start_index"></a>

#### \_start\_index

```python
def _start_index(run: _WizardRun, backward: bool) -> int
```

Return the first step index for the requested direction.

<a id="tableio_cfg_json.wizard._build_steps"></a>

#### \_build\_steps

```python
def _build_steps(run: _WizardRun) -> list[_Step]
```

Return the ordered steps implied by the answers collected so far.

<a id="tableio_cfg_json.wizard._relevant_specs"></a>

#### \_relevant\_specs

```python
def _relevant_specs(format_name: str,
                    selected_impls: Sequence[str]) -> tuple[ConfigSpec, ...]
```

Return the config specs the option form should ask for.

<a id="tableio_cfg_json.wizard._run_step"></a>

#### \_run\_step

```python
def _run_step(run: _WizardRun, step: _Step) -> None
```

Dispatch one step to the function that asks its question.

<a id="tableio_cfg_json.wizard._run_format_step"></a>

#### \_run\_format\_step

```python
def _run_format_step(run: _WizardRun) -> None
```

Ask for the format and store it in the wizard data.

<a id="tableio_cfg_json.wizard._run_impl_step"></a>

#### \_run\_impl\_step

```python
def _run_impl_step(run: _WizardRun) -> None
```

Ask for the implementation and store or clear it in the data.

<a id="tableio_cfg_json.wizard._clear_after_format"></a>

#### \_clear\_after\_format

```python
def _clear_after_format(data: dict[str, object]) -> None
```

Keep the selected format and discard dependent option values.

<a id="tableio_cfg_json.wizard._run_options_step"></a>

#### \_run\_options\_step

```python
def _run_options_step(run: _WizardRun, specs: tuple[ConfigSpec, ...]) -> None
```

Ask one form of all optional members and store the answers.

<a id="tableio_cfg_json.wizard._options_question"></a>

#### \_options\_question

```python
def _options_question(data: dict[str, object]) -> str
```

Return the instruction shown above the option form.

<a id="tableio_cfg_json.wizard._apply_options"></a>

#### \_apply\_options

```python
def _apply_options(run: _WizardRun, specs: tuple[ConfigSpec, ...],
                   values: dict[str, object]) -> Optional[str]
```

Build data from the answers, validate it and commit on success.

<a id="tableio_cfg_json.wizard._options_validator"></a>

#### \_options\_validator

```python
def _options_validator(run: _WizardRun,
                       specs: tuple[ConfigSpec, ...]) -> PartialFormValidator
```

Return a partial-form validator for the option form.

<a id="tableio_cfg_json.wizard._current_values"></a>

#### \_current\_values

```python
def _current_values(data: dict[str, object],
                    specs: tuple[ConfigSpec, ...]) -> dict[str, object]
```

Return the members already set in the data, keyed by member name.

<a id="tableio_cfg_json.wizard._answer_values"></a>

#### \_answer\_values

```python
def _answer_values(specs: tuple[ConfigSpec, ...],
                   answers: AnswerFields) -> dict[str, object]
```

Return the answered members, dropping omitted ones, by member name.

<a id="tableio_cfg_json.wizard._answer_value"></a>

#### \_answer\_value

```python
def _answer_value(answer: AnswerField) -> Optional[object]
```

Return one member value from a form answer, or None when omitted.

<a id="tableio_cfg_json.wizard._option_fields"></a>

#### \_option\_fields

```python
def _option_fields(specs: tuple[ConfigSpec, ...],
                   values: dict[str, object]) -> list[AskField]
```

Return one form field per config member, pre-filled from values.

<a id="tableio_cfg_json.wizard._option_field"></a>

#### \_option\_field

```python
def _option_field(spec: ConfigSpec, current: Optional[object]) -> AskField
```

Return the form field that asks for one config member.

<a id="tableio_cfg_json.wizard._choice_field"></a>

#### \_choice\_field

```python
def _choice_field(spec: ConfigSpec,
                  current: Optional[object]) -> AskChoiceField
```

Return a choice field with a leading use-the-default option.

<a id="tableio_cfg_json.wizard._int_default"></a>

#### \_int\_default

```python
def _int_default(spec: ConfigSpec, current: Optional[object]) -> Optional[int]
```

Return the pre-filled integer default for one member.

<a id="tableio_cfg_json.wizard._text_default"></a>

#### \_text\_default

```python
def _text_default(spec: ConfigSpec,
                  current: Optional[object]) -> Optional[str]
```

Return the pre-filled text default for one member.

<a id="tableio_cfg_json.wizard._spec_choices"></a>

#### \_spec\_choices

```python
def _spec_choices(spec: ConfigSpec) -> Optional[tuple[str, ...]]
```

Return the advertised choices of one config member as strings.

<a id="tableio_cfg_json.wizard._data_from_values"></a>

#### \_data\_from\_values

```python
def _data_from_values(data: dict[str, object], specs: tuple[ConfigSpec, ...],
                      values: dict[str, object]) -> dict[str, object]
```

Return fresh data from the chosen format and the answered members.

<a id="tableio_cfg_json.wizard._resolve_member_value"></a>

#### \_resolve\_member\_value

```python
def _resolve_member_value(spec: ConfigSpec, raw: object) -> object
```

Convert one answered value to the type TableIO expects.

<a id="tableio_cfg_json.wizard._commit"></a>

#### \_commit

```python
def _commit(data: dict[str, object], new_data: dict[str, object],
            caps: Capabilities, file_access: FileAccess,
            stderr_file: TextIO) -> Optional[str]
```

Validate new_data; on success copy it into data and return None.

Returns an error reason to show the user when validation fails, so the
caller can re-ask. On success the data is updated in place.

<a id="tableio_cfg_json.wizard._ask_format"></a>

#### \_ask\_format

```python
def _ask_format(capabilities: Capabilities, ui_bridge: WizardUiBridge,
                default: object) -> str
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
def _ask_implementation(impl_names: Sequence[str], ui_bridge: WizardUiBridge,
                        default: object) -> Optional[str]
```

Ask for an implementation only when TableIO exposes a choice.

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

<a id="tableio_cfg_json.wizard._parse_member_value"></a>

#### \_parse\_member\_value

```python
def _parse_member_value(spec: ConfigSpec, answer: str) -> object
```

Convert a free-text answer to the type expected by TableIO.

<a id="tableio_cfg_json.wizard._member_default"></a>

#### \_member\_default

```python
def _member_default(spec: ConfigSpec) -> Optional[str]
```

Return a concrete default text value for one spec, if available.

<a id="tableio_cfg_json.wizard._set_json_member"></a>

#### \_set\_json\_member

```python
def _set_json_member(data: dict[str, object], member_name: str,
                     value: object) -> None
```

Set a top-level or dotted member in the JSON data being built.

<a id="tableio_cfg_json.wizard._get_json_member"></a>

#### \_get\_json\_member

```python
def _get_json_member(data: dict[str, object], member_name: str) -> object
```

Return a top-level or dotted member from JSON data, or None.

<a id="tableio_cfg_json.wizard._config_from_data"></a>

#### \_config\_from\_data

```python
def _config_from_data(data: dict[str, object], capabilities: Capabilities,
                      file_access: FileAccess,
                      stderr_file: TextIO) -> TioJsonConfig
```

Validate JSON data and return it as a TableIO JSON config.

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

<a id="tableio_cfg_json.loader._json_member"></a>

#### \_json\_member

```python
def _json_member(text: Optional[str], name: str,
                 fallback: Optional[str]) -> Optional[str]
```

Return one top-level string member of JSON text, or a fallback.

Only which defaults to build on is decided here, so anything that is not
a JSON object holding that member as a string is left to the parse step,
which reports what is wrong with it properly.

**Arguments**:

- `text` - JSON text to look in, or None when there is none.
- `name` - Name of the top-level member to look for.
- `fallback` - Value to use when the text does not answer.

**Returns**:

  The value of that member, or the fallback.

<a id="tableio_cfg_json.loader.tio_json_loader"></a>

#### tio\_json\_loader

```python
def tio_json_loader(capabilities: Capabilities,
                    file_access: FileAccess,
                    format_name: Optional[str] = None,
                    implementation: Optional[str] = None,
                    include_all_options: bool = True) -> ConfigLoader
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

<a id="tableio_cfg_json.wizard_ui_bridge_table"></a>

# tableio\_cfg\_json.wizard\_ui\_bridge\_table

Deprecated location of the console table editor internals.

This module moved to wizard_ui_bridge._table. Importing from here still
works and warns, see tableio_cfg_json._moved for how to make it fail
instead.

<a id="tableio_cfg_json.wizard_ui_bridge_table.__getattr__"></a>

#### \_\_getattr\_\_

```python
def __getattr__(name: str) -> object
```

Return name from its new module, warning that it moved.

<a id="tableio_cfg_json.wizard_ui_bridge_form_defs"></a>

# tableio\_cfg\_json.wizard\_ui\_bridge\_form\_defs

Deprecated location of the wizard UI bridge form fields.

This module moved to wizard_ui_bridge.form_defs. Importing from here still
works and warns, see tableio_cfg_json._moved for how to make it fail
instead.

<a id="tableio_cfg_json.wizard_ui_bridge_form_defs.__getattr__"></a>

#### \_\_getattr\_\_

```python
def __getattr__(name: str) -> object
```

Return name from its new module, warning that it moved.

<a id="tableio_cfg_json.wizard_ui_factory"></a>

# tableio\_cfg\_json.wizard\_ui\_factory

Deprecated location of the text-mode wizard UI bridge factory.

This module moved to wizard_ui_bridge.factory. Importing from here still
works and warns, see tableio_cfg_json._moved for how to make it fail
instead.

<a id="tableio_cfg_json.wizard_ui_factory.__getattr__"></a>

#### \_\_getattr\_\_

```python
def __getattr__(name: str) -> object
```

Return name from its new module, warning that it moved.

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

<a id="tableio_cfg_json.descriptions._choice_lines"></a>

#### \_choice\_lines

```python
def _choice_lines(spec: ConfigSpec) -> list[str]
```

Return the lines saying which values one member accepts.

**Arguments**:

- `spec` - TableIO configuration specification.

**Returns**:

  The list of accepted values where the editor cannot show it, followed
  by one line per value that needs explaining.

<a id="tableio_cfg_json.descriptions._member_lines"></a>

#### \_member\_lines

```python
def _member_lines(spec: ConfigSpec) -> list[str]
```

Return everything this package says about one member.

**Arguments**:

- `spec` - TableIO configuration specification.

**Returns**:

  The lines of the description of that member, most important first.

<a id="tableio_cfg_json.descriptions._relevance_lines"></a>

#### \_relevance\_lines

```python
def _relevance_lines(spec: ConfigSpec) -> list[str]
```

Return the lines saying where one member has an effect.

**Arguments**:

- `spec` - TableIO configuration specification.

**Returns**:

  The formats and the implementations the member matters for, leaving
  out whichever of the two TableIO does not restrict.

<a id="tableio_cfg_json.descriptions._section_formats"></a>

#### \_section\_formats

```python
def _section_formats(specs: Collection[ConfigSpec]) -> dict[str, list[str]]
```

Return the formats that each optional nested section belongs to.

A section is described by what its own members are relevant for, so a
section added to TableIO later is described without being named here.

**Arguments**:

- `specs` - TableIO configuration specifications.

**Returns**:

  The relevant format names of each section, in metadata order and
  without duplicates, keyed by the section member name.

<a id="tableio_cfg_json.descriptions._section_lines"></a>

#### \_section\_lines

```python
def _section_lines(formats: list[str]) -> list[str]
```

Return the description lines of one optional nested section.

**Arguments**:

- `formats` - Format names that the members of the section matter for.

**Returns**:

  The lines of the description, and nothing at all when TableIO
  restricts the section to no particular format.

<a id="tableio_cfg_json.descriptions._described"></a>

#### \_described

```python
def _described(specs: Collection[ConfigSpec]) -> dict[ConfigPath, str]
```

Return the description of every member and every nested section.

**Arguments**:

- `specs` - TableIO configuration specifications.

**Returns**:

  One description per member of the TioJsonConfig tree, under the path
  that addresses it inside a TioJsonConfig.

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

