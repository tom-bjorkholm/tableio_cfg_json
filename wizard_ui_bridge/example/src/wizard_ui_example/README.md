# wizard-ui-bridge teaching examples

## Introduction

These examples show how to ask a user a series of questions through
`WizardUiBridge`, without tying the questions to one user interface. They
are meant to be read in order by a fluent Python programmer who is new to
the API.

Both examples are self-contained: they ask a form and print a summary of
the answers, so nothing but the bridge itself is in the way.

- [`e01_ask_form.py`](https://github.com/tom-bjorkholm/tableio_cfg_json/blob/master/wizard_ui_bridge/example/src/wizard_ui_example/e01_ask_form.py)
  asks one export-settings form with the six basic field types.
- [`e02_schedule_form.py`](https://github.com/tom-bjorkholm/tableio_cfg_json/blob/master/wizard_ui_bridge/example/src/wizard_ui_example/e02_schedule_form.py)
  adds the typed fields for numbers, dates, times and durations, and shows
  prefilling one field from the answers to others.

Run them with, for example:

```sh
python -m wizard_ui_example.e01_ask_form
python -m wizard_ui_example.e02_schedule_form --ui console
```

## Asking a Whole Form at Once: `ask_form()`

The wizards above ask one question at a time. That is natural on a plain
console, but a graphical or full-screen textual interface can do better: it can
show several related questions together, so the user sees the whole picture and
fills the fields in any order before submitting. `WizardUiBridge.ask_form()` is
the bridge method for that.

- [`e01_ask_form.py`](https://github.com/tom-bjorkholm/tableio_cfg_json/blob/master/wizard_ui_bridge/example/src/wizard_ui_example/e01_ask_form.py)
  is a small, self-contained program that asks one export-settings form with
  `ask_form()` and then prints a summary of the answers. It does not read or
  write any configuration, so it isolates the `ask_form()` API. The form uses
  every field type, including a path field for a new output file, and a partial
  validator that both disables an irrelevant field and reports a bad value.

### `ask_form()` Walkthrough

The example builds its bridge with `make_text_ui_bridge()`, so in a real
terminal it shows a full-screen Textual form and with redirected input it falls
back to the console bridge. A `--ui {auto,console,textual}` switch forces the
choice:

```sh
python -m wizard_ui_example.e01_ask_form
python -m wizard_ui_example.e01_ask_form --ui console
```

In a terminal the whole form appears on one screen with a labelled input widget
per row; press `Ctrl+S` (or the Submit button) to submit. On the console the
same program asks each field in turn and then prints the summary.

### How To Use `ask_form()`

Describe the form as a list of `Ask*Field` objects, one per row. The Python type
of each object tells the bridge which input widget to show, so there is one
class per kind of question:

| Field class | Question kind | Typical widget |
| ----------- | ------------- | -------------- |
| `AskTextField` | free text | text input |
| `AskIntField` | integer, optionally bounded/nullable | numeric input |
| `AskPathField` | file or directory path | text input plus a picker |
| `AskYesNoField` | boolean | check box or toggle |
| `AskChoiceField` | pick one of a fixed list | drop-down or radio buttons |
| `AskMultiChoiceField` | pick several of a fixed list | check-box list |

Every field carries a `short_question` (the label) and an optional `help_text`
(a tooltip in a graphical or textual bridge). A path field is configured with
`PathAskOptions`, whose `WizardPathKind` says whether the path must exist and
whether it must be a file or a directory:

```python
AskPathField(short_question='Output file',
             help_text='Where the report will be written.',
             path_options=PathAskOptions(kind=WizardPathKind.NON_EXISTING_FILE))
```

Call `ask_form()` with the main instruction and the fields, and read back one
`Answer*Field` per field, in the same order:

```python
answers = bridge.ask_form(long_question, ask_fields,
                          re_ask_reason=reason,
                          partial_validator=export_validator)
title = answers[0].value        # each Answer*Field.value holds the typed answer
```

The optional `partial_validator` gives early feedback. It receives the current
answers and the index of the field that changed, and returns a
`PartFormValidationResult(is_valid, message, disable_row_idxs)`:

- `disable_row_idxs` lists rows that are irrelevant given the current answers,
  for example the CSV delimiter when the chosen format is not CSV. Disabling a
  row never blocks submitting the form.
- `is_valid` and `message` report a real problem the user must fix. A graphical
  or textual bridge refuses to submit while `is_valid` is `False`, so an
  informational note should leave `is_valid` `True` and only genuine errors
  should set it `False`.

The base `ask_form()` is a permanent console implementation: it simply asks each
field with the ordinary typed ask methods, so a program keeps working when
output is redirected or under tests. A graphical, textual, curses or web bridge
overrides `ask_form()` to show the whole form on one screen; the Textual bridge
in this package already does. Because the console fallback treats validator
messages as advisory, a caller that must reject a bad final value re-calls
`ask_form()` with a `re_ask_reason`, which `e01_ask_form.py` demonstrates.

## Typed Form Fields And Prefills: `e02_schedule_form.py`

On top of the six fields above, `ask_form()` supports five *typed* fields whose
answer is a real Python object, so a graphical or textual bridge can offer a
better editor and no string parsing leaks into the application:

| Field class | Answer type | Accepted text / widget |
| ----------- | ----------- | ---------------------- |
| `AskFloatField` | `float` | a number, optionally bounded |
| `AskDateField` | `date` | `YYYY-MM-DD`; the Textual bridge opens a calendar |
| `AskTimeField` | `time` | `HH:MM` or `HH:MM:SS` |
| `AskDateTimeField` | `datetime` | `YYYY-MM-DD HH:MM:SS`; calendar for the date part |
| `AskDurationField` | `timedelta` | `<days> d HH:MM:SS`, or a number of seconds |

Each typed field takes the same `short_question`, `help_text`, `nullable` and
`default` as the other fields, and the date-like and numeric fields also take
inclusive `min_value` and `max_value` bounds. A duration is written as an
optional day count and a clock part, so `1 d 02:30:00` and a plain `9000`
(seconds) both work, which is friendlier than one large second count.

- [`e02_schedule_form.py`](https://github.com/tom-bjorkholm/tableio_cfg_json/blob/master/wizard_ui_bridge/example/src/wizard_ui_example/e02_schedule_form.py)
  asks a small event-scheduling form that uses every typed field, and it shows a
  partial validator that *prefills* one field from others. It is self-contained
  and writes nothing to disk, so it isolates the typed fields and prefills.

```sh
python -m wizard_ui_example.e02_schedule_form
python -m wizard_ui_example.e02_schedule_form --ui console
```

In a real terminal the date and "Ends at" fields show a **Pick** button (or
accept the `?` token) that opens a full-screen calendar; on the console every
field is asked as text and parsed, so the same program stays scriptable.

### Prefilling A Field From Others

`PartFormValidationResult` has a fourth part, `prefill_values`: a tuple of
`(row_index, value)` pairs the validator asks the bridge to place into other
rows, exactly as if the user had typed them. `e02_schedule_form.py` uses it to
fill the "Ends at" date-time from the event date, the start time and the
duration whenever any of those change:

```python
def schedule_validator(answers, changed):
    disable = () if not _is_free(answers) else (_PRICE,)   # hide an irrelevant row
    end = _computed_end(answers)                            # date + time + duration
    prefill = () if end is None else ((_END, end),)         # offer it in "Ends at"
    return PartFormValidationResult(True, '', disable, prefill)
```

The prefilled value is only a starting point the user may edit. A prefill aimed
at the row that just changed is ignored, so writing back never fights the user's
own edit, and emitting a stable value (the same computed end) does not loop. The
value must match the target field's answer type: a `date` for a date field, a
`datetime` for a date-time field, a `float` for a float field, and so on.

### Working With Older Bridges: `ask_form_w_fake()`

A bridge that overrides `ask_form()` but predates the typed fields reports
through `supports_form_field()` that it cannot show them. A wizard that wants
the typed fields anyway can call `bridge.ask_form_w_fake(...)` instead of
`ask_form()`: each unsupported field is shown as a text field with the format in
its help text, a wrapping validator guides the entry and converts it, and the
answers come back as the requested typed answers. On a bridge that already
supports the typed fields — the console and Textual bridges here both do —
`ask_form_w_fake()` simply calls `ask_form()`.
