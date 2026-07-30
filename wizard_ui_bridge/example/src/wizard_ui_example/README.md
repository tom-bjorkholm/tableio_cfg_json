# wizard-ui-bridge teaching examples

## Introduction

A *wizard* is any code that asks a user a series of questions. A
`WizardUiBridge` is the user-interface-independent object the wizard asks them
through, so one wizard can run on a plain console, on a full-screen Textual
interface, or on any other bridge an application supplies. (The
`tableio-cfg-json` package is one such application; these examples need nothing
from it.)

These examples are meant to be read in order by a fluent Python programmer who
is new to the API. Each one is self-contained: it asks some questions and
prints a summary, so nothing but the bridge itself is in the way. Each is also
fully scriptable — `make_text_ui_bridge()` shows a full-screen Textual form in
a real terminal (with the optional `wizard-ui-bridge[textual]` extra) and falls
back to the plain console bridge when input is redirected, which is what the
tests rely on.

Run any example as a module, optionally forcing a bridge with `--ui`:

```sh
python -m wizard_ui_example.e01_one_question
python -m wizard_ui_example.e02_question_kinds --ui console
```

## The examples, in reading order

- [`e01_one_question.py`](https://github.com/tom-bjorkholm/tableio_cfg_json/blob/master/wizard_ui_bridge/example/src/wizard_ui_example/e01_one_question.py)
  obtains a bridge and asks a few free-text questions.
- [`e02_question_kinds.py`](https://github.com/tom-bjorkholm/tableio_cfg_json/blob/master/wizard_ui_bridge/example/src/wizard_ui_example/e02_question_kinds.py)
  uses each one-at-a-time ask method once to gather export settings.
- [`e03_navigation.py`](https://github.com/tom-bjorkholm/tableio_cfg_json/blob/master/wizard_ui_bridge/example/src/wizard_ui_example/e03_navigation.py)
  lets the user step back, cancel a nested section or abort the wizard.
- [`e04_table_question.py`](https://github.com/tom-bjorkholm/tableio_cfg_json/blob/master/wizard_ui_bridge/example/src/wizard_ui_example/e04_table_question.py)
  edits a fixed-row table and then a variable-row table.
- [`e05_ask_form.py`](https://github.com/tom-bjorkholm/tableio_cfg_json/blob/master/wizard_ui_bridge/example/src/wizard_ui_example/e05_ask_form.py)
  asks the same kind of export settings as one whole form.
- [`e06_typed_form.py`](https://github.com/tom-bjorkholm/tableio_cfg_json/blob/master/wizard_ui_bridge/example/src/wizard_ui_example/e06_typed_form.py)
  adds the typed form fields (numbers, dates, times, durations) and prefills.

The numbering leaves room for one more example added in a later stage: `e07`
(implementing a bridge of your own). This document is extended when it
arrives.

## `e01_one_question.py`: obtaining a bridge and asking

The smallest useful program that talks to a user through the bridge.

**Getting a bridge.** `make_text_ui_bridge(out, in_, err, kind)` returns a
ready-to-use text-mode bridge. `UiBridgeType.AUTO` builds the Textual
full-screen bridge when Textual is installed and the streams are a real
terminal, and the plain console bridge otherwise; `textual_installed()` reports
whether the optional extra is available, which is exactly what `AUTO` checks
first. `UiBridgeType.CONSOLE` and `UiBridgeType.TEXTUAL` force one bridge.

**Asking one question.** `ask_text()` asks for one line of free text. Three of
its options appear here:

- `default` — an empty answer returns the default instead of an empty string.
- `nullable` — an empty answer with no default returns `None`, so "left blank"
  is distinguishable from a real value.
- `sensitive` — the bridge must not echo the text (a password field, or
  `getpass` on a real console). No default may be combined with it.

**Showing output and side notes.** `show()` presents a message to the user. On
the console it prints at once, but on a graphical or full-screen textual bridge
`show()` only *buffers* the message for the next question's screen — a message
with no following question is never seen. So the example ends with a short
acknowledgement question, which keeps the greeting on screen until the user has
read it (a GUI such as Tkinter needs the same). `error_file()` returns the
stream for side notes and diagnostics, kept apart from the primary output; on
the console bridge it is standard error. The example writes a note there when
the optional nickname is left blank.

**Cancelling.** Any ask method may raise a `WizardNavigation` request instead of
returning, when the user asks to go back, cancel or abort (`:b`, `:c` or `:q` on
the console). A single question has nowhere to go back to, so the example treats
any such request as "the user gave up".

```sh
python -m wizard_ui_example.e01_one_question
python -m wizard_ui_example.e01_one_question --ui console
```

## `e02_question_kinds.py`: the kinds of question

This example uses each of the one-at-a-time ask methods exactly once to gather a
small "export settings" configuration:

| Ask method | Question kind | Answer type |
| ---------- | ------------- | ----------- |
| `ask_text` | free text (the report title) | `str` |
| `ask_choice` | pick one of a fixed list (the format) | `str` |
| `ask_path` | a file or directory path (the output file) | `Path` |
| `ask_int` | an integer, optionally bounded/nullable (a row limit) | `int` or `None` |
| `ask_yes_no` | a boolean (write a header row?) | `bool` |
| `ask_multi` | pick several of a fixed list (which columns) | `list[str]` |

**The ask methods validate for you.** Each method already re-asks on input it
can judge on its own: `ask_int` rejects non-integers and out-of-range values,
`ask_choice` and `ask_multi` reject unknown items, and `ask_path` rejects a path
of the wrong kind. The program does not loop for those.

**`re_ask_reason`: application-level checks.** Some rules only the application
knows. Here the output file should end with the extension matching the chosen
format, which `ask_path()` cannot know. So the example checks it and, when it
fails, calls `ask_path()` again with a `re_ask_reason` that explains why.
`re_ask_reason` is the shared argument every ask method takes for exactly this.

Per-question help text is *not* a feature of the one-at-a-time ask methods; it
belongs to the form fields shown in `e05_ask_form.py`.

The same export settings appear again in `e05_ask_form.py` as one whole form.
Reading `e02` then `e05` is the intended way to see the difference between asking
questions one at a time and asking them all at once.

```sh
python -m wizard_ui_example.e02_question_kinds
python -m wizard_ui_example.e02_question_kinds --ui console
```

## `e03_navigation.py`: letting the user move around

The wizards above only move forward. A real wizard also lets the user change
their mind. Any ask method may raise a `WizardNavigation` subclass instead of
returning, and the wizard author writes the control flow that reacts to it.
`e03_navigation.py` is a small account-setup wizard (username → email →
account type → password) where choosing the *Organization* account type opens
a **nested level** of organization questions. That nested level is what makes
the difference between the two "go somewhere" requests visible:

| Request | Console token | Meaning |
| ------- | ------------- | ------- |
| `WizardBack` | `:b` | Step to the previous question. At the first question of a level there is no earlier question, so it is left to the enclosing level. |
| `WizardCancelLevel` | `:c` | Leave the whole current level and return to the question that opened it, however deep in the level the user is. Here it leaves the organization section and re-asks the account type. The level's answers are not thrown away: they are kept and offered as defaults if it is re-entered, unless a changed outer answer has made them invalid. |
| `WizardAbort` | `:q` | Abandon the whole wizard. |

**The driver pattern.** `drive_level()` is the small reusable driver written
around the ask methods. It walks a list of step functions, stepping back on
`WizardBack`. The nested organization level runs the *same* driver; being an
inner level it re-raises a `WizardBack` from its first question and any
`WizardCancelLevel`, so the driver that opened it (`ask_account_details()`)
can re-ask the opening question. `WizardAbort` is never caught by a level, so
it propagates out and `run_account_setup()` stops.

**Answers become the new default.** Whenever the user returns to a question —
by stepping back, or by re-entering a level they cancelled out of — the
answer given earlier is offered as its default, so pressing enter keeps it.
The example keeps every answer in a draft object (including a nested
`OrgDraft` for the organization level) and passes the stored value back as
the ask method's `default`. The password is the one exception: a sensitive
question cannot carry a default, so it is entered again on return.

The console tokens (`:b`, `:c`, `:q`) make the whole flow scriptable, which is
how the tests drive back, cancel and abort.

```sh
python -m wizard_ui_example.e03_navigation
python -m wizard_ui_example.e03_navigation --ui console
```

## `e04_table_question.py`: editing a table

`WizardUiBridge.ask_table()` asks the user to fill in a table. A table
question is described by one `TableColumn` per column (its header and whether
the whole column is read-only) and a grid of `TableCell` objects giving each
starting cell's value and its constraints (an optional finite set of
`choices`, and whether an empty cell is allowed). `ask_table()` returns the
whole table as rows of strings — or `None` for an empty cell — including the
read-only columns. `e04_table_question.py` asks two table questions:

- a **fixed-row** table for renaming a known set of columns: a read-only
  *source column*, a free-text *rename to* column, and a per-row *data type*
  choice cell (showing that each `TableCell` can carry its own choices);
- a **variable-row** guest list, where the user adds rows (`:+` on the
  console, an Add-row button in a graphical bridge) and removes them
  (`:- N` on the console) within a minimum and maximum row count.

**Early feedback vs final verification.** The variable table passes a
`PartialCheck`. It is *intended* as advisory early feedback: a graphical or
Textual bridge shows the message beside the cell as the user types, without
blocking, so the answer is guided rather than forced. A console has nowhere to
show such an unobtrusive inline hint, so the console bridge instead re-asks
the cell until the check passes (an optional-to-heed prompt reads badly on a
console). Because a bridge might handle — or even skip — the check in different
ways, **a wizard must not trust the bridge to enforce it.** After `ask_table()`
returns, `ask_guest_list()` verifies the whole table itself and, when
something is wrong, calls `ask_table()` again with a `re_ask_reason` and the
user's current rows, so nothing is retyped. The final pass also enforces a
rule a per-cell check cannot see — that the guest names are unique.

Editing a table also honors the navigation requests from `e03_navigation.py`;
this example simply treats any request that propagates out of a table as
"cancelled".

```sh
python -m wizard_ui_example.e04_table_question
python -m wizard_ui_example.e04_table_question --ui console
```

## `e05_ask_form.py`: asking a whole form at once

The wizards above ask one question at a time. That is natural on a plain
console, but a graphical or full-screen textual interface can do better: it can
show several related questions together, so the user sees the whole picture and
fills the fields in any order before submitting. `WizardUiBridge.ask_form()` is
the bridge method for that. `e05_ask_form.py` asks one export-settings form with
`ask_form()` and prints a summary; it reads or writes nothing, so it isolates
the `ask_form()` API. In a real terminal the whole form appears on one screen;
on the console the same program asks each field in turn.

### How to use `ask_form()`

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
`ask_form()` with a `re_ask_reason`, which `e05_ask_form.py` demonstrates.

```sh
python -m wizard_ui_example.e05_ask_form
python -m wizard_ui_example.e05_ask_form --ui console
```

## `e06_typed_form.py`: typed form fields and prefills

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
inclusive `min_value` and `max_value` bounds. `e06_typed_form.py` asks a small
event-scheduling form that uses every typed field. On the plain console bridge
each field is still asked as text and parsed, so the same program stays
scriptable even though it shows a calendar in a real terminal.

### Prefilling a field from others

`PartFormValidationResult` has a fourth part, `prefill_values`: a tuple of
`(row_index, value)` pairs the validator asks the bridge to place into other
rows, exactly as if the user had typed them. `e06_typed_form.py` uses it to fill
the "Ends at" date-time from the event date, the start time and the duration
whenever any of those change:

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

### Working with older bridges: `ask_form_w_fake()`

A bridge that overrides `ask_form()` but predates the typed fields reports
through `supports_form_field()` that it cannot show them. A wizard that wants the
typed fields anyway can call `bridge.ask_form_w_fake(...)` instead of
`ask_form()`: each unsupported field is shown as a text field with the format in
its help text, a wrapping validator guides the entry and converts it, and the
answers come back as the requested typed answers. On a bridge that already
supports the typed fields — the console and Textual bridges here both do —
`ask_form_w_fake()` simply calls `ask_form()`.

```sh
python -m wizard_ui_example.e06_typed_form
python -m wizard_ui_example.e06_typed_form --ui console
```
