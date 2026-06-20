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
* [tableio\_cfg\_json.wizard\_ui\_bridge](#tableio_cfg_json.wizard_ui_bridge)
  * [\_ERASE\_TOKEN](#tableio_cfg_json.wizard_ui_bridge._ERASE_TOKEN)
  * [WizardNavigation](#tableio_cfg_json.wizard_ui_bridge.WizardNavigation)
  * [WizardBack](#tableio_cfg_json.wizard_ui_bridge.WizardBack)
  * [WizardCancelLevel](#tableio_cfg_json.wizard_ui_bridge.WizardCancelLevel)
  * [WizardAbort](#tableio_cfg_json.wizard_ui_bridge.WizardAbort)
  * [TableColumn](#tableio_cfg_json.wizard_ui_bridge.TableColumn)
  * [TableCell](#tableio_cfg_json.wizard_ui_bridge.TableCell)
  * [WizardUiBridge](#tableio_cfg_json.wizard_ui_bridge.WizardUiBridge)
    * [ask](#tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.ask)
    * [ask\_yes\_no](#tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.ask_yes_no)
    * [ask\_table](#tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.ask_table)
    * [\_fill\_table](#tableio_cfg_json.wizard_ui_bridge.WizardUiBridge._fill_table)
    * [\_fill\_cell](#tableio_cfg_json.wizard_ui_bridge.WizardUiBridge._fill_cell)
    * [error\_file](#tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.error_file)
    * [show](#tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.show)
  * [\_interpret\_yes\_no](#tableio_cfg_json.wizard_ui_bridge._interpret_yes_no)
  * [\_yes\_no\_from\_index](#tableio_cfg_json.wizard_ui_bridge._yes_no_from_index)
  * [\_yes\_no\_from\_text](#tableio_cfg_json.wizard_ui_bridge._yes_no_from_text)
  * [\_cell\_prompt](#tableio_cfg_json.wizard_ui_bridge._cell_prompt)
  * [\_cell\_checker](#tableio_cfg_json.wizard_ui_bridge._cell_checker)
  * [\_cell\_value](#tableio_cfg_json.wizard_ui_bridge._cell_value)
  * [\_erased\_value](#tableio_cfg_json.wizard_ui_bridge._erased_value)
  * [\_indexed\_value](#tableio_cfg_json.wizard_ui_bridge._indexed_value)
  * [\_int\_text](#tableio_cfg_json.wizard_ui_bridge._int_text)
* [tableio\_cfg\_json.wizard\_ui\_bridge\_console](#tableio_cfg_json.wizard_ui_bridge_console)
  * [WizardUiBridgeConsole](#tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole)
    * [\_\_init\_\_](#tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole.__init__)
    * [ask](#tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole.ask)
    * [error\_file](#tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole.error_file)
    * [show](#tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole.show)
  * [\_raise\_for\_navigation](#tableio_cfg_json.wizard_ui_bridge_console._raise_for_navigation)
* [tableio\_cfg\_json.wizard](#tableio_cfg_json.wizard)
  * [\_WizardRun](#tableio_cfg_json.wizard._WizardRun)
  * [\_Step](#tableio_cfg_json.wizard._Step)
  * [tio\_json\_config\_wizard](#tableio_cfg_json.wizard.tio_json_config_wizard)
  * [\_drive](#tableio_cfg_json.wizard._drive)
  * [\_build\_steps](#tableio_cfg_json.wizard._build_steps)
  * [\_member\_steps](#tableio_cfg_json.wizard._member_steps)
  * [\_section\_specs](#tableio_cfg_json.wizard._section_specs)
  * [\_run\_step](#tableio_cfg_json.wizard._run_step)
  * [\_run\_format\_step](#tableio_cfg_json.wizard._run_format_step)
  * [\_run\_impl\_step](#tableio_cfg_json.wizard._run_impl_step)
  * [\_run\_section\_step](#tableio_cfg_json.wizard._run_section_step)
  * [\_section\_question](#tableio_cfg_json.wizard._section_question)
  * [\_section\_cells](#tableio_cfg_json.wizard._section_cells)
  * [\_spec\_choices](#tableio_cfg_json.wizard._spec_choices)
  * [\_resolve\_section](#tableio_cfg_json.wizard._resolve_section)
  * [\_resolve\_member\_value](#tableio_cfg_json.wizard._resolve_member_value)
  * [\_section\_check](#tableio_cfg_json.wizard._section_check)
  * [\_commit](#tableio_cfg_json.wizard._commit)
  * [\_ask\_format](#tableio_cfg_json.wizard._ask_format)
  * [\_impl\_names](#tableio_cfg_json.wizard._impl_names)
  * [\_ask\_implementation](#tableio_cfg_json.wizard._ask_implementation)
  * [\_ask\_member](#tableio_cfg_json.wizard._ask_member)
  * [\_matches](#tableio_cfg_json.wizard._matches)
  * [\_ask\_config\_member](#tableio_cfg_json.wizard._ask_config_member)
  * [\_ask\_member\_value](#tableio_cfg_json.wizard._ask_member_value)
  * [\_ask\_text\_member\_value](#tableio_cfg_json.wizard._ask_text_member_value)
  * [\_parse\_member\_value](#tableio_cfg_json.wizard._parse_member_value)
  * [\_member\_question](#tableio_cfg_json.wizard._member_question)
  * [\_ask\_choice](#tableio_cfg_json.wizard._ask_choice)
  * [\_choice\_question](#tableio_cfg_json.wizard._choice_question)
  * [\_choice\_from\_answer](#tableio_cfg_json.wizard._choice_from_answer)
  * [\_choice\_from\_index](#tableio_cfg_json.wizard._choice_from_index)
  * [\_choice\_from\_enum](#tableio_cfg_json.wizard._choice_from_enum)
  * [\_enum\_type](#tableio_cfg_json.wizard._enum_type)
  * [\_optional\_type\_name](#tableio_cfg_json.wizard._optional_type_name)
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

<a id="tableio_cfg_json.wizard_ui_bridge"></a>

# tableio\_cfg\_json.wizard\_ui\_bridge

User interface bridge for the TableIO JSON configuration wizard.

This module defines the abstract bridge between the wizard and a user
interface, the navigation requests a bridge raises to steer wizard flow,
and the column and cell descriptors used by table questions. Concrete
console and graphical bridges derive from WizardUiBridge.

Design status: the method bodies below are stubs. The signatures and
docstrings describe the intended public interface for review before the
behaviour is implemented. Where a docstring states that the base class
provides a fallback implementation, that fallback is written in terms of
ask() during the implementation phase so that older bridges that only
override ask() keep working until their maintainer overrides the method.

<a id="tableio_cfg_json.wizard_ui_bridge._ERASE_TOKEN"></a>

#### \_ERASE\_TOKEN

empties an editable cell in the ask_table fallback

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

Request to leave the current configuration level.

A bridge raises this when the user cancels the current grouped
sub-dialog, such as a table of format-specific parameters. The
wizard discards the values collected for that group and continues at
the enclosing level. When no group encloses the current question
inside one wizard call, the exception propagates out of the wizard
call so the application can treat that whole endpoint as one level of
its own larger flow.

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

A concrete bridge must implement ask() and show(). The base class
provides fallback implementations of ask_yes_no() and ask_table() in
terms of ask(), so a bridge keeps working before its maintainer adds
the better overrides. Any ask method may raise a WizardNavigation
subclass to request back, cancel-level or abort instead of returning
an answer.

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

The wizard asks every yes/no question through this method.
Application programmers are strongly encouraged to override it
with a real yes/no interface, such as a pair of yes and no
buttons in a graphical bridge or a y/n prompt in a console
bridge. The base class provides a fallback in terms of ask() with
the choices ('yes', 'no') so an application keeps working until
its maintainer has implemented the override: an empty answer
selects default, an index or matching text selects the boolean,
and any other answer is re-asked.

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

Application programmers are strongly encouraged to override this
with a real table widget. The base class provides a fallback in
terms of ask(), asking once per editable cell and folding the
read-only cells of the row into the prompt, so an application
keeps working until its maintainer has implemented the override.
In that fallback an empty answer keeps the cell's current value
and a reserved erase token empties the cell, which is how a
console user replaces a pre-filled default with an empty cell.

How an empty editable cell is reported follows its TableCell: a
nullable cell reports None, a free-text cell reports an empty
string, and a cell with choices treats empty as not yet a valid
value. When a cell reports None, the caller decides whether that
means omit the value or store an explicit null.

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

<a id="tableio_cfg_json.wizard_ui_bridge.WizardUiBridge._fill_table"></a>

#### \_fill\_table

```python
def _fill_table(columns: Sequence[TableColumn], cells: list[list[TableCell]],
                table: list[list[Optional[str]]],
                partial_check: Optional[PartialCheck]) -> None
```

Fill the editable cells, stepping back one cell on WizardBack.

WizardBack from the first editable cell has no earlier cell to
return to, so it propagates and the wizard steps to the previous
question. Cells already filled stay in the table while the user
moves between cells.

<a id="tableio_cfg_json.wizard_ui_bridge.WizardUiBridge._fill_cell"></a>

#### \_fill\_cell

```python
def _fill_cell(
        columns: Sequence[TableColumn], row: list[TableCell], col: int,
        current: Optional[str],
        check: Callable[[Optional[str]], Optional[str]]) -> Optional[str]
```

Ask one editable cell until its value is accepted.

**Arguments**:

- `columns` - The table columns, used to build the prompt.
- `row` - The cells of the row being filled.
- `col` - The index of the cell being filled.
- `current` - The cell's current value, kept when the user presses
  enter and shown in the prompt.
- `check` - Records a candidate in the table and returns an error
  message, or None when the candidate is accepted.
  

**Returns**:

  The accepted cell value, or None for an empty nullable cell.

**Raises**:

- `WizardBack` - The user asked to return to the previous cell.
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

<a id="tableio_cfg_json.wizard_ui_bridge._interpret_yes_no"></a>

#### \_interpret\_yes\_no

```python
def _interpret_yes_no(answer: str | int, default: bool) -> Optional[bool]
```

Map a bridge answer to a yes/no boolean, or None to re-ask.

<a id="tableio_cfg_json.wizard_ui_bridge._yes_no_from_index"></a>

#### \_yes\_no\_from\_index

```python
def _yes_no_from_index(index: int) -> Optional[bool]
```

Map a 0-based ('yes', 'no') index to a boolean, or None.

<a id="tableio_cfg_json.wizard_ui_bridge._yes_no_from_text"></a>

#### \_yes\_no\_from\_text

```python
def _yes_no_from_text(text: str) -> Optional[bool]
```

Map yes/no free text to a boolean, or None when unrecognised.

<a id="tableio_cfg_json.wizard_ui_bridge._cell_prompt"></a>

#### \_cell\_prompt

```python
def _cell_prompt(columns: Sequence[TableColumn], row: list[TableCell],
                 col_index: int, current: Optional[str]) -> str
```

Return the console prompt for one editable cell.

<a id="tableio_cfg_json.wizard_ui_bridge._cell_checker"></a>

#### \_cell\_checker

```python
def _cell_checker(
    table: list[list[Optional[str]]], position: tuple[int, int],
    partial_check: Optional[PartialCheck]
) -> Callable[[Optional[str]], Optional[str]]
```

Return a per-cell check that records a candidate and validates it.

<a id="tableio_cfg_json.wizard_ui_bridge._cell_value"></a>

#### \_cell\_value

```python
def _cell_value(answer: str | int, cell: TableCell,
                current: Optional[str]) -> tuple[bool, Optional[str]]
```

Map a bridge answer to a cell value and whether it is usable.

<a id="tableio_cfg_json.wizard_ui_bridge._erased_value"></a>

#### \_erased\_value

```python
def _erased_value(cell: TableCell) -> tuple[bool, Optional[str]]
```

Map an erase request to a cell value and whether it is usable.

<a id="tableio_cfg_json.wizard_ui_bridge._indexed_value"></a>

#### \_indexed\_value

```python
def _indexed_value(index: int, cell: TableCell) -> tuple[bool, Optional[str]]
```

Map a 0-based choice index to a cell value, or mark it unusable.

<a id="tableio_cfg_json.wizard_ui_bridge._int_text"></a>

#### \_int\_text

```python
def _int_text(text: str) -> Optional[int]
```

Return an integer from text, or None when text is not an integer.

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

<a id="tableio_cfg_json.wizard_ui_bridge_console._raise_for_navigation"></a>

#### \_raise\_for\_navigation

```python
def _raise_for_navigation(text: str) -> None
```

Raise a navigation request when text is a reserved token.

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

One navigable question or grouped table in a wizard run.

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

<a id="tableio_cfg_json.wizard._drive"></a>

#### \_drive

```python
def _drive(run: _WizardRun) -> TioJsonConfig
```

Run wizard steps with back navigation until the config validates.

<a id="tableio_cfg_json.wizard._build_steps"></a>

#### \_build\_steps

```python
def _build_steps(run: _WizardRun) -> list[_Step]
```

Return the ordered steps implied by the answers collected so far.

<a id="tableio_cfg_json.wizard._member_steps"></a>

#### \_member\_steps

```python
def _member_steps(format_name: str,
                  selected_impls: Sequence[str]) -> list[_Step]
```

Return scalar and section steps for the relevant config members.

<a id="tableio_cfg_json.wizard._section_specs"></a>

#### \_section\_specs

```python
def _section_specs(section: str, format_name: str,
                   selected_impls: Sequence[str]) -> tuple[ConfigSpec, ...]
```

Return the relevant config specs that belong to one section.

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

<a id="tableio_cfg_json.wizard._run_section_step"></a>

#### \_run\_section\_step

```python
def _run_section_step(run: _WizardRun, section: str,
                      specs: tuple[ConfigSpec, ...]) -> None
```

Ask one table of section members and store the entered values.

<a id="tableio_cfg_json.wizard._section_question"></a>

#### \_section\_question

```python
def _section_question(section: str) -> str
```

Return the instruction shown above one section table.

<a id="tableio_cfg_json.wizard._section_cells"></a>

#### \_section\_cells

```python
def _section_cells(run: _WizardRun, section: str,
                   specs: tuple[ConfigSpec, ...]) -> list[list[TableCell]]
```

Return the table rows for one section, pre-filled from the data.

<a id="tableio_cfg_json.wizard._spec_choices"></a>

#### \_spec\_choices

```python
def _spec_choices(spec: ConfigSpec) -> Optional[tuple[str, ...]]
```

Return the advertised choices of one config member as strings.

<a id="tableio_cfg_json.wizard._resolve_section"></a>

#### \_resolve\_section

```python
def _resolve_section(data: dict[str, object], section: str,
                     specs: tuple[ConfigSpec,
                                  ...], result: list[list[Optional[str]]],
                     stderr_file: TextIO) -> dict[str, object]
```

Return data with one section rebuilt from a filled-in table.

<a id="tableio_cfg_json.wizard._resolve_member_value"></a>

#### \_resolve\_member\_value

```python
def _resolve_member_value(spec: ConfigSpec, raw: str,
                          stderr_file: TextIO) -> object
```

Convert one entered table value to the type TableIO expects.

<a id="tableio_cfg_json.wizard._section_check"></a>

#### \_section\_check

```python
def _section_check(run: _WizardRun, section: str,
                   specs: tuple[ConfigSpec, ...]) -> PartialCheck
```

Return a partial-check callback for one section table.

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
                stderr_file: TextIO) -> str
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
                        stderr_file: TextIO) -> Optional[str]
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

<a id="tableio_cfg_json.wizard._ask_config_member"></a>

#### \_ask\_config\_member

```python
def _ask_config_member(spec: ConfigSpec, data: dict[str, object],
                       caps: Capabilities, file_access: FileAccess,
                       ui_bridge: WizardUiBridge, stderr_file: TextIO) -> None
```

Ask for one optional member and keep retrying until it validates.

<a id="tableio_cfg_json.wizard._ask_member_value"></a>

#### \_ask\_member\_value

```python
def _ask_member_value(spec: ConfigSpec, ui_bridge: WizardUiBridge,
                      stderr_file: TextIO,
                      re_ask_reason: Optional[str]) -> Optional[object]
```

Ask for one optional value and convert simple scalar types.

<a id="tableio_cfg_json.wizard._ask_text_member_value"></a>

#### \_ask\_text\_member\_value

```python
def _ask_text_member_value(spec: ConfigSpec, ui_bridge: WizardUiBridge,
                           re_ask_reason: Optional[str]) -> Optional[object]
```

Ask for one free-text optional value.

<a id="tableio_cfg_json.wizard._parse_member_value"></a>

#### \_parse\_member\_value

```python
def _parse_member_value(spec: ConfigSpec, answer: str) -> object
```

Convert a free-text answer to the type expected by TableIO.

<a id="tableio_cfg_json.wizard._member_question"></a>

#### \_member\_question

```python
def _member_question(spec: ConfigSpec) -> str
```

Return the explanatory question for one free-text member.

<a id="tableio_cfg_json.wizard._ask_choice"></a>

#### \_ask\_choice

```python
def _ask_choice(title: str,
                member_name: str,
                choices: Sequence[str],
                allow_blank: bool,
                blank_text: str,
                ui_bridge: WizardUiBridge,
                stderr_file: TextIO,
                enum_type: Optional[type[Enum]] = None,
                first_re_ask: Optional[str] = None) -> str
```

Ask for one answer from a list of choices.

<a id="tableio_cfg_json.wizard._choice_question"></a>

#### \_choice\_question

```python
def _choice_question(title: str, allow_blank: bool, blank_text: str) -> str
```

Return the question text for one list choice.

<a id="tableio_cfg_json.wizard._choice_from_answer"></a>

#### \_choice\_from\_answer

```python
def _choice_from_answer(answer: str | int, choices: Sequence[str],
                        allow_blank: bool, member_name: str,
                        stderr_file: TextIO,
                        enum_type: Optional[type[Enum]]) -> str
```

Return a validated choice selected by an answer.

<a id="tableio_cfg_json.wizard._choice_from_index"></a>

#### \_choice\_from\_index

```python
def _choice_from_index(index: int, choices: Sequence[str]) -> str
```

Return the choice at a 0-based index.

<a id="tableio_cfg_json.wizard._choice_from_enum"></a>

#### \_choice\_from\_enum

```python
def _choice_from_enum(answer: str, choices: Sequence[str],
                      enum_type: type[Enum]) -> str
```

Return the enum choice whose name best matches the answer.

<a id="tableio_cfg_json.wizard._enum_type"></a>

#### \_enum\_type

```python
def _enum_type(spec: ConfigSpec) -> Optional[type[Enum]]
```

Return the enum type used by a config member choice list.

<a id="tableio_cfg_json.wizard._optional_type_name"></a>

#### \_optional\_type\_name

```python
def _optional_type_name(value_type: str) -> Optional[str]
```

Return the inner type name from an Optional type description.

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

