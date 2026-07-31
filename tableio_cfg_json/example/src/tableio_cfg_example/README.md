# tableio-cfg-json teaching examples

## Introduction

These examples show how four packages fit together:

- `tableio` reads and writes table-like files.
- `config-as-json` reads and writes validated JSON configuration objects.
- `tableio-cfg-json` connects them by making TableIO configuration available
  as config-as-json configuration classes.
- `wizard-ui-bridge` defines how a wizard can talk to any user interface and
  is used by the wizard in `tableio-cfg-json`.

The examples are meant to be read in order by a fluent Python programmer who
is new to these APIs. The first class (e01–e04) uses one TableIO endpoint
config at a time. The second class (e05–e06) shows a more realistic
application config that owns several TableIO endpoint configs and also has
application-specific settings, built directly in code. A set of interactive
wizard examples then produces that same application config by asking the user
questions.

TableIO, config-as-json and wizard-ui-bridge have their own larger example sets:

- TableIO: [https://pypi.org/project/tableio/](https://pypi.org/project/tableio/)
- config-as-json: [https://pypi.org/project/config-as-json/](https://pypi.org/project/config-as-json/)
- wizard-ui-bridge: [https://pypi.org/project/wizard-ui-bridge/](https://pypi.org/project/wizard-ui-bridge/)

The examples here focus only on the bridge supplied by `tableio-cfg-json`. The
user interface bridge used by the wizard examples is its own package; see
[wizard_ui_bridge/example/src/wizard_ui_example](https://github.com/tom-bjorkholm/tableio_cfg_json/blob/master/wizard_ui_bridge/example/src/wizard_ui_example).

## Class A: One TableIO Endpoint Config

The first class teaches the smallest useful shape: one JSON configuration file
describes one TableIO input or output endpoint. This is the best place to
start, because the application config and the TableIO config are the same
thing.

### Class A: Example Programs

The example source files are:

- [`e01_create_config.py`](https://github.com/tom-bjorkholm/tableio_cfg_json/blob/master/tableio_cfg_json/example/src/tableio_cfg_example/e01_create_config.py)
  writes a JSON configuration file and a plain text syntax guide for that
  file.
- [`e02_write_table.py`](https://github.com/tom-bjorkholm/tableio_cfg_json/blob/master/tableio_cfg_json/example/src/tableio_cfg_example/e02_write_table.py)
  reads a write-capable JSON config and writes a small table with the columns
  `Capital`, `Country` and `Continent`.
- [`e03_read_table.py`](https://github.com/tom-bjorkholm/tableio_cfg_json/blob/master/tableio_cfg_json/example/src/tableio_cfg_example/e03_read_table.py)
  reads a read-capable JSON config and prints an existing table as
  tab-separated text.
- [`e04_custom_config.py`](https://github.com/tom-bjorkholm/tableio_cfg_json/blob/master/tableio_cfg_json/example/src/tableio_cfg_example/e04_custom_config.py)
  starts from the same kind of default config as `e01_create_config.py`, then
  stores a few explicit non-default values. It also shows how to discover
  which members can be set.

### CSV Walkthrough

CSV is the easiest format to inspect because the output file is plain text.
The same CSV configuration can be used for writing and reading:

```sh
python -m tableio_cfg_example.e01_create_config \
  --cfg capitals-csv.json \
  --txt capitals-csv-syntax.txt \
  --write \
  --format CSV

python -m tableio_cfg_example.e02_write_table \
  --cfg capitals-csv.json \
  --output capitals.csv

python -m tableio_cfg_example.e03_read_table \
  --cfg capitals-csv.json \
  --input capitals.csv
```

The first command writes a compact config. Add `--complete` if you want a
template where optional defaults are visible:

```sh
python -m tableio_cfg_example.e01_create_config \
  --cfg capitals-csv-complete.json \
  --txt capitals-csv-complete-syntax.txt \
  --write \
  --format CSV \
  --complete
```

### Custom Configuration Walkthrough

The compact config from `e01_create_config.py` only stores durable choices
that need to be fixed. `e04_custom_config.py` shows the next step: start from
the same default object and then set a few values before writing the JSON
file.

```sh
python -m tableio_cfg_example.e04_custom_config \
  --cfg capitals-custom-csv.json \
  --txt capitals-custom-csv-syntax.txt \
  --write \
  --format CSV \
  --csv-delimiter : \
  --encoding utf-8 \
  --alignment CENTER

python -m tableio_cfg_example.e02_write_table \
  --cfg capitals-custom-csv.json \
  --output capitals-custom.csv
```

The CSV delimiter is stored in the optional nested `csv` section. If you use
the same option while creating an Excel config, the value is still valid JSON
configuration, but it has no effect when TableIO later uses an Excel backend.

The syntax guide this example writes ends with a "Discovering what can be set"
section. It is built from three helpers that answer "what can I set?":
`get_config_member_names()` lists the member names for the access mode,
`describe_config_members()` explains each member, and
`describe_config_reference()` gives the allowed values for a chosen list of
names.

### Excel Walkthrough

Excel is a useful second format because TableIO commonly uses one
implementation for writing and another for reading. For that reason the
walkthrough creates two config files:

```sh
python -m tableio_cfg_example.e01_create_config \
  --cfg capitals-excel-write.json \
  --txt capitals-excel-write-syntax.txt \
  --write \
  --format Excel

python -m tableio_cfg_example.e01_create_config \
  --cfg capitals-excel-read.json \
  --txt capitals-excel-read-syntax.txt \
  --read \
  --format Excel

python -m tableio_cfg_example.e02_write_table \
  --cfg capitals-excel-write.json \
  --output capitals.xlsx

python -m tableio_cfg_example.e03_read_table \
  --cfg capitals-excel-read.json \
  --input capitals.xlsx
```

This is an important point for real programs: the JSON file stores durable
TableIO choices such as `format_name`, and may also store an explicit
`implementation` when the user wants to lock one down. When `implementation`
is omitted, TableIO selects the best matching implementation at runtime.

### Class A: What To Look For In The Code

The configuration creator shows how to ask TableIO for a recommended default
configuration and then write that object as JSON. In compact output, an
unselected implementation is omitted so TableIO can choose at runtime:

```python
config = tio_json_config_default(capabilities=capabilities,
                                 file_access=file_access,
                                 format_name=format_name,
                                 include_all_options=complete)
config.write(to_json_filename=config_file)
```

The writer and reader show the bridge in the other direction:

```python
capabilities = access_capabilities(file_access, error_file=sys.stderr)
config = TioJsonConfig(capabilities=capabilities, file_access=file_access,
                       from_json_filename=config_file)
with tio_config_create(config=config, file_name=table_file,
                       file_access=file_access,
                       capabilities=capabilities) as tableio:
    ...
```

The resulting config supplies durable TableIO choices such as format and any
explicit optional settings. `tio_config_create()` then validates those choices
for the runtime task, filters the format-specific optional settings, and
returns the actual TableIO backend object.

## Class B: Application Config With Several TableIO Endpoints

The second class is closer to a real application. One JSON configuration file
has three nested TableIO endpoint configs and two application-owned settings:
the column used for splitting rows and the string limit used by the split.

The task done by the example programs in class B is trivial:
It reads a table with many rows and each row has the three columns `City`,
`Country` and `Continent`. The example program can be configured to read this
input from different file formats (like Excel, CSV, ODS) and with different
parameters for the format like character encoding, delimiter and so on.

The example program can be configured to split this list into two lists based
on a configurable criteria: a configured column has a value that is less than
or not less than a configured string.
The output formats for the less than output and not less than output are
configured independently. Each can be any format TableIO supports with any
parameters TableIO supports.

The application config is built directly in code first (`e05_app_config.py`),
before any wizard is introduced. Building it in code makes the point that the
config object is ordinary data: the interactive wizards shown further down
produce the very same object, and nothing about the config depends on a
wizard.

### Class B: Example Programs

The core example source files are:

- [`e05_app_config.py`](https://github.com/tom-bjorkholm/tableio_cfg_json/blob/master/tableio_cfg_json/example/src/tableio_cfg_example/e05_app_config.py)
  defines the `SplitCitiesConfig` application config, builds one instance in
  code, and writes the larger JSON application configuration plus its syntax
  guide. To show that the endpoints are configured independently, the two
  outputs use different formats: the less-than output is CSV and the
  not-less-than output is ODS.
- [`e06_split_cities.py`](https://github.com/tom-bjorkholm/tableio_cfg_json/blob/master/tableio_cfg_json/example/src/tableio_cfg_example/e06_split_cities.py)
  reads the larger JSON configuration, reads a city table as dictionaries,
  and writes two independently configured output tables.

### Application Config Walkthrough

First build the application config and the matching syntax guide. There is no
user interaction here, so the command needs no input:

```sh
python -m tableio_cfg_example.e05_app_config \
  --cfg split-cities.json \
  --txt split-cities-syntax.txt
```

Then run the splitter. File paths are command-line arguments because they are
runtime values, not durable configuration. The output formats come from the
config, so the less-than output is CSV and the not-less-than output is ODS:

```sh
python -m tableio_cfg_example.e06_split_cities \
  --cfg split-cities.json \
  --input example/data/cities_input.csv \
  --less-than-output cities-before-limit.csv \
  --not-less-than-output cities-from-limit.ods
```

The input table is expected to have the header row `City`, `Country`,
`Continent`. The splitter reads the table as dictionaries, so each data row
uses those column names as keys. The comparison is normal case-sensitive
Python string comparison, deliberately kept simple because the teaching point
is configuration composition.

### Sample Data

The repository includes a sample input file:

- [`example/data/cities_input.csv`](https://github.com/tom-bjorkholm/tableio_cfg_json/blob/master/tableio_cfg_json/example/data/cities_input.csv)

It contains three continents, five countries per continent, and two cities per
country. You can use that file to test the walkthrough, or create your own CSV
file with the same `City`, `Country`, `Continent` header.

### Class B: What To Look For In The Code

`SplitCitiesConfig` is an application config class. It owns three nested
`TioJsonConfig` members named `input`, `less_than_output` and
`not_less_than_output`, plus the application-owned members `split_column` and
`split_limit`.

`e05_app_config.py` creates a default `SplitCitiesConfig` and then assigns the
values it wants directly in code, giving each output its own format:

```python
config = SplitCitiesConfig(stderr_file=err_file)
config.input = _default_config(FileAccess.READ, err_file, 'CSV')
config.less_than_output = _default_config(FileAccess.CREATE, err_file, 'CSV')
config.not_less_than_output = _default_config(FileAccess.CREATE, err_file,
                                              'ODS')
config.split_column = 'Country'
config.split_limit = 'M'
```

The runner example reads and writes dict data:

```python
read_result = tableio.read_table_dictdata()
...
tableio.write_table_dictdata(rows, column_order=list(CITY_COLUMNS),
                             missing_ok=True, extra_ok=True)
```

That keeps the application logic focused on named columns instead of numeric
indexes, and shows a second TableIO data shape after the simpler list-data
examples in Class A.

## Building the Application Config Interactively (wizard examples)

The examples below build the same kind of application config by asking the
user questions instead of hard-coding the values. Each uses a `WizardUiBridge`
from the `wizard_ui_bridge` package. These examples teach only the minimal
wizard mechanics they use; that package's own examples teach the rest, and the
matching example is named where each mechanic first appears: bridge selection
(wizard_ui_bridge `e01`), the one-question-at-a-time ask methods
(wizard_ui_bridge `e02`), navigation (wizard_ui_bridge `e03`),
table questions (wizard_ui_bridge `e04`) and whole forms
(wizard_ui_bridge `e05`, `e06`).

The core wizard example source files are:

- [`e07_config_wizard.py`](https://github.com/tom-bjorkholm/tableio_cfg_json/blob/master/tableio_cfg_json/example/src/tableio_cfg_example/e07_config_wizard.py)
  asks questions and writes the same JSON application configuration as
  `e05_app_config.py`. It calls `tio_json_config_wizard()` once for the input
  endpoint and once for each output endpoint, and asks the application's own
  split column and split limit with the bridge's ask methods. It obtains its
  bridge from `make_text_ui_bridge()`: in a real terminal that is a full-screen
  Textual interface, and with redirected input it is the console bridge, so the
  same program is both interactive and scriptable.
- [`e08_edit_config.py`](https://github.com/tom-bjorkholm/tableio_cfg_json/blob/master/tableio_cfg_json/example/src/tableio_cfg_example/e08_edit_config.py)
  reopens a stored application config and re-asks the same items, seeding each
  one with the stored value so pressing Enter keeps it. It reuses the same
  outer navigation loop as `e07_config_wizard.py` to move between the
  application's endpoints, re-opening an earlier endpoint at its last question
  when the user goes back into it.

The advanced capstone pair reinforces these ideas with an extra table
question. It introduces no new core concept, so read the earlier examples
first:

- [`e09_rename_wizard.py`](https://github.com/tom-bjorkholm/tableio_cfg_json/blob/master/tableio_cfg_json/example/src/tableio_cfg_example/e09_rename_wizard.py)
  builds on `e07_config_wizard.py` and adds, for each output, a variable-row
  table that maps input columns to the column names written in that output
  file. It also adds a `--ui {auto,console,textual}` switch that forces the
  bridge through `make_text_ui_bridge()` instead of auto-selecting by terminal.
  Enough of both is explained inline to follow the example on its own; the
  table mechanics are taught in full in wizard_ui_bridge `e04` and bridge
  selection in wizard_ui_bridge `e01`.
- [`e10_split_rename.py`](https://github.com/tom-bjorkholm/tableio_cfg_json/blob/master/tableio_cfg_json/example/src/tableio_cfg_example/e10_split_rename.py)
  builds on `e06_split_cities.py`. It reads the configuration written by
  `e09_rename_wizard.py` and splits the city table the same way, but renames
  each output's columns independently using the two mappings
  `less_output_names` and `not_less_output_names`.

### Wizard Walkthrough

To build the split-cities config by answering questions instead of running
`e05_app_config.py`, run the wizard with the same output arguments:

```sh
python -m tableio_cfg_example.e07_config_wizard \
  --cfg split-cities.json \
  --txt split-cities-syntax.txt
```

Run in a terminal, this shows a full-screen Textual interface; with redirected
input it falls back to the console bridge and produces the same files, so the
example is fully scriptable. Choosing the interface is a single line,
`make_text_ui_bridge(out_file, in_file, err_file)`; see wizard_ui_bridge `e01`
for the details of bridge selection.

### Edit Configuration Walkthrough

After creating the split-cities config, you can reopen it and keep or change
the stored answers:

```sh
python -m tableio_cfg_example.e08_edit_config \
  --cfg split-cities.json
```

The example reads the file as a `SplitCitiesConfig` and passes each stored
endpoint to the wizard as its `default`, so pressing Enter keeps the old
answer. The same outer navigation loop that `e07_config_wizard.py` uses lets
the user move between the application's endpoints: going back into an earlier
endpoint reopens it at its last question by calling the TableIO wizard with
`backward=True`.

```python
tio_json_config_wizard(capabilities, file_access, ui_bridge,
                       default=stored_endpoint, backward=backward)
```

The `default` argument is what makes editing possible; the `backward` argument
tells the TableIO wizard to start at the last question implied by that default.
The back, cancel and abort exceptions the loop catches are taught on their own
in wizard_ui_bridge `e03`.

### Advanced Capstone Walkthrough

The capstone mirrors the wizard-and-runner split of `e07_config_wizard.py`
and `e06_split_cities.py`. First build a rename-split config by answering
questions. In addition to the split-cities questions, it asks one
variable-row table per output that maps input columns to the names written
in that output file:

```sh
python -m tableio_cfg_example.e09_rename_wizard \
  --cfg rename-cities.json \
  --txt rename-cities-syntax.txt
```

Run in a terminal, the table is edited with the Textual Add row and Remove
row buttons; with redirected input the console row-menu editor uses `:+` to
add a row and `:- N` to delete row N. The `--ui {auto,console,textual}`
option forces one bridge regardless of the terminal. Table questions are
taught on their own in wizard_ui_bridge `e04` and bridge selection in
wizard_ui_bridge `e01`.

Then run the renaming splitter. It splits exactly like `e06_split_cities.py`
but renames each output's columns using the stored mappings. A column that is
not listed keeps its original name, and the two outputs are renamed
independently. The output file extensions match the formats chosen in the
wizard, shown here as CSV for both:

```sh
python -m tableio_cfg_example.e10_split_rename \
  --cfg rename-cities.json \
  --input example/data/cities_input.csv \
  --less-than-output cities-before-limit.csv \
  --not-less-than-output cities-from-limit.csv
```

## Asking a Whole Form at Once: `ask_form()`

The wizards above ask one question at a time. A graphical or full-screen
textual interface can do better and show several related questions
together. That is `WizardUiBridge.ask_form()`.

The wizard user interface bridge is its own package now, and its examples
of `ask_form()` and of the typed form fields live with it, in
[wizard_ui_bridge/example/src/wizard_ui_example](https://github.com/tom-bjorkholm/tableio_cfg_json/blob/master/wizard_ui_bridge/example/src/wizard_ui_example).
