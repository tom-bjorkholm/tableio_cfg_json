# tableio-cfg-json teaching examples

## Introduction

These examples show how three packages fit together:

- `tableio` reads and writes table-like files.
- `config-as-json` reads and writes validated JSON configuration objects.
- `tableio-cfg-json` connects them by making TableIO configuration available
  as config-as-json configuration classes.

The examples are meant to be read in order by a fluent Python programmer who
is new to the three APIs. The first class uses one TableIO endpoint config at
a time. The second class shows a more realistic application config that owns
several TableIO endpoint configs and also has application-specific settings.

TableIO and config-as-json have their own larger example sets:

- TableIO: [https://pypi.org/project/tableio/](https://pypi.org/project/tableio/)
- config-as-json: [https://pypi.org/project/config-as-json/](https://pypi.org/project/config-as-json/)

The examples here focus only on the bridge supplied by `tableio-cfg-json`.

## Class A: One TableIO Endpoint Config

The first class teaches the smallest useful shape: one JSON configuration file
describes one TableIO input or output endpoint. This is the best place to
start, because the application config and the TableIO config are the same
thing.

### Class A: Example Programs

The example source files are:

- [`e01_create_config.py`](https://bitbucket.org/tom-bjorkholm/tableio_cfg_json/src/master/example/src/example/e01_create_config.py)
  writes a JSON configuration file and a plain text syntax guide for that
  file.
- [`e02_write_table.py`](https://bitbucket.org/tom-bjorkholm/tableio_cfg_json/src/master/example/src/example/e02_write_table.py)
  reads a write-capable JSON config and writes a small table with the columns
  `Capital`, `Country` and `Continent`.
- [`e03_read_table.py`](https://bitbucket.org/tom-bjorkholm/tableio_cfg_json/src/master/example/src/example/e03_read_table.py)
  reads a read-capable JSON config and prints an existing table as
  tab-separated text.
- [`e04_create_custom_config.py`](https://bitbucket.org/tom-bjorkholm/tableio_cfg_json/src/master/example/src/example/e04_create_custom_config.py)
  starts from the same kind of default config as `e01_create_config.py`, then
  stores a few explicit non-default values.

### CSV Walkthrough

CSV is the easiest format to inspect because the output file is plain text.
The same CSV configuration can be used for writing and reading:

```sh
python -m example.e01_create_config \
  --cfg capitals-csv.json \
  --txt capitals-csv-syntax.txt \
  --write \
  --format CSV

python -m example.e02_write_table \
  --cfg capitals-csv.json \
  --output capitals.csv

python -m example.e03_read_table \
  --cfg capitals-csv.json \
  --input capitals.csv
```

The first command writes a compact config. Add `--complete` if you want a
template where optional defaults are visible:

```sh
python -m example.e01_create_config \
  --cfg capitals-csv-complete.json \
  --txt capitals-csv-complete-syntax.txt \
  --write \
  --format CSV \
  --complete
```

### Custom Configuration Walkthrough

The compact config from `e01_create_config.py` only stores durable choices
that need to be fixed. `e04_create_custom_config.py` shows the next step:
start from the same default object and then set a few values before writing
the JSON file.

```sh
python -m example.e04_create_custom_config \
  --cfg capitals-custom-csv.json \
  --txt capitals-custom-csv-syntax.txt \
  --write \
  --format CSV \
  --csv-delimiter : \
  --encoding utf-8 \
  --alignment CENTER

python -m example.e02_write_table \
  --cfg capitals-custom-csv.json \
  --output capitals-custom.csv
```

The CSV delimiter is stored in the optional nested `csv` section. If you use
the same option while creating an Excel config, the value is still valid JSON
configuration, but it has no effect when TableIO later uses an Excel backend.

### Excel Walkthrough

Excel is a useful second format because TableIO commonly uses one
implementation for writing and another for reading. For that reason the
walkthrough creates two config files:

```sh
python -m example.e01_create_config \
  --cfg capitals-excel-write.json \
  --txt capitals-excel-write-syntax.txt \
  --write \
  --format Excel

python -m example.e01_create_config \
  --cfg capitals-excel-read.json \
  --txt capitals-excel-read-syntax.txt \
  --read \
  --format Excel

python -m example.e02_write_table \
  --cfg capitals-excel-write.json \
  --output capitals.xlsx

python -m example.e03_read_table \
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

The example program can be configured to split this list into two list based
on a configurable criteria: a configured column has a value that is less than
or not less than a configured string.
The output formats for the less than output and not less than output is
configured independently. Each can be any format TableIO supports with any
parameters TableIO supports.

As a companion to the table splitting example program, there is another
example program with a wizard functionality to ask the user for the wanted
configuration and create the configuration file. As a help for the user to
understand and later hand-edit the configuration file the wizard program
also prints a text description of the configuration options.

### Class B: Example Programs

The example source files are:

- [`e05_split_cities_wizard.py`](https://bitbucket.org/tom-bjorkholm/tableio_cfg_json/src/master/example/src/example/e05_split_cities_wizard.py)
  asks questions and writes the larger JSON application configuration. It
  calls `tio_json_config_wizard()` once for the input endpoint and once for
  each output endpoint.
- [`e06_split_cities.py`](https://bitbucket.org/tom-bjorkholm/tableio_cfg_json/src/master/example/src/example/e06_split_cities.py)
  reads the larger JSON configuration, reads a city table as dictionaries,
  and writes two independently configured output tables.

### Split-Cities Walkthrough

First create the application config and the matching syntax guide:

```sh
python -m example.e05_split_cities_wizard \
  --cfg split-cities.json \
  --txt split-cities-syntax.txt
```

Then run the splitter. File paths are command-line arguments because they are
runtime values, not durable configuration:

```sh
python -m example.e06_split_cities \
  --cfg split-cities.json \
  --input example/data/cities_input.csv \
  --less-than-output cities-before-limit.csv \
  --not-less-than-output cities-from-limit.csv
```

The input table is expected to have the header row `City`, `Country`,
`Continent`. The splitter reads the table as dictionaries, so each data row
uses those column names as keys. The comparison is normal case-sensitive
Python string comparison, deliberately kept simple because the teaching point
is configuration composition.

### Sample Data

The repository includes a sample input file:

- [`example/data/cities_input.csv`](https://bitbucket.org/tom-bjorkholm/tableio_cfg_json/src/master/example/data/cities_input.csv)

It contains three continents, five countries per continent, and two cities per
country. You can use that file to test the walkthrough, or create your own CSV
file with the same `City`, `Country`, `Continent` header.

### Class B: What To Look For In The Code

`SplitCitiesConfig` is an application config class. It owns three nested
`TioJsonConfig` members named `input`, `less_than_output` and
`not_less_than_output`, plus the application-owned members `split_column` and
`split_limit`.

The wizard example creates a default `SplitCitiesConfig` and then assigns the
values collected from the user:

```python
config = SplitCitiesConfig(stderr_file=err_file)
config.input = input_config
config.less_than_output = less_config
config.not_less_than_output = not_less_config
config.split_column = split_column
config.split_limit = split_limit
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
