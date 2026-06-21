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
    * [\_\_init\_subclass\_\_](#tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.__init_subclass__)
    * [ask](#tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.ask)
    * [ask\_text](#tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.ask_text)
    * [ask\_yes\_no](#tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.ask_yes_no)
    * [ask\_choice](#tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.ask_choice)
    * [ask\_multi](#tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.ask_multi)
    * [ask\_table](#tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.ask_table)
    * [\_guard\_fallback](#tableio_cfg_json.wizard_ui_bridge.WizardUiBridge._guard_fallback)
    * [error\_file](#tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.error_file)
    * [show](#tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.show)
  * [\_interpret\_yes\_no](#tableio_cfg_json.wizard_ui_bridge._interpret_yes_no)
  * [\_yes\_no\_from\_index](#tableio_cfg_json.wizard_ui_bridge._yes_no_from_index)
  * [\_yes\_no\_from\_text](#tableio_cfg_json.wizard_ui_bridge._yes_no_from_text)
  * [\_ask\_yes\_no](#tableio_cfg_json.wizard_ui_bridge._ask_yes_no)
  * [\_run\_table](#tableio_cfg_json.wizard_ui_bridge._run_table)
  * [\_fill\_table](#tableio_cfg_json.wizard_ui_bridge._fill_table)
  * [\_fill\_cell](#tableio_cfg_json.wizard_ui_bridge._fill_cell)
  * [\_cell\_prompt](#tableio_cfg_json.wizard_ui_bridge._cell_prompt)
  * [\_cell\_checker](#tableio_cfg_json.wizard_ui_bridge._cell_checker)
  * [\_cell\_value](#tableio_cfg_json.wizard_ui_bridge._cell_value)
  * [\_erased\_value](#tableio_cfg_json.wizard_ui_bridge._erased_value)
  * [\_indexed\_value](#tableio_cfg_json.wizard_ui_bridge._indexed_value)
  * [\_int\_text](#tableio_cfg_json.wizard_ui_bridge._int_text)
  * [\_ask\_one](#tableio_cfg_json.wizard_ui_bridge._ask_one)
  * [\_ask\_many](#tableio_cfg_json.wizard_ui_bridge._ask_many)
  * [\_resolve\_choice](#tableio_cfg_json.wizard_ui_bridge._resolve_choice)
  * [\_resolve\_multi](#tableio_cfg_json.wizard_ui_bridge._resolve_multi)
  * [\_multi\_labels](#tableio_cfg_json.wizard_ui_bridge._multi_labels)
  * [\_tokens\_to\_labels](#tableio_cfg_json.wizard_ui_bridge._tokens_to_labels)
  * [\_match\_token](#tableio_cfg_json.wizard_ui_bridge._match_token)
  * [\_best\_match](#tableio_cfg_json.wizard_ui_bridge._best_match)
  * [\_choice\_at\_index](#tableio_cfg_json.wizard_ui_bridge._choice_at_index)
  * [\_multi\_count\_error](#tableio_cfg_json.wizard_ui_bridge._multi_count_error)
* [tableio\_cfg\_json.wizard\_ui\_bridge\_textual](#tableio_cfg_json.wizard_ui_bridge_textual)
  * [\_NavApp](#tableio_cfg_json.wizard_ui_bridge_textual._NavApp)
    * [\_\_init\_\_](#tableio_cfg_json.wizard_ui_bridge_textual._NavApp.__init__)
    * [action\_nav\_back](#tableio_cfg_json.wizard_ui_bridge_textual._NavApp.action_nav_back)
    * [action\_nav\_cancel](#tableio_cfg_json.wizard_ui_bridge_textual._NavApp.action_nav_cancel)
  * [\_header\_widgets](#tableio_cfg_json.wizard_ui_bridge_textual._header_widgets)
  * [\_TextApp](#tableio_cfg_json.wizard_ui_bridge_textual._TextApp)
    * [\_\_init\_\_](#tableio_cfg_json.wizard_ui_bridge_textual._TextApp.__init__)
    * [compose](#tableio_cfg_json.wizard_ui_bridge_textual._TextApp.compose)
    * [\_entered](#tableio_cfg_json.wizard_ui_bridge_textual._TextApp._entered)
  * [\_ChoiceApp](#tableio_cfg_json.wizard_ui_bridge_textual._ChoiceApp)
    * [\_\_init\_\_](#tableio_cfg_json.wizard_ui_bridge_textual._ChoiceApp.__init__)
    * [compose](#tableio_cfg_json.wizard_ui_bridge_textual._ChoiceApp.compose)
    * [on\_mount](#tableio_cfg_json.wizard_ui_bridge_textual._ChoiceApp.on_mount)
    * [\_picked](#tableio_cfg_json.wizard_ui_bridge_textual._ChoiceApp._picked)
  * [\_MultiApp](#tableio_cfg_json.wizard_ui_bridge_textual._MultiApp)
    * [\_\_init\_\_](#tableio_cfg_json.wizard_ui_bridge_textual._MultiApp.__init__)
    * [compose](#tableio_cfg_json.wizard_ui_bridge_textual._MultiApp.compose)
    * [\_selections](#tableio_cfg_json.wizard_ui_bridge_textual._MultiApp._selections)
    * [\_clicked](#tableio_cfg_json.wizard_ui_bridge_textual._MultiApp._clicked)
    * [action\_submit](#tableio_cfg_json.wizard_ui_bridge_textual._MultiApp.action_submit)
    * [\_count\_ok](#tableio_cfg_json.wizard_ui_bridge_textual._MultiApp._count_ok)
  * [\_default\_index](#tableio_cfg_json.wizard_ui_bridge_textual._default_index)
  * [\_preselected](#tableio_cfg_json.wizard_ui_bridge_textual._preselected)
  * [\_parse\_cell\_id](#tableio_cfg_json.wizard_ui_bridge_textual._parse_cell_id)
  * [\_make\_select](#tableio_cfg_json.wizard_ui_bridge_textual._make_select)
  * [\_uniform](#tableio_cfg_json.wizard_ui_bridge_textual._uniform)
  * [\_new\_row\_template](#tableio_cfg_json.wizard_ui_bridge_textual._new_row_template)
  * [\_TableApp](#tableio_cfg_json.wizard_ui_bridge_textual._TableApp)
    * [\_\_init\_\_](#tableio_cfg_json.wizard_ui_bridge_textual._TableApp.__init__)
    * [compose](#tableio_cfg_json.wizard_ui_bridge_textual._TableApp.compose)
    * [on\_mount](#tableio_cfg_json.wizard_ui_bridge_textual._TableApp.on_mount)
    * [\_focus\_first\_cell](#tableio_cfg_json.wizard_ui_bridge_textual._TableApp._focus_first_cell)
    * [\_grid\_cells](#tableio_cfg_json.wizard_ui_bridge_textual._TableApp._grid_cells)
    * [\_row\_widgets](#tableio_cfg_json.wizard_ui_bridge_textual._TableApp._row_widgets)
    * [\_is\_readonly](#tableio_cfg_json.wizard_ui_bridge_textual._TableApp._is_readonly)
    * [\_cell\_widget](#tableio_cfg_json.wizard_ui_bridge_textual._TableApp._cell_widget)
    * [\_on\_input](#tableio_cfg_json.wizard_ui_bridge_textual._TableApp._on_input)
    * [\_on\_select](#tableio_cfg_json.wizard_ui_bridge_textual._TableApp._on_select)
    * [\_recheck](#tableio_cfg_json.wizard_ui_bridge_textual._TableApp._recheck)
    * [action\_submit](#tableio_cfg_json.wizard_ui_bridge_textual._TableApp.action_submit)
    * [\_submit\_clicked](#tableio_cfg_json.wizard_ui_bridge_textual._TableApp._submit_clicked)
    * [\_add\_clicked](#tableio_cfg_json.wizard_ui_bridge_textual._TableApp._add_clicked)
    * [\_remove\_clicked](#tableio_cfg_json.wizard_ui_bridge_textual._TableApp._remove_clicked)
    * [\_add\_row](#tableio_cfg_json.wizard_ui_bridge_textual._TableApp._add_row)
    * [\_remove\_row](#tableio_cfg_json.wizard_ui_bridge_textual._TableApp._remove_row)
    * [\_set\_status](#tableio_cfg_json.wizard_ui_bridge_textual._TableApp._set_status)
    * [\_read\_cell](#tableio_cfg_json.wizard_ui_bridge_textual._TableApp._read_cell)
  * [WizardUiBridgeTextual](#tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual)
    * [\_\_init\_\_](#tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual.__init__)
    * [ask\_text](#tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual.ask_text)
    * [ask\_yes\_no](#tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual.ask_yes_no)
    * [ask\_choice](#tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual.ask_choice)
    * [ask\_multi](#tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual.ask_multi)
    * [ask\_table](#tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual.ask_table)
    * [\_run](#tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual._run)
    * [\_launch](#tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual._launch)
    * [\_collect](#tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual._collect)
    * [\_drain\_messages](#tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual._drain_messages)
    * [error\_file](#tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual.error_file)
    * [show](#tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual.show)
* [tableio\_cfg\_json.wizard\_ui\_bridge\_console](#tableio_cfg_json.wizard_ui_bridge_console)
  * [WizardUiBridgeConsole](#tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole)
    * [\_\_init\_\_](#tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole.__init__)
    * [ask\_text](#tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole.ask_text)
    * [ask\_yes\_no](#tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole.ask_yes_no)
    * [ask\_table](#tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole.ask_table)
    * [\_ask\_raw](#tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole._ask_raw)
    * [ask\_choice](#tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole.ask_choice)
    * [ask\_multi](#tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole.ask_multi)
    * [\_emit\_question](#tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole._emit_question)
    * [\_read\_answer](#tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole._read_answer)
    * [error\_file](#tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole.error_file)
    * [show](#tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole.show)
  * [\_raise\_for\_navigation](#tableio_cfg_json.wizard_ui_bridge_console._raise_for_navigation)
  * [\_to\_index](#tableio_cfg_json.wizard_ui_bridge_console._to_index)
  * [\_menu\_lines](#tableio_cfg_json.wizard_ui_bridge_console._menu_lines)
  * [\_multi\_question](#tableio_cfg_json.wizard_ui_bridge_console._multi_question)
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
  * [\_set\_json\_member](#tableio_cfg_json.wizard._set_json_member)
  * [\_config\_from\_data](#tableio_cfg_json.wizard._config_from_data)
* [tableio\_cfg\_json.wizard\_ui\_factory](#tableio_cfg_json.wizard_ui_factory)
  * [make\_text\_ui\_bridge](#tableio_cfg_json.wizard_ui_factory.make_text_ui_bridge)
  * [\_is\_tty](#tableio_cfg_json.wizard_ui_factory._is_tty)

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

An application that drives the wizard is responsible for implementing
the typed ask methods of its bridge, together with show(). The typed
methods are ask_text() for free text, ask_choice() for one choice,
ask_multi() for several choices, ask_yes_no() for a boolean and
ask_table() for a table. The low-level ask() is deprecated: it warns
when called and when a bridge overrides it. To give application bridge
authors time to migrate, the base class keeps temporary fallback
implementations of the typed methods written in terms of ask(), so a
bridge that still overrides ask() keeps working while it is adjusted to
implement the typed methods directly. These fallbacks are a temporary
compatibility aid that warns on use and will be withdrawn once bridges
implement the typed methods directly.

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

A concrete bridge implements the typed ask methods, ask_text(),
ask_choice(), ask_multi(), ask_yes_no() and ask_table(), together
with show(). The low-level ask() is deprecated: it warns when called
and when a bridge overrides it. As a temporary migration aid the base
class implements the typed methods in terms of the deprecated ask(),
so a bridge that still overrides ask() keeps working while it is
adjusted; each fallback warns that the typed method should be
overridden instead. These fallbacks are temporary and will be
withdrawn once bridges implement the typed methods directly. Any ask
method may raise a WizardNavigation subclass to request back,
cancel-level or abort instead of returning an answer.

<a id="tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.__init_subclass__"></a>

#### \_\_init\_subclass\_\_

```python
def __init_subclass__(cls, **kwargs: object) -> None
```

Warn when a subclass overrides the deprecated ask().

<a id="tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.ask"></a>

#### ask

```python
def ask(question: str,
        re_ask_reason: Optional[str] = None,
        choices: Optional[Sequence[str]] = None) -> str | int
```

Ask a question and return the user's answer.

Deprecated. Call ask_text() for free text or ask_choice() for a
single choice instead. This base implementation is temporary
plumbing: it warns and then dispatches to ask_text() when no
choices are given and to ask_choice() otherwise, so existing
callers keep working against a bridge that implements the typed
methods.

**Arguments**:

- `question` - The question to ask the user.
- `re_ask_reason` - The reason for re-asking the question, for
  instance that the user's answer was invalid.
- `choices` - The choices to offer the user as a sequence of
  strings.
  

**Returns**:

  The user's answer: the entered text when no choices are
  given, otherwise the chosen one of choices.

**Raises**:

- `WizardBack` - The user asked to return to the previous question.
- `WizardCancelLevel` - The user cancelled the current level.
- `WizardAbort` - The user abandoned the whole configuration.

<a id="tableio_cfg_json.wizard_ui_bridge.WizardUiBridge.ask_text"></a>

#### ask\_text

```python
def ask_text(question: str,
             re_ask_reason: Optional[str] = None,
             nullable: bool = False) -> Optional[str]
```

Ask a free-text question and return the entered text.

The application is responsible for implementing this method with
a real text-entry control. As a temporary migration aid the base
class provides a fallback in terms of the deprecated ask(), so a
bridge that still overrides ask() keeps working.

**Arguments**:

- `question` - The question to ask the user.
- `re_ask_reason` - The reason for re-asking the question, for
  instance that the user's answer was invalid.
- `nullable` - When True an empty answer is reported as None, so
  the caller can treat it as a request to use the
  default. When False an empty answer is the empty
  string.
  

**Returns**:

  The entered text, or None for an empty answer when nullable.

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
migration aid the base class provides a fallback in terms of the
deprecated ask() with the choices ('yes', 'no'): an empty answer
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
the base class provides a fallback in terms of the deprecated
ask().

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
migration aid the base class provides a fallback in terms of the
deprecated ask() that reads one comma-separated answer of menu
indexes or names.

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
provides a fallback in terms of the deprecated ask(), asking once
per editable cell and folding the read-only cells of the row into
the prompt, so a bridge that still overrides ask() keeps working.
The fallback only fills the rows given in cells, so it ignores
min_rows and max_rows and cannot add or remove rows. In that
fallback an empty answer keeps the cell's current value and a
reserved erase token empties the cell, which is how a console
user replaces a pre-filled default with an empty cell.

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

<a id="tableio_cfg_json.wizard_ui_bridge.WizardUiBridge._guard_fallback"></a>

#### \_guard\_fallback

```python
def _guard_fallback(method_name: str) -> None
```

Guard a deprecated fallback and warn that it is temporary.

The base typed-method fallbacks work only while a bridge still
overrides the deprecated ask(). A bridge that overrides neither
ask() nor method_name has no implementation for it, so this
raises NotImplementedError; otherwise it warns that method_name
should be overridden instead of relying on the fallback.

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

<a id="tableio_cfg_json.wizard_ui_bridge._ask_yes_no"></a>

#### \_ask\_yes\_no

```python
def _ask_yes_no(reader: Callable[[Optional[str]], str | int], default: bool,
                re_ask_reason: Optional[str]) -> bool
```

Re-ask through reader until a yes/no answer is understood.

<a id="tableio_cfg_json.wizard_ui_bridge._run_table"></a>

#### \_run\_table

```python
def _run_table(
        ask: AskReader, show: Callable[[str], None],
        columns: Sequence[TableColumn], cells: list[list[TableCell]],
        question: str, re_ask_reason: Optional[str],
        partial_check: Optional[PartialCheck]) -> list[list[Optional[str]]]
```

Show one table question and fill its editable cells via ask.

The read-only cells stay fixed and only the editable cells are asked,
one at a time, through the ask reader. This is the shared core of the
console table interface and the deprecated base-class table fallback.

<a id="tableio_cfg_json.wizard_ui_bridge._fill_table"></a>

#### \_fill\_table

```python
def _fill_table(ask: AskReader, columns: Sequence[TableColumn],
                cells: list[list[TableCell]], table: list[list[Optional[str]]],
                partial_check: Optional[PartialCheck]) -> None
```

Fill the editable cells, stepping back one cell on WizardBack.

WizardBack from the first editable cell has no earlier cell to
return to, so it propagates and the wizard steps to the previous
question. Cells already filled stay in the table while the user
moves between cells.

<a id="tableio_cfg_json.wizard_ui_bridge._fill_cell"></a>

#### \_fill\_cell

```python
def _fill_cell(
        ask: AskReader, columns: Sequence[TableColumn], row: list[TableCell],
        col: int, current: Optional[str],
        check: Callable[[Optional[str]], Optional[str]]) -> Optional[str]
```

Ask one editable cell until its value is accepted.

**Arguments**:

- `ask` - The ask reader used to read the cell value.
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

<a id="tableio_cfg_json.wizard_ui_bridge._ask_one"></a>

#### \_ask\_one

```python
def _ask_one(reader: Callable[[Optional[str]],
                              str | int], choices: Sequence[str],
             default: Optional[str], re_ask_reason: Optional[str]) -> str
```

Re-ask through reader until one valid choice is selected.

<a id="tableio_cfg_json.wizard_ui_bridge._ask_many"></a>

#### \_ask\_many

```python
def _ask_many(reader: Callable[[Optional[str]], str | int],
              choices: Sequence[str], default: Optional[Sequence[str]],
              min_select: int, max_select: Optional[int],
              re_ask_reason: Optional[str], one_based: bool) -> list[str]
```

Re-ask through reader until a valid set of choices is selected.

<a id="tableio_cfg_json.wizard_ui_bridge._resolve_choice"></a>

#### \_resolve\_choice

```python
def _resolve_choice(answer: str | int, choices: Sequence[str],
                    default: Optional[str]) -> Optional[str]
```

Map a single-choice answer to a choice, or None to re-ask.

<a id="tableio_cfg_json.wizard_ui_bridge._resolve_multi"></a>

#### \_resolve\_multi

```python
def _resolve_multi(answer: str | int, choices: Sequence[str],
                   default: Optional[Sequence[str]], min_select: int,
                   max_select: Optional[int],
                   one_based: bool) -> tuple[Optional[list[str]], str]
```

Map a multi-choice answer to choices and an error to re-ask.

<a id="tableio_cfg_json.wizard_ui_bridge._multi_labels"></a>

#### \_multi\_labels

```python
def _multi_labels(answer: str | int, choices: Sequence[str],
                  default: Optional[Sequence[str]],
                  one_based: bool) -> Optional[list[str]]
```

Map a multi-choice answer to chosen labels, or None to re-ask.

<a id="tableio_cfg_json.wizard_ui_bridge._tokens_to_labels"></a>

#### \_tokens\_to\_labels

```python
def _tokens_to_labels(text: str, choices: Sequence[str],
                      one_based: bool) -> Optional[list[str]]
```

Map a comma-separated answer to labels, or None to re-ask.

<a id="tableio_cfg_json.wizard_ui_bridge._match_token"></a>

#### \_match\_token

```python
def _match_token(token: str, choices: Sequence[str],
                 one_based: bool) -> Optional[str]
```

Map one menu index or name to a choice, or None when no match.

<a id="tableio_cfg_json.wizard_ui_bridge._best_match"></a>

#### \_best\_match

```python
def _best_match(token: str, choices: Sequence[str]) -> Optional[str]
```

Return the unique best name match for token, or None.

<a id="tableio_cfg_json.wizard_ui_bridge._choice_at_index"></a>

#### \_choice\_at\_index

```python
def _choice_at_index(index: int, choices: Sequence[str]) -> Optional[str]
```

Return the choice at a 0-based index, or None when out of range.

<a id="tableio_cfg_json.wizard_ui_bridge._multi_count_error"></a>

#### \_multi\_count\_error

```python
def _multi_count_error(min_select: int, max_select: Optional[int]) -> str
```

Return the message shown when the selected count is not allowed.

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

<a id="tableio_cfg_json.wizard_ui_bridge_textual._NavApp"></a>

## \_NavApp Objects

```python
class _NavApp(App[_T])
```

Base screen translating navigation keys into wizard requests.

A subclass lays out one question. ctrl+b records a request to go
back and ctrl+o a request to cancel the current level; the mnemonic
for ctrl+o is "out one level". Both exit the screen with no value so
the bridge can raise the matching request. The built-in ctrl+q quit
also exits with no value, which the bridge treats as an abort. These
keys avoid the editing shortcuts that the text input widget binds,
so they work on every screen.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._NavApp.__init__"></a>

#### \_\_init\_\_

```python
def __init__() -> None
```

Initialize with no pending navigation request.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._NavApp.action_nav_back"></a>

#### action\_nav\_back

```python
def action_nav_back() -> None
```

Record a request to return to the previous question.

The name avoids App.action_back, the built-in screen-history
action, so this records a wizard back request instead.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._NavApp.action_nav_cancel"></a>

#### action\_nav\_cancel

```python
def action_nav_cancel() -> None
```

Record a request to cancel the current level.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._header_widgets"></a>

#### \_header\_widgets

```python
def _header_widgets(messages: list[str], question: str) -> Iterator[Static]
```

Yield one static line per message and one for the question.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._TextApp"></a>

## \_TextApp Objects

```python
class _TextApp(_NavApp[str])
```

Free-text screen returning the string the user typed.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._TextApp.__init__"></a>

#### \_\_init\_\_

```python
def __init__(question: str, messages: list[str]) -> None
```

Store the prompt and any buffered messages.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._TextApp.compose"></a>

#### compose

```python
def compose() -> ComposeResult
```

Lay out the header, the input field and the footer.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._TextApp._entered"></a>

#### \_entered

```python
@on(Input.Submitted)
def _entered(event: Input.Submitted) -> None
```

Exit returning the entered text, empty when nothing typed.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._ChoiceApp"></a>

## \_ChoiceApp Objects

```python
class _ChoiceApp(_NavApp[int])
```

Single-choice screen returning the chosen 0-based index.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._ChoiceApp.__init__"></a>

#### \_\_init\_\_

```python
def __init__(question: str, choices: list[str], default_index: Optional[int],
             messages: list[str]) -> None
```

Store the prompt, choices and the index to highlight.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._ChoiceApp.compose"></a>

#### compose

```python
def compose() -> ComposeResult
```

Lay out the header, the option list and the footer.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._ChoiceApp.on_mount"></a>

#### on\_mount

```python
def on_mount() -> None
```

Highlight the default option when one is given.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._ChoiceApp._picked"></a>

#### \_picked

```python
@on(OptionList.OptionSelected)
def _picked(event: OptionList.OptionSelected) -> None
```

Exit returning the index of the selected option.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._MultiApp"></a>

## \_MultiApp Objects

```python
class _MultiApp(_NavApp[list[int]])
```

Multi-choice screen returning the chosen 0-based indexes.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._MultiApp.__init__"></a>

#### \_\_init\_\_

```python
def __init__(question: str, choices: list[str], preselected: list[int],
             min_select: int, max_select: Optional[int],
             messages: list[str]) -> None
```

Store the prompt, choices, preselection and count limits.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._MultiApp.compose"></a>

#### compose

```python
def compose() -> ComposeResult
```

Lay out the header, the check-box list, submit and footer.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._MultiApp._selections"></a>

#### \_selections

```python
def _selections() -> list[Selection[int]]
```

Return one selection per choice, preselected as requested.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._MultiApp._clicked"></a>

#### \_clicked

```python
@on(Button.Pressed)
def _clicked(_event: Button.Pressed) -> None
```

Treat a click on the submit button like the submit action.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._MultiApp.action_submit"></a>

#### action\_submit

```python
def action_submit() -> None
```

Exit with the selection, or show why the count is wrong.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._MultiApp._count_ok"></a>

#### \_count\_ok

```python
def _count_ok(count: int) -> bool
```

Return whether count is within the allowed selection range.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._default_index"></a>

#### \_default\_index

```python
def _default_index(choices: Sequence[str],
                   default: Optional[str]) -> Optional[int]
```

Return the index of default within choices, or None.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._preselected"></a>

#### \_preselected

```python
def _preselected(choices: Sequence[str],
                 default: Optional[Sequence[str]]) -> list[int]
```

Return the indexes of the default values within choices.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._parse_cell_id"></a>

#### \_parse\_cell\_id

```python
def _parse_cell_id(widget_id: Optional[str]) -> Optional[tuple[int, int]]
```

Return the (row, column) encoded in an editable cell id.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._make_select"></a>

#### \_make\_select

```python
def _make_select(cell: TableCell, widget_id: str) -> Select[str]
```

Return a drop-down for one cell, blank only when nullable.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._uniform"></a>

#### \_uniform

```python
def _uniform(values: list[_V], default: _V) -> _V
```

Return the value shared by every entry, or the default.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._new_row_template"></a>

#### \_new\_row\_template

```python
def _new_row_template(columns: Sequence[TableColumn],
                      cells: list[list[TableCell]]) -> list[TableCell]
```

Return the cell descriptors used for rows added to the table.

For each column, a member of the new cell keeps the value shared by
every template cell in that column, or falls back to a default when
they differ: an empty string for value, None for choices and False
for nullable.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._TableApp"></a>

## \_TableApp Objects

```python
class _TableApp(_NavApp[list[list[Optional[str]]]])
```

Editable grid returning every cell the user left.

Read-only columns show fixed text in the template rows. Editable
cells are a text input, or a drop-down when the cell offers choices.
An empty editable cell is reported as None when the cell is nullable
and as an empty string for a free-text cell, while a drop-down is
blank only when the cell is nullable.

When min_rows and max_rows are both given the table has a variable
number of rows: an Add row and a Remove row button grow the table up
to max_rows and shrink it down to min_rows. Every cell in an added
row is editable, even in a read-only column, and its descriptor comes
from _new_row_template().

<a id="tableio_cfg_json.wizard_ui_bridge_textual._TableApp.__init__"></a>

#### \_\_init\_\_

```python
def __init__(columns: Sequence[TableColumn],
             cells: list[list[TableCell]],
             question: str,
             messages: list[str],
             partial_check: Optional[PartialCheck],
             min_rows: Optional[int] = None,
             max_rows: Optional[int] = None) -> None
```

Store the columns, starting rows, prompt, check and bounds.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._TableApp.compose"></a>

#### compose

```python
def compose() -> ComposeResult
```

Lay out the header, the editable grid, the buttons and footer.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._TableApp.on_mount"></a>

#### on\_mount

```python
def on_mount() -> None
```

Size the grid, keep the scroll unfocused, focus a cell.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._TableApp._focus_first_cell"></a>

#### \_focus\_first\_cell

```python
def _focus_first_cell() -> None
```

Move focus to the first editable cell of the first row.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._TableApp._grid_cells"></a>

#### \_grid\_cells

```python
def _grid_cells() -> Iterator[Widget]
```

Yield the header labels and then the rows, top to bottom.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._TableApp._row_widgets"></a>

#### \_row\_widgets

```python
def _row_widgets(row: int) -> Iterator[Widget]
```

Yield the widgets of one data row, left to right.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._TableApp._is_readonly"></a>

#### \_is\_readonly

```python
def _is_readonly(row: int, col: int) -> bool
```

Return whether a cell shows fixed text instead of a widget.

Cells in added rows are always editable, even in a column that is
read-only in the template rows.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._TableApp._cell_widget"></a>

#### \_cell\_widget

```python
def _cell_widget(row: int, col: int) -> Widget
```

Return the widget shown for one cell of the grid.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._TableApp._on_input"></a>

#### \_on\_input

```python
@on(Input.Changed)
def _on_input(event: Input.Changed) -> None
```

Re-check the table after a text cell changes.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._TableApp._on_select"></a>

#### \_on\_select

```python
@on(Select.Changed)
def _on_select(event: Select.Changed) -> None
```

Re-check the table after a drop-down cell changes.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._TableApp._recheck"></a>

#### \_recheck

```python
def _recheck(position: Optional[tuple[int, int]]) -> None
```

Update the changed cell and show any partial-check message.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._TableApp.action_submit"></a>

#### action\_submit

```python
def action_submit() -> None
```

Exit returning every cell, including the read-only columns.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._TableApp._submit_clicked"></a>

#### \_submit\_clicked

```python
@on(Button.Pressed, '#submit')
def _submit_clicked(_event: Button.Pressed) -> None
```

Submit the table when the submit button is pressed.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._TableApp._add_clicked"></a>

#### \_add\_clicked

```python
@on(Button.Pressed, '#add_row')
def _add_clicked(_event: Button.Pressed) -> None
```

Add a row when the add-row button is pressed.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._TableApp._remove_clicked"></a>

#### \_remove\_clicked

```python
@on(Button.Pressed, '#remove_row')
def _remove_clicked(_event: Button.Pressed) -> None
```

Remove the last row when the remove-row button is pressed.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._TableApp._add_row"></a>

#### \_add\_row

```python
def _add_row() -> None
```

Append one editable row, up to max_rows.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._TableApp._remove_row"></a>

#### \_remove\_row

```python
def _remove_row() -> None
```

Remove the last row, down to min_rows.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._TableApp._set_status"></a>

#### \_set\_status

```python
def _set_status(message: str) -> None
```

Show a status message below the table.

<a id="tableio_cfg_json.wizard_ui_bridge_textual._TableApp._read_cell"></a>

#### \_read\_cell

```python
def _read_cell(row: int, col: int) -> Optional[str]
```

Return the current value of one cell for the result table.

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

<a id="tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual.ask_text"></a>

#### ask\_text

```python
def ask_text(question: str,
             re_ask_reason: Optional[str] = None,
             nullable: bool = False) -> Optional[str]
```

Ask for free text; see WizardUiBridge.ask_text.

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

<a id="tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual._run"></a>

#### \_run

```python
def _run(app: _NavApp[_T]) -> _T
```

Run one screen and translate its outcome.

A recorded navigation request is re-raised. A screen that ends
with no value, such as the built-in quit, is treated as an
abort.

<a id="tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual._launch"></a>

#### \_launch

```python
def _launch(app: _NavApp[_T]) -> Optional[_T]
```

Run the app and return its result.

This is the only place that drives the terminal, so tests
override it to exercise the bridge without a real terminal.

<a id="tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual._collect"></a>

#### \_collect

```python
def _collect(re_ask_reason: Optional[str]) -> list[str]
```

Drain buffered messages and append any re-ask reason.

<a id="tableio_cfg_json.wizard_ui_bridge_textual.WizardUiBridgeTextual._drain_messages"></a>

#### \_drain\_messages

```python
def _drain_messages() -> list[str]
```

Return and clear buffered show() and diagnostic lines.

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

<a id="tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole.ask_text"></a>

#### ask\_text

```python
def ask_text(question: str,
             re_ask_reason: Optional[str] = None,
             nullable: bool = False) -> Optional[str]
```

Ask for free text on the console; see WizardUiBridge.ask_text.

<a id="tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole.ask_yes_no"></a>

#### ask\_yes\_no

```python
def ask_yes_no(question: str,
               default: bool,
               re_ask_reason: Optional[str] = None) -> bool
```

Ask a yes/no question on the console; see ask_yes_no.

<a id="tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole.ask_table"></a>

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

Ask the user to fill a table on the console; see ask_table.

<a id="tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole._ask_raw"></a>

#### \_ask\_raw

```python
def _ask_raw(question: str,
             re_ask_reason: Optional[str] = None,
             choices: Optional[Sequence[str]] = None) -> str | int
```

Emit one question and read a navigation-checked raw answer.

Returns the entered text, or a 0-based index into choices when
choices are offered, like the deprecated WizardUiBridge.ask().

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

<a id="tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole._emit_question"></a>

#### \_emit\_question

```python
def _emit_question(question: str, re_ask_reason: Optional[str],
                   lines: Sequence[str]) -> None
```

Print one question, any re-ask reason, choices and the prompt.

<a id="tableio_cfg_json.wizard_ui_bridge_console.WizardUiBridgeConsole._read_answer"></a>

#### \_read\_answer

```python
def _read_answer(question: str) -> str
```

Read one navigation-checked answer line from the input stream.

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

<a id="tableio_cfg_json.wizard_ui_bridge_console._to_index"></a>

#### \_to\_index

```python
def _to_index(text: str) -> str | int
```

Map a numeric menu answer to a 0-based index, else keep the text.

<a id="tableio_cfg_json.wizard_ui_bridge_console._menu_lines"></a>

#### \_menu\_lines

```python
def _menu_lines(choices: Optional[Sequence[str]],
                marked: Optional[Sequence[str]] = None) -> list[str]
```

Return the numbered menu lines, marking any choice in marked.

<a id="tableio_cfg_json.wizard_ui_bridge_console._multi_question"></a>

#### \_multi\_question

```python
def _multi_question(question: str) -> str
```

Return the multi-choice question with an entry hint appended.

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

Run the endpoint steps until the configuration validates.

Back steps to the previous question, restoring the data from before
it. Cancel-level returns to the first step, the format question that
opened the later option questions, and discards the answers given
after it. Raised at the format question it propagates out, so the
application can handle the level enclosing this endpoint.

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
                     specs: tuple[ConfigSpec, ...],
                     result: list[list[Optional[str]]]) -> dict[str, object]
```

Return data with one section rebuilt from a filled-in table.

<a id="tableio_cfg_json.wizard._resolve_member_value"></a>

#### \_resolve\_member\_value

```python
def _resolve_member_value(spec: ConfigSpec, raw: str) -> object
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
def _ask_format(capabilities: Capabilities, ui_bridge: WizardUiBridge) -> str
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
def _ask_implementation(impl_names: Sequence[str],
                        ui_bridge: WizardUiBridge) -> Optional[str]
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

<a id="tableio_cfg_json.wizard_ui_factory._is_tty"></a>

#### \_is\_tty

```python
def _is_tty(stream: TextIO) -> bool
```

Return whether a stream reports that it is a terminal.

