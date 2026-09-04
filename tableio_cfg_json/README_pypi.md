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
- You want an interactive wizard that asks a user for the TableIO
  configuration.
- You want your users to edit stored TableIO configuration in an
  [edit-cfg-json](https://pypi.org/project/edit-cfg-json/) editor, without
  writing the TableIO documentation down a second time.

This package is probably not the right one when:

- You are looking for the table reader or writer itself. Use
  [TableIO](https://pypi.org/project/tableio/) directly.
- Your program always uses one hard-coded table format and has no persistent
  configuration.
- You do not want to use config-as-json for configuration files.
- You only want the wizard user interface bridge. That is now the separate
  package [wizard-ui-bridge](https://pypi.org/project/wizard-ui-bridge/),
  which does not depend on TableIO. See *The wizard UI bridge moved* below.

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

Please see the [teaching examples](https://github.com/tom-bjorkholm/tableio_cfg_json/blob/master/tableio_cfg_json/example/src/tableio_cfg_example/README.md) for a more
thorough introduction.

## Main entry points

- `TioJsonConfig`
  Complete JSON-backed TableIO configuration for one endpoint. It can read
  JSON, write JSON and be passed to TableIO as normal configuration data.

- `tio_config_create()`
  TableIO's own function for creating a TableIO object. Import it from
  `tableio` and pass it a `TioJsonConfig` object.

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

- `tio_json_descriptions()` and `TIO_JSON_DESCRIPTIONS`
  What each configuration member means, as an `edit_cfg_json.Descriptions`
  mapping. See *Editing the configuration* below.

- `tio_json_loader()`
  How an `edit-cfg-json` editor constructs a `TioJsonConfig`.

- `tio_json_read_loader`, `tio_json_create_loader` and
  `tio_json_update_loader`
  Ready-made loaders, one per file access, for a program that needs a name to
  point at rather than a call to make.

- `WizardUiBridge`, `WizardUiBridgeConsole`, `WizardUiBridgeTextual` and
  `make_text_ui_bridge`
  Interfaces for connecting the wizard to a console, GUI or scripted UI.
  These now live in
  [wizard-ui-bridge](https://pypi.org/project/wizard-ui-bridge/) and are
  only re-exported here, deprecated. See *The wizard UI bridge moved*.

## Editing the configuration

The [edit-cfg-json](https://pypi.org/project/edit-cfg-json/) family gives an
application a folding editor for a config-as-json configuration object. It
discovers the editable structure by introspection, so the configuration is
never described a second time to get one. The editors an end user sees are
[edit-cfg-json-tk](https://pypi.org/project/edit-cfg-json-tk/) and
[edit-cfg-json-textual](https://pypi.org/project/edit-cfg-json-textual/).

What that editor cannot work out is what a member is *for*, which values a
plain string member accepts and what those values mean, because it reads the
class and never a validator. `tio_json_descriptions()` is the one source of
truth for that text, so an application that stores TableIO configuration does
not repeat the TableIO documentation and cannot have it drift:

```python
from edit_cfg_json import edit
from edit_cfg_json_textual import TextualEditor
from tableio import FileAccess, access_capabilities
from tableio_cfg_json import TIO_JSON_DESCRIPTIONS, tio_json_config_default, \
    tio_json_loader

file_access = FileAccess.CREATE
capabilities = access_capabilities(file_access)
config = tio_json_config_default(capabilities, file_access,
                                 include_all_options=True)
saved = edit(config, TextualEditor(),
             descriptions=TIO_JSON_DESCRIPTIONS,
             in_file='tableio.cfg',
             loader=tio_json_loader(capabilities, file_access))
```

`tio_json_loader()` is needed because `TioJsonConfig` takes the runtime
capabilities and file access that no configuration file holds, so the editor
cannot construct it on its own.

A program that is told a name rather than making a call — such as the
`--loader` option of `python3 -m edit_cfg_json.dump` — uses one of the
ready-made loaders instead. There is one per file access, and which one is
right is the caller's to know, because the access is not in the file:

```sh
python3 -m edit_cfg_json.dump --module tableio_cfg_json \
  --loader tio_json_create_loader --descriptions TIO_JSON_DESCRIPTIONS \
  --input tableio.cfg --unfold
```

An application that nests `TioJsonConfig` inside its own configuration class
needs no loader, and passes the path of the member that holds each endpoint:

```python
descriptions = {**own_descriptions,
                **tio_json_descriptions(('input',)),
                **tio_json_descriptions(('output',))}
```

A member that is not in the configuration file is not a row in the editor, so
`tio_json_loader()` builds on a complete set of defaults by default. The
editor then marks every value the file did not hold, and a compact
configuration file opens with everything there is to set. Pass
`include_all_options=False` to keep an edited file as compact as it was.

## The wizard UI bridge moved

The wizard user interface bridge is now the separate package
[wizard-ui-bridge](https://pypi.org/project/wizard-ui-bridge/), so that a
wizard that has nothing to do with TableIO does not have to install TableIO
and everything TableIO depends on. `tableio-cfg-json` depends on
`wizard-ui-bridge[textual]`, so nothing changes at install time.

Programs keep working unchanged: every moved name is still available from
`tableio_cfg_json`. Each use of an old name raises a
`tableio_cfg_json.WizardUiBridgeMoved` warning, which is a
`DeprecationWarning`, so it is hidden from end users by default and shown
by pytest and unittest. The old names are removed in a later release,
tentatively `tableio-cfg-json` 2.0, so please change the imports:

| Old import | New import |
| --- | --- |
| `from tableio_cfg_json import <name>` | `from wizard_ui_bridge import <name>` |
| `tableio_cfg_json.wizard_ui_bridge` | `wizard_ui_bridge.bridge` |
| `tableio_cfg_json.wizard_ui_bridge_arg_types` | `wizard_ui_bridge.arg_types` |
| `tableio_cfg_json.wizard_ui_bridge_console` | `wizard_ui_bridge.console` |
| `tableio_cfg_json.wizard_ui_bridge_form_defs` | `wizard_ui_bridge.form_defs` |
| `tableio_cfg_json.wizard_ui_bridge_textual` | `wizard_ui_bridge.textual_bridge` |
| `tableio_cfg_json.wizard_ui_factory` | `wizard_ui_bridge.factory` |

Add `wizard-ui-bridge` to your own dependencies when you import from it,
and `wizard-ui-bridge[textual]` when you use the Textual bridge, because
Textual is an optional extra of that package.

To find every remaining old import, make them fail instead of warn in one
of these ways:

- Set the environment variable `WIZARD_UI_BRIDGE_STRICT` to any non-empty
  value. Every old name then raises `ImportError` naming its replacement.
  This works for any program, with or without tests.
- Run pytest with `-W error::tableio_cfg_json.WizardUiBridgeMoved`, or put
  that line under `filterwarnings` in your pytest configuration. Note that
  the interpreter's own `-W` and `PYTHONWARNINGS` cannot be used for this
  category, because they are resolved before `tableio_cfg_json` can be
  imported; use `WIZARD_UI_BRIDGE_STRICT` there.

### Source code repo history

The wizard UI bridge `wizard-ui-bridge` code used to be part of
`tableio-cfg-json` git repo, but has been split out.

The two git repos
[https://github.com/tom-bjorkholm/wizard-ui-bridge](https://github.com/tom-bjorkholm/wizard-ui-bridge)
and
[https://github.com/tom-bjorkholm/tableio_cfg_json](https://github.com/tom-bjorkholm/tableio_cfg_json)
share a common history. Up until version 1.1 there was only one repo.
Now that repo is split in two, and each repo holds only code for its
package. However, both repos have the common history.

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

### A diagnostic names the whole path

A message about a refused value names the path from the top of the
configuration down to that value, and not just the local member name. A
delimiter refused in the CSV section is `csv.delimiter`, and the same
delimiter in an endpoint that an application configuration calls `input` is
`input.csv.delimiter`. This matters because every endpoint declares the same
member names, so a message naming only `delimiter` would leave the user
guessing which endpoint it was about.

The TableIO whole-configuration rules take part in the same naming. TableIO
reports an issue under its own dotted parameter name, such as
`csv.quoting`, and that name is joined onto the path of the endpoint it came
from, so an application configuration reports
`not_less_than_output.implementation`.

`TioJsonConfig`, the three section classes and `tio_json_config_default()`
all take a `member_name` keyword for this, and so does `tio_json_loader()`.
A whole configuration file is a member of nothing and leaves it out.

## Nested application configs

`TioJsonConfig` can be used as the whole configuration file for a small
program, or as a nested member inside a larger config-as-json application
configuration. This is useful when one application has several TableIO
endpoints, for example one input table and two independently configured
output tables.

For larger configs, create each nested `TioJsonConfig` with the capabilities
and file access for that endpoint. A read endpoint and a create endpoint may
need different defaults and may validate different implementations.

Because the two endpoints differ, the application declares each of them with
a `config_as_json.ConfigFactory` of its own, or one factory that reads the
`member_name` it is called with. Passing that `member_name` on to
`TioJsonConfig` is what names the endpoint in its diagnostics; a factory
that does not accept it is called without it and config-as-json warns that
it should be changed.

The teaching examples show both styles.

## Documentation

- Teaching examples and walkthroughs: [tableio_cfg_json/example/src/tableio_cfg_example/README.md](https://github.com/tom-bjorkholm/tableio_cfg_json/blob/master/tableio_cfg_json/example/src/tableio_cfg_example/README.md)

- Public API notes: [doc/tableio_cfg_json_api.md](https://github.com/tom-bjorkholm/tableio_cfg_json/blob/master/doc/tableio_cfg_json_api.md)

- Protected/internal API notes: [doc/tableio_cfg_json_protected_api.md](https://github.com/tom-bjorkholm/tableio_cfg_json/blob/master/doc/tableio_cfg_json_protected_api.md)

- Source repository: [tableio_cfg_json](https://github.com/tom-bjorkholm/tableio_cfg_json/)

## License

MIT

## Test summary

- Test result: 646 passed in 49s
- No flake8 warnings.
- No mypy errors found.
- No pylint warnings.
- No python layout warnings.
- Built version(s): 1.4
- Build and test using Python 3.12.10
