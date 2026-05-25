# tableio-cfg-json teaching examples

These examples show the smallest useful path through three packages:

- `tableio` reads and writes table-like files.
- `config-as-json` reads and writes validated JSON configuration objects.
- `tableio-cfg-json` connects them by making TableIO configuration available
  as a config-as-json configuration class.

The examples are meant to be read in order by a fluent Python programmer who
is new to the three APIs.

## Where the larger examples are

- TableIO: https://pypi.org/project/tableio/
- config-as-json: https://pypi.org/project/config-as-json/

Those projects have their own teaching examples. The examples here focus only
on the bridge supplied by `tableio-cfg-json`.

## Example programs

`e01_create_config.py` writes two files:

- a JSON configuration file that can be read by `TioJsonConfig`
- a plain text syntax guide that explains the values accepted by that config

`e02_write_table.py` reads a write-capable JSON config and writes a small
table with the columns `Capital`, `Country` and `Continent`.

`e03_read_table.py` reads a read-capable JSON config and prints the table from
an existing file as tab-separated text.

`e04_create_custom_config.py` writes the same kind of config as
`e01_create_config.py`, but then stores a few explicit non-default values:
character encoding, table alignment and a CSV delimiter.

## CSV walkthrough

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

## Custom configuration walkthrough

The compact config from `e01_create_config.py` only stores the durable choices
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

## Excel walkthrough

Excel is a useful second example because TableIO commonly uses one
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
is omitted, TableIO selects the best matching implementation at runtime. File
access is also a runtime fact. A configuration that selects the best Excel
writer may not be the same as a configuration that selects the best Excel
reader.

## What to look for in the code

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
