# Table of Contents

* [tableio\_cfg\_json.config](#tableio_cfg_json.config)
  * [\_choices](#tableio_cfg_json.config._choices)
  * [\_format\_choices](#tableio_cfg_json.config._format_choices)
  * [\_impl\_choices](#tableio_cfg_json.config._impl_choices)
  * [\_paper\_choices](#tableio_cfg_json.config._paper_choices)
  * [\_align\_choices](#tableio_cfg_json.config._align_choices)
  * [\_quoting\_choices](#tableio_cfg_json.config._quoting_choices)
  * [\_latex\_doc\_choices](#tableio_cfg_json.config._latex_doc_choices)
  * [\_raise\_invalid](#tableio_cfg_json.config._raise_invalid)
  * [\_optional\_string](#tableio_cfg_json.config._optional_string)
  * [\_optional\_choice](#tableio_cfg_json.config._optional_choice)
  * [\_optional\_int\_at\_least](#tableio_cfg_json.config._optional_int_at_least)
  * [\_none\_members](#tableio_cfg_json.config._none_members)
  * [TioWholeValidator](#tableio_cfg_json.config.TioWholeValidator)
    * [validate](#tableio_cfg_json.config.TioWholeValidator.validate)
  * [\_issue\_message](#tableio_cfg_json.config._issue_message)
  * [\_one\_char\_validator](#tableio_cfg_json.config._one_char_validator)
  * [\_non\_empty\_validator](#tableio_cfg_json.config._non_empty_validator)
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

Config-as-json bridge for framework-neutral tableio configuration.

<a id="tableio_cfg_json.config._choices"></a>

#### \_choices

```python
def _choices(name: str) -> tuple[str, ...]
```

Return advertised choices for one tableio configuration member.

<a id="tableio_cfg_json.config._format_choices"></a>

#### \_format\_choices

```python
def _format_choices() -> tuple[str, ...]
```

Return currently registered tableio format names.

<a id="tableio_cfg_json.config._impl_choices"></a>

#### \_impl\_choices

```python
def _impl_choices() -> tuple[str, ...]
```

Return currently registered tableio implementation names.

<a id="tableio_cfg_json.config._paper_choices"></a>

#### \_paper\_choices

```python
def _paper_choices() -> tuple[str, ...]
```

Return advertised paper size values.

<a id="tableio_cfg_json.config._align_choices"></a>

#### \_align\_choices

```python
def _align_choices() -> tuple[str, ...]
```

Return advertised text table alignment values.

<a id="tableio_cfg_json.config._quoting_choices"></a>

#### \_quoting\_choices

```python
def _quoting_choices() -> tuple[str, ...]
```

Return advertised CSV quoting values.

<a id="tableio_cfg_json.config._latex_doc_choices"></a>

#### \_latex\_doc\_choices

```python
def _latex_doc_choices() -> tuple[str, ...]
```

Return advertised LaTeX document class values.

<a id="tableio_cfg_json.config._raise_invalid"></a>

#### \_raise\_invalid

```python
def _raise_invalid(message: str, stderr_file: TextIO) -> NoReturn
```

Write one validation message and raise InvalidConfiguration.

<a id="tableio_cfg_json.config._optional_string"></a>

#### \_optional\_string

```python
def _optional_string() -> OptionalMemberValidator
```

Return a validator for an optional string member.

<a id="tableio_cfg_json.config._optional_choice"></a>

#### \_optional\_choice

```python
def _optional_choice(
        choices: Callable[[], tuple[str, ...]]) -> OptionalMemberValidator
```

Return a validator for an optional string with known choices.

<a id="tableio_cfg_json.config._optional_int_at_least"></a>

#### \_optional\_int\_at\_least

```python
def _optional_int_at_least(min_value: int) -> OptionalMemberValidator
```

Return a validator for an optional integer lower bound.

<a id="tableio_cfg_json.config._none_members"></a>

#### \_none\_members

```python
def _none_members(config: object, names: list[str]) -> list[str]
```

Return member names whose current value is None.

<a id="tableio_cfg_json.config.TioWholeValidator"></a>

## TioWholeValidator Objects

```python
class TioWholeValidator(WholeConfigValidator)
```

Validate the complete bridge object with tableio rules.

<a id="tableio_cfg_json.config.TioWholeValidator.validate"></a>

#### validate

```python
def validate(config: Config, stderr_file: TextIO = sys.stderr) -> None
```

Validate one complete tableio JSON configuration.

<a id="tableio_cfg_json.config._issue_message"></a>

#### \_issue\_message

```python
def _issue_message(error: ConfigError) -> str
```

Return one compact config-as-json message from tableio issues.

<a id="tableio_cfg_json.config._one_char_validator"></a>

#### \_one\_char\_validator

```python
def _one_char_validator() -> OptionalMemberValidator
```

Return a validator for optional one-character strings.

<a id="tableio_cfg_json.config._non_empty_validator"></a>

#### \_non\_empty\_validator

```python
def _non_empty_validator() -> OptionalMemberValidator
```

Return a validator for optional non-empty strings.

<a id="tableio_cfg_json.config.TioJsonCsvConfig"></a>

## TioJsonCsvConfig Objects

```python
class TioJsonCsvConfig(CsvConfigData, Config)
```

CSV tableio configuration section backed by config-as-json.

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

Initialize the CSV configuration section.

<a id="tableio_cfg_json.config.TioJsonCsvConfig._omit_none_from_json"></a>

#### \_omit\_none\_from\_json

```python
@override
def _omit_none_from_json() -> list[str]
```

Return optional CSV members omitted while set to None.

<a id="tableio_cfg_json.config.TioJsonCsvConfig.parse_converters"></a>

#### parse\_converters

```python
@override
def parse_converters() -> dict[str, ParseConverter]
```

Return JSON read conversions for CSV values.

<a id="tableio_cfg_json.config.TioJsonCsvConfig.get_validation_plan"></a>

#### get\_validation\_plan

```python
def get_validation_plan(stderr_file: TextIO) -> ValidationPlan
```

Return config-as-json validation steps for CSV values.

<a id="tableio_cfg_json.config.TioJsonHtmlConfig"></a>

## TioJsonHtmlConfig Objects

```python
class TioJsonHtmlConfig(HtmlConfigData, Config)
```

HTML tableio configuration section backed by config-as-json.

<a id="tableio_cfg_json.config.TioJsonHtmlConfig.__init__"></a>

#### \_\_init\_\_

```python
def __init__(css_file: Optional[str] = None,
             from_json_data_text: Optional[str] = None,
             from_json_filename: Optional[PathOrStr] = None,
             stderr_file: TextIO = sys.stderr) -> None
```

Initialize the HTML configuration section.

<a id="tableio_cfg_json.config.TioJsonHtmlConfig._omit_none_from_json"></a>

#### \_omit\_none\_from\_json

```python
@override
def _omit_none_from_json() -> list[str]
```

Return optional HTML members omitted while set to None.

<a id="tableio_cfg_json.config.TioJsonHtmlConfig.get_validation_plan"></a>

#### get\_validation\_plan

```python
def get_validation_plan(stderr_file: TextIO) -> ValidationPlan
```

Return config-as-json validation steps for HTML values.

<a id="tableio_cfg_json.config.TioJsonLatexConfig"></a>

## TioJsonLatexConfig Objects

```python
class TioJsonLatexConfig(LatexConfigData, Config)
```

LaTeX tableio configuration section backed by config-as-json.

<a id="tableio_cfg_json.config.TioJsonLatexConfig.__init__"></a>

#### \_\_init\_\_

```python
def __init__(document_class: Optional[str] = None,
             preamble: Optional[str] = None,
             from_json_data_text: Optional[str] = None,
             from_json_filename: Optional[PathOrStr] = None,
             stderr_file: TextIO = sys.stderr) -> None
```

Initialize the LaTeX configuration section.

<a id="tableio_cfg_json.config.TioJsonLatexConfig._omit_none_from_json"></a>

#### \_omit\_none\_from\_json

```python
@override
def _omit_none_from_json() -> list[str]
```

Return optional LaTeX members omitted while set to None.

<a id="tableio_cfg_json.config.TioJsonLatexConfig.get_validation_plan"></a>

#### get\_validation\_plan

```python
def get_validation_plan(stderr_file: TextIO) -> ValidationPlan
```

Return config-as-json validation steps for LaTeX values.

<a id="tableio_cfg_json.config.TioJsonConfig"></a>

## TioJsonConfig Objects

```python
class TioJsonConfig(ConfigData, Config)
```

Complete tableio configuration backed by config-as-json.

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

Initialize a tableio JSON configuration.

<a id="tableio_cfg_json.config.TioJsonConfig.capabilities"></a>

#### capabilities

```python
@property
def capabilities() -> Capabilities
```

Return runtime capabilities used for validation.

<a id="tableio_cfg_json.config.TioJsonConfig.file_access"></a>

#### file\_access

```python
@property
def file_access() -> FileAccess
```

Return runtime file access used for validation.

<a id="tableio_cfg_json.config.TioJsonConfig._omit_none_from_json"></a>

#### \_omit\_none\_from\_json

```python
@override
def _omit_none_from_json() -> list[str]
```

Return optional top-level members omitted while set to None.

<a id="tableio_cfg_json.config.TioJsonConfig.nested_configs"></a>

#### nested\_configs

```python
@override
def nested_configs() -> NestedConfigs
```

Return nested tableio configuration section declarations.

<a id="tableio_cfg_json.config.TioJsonConfig.get_validation_plan"></a>

#### get\_validation\_plan

```python
def get_validation_plan(stderr_file: TextIO) -> ValidationPlan
```

Return config-as-json validation steps for top-level values.

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

Return a default tableio configuration backed by config-as-json.

