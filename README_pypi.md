# tableio-cfg-json

`tableio-cfg-json` stores
[TableIO](https://pypi.org/project/tableio/) configuration as validated JSON
by using [config-as-json](https://pypi.org/project/config-as-json/).

Use it when an application uses TableIO for table-like files and wants
persistent, user-editable configuration for formats, implementations and
format-specific options. The configuration objects are both TableIO
`ConfigData` objects and config-as-json `Config` objects, so the same object
can be written as configuration file (as JSON), read back later, validated,
and passed to TableIO.

## Is this package for you?

This package is a good fit when one or more of these apply:

- Your application uses TableIO.
- You already use config-as-json, or can accept using it for persistent
  configuration.
- You want one configuration file to describe one TableIO input or output
  endpoint.
- You want to nest one or more TableIO endpoint configurations inside a
  larger application configuration file.
- You want validation and generated user documentation for the TableIO
  options that are relevant to your application's capabilities.

This package is probably not the right one when:

- You are looking for the table reader or writer itself. Use
  [TableIO](https://pypi.org/project/tableio/) directly.
- Your program always uses one hard-coded table format and has no persistent
  configuration.
- You do not want to use config-as-json for configuration files.

## Installation

`tableio-cfg-json` requires Python 3.12 or newer.

```sh
pip install --upgrade tableio-cfg-json
```

## Quick start

Create a compact JSON configuration file for one TableIO endpoint:

```python
from pathlib import Path
import sys

from tableio import FileAccess, access_capabilities
from tableio_cfg_json import tio_json_config_default

config_file = Path('tableio.cfg')
file_access = FileAccess.CREATE
capabilities = access_capabilities(file_access, error_file=sys.stderr)
config = tio_json_config_default(capabilities=capabilities,
                                 file_access=file_access,
                                 format_name='CSV')
config.write(to_json_filename=config_file)
```

For CSV this writes a small file like:

```json
{
    "format_name": "CSV"
}
```

Read the configuration back and use it with TableIO:

```python
from pathlib import Path
import sys

from tableio import FileAccess, access_capabilities, tio_config_create
from tableio_cfg_json import TioJsonConfig

config_file = Path('tableio.cfg')
table_file = Path('capitals.csv')
file_access = FileAccess.CREATE
capabilities = access_capabilities(file_access, error_file=sys.stderr)
config = TioJsonConfig(capabilities=capabilities,
                       file_access=file_access,
                       from_json_filename=config_file)
with tio_config_create(config=config, file_name=table_file,
                       file_access=file_access,
                       capabilities=capabilities) as table_io:
    table_io.write_table_listdata([
        ['Capital', 'Country'],
        ['Copenhagen', 'Denmark']
    ])
```

If `implementation` is omitted, TableIO chooses a matching implementation at
runtime. If the user wants to lock down a specific implementation, it can be
stored explicitly in JSON.

Optional settings can be added at the top level or in format-specific nested
sections such as `csv`, `html` and `latex`. Compact output omits unset
optional values, while template-style output can include all current default
options.

Please see the [teaching examples](https://bitbucket.org/tom-bjorkholm/tableio_cfg_json/src/master/example/src/example/README.md) for a more
thorough introduction.

## Main entry points

- `TioJsonConfig`
  Complete JSON-backed TableIO configuration for one endpoint. It can read
  JSON, write JSON and be passed to TableIO as normal configuration data.

- `tio_config_create()` create a TableIO object from a `TioJsonConfig`
  object.

### Helpers and details

- `tio_json_config_default()`
  Create a validated default `TioJsonConfig` using TableIO's recommended
  choices for the requested capabilities and file access.

- `TioJsonCsvConfig`, `TioJsonHtmlConfig`, `TioJsonLatexConfig`
  Optional nested configuration sections for format-specific settings.

- `describe_config()`, `describe_config_members()`,
  `describe_config_reference()`, `describe_config_example()`,
  `get_config_member_names()` and `get_general_cfg_info()`
  Helpers for generating plain text syntax guides for configuration files.

- `tio_json_config_wizard()`
  Interactive helper for creating one TableIO endpoint configuration through
  a user interface bridge.

- `WizardUiBridge`, `WizardUiBridgeConsole`, `WizardUiBridgeTextual` and
  `make_text_ui_bridge`
  Interfaces for connecting the wizard to a console, GUI or scripted UI.

## Validation model

The configuration file (in JSON) stores durable TableIO choices such
as `format_name`, `implementation`, character encoding, presentation
options and format-specific settings. Runtime values such as the actual
file name are not stored in this configuration.

Validation happens in two layers:

- config-as-json validates JSON structure, member names and member value
  types.
- TableIO validates whether the selected format, implementation,
  capabilities and file access can work together.

Choice values are matched case-insensitively where TableIO defines a finite
set of choices. For example, configuration file may use `excel` and the
config object will store TableIO's normal `Excel` spelling after validation.

## Nested application configs

`TioJsonConfig` can be used as the whole configuration file for a small
program, or as a nested member inside a larger config-as-json application
configuration. This is useful when one application has several TableIO
endpoints, for example one input table and two independently configured
output tables.

For larger configs, create each nested `TioJsonConfig` with the capabilities
and file access for that endpoint. A read endpoint and a create endpoint may
need different defaults and may validate different implementations.

The teaching examples show both styles.

## Documentation

- Teaching examples and walkthroughs: [example/src/example/README.md](https://bitbucket.org/tom-bjorkholm/tableio_cfg_json/src/master/example/src/example/README.md)

- Public API notes: [doc/api.md](https://bitbucket.org/tom-bjorkholm/tableio_cfg_json/src/master/doc/api.md)

- Protected/internal API notes: [doc/protected_api.md](https://bitbucket.org/tom-bjorkholm/tableio_cfg_json/src/master/doc/protected_api.md)

- Source repository: [tableio_cfg_json](https://bitbucket.org/tom-bjorkholm/tableio_cfg_json/)

## License

MIT

## Test summary

- Test result: 498 passed in 44s
- No flake8 warnings.
- No mypy errors found.
- No python layout warnings.
- Built version(s): 0.5
- Build and test using Python 3.13.7
