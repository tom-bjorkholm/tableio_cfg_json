# Table of Contents

* [wizard\_ui\_bridge.form\_defs](#wizard_ui_bridge.form_defs)
  * [value\_out\_of\_range](#wizard_ui_bridge.form_defs.value_out_of_range)
  * [AskFieldCommon](#wizard_ui_bridge.form_defs.AskFieldCommon)
  * [AskTextField](#wizard_ui_bridge.form_defs.AskTextField)
  * [AskIntField](#wizard_ui_bridge.form_defs.AskIntField)
  * [AskPathField](#wizard_ui_bridge.form_defs.AskPathField)
  * [AskYesNoField](#wizard_ui_bridge.form_defs.AskYesNoField)
  * [AskChoiceField](#wizard_ui_bridge.form_defs.AskChoiceField)
  * [AskMultiChoiceField](#wizard_ui_bridge.form_defs.AskMultiChoiceField)
  * [AskFloatField](#wizard_ui_bridge.form_defs.AskFloatField)
  * [AskDateField](#wizard_ui_bridge.form_defs.AskDateField)
  * [AskTimeField](#wizard_ui_bridge.form_defs.AskTimeField)
  * [AskDateTimeField](#wizard_ui_bridge.form_defs.AskDateTimeField)
  * [AskDurationField](#wizard_ui_bridge.form_defs.AskDurationField)
  * [ALL\_ASK\_FIELD\_TYPES](#wizard_ui_bridge.form_defs.ALL_ASK_FIELD_TYPES)
  * [AnswerTextField](#wizard_ui_bridge.form_defs.AnswerTextField)
  * [AnswerIntField](#wizard_ui_bridge.form_defs.AnswerIntField)
  * [AnswerPathField](#wizard_ui_bridge.form_defs.AnswerPathField)
  * [AnswerYesNoField](#wizard_ui_bridge.form_defs.AnswerYesNoField)
  * [AnswerChoiceField](#wizard_ui_bridge.form_defs.AnswerChoiceField)
  * [AnswerMultiChoiceField](#wizard_ui_bridge.form_defs.AnswerMultiChoiceField)
  * [AnswerFloatField](#wizard_ui_bridge.form_defs.AnswerFloatField)
  * [AnswerDateField](#wizard_ui_bridge.form_defs.AnswerDateField)
  * [AnswerTimeField](#wizard_ui_bridge.form_defs.AnswerTimeField)
  * [AnswerDateTimeField](#wizard_ui_bridge.form_defs.AnswerDateTimeField)
  * [AnswerDurationField](#wizard_ui_bridge.form_defs.AnswerDurationField)
  * [PartFormValidationResult](#wizard_ui_bridge.form_defs.PartFormValidationResult)
* [wizard\_ui\_bridge.console](#wizard_ui_bridge.console)
  * [WizardUiBridgeConsole](#wizard_ui_bridge.console.WizardUiBridgeConsole)
    * [\_\_init\_\_](#wizard_ui_bridge.console.WizardUiBridgeConsole.__init__)
    * [ask\_text](#wizard_ui_bridge.console.WizardUiBridgeConsole.ask_text)
    * [supports\_form\_field](#wizard_ui_bridge.console.WizardUiBridgeConsole.supports_form_field)
    * [ask\_yes\_no](#wizard_ui_bridge.console.WizardUiBridgeConsole.ask_yes_no)
    * [ask\_table](#wizard_ui_bridge.console.WizardUiBridgeConsole.ask_table)
    * [ask\_choice](#wizard_ui_bridge.console.WizardUiBridgeConsole.ask_choice)
    * [ask\_multi](#wizard_ui_bridge.console.WizardUiBridgeConsole.ask_multi)
    * [error\_file](#wizard_ui_bridge.console.WizardUiBridgeConsole.error_file)
    * [show](#wizard_ui_bridge.console.WizardUiBridgeConsole.show)
* [wizard\_ui\_bridge.arg\_types](#wizard_ui_bridge.arg_types)
  * [WizardNavigation](#wizard_ui_bridge.arg_types.WizardNavigation)
  * [WizardBack](#wizard_ui_bridge.arg_types.WizardBack)
  * [WizardCancelLevel](#wizard_ui_bridge.arg_types.WizardCancelLevel)
  * [WizardAbort](#wizard_ui_bridge.arg_types.WizardAbort)
  * [WizardPathKind](#wizard_ui_bridge.arg_types.WizardPathKind)
  * [PathAskOptions](#wizard_ui_bridge.arg_types.PathAskOptions)
  * [TableColumn](#wizard_ui_bridge.arg_types.TableColumn)
  * [TableCell](#wizard_ui_bridge.arg_types.TableCell)
* [wizard\_ui\_bridge.form\_helpers](#wizard_ui_bridge.form_helpers)
  * [initial\_answer](#wizard_ui_bridge.form_helpers.initial_answer)
  * [valid\_prefills](#wizard_ui_bridge.form_helpers.valid_prefills)
  * [prefilled\_field](#wizard_ui_bridge.form_helpers.prefilled_field)
* [wizard\_ui\_bridge.bridge](#wizard_ui_bridge.bridge)
  * [WizardUiBridge](#wizard_ui_bridge.bridge.WizardUiBridge)
    * [ask](#wizard_ui_bridge.bridge.WizardUiBridge.ask)
    * [ask\_text](#wizard_ui_bridge.bridge.WizardUiBridge.ask_text)
    * [ask\_int](#wizard_ui_bridge.bridge.WizardUiBridge.ask_int)
    * [ask\_path](#wizard_ui_bridge.bridge.WizardUiBridge.ask_path)
    * [ask\_yes\_no](#wizard_ui_bridge.bridge.WizardUiBridge.ask_yes_no)
    * [ask\_choice](#wizard_ui_bridge.bridge.WizardUiBridge.ask_choice)
    * [ask\_multi](#wizard_ui_bridge.bridge.WizardUiBridge.ask_multi)
    * [ask\_table](#wizard_ui_bridge.bridge.WizardUiBridge.ask_table)
    * [ask\_form](#wizard_ui_bridge.bridge.WizardUiBridge.ask_form)
    * [supports\_form\_field](#wizard_ui_bridge.bridge.WizardUiBridge.supports_form_field)
    * [ask\_form\_w\_fake](#wizard_ui_bridge.bridge.WizardUiBridge.ask_form_w_fake)
    * [error\_file](#wizard_ui_bridge.bridge.WizardUiBridge.error_file)
    * [show](#wizard_ui_bridge.bridge.WizardUiBridge.show)
* [wizard\_ui\_bridge.factory](#wizard_ui_bridge.factory)
  * [textual\_installed](#wizard_ui_bridge.factory.textual_installed)
  * [load\_textual\_bridge](#wizard_ui_bridge.factory.load_textual_bridge)
  * [UiBridgeType](#wizard_ui_bridge.factory.UiBridgeType)
  * [make\_text\_ui\_bridge](#wizard_ui_bridge.factory.make_text_ui_bridge)
* [wizard\_ui\_bridge.\_parse](#wizard_ui_bridge._parse)
  * [NEW\_FIELD\_TYPES](#wizard_ui_bridge._parse.NEW_FIELD_TYPES)
  * [parse\_float](#wizard_ui_bridge._parse.parse_float)
  * [parse\_date](#wizard_ui_bridge._parse.parse_date)
  * [parse\_time](#wizard_ui_bridge._parse.parse_time)
  * [parse\_datetime](#wizard_ui_bridge._parse.parse_datetime)
  * [parse\_duration](#wizard_ui_bridge._parse.parse_duration)
  * [format\_duration](#wizard_ui_bridge._parse.format_duration)
  * [format\_new\_value](#wizard_ui_bridge._parse.format_new_value)
  * [ordered\_range\_error](#wizard_ui_bridge._parse.ordered_range_error)
  * [ask\_typed](#wizard_ui_bridge._parse.ask_typed)
  * [resolve\_new](#wizard_ui_bridge._parse.resolve_new)
  * [new\_answer](#wizard_ui_bridge._parse.new_answer)
  * [field\_hint](#wizard_ui_bridge._parse.field_hint)
  * [value\_from\_text](#wizard_ui_bridge._parse.value_from_text)
  * [error\_from\_text](#wizard_ui_bridge._parse.error_from_text)
  * [fake\_field](#wizard_ui_bridge._parse.fake_field)
* [wizard\_ui\_bridge.\_form\_prefill](#wizard_ui_bridge._form_prefill)
  * [apply\_prefills](#wizard_ui_bridge._form_prefill.apply_prefills)
* [wizard\_ui\_bridge.\_fake](#wizard_ui_bridge._fake)
  * [ask\_form\_faking](#wizard_ui_bridge._fake.ask_form_faking)
* [wizard\_ui\_bridge.bridge\_helpers](#wizard_ui_bridge.bridge_helpers)
  * [check\_text\_args](#wizard_ui_bridge.bridge_helpers.check_text_args)
  * [question\_with\_default](#wizard_ui_bridge.bridge_helpers.question_with_default)
  * [text\_answer](#wizard_ui_bridge.bridge_helpers.text_answer)
  * [path\_answer](#wizard_ui_bridge.bridge_helpers.path_answer)
  * [ask\_yes\_no](#wizard_ui_bridge.bridge_helpers.ask_yes_no)
  * [run\_table](#wizard_ui_bridge.bridge_helpers.run_table)
  * [fill\_cell](#wizard_ui_bridge.bridge_helpers.fill_cell)
  * [cell\_checker](#wizard_ui_bridge.bridge_helpers.cell_checker)
  * [int\_text](#wizard_ui_bridge.bridge_helpers.int_text)
  * [out\_of\_range](#wizard_ui_bridge.bridge_helpers.out_of_range)
  * [range\_error](#wizard_ui_bridge.bridge_helpers.range_error)
  * [ask\_one](#wizard_ui_bridge.bridge_helpers.ask_one)
  * [ask\_many](#wizard_ui_bridge.bridge_helpers.ask_many)
  * [match\_token](#wizard_ui_bridge.bridge_helpers.match_token)
  * [multi\_count\_error](#wizard_ui_bridge.bridge_helpers.multi_count_error)
* [wizard\_ui\_bridge.textual\_bridge](#wizard_ui_bridge.textual_bridge)
  * [WizardUiBridgeTextual](#wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual)
    * [\_\_init\_\_](#wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.__init__)
    * [ask\_text](#wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.ask_text)
    * [ask\_path](#wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.ask_path)
    * [ask\_yes\_no](#wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.ask_yes_no)
    * [ask\_choice](#wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.ask_choice)
    * [ask\_multi](#wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.ask_multi)
    * [ask\_table](#wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.ask_table)
    * [ask\_form](#wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.ask_form)
    * [supports\_form\_field](#wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.supports_form_field)
    * [error\_file](#wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.error_file)
    * [show](#wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.show)

<a id="wizard_ui_bridge.form_defs"></a>

# wizard\_ui\_bridge.form\_defs

Definitions of types for wizard UI bridge forms.

Wizard UI bridge forms are used when a number of questions should preferably
be asked on a single form (in a GUI, textual or curses implementation).
For a good user experience the user should see all questions at the same time,
and the user should be able to fill in the answers in any order, and change
them before submitting the form.

In a GUI, curses or textual implementation, the form is typically displayed
in a single window, in something like a grid layout, with 2 columns and
2 - 10 rows. The left column contains the questions, and the right column
contains the input fields. Above the grid there is typically a longer question
or instruction, that explains to the user what the form is about. Below the
grid there are typically buttons for submitting the form, canceling the form,
and possibly for going back to a previous form step in a multi-step wizard.

This file defines the data types used to describe the questions and answers of
a form, and the validation callback function that is used to validate the
answers of a partly filled form.

<a id="wizard_ui_bridge.form_defs.value_out_of_range"></a>

#### value\_out\_of\_range

```python
def value_out_of_range(value: _OrderedT, minimum: Optional[_OrderedT],
                       maximum: Optional[_OrderedT]) -> bool
```

Return whether value lies outside the inclusive bounds.

<a id="wizard_ui_bridge.form_defs.AskFieldCommon"></a>

## AskFieldCommon Objects

```python
@dataclass
class AskFieldCommon()
```

Common attributes of a field in a form.

Each concrete field is one of the Ask*Field subclasses, so its Python
type already tells the bridge which kind of input to show. There is no
separate kind attribute to keep in sync.

**Attributes**:

- `short_question` - A short question to be displayed to the user.
  In a GUI implementation this is typically displayed
  as a label in a left column next to the input field.
- `help_text` - Optional help text to be displayed to the user. Could be
  used as tooltip text in a GUI implementation, or as a
  popup message in a in response to a help button click
  or similar user action.

<a id="wizard_ui_bridge.form_defs.AskTextField"></a>

## AskTextField Objects

```python
@dataclass
class AskTextField(AskFieldCommon)
```

A text field in a form.

**Attributes**:

- `nullable` - When True an empty answer with no default is reported
  as None. When False an empty answer with no default is
  the empty string.
- `default` - The value returned when user fills in nothing, or None for
  no default. In a GUI implementation this is typically shown
  as the starting value in the input field, and the user can
  change it.
- `sensitive` - True when the bridge must avoid echoing the entered text,
  such as for passwords. A default is not allowed for a
  sensitive question.

<a id="wizard_ui_bridge.form_defs.AskIntField"></a>

## AskIntField Objects

```python
@dataclass
class AskIntField(AskFieldCommon)
```

An integer field in a form.

**Attributes**:

- `nullable` - When True an empty answer with no default is reported
  as None. When False an empty answer with no default will
  be re-asked until the user fills in a valid integer.
- `default` - The value returned when user fills in nothing, or None for
  no default. In a GUI implementation this is typically shown
  as the starting value in the input field, and the user can
  change it.
- `min_value` - The minimum allowed value, or None for no minimum.
- `max_value` - The maximum allowed value, or None for no maximum.

<a id="wizard_ui_bridge.form_defs.AskPathField"></a>

## AskPathField Objects

```python
@dataclass
class AskPathField(AskFieldCommon)
```

A path field in a form.

In a GUI implementation this is typically displayed as a text input field
with a button next to it that opens a file/directory chooser dialog.

**Attributes**:

- `path_options` - Options for how the path question is asked, including
  whether the path must exist, whether it must be a file
  or a directory.

<a id="wizard_ui_bridge.form_defs.AskYesNoField"></a>

## AskYesNoField Objects

```python
@dataclass
class AskYesNoField(AskFieldCommon)
```

A yes/no field in a form.

In a GUI implementation this is typically displayed as a checkbox or a
toggle button.

**Attributes**:

- `default` - The boolean value used when the user makes no explicit
  choice. In a GUI implementation this is typically shown as
  the starting value in the checkbox or toggle, and the user
  can change it.

<a id="wizard_ui_bridge.form_defs.AskChoiceField"></a>

## AskChoiceField Objects

```python
@dataclass
class AskChoiceField(AskFieldCommon)
```

A choice field in a form.

In a GUI implementation this is typically displayed as a dropdown list
or a set of radio buttons.

**Attributes**:

- `choices` - The allowed choices for the answer.
- `default` - The value returned when user fills in nothing, or None for
  no default. In a GUI implementation this is typically shown
  as the starting value in the input field, and the user can
  change it.

<a id="wizard_ui_bridge.form_defs.AskMultiChoiceField"></a>

## AskMultiChoiceField Objects

```python
@dataclass
class AskMultiChoiceField(AskFieldCommon)
```

A multi-choice field in a form.

In a GUI implementation this is typically displayed as a list of checkboxes
or a list of items with multiple selection enabled.

**Attributes**:

- `choices` - The allowed choices for the answer.
- `default` - The values returned when user fills in nothing, or None for
  no default. In a GUI implementation this is typically shown
  as the starting value in the input field, and the user can
  change it.
- `min_select` - The minimum number of choices that must be selected.
- `max_select` - The maximum number of choices that can be selected,
  or None for no maximum.

<a id="wizard_ui_bridge.form_defs.AskFloatField"></a>

## AskFloatField Objects

```python
@dataclass
class AskFloatField(AskFieldCommon)
```

A float field in a form.

**Attributes**:

- `nullable` - When True an empty answer with no default is reported
  as None. When False an empty answer with no default will
  be re-asked until the user fills in a valid number.
- `default` - The value returned when user fills in nothing, or None for
  no default. In a GUI implementation this is typically shown
  as the starting value in the input field, and the user can
  change it.
- `min_value` - The minimum allowed value, or None for no minimum.
  The min value is inclusive.
- `max_value` - The maximum allowed value, or None for no maximum.
  The max value is inclusive.

<a id="wizard_ui_bridge.form_defs.AskDateField"></a>

## AskDateField Objects

```python
@dataclass
class AskDateField(AskFieldCommon)
```

A date field in a form.

In a GUI implementation this is typically displayed as a text input field
with a button next to it that opens a date chooser dialog.

**Attributes**:

- `nullable` - When True an empty answer with no default is reported
  as None. When False an empty answer with no default will
  be re-asked until the user fills in a valid date.
- `default` - The value returned when user fills in nothing, or None for
  no default. In a GUI implementation this is typically shown
  as the starting value in the input field, and the user can
  change it.
- `min_value` - The minimum allowed value, or None for no minimum.
  The min value is inclusive.
- `max_value` - The maximum allowed value, or None for no maximum.
  The max value is inclusive.

<a id="wizard_ui_bridge.form_defs.AskTimeField"></a>

## AskTimeField Objects

```python
@dataclass
class AskTimeField(AskFieldCommon)
```

A time field in a form.

**Attributes**:

- `nullable` - When True an empty answer with no default is reported
  as None. When False an empty answer with no default will
  be re-asked until the user fills in a valid time.
- `default` - The value returned when user fills in nothing, or None for
  no default. In a GUI implementation this is typically shown
  as the starting value in the input field, and the user can
  change it.
- `min_value` - The minimum allowed value, or None for no minimum.
  The min value is inclusive.
- `max_value` - The maximum allowed value, or None for no maximum.
  The max value is inclusive.

<a id="wizard_ui_bridge.form_defs.AskDateTimeField"></a>

## AskDateTimeField Objects

```python
@dataclass
class AskDateTimeField(AskFieldCommon)
```

A date-time field in a form.

In a GUI implementation this is typically displayed as a text input field
with a button next to it that opens a date-time chooser dialog for the
date part.

**Attributes**:

- `nullable` - When True an empty answer with no default is reported
  as None. When False an empty answer with no default will
  be re-asked until the user fills in a valid date-time.
- `default` - The value returned when user fills in nothing, or None for
  no default. In a GUI implementation this is typically shown
  as the starting value in the input field, and the user can
  change it.
- `min_value` - The minimum allowed value, or None for no minimum.
  The min value is inclusive.
- `max_value` - The maximum allowed value, or None for no maximum.
  The max value is inclusive.

<a id="wizard_ui_bridge.form_defs.AskDurationField"></a>

## AskDurationField Objects

```python
@dataclass
class AskDurationField(AskFieldCommon)
```

A duration field in a form.

**Attributes**:

- `nullable` - When True an empty answer with no default is reported
  as None. When False an empty answer with no default will
  be re-asked until the user fills in a valid duration.
- `default` - The value returned when user fills in nothing, or None for
  no default. In a GUI implementation this is typically shown
  as the starting value in the input field, and the user can
  change it.
- `min_value` - The minimum allowed value, or None for no minimum.
  The min value is inclusive.
- `max_value` - The maximum allowed value, or None for no maximum.
  The max value is inclusive.

<a id="wizard_ui_bridge.form_defs.ALL_ASK_FIELD_TYPES"></a>

#### ALL\_ASK\_FIELD\_TYPES

Every concrete AskField class, in the order of the AskField union.

A bridge that shows all field types checks membership against this tuple
in supports_form_field(), so a field type added later is reported as
unsupported until this tuple and the bridge are extended together.

<a id="wizard_ui_bridge.form_defs.AnswerTextField"></a>

## AnswerTextField Objects

```python
@dataclass
class AnswerTextField()
```

An answer to a text field in a form.

**Attributes**:

- `asking` - How the question was asked, including the question text, help
  text, and other attributes of the question.
- `value` - The value of the answer, or None when the user did not fill in
  anything and the field is nullable.

<a id="wizard_ui_bridge.form_defs.AnswerIntField"></a>

## AnswerIntField Objects

```python
@dataclass
class AnswerIntField()
```

An answer to an integer field in a form.

**Attributes**:

- `asking` - How the question was asked, including the question text, help
  text, and other attributes of the question.
- `value` - The value of the answer, or None when the user did not fill in
  anything and the field is nullable.

<a id="wizard_ui_bridge.form_defs.AnswerPathField"></a>

## AnswerPathField Objects

```python
@dataclass
class AnswerPathField()
```

An answer to a path field in a form.

**Attributes**:

- `asking` - How the question was asked, including the question text, help
  text, and other attributes of the question.
- `value` - The value of the answer, or None when the user did not fill in
  anything and the field is nullable.

<a id="wizard_ui_bridge.form_defs.AnswerYesNoField"></a>

## AnswerYesNoField Objects

```python
@dataclass
class AnswerYesNoField()
```

An answer to a yes/no field in a form.

**Attributes**:

- `asking` - How the question was asked, including the question text, help
  text, and other attributes of the question.
- `value` - The value of the answer.

<a id="wizard_ui_bridge.form_defs.AnswerChoiceField"></a>

## AnswerChoiceField Objects

```python
@dataclass
class AnswerChoiceField()
```

An answer to a choice field in a form.

**Attributes**:

- `asking` - How the question was asked, including the question text, help
  text, and other attributes of the question.
- `value` - The chosen value, one of the choices. It is None only to
  tell a partial validator that a choice with no default has
  not been answered yet. A bridge never returns None as a final
  choice answer: it makes sure a choice with no default is
  answered before the form is submitted for final validation,
  unless the choice is disabled by a partial validator because
  it is irrelevant given the current state of the form.

<a id="wizard_ui_bridge.form_defs.AnswerMultiChoiceField"></a>

## AnswerMultiChoiceField Objects

```python
@dataclass
class AnswerMultiChoiceField()
```

An answer to a multi-choice field in a form.

**Attributes**:

- `asking` - How the question was asked, including the question text, help
  text, and other attributes of the question.
- `value` - The values of the answer.

<a id="wizard_ui_bridge.form_defs.AnswerFloatField"></a>

## AnswerFloatField Objects

```python
@dataclass
class AnswerFloatField()
```

An answer to a float field in a form.

**Attributes**:

- `asking` - How the question was asked, including the question text, help
  text, and other attributes of the question.
- `value` - The value of the answer, or None when the user did not fill in
  anything and the field is nullable.

<a id="wizard_ui_bridge.form_defs.AnswerDateField"></a>

## AnswerDateField Objects

```python
@dataclass
class AnswerDateField()
```

An answer to a date field in a form.

**Attributes**:

- `asking` - How the question was asked, including the question text, help
  text, and other attributes of the question.
- `value` - The value of the answer, or None when the user did not fill in
  anything and the field is nullable.

<a id="wizard_ui_bridge.form_defs.AnswerTimeField"></a>

## AnswerTimeField Objects

```python
@dataclass
class AnswerTimeField()
```

An answer to a time field in a form.

**Attributes**:

- `asking` - How the question was asked, including the question text, help
  text, and other attributes of the question.
- `value` - The value of the answer, or None when the user did not fill in
  anything and the field is nullable.

<a id="wizard_ui_bridge.form_defs.AnswerDateTimeField"></a>

## AnswerDateTimeField Objects

```python
@dataclass
class AnswerDateTimeField()
```

An answer to a date-time field in a form.

**Attributes**:

- `asking` - How the question was asked, including the question text, help
  text, and other attributes of the question.
- `value` - The value of the answer, or None when the user did not fill in
  anything and the field is nullable.

<a id="wizard_ui_bridge.form_defs.AnswerDurationField"></a>

## AnswerDurationField Objects

```python
@dataclass
class AnswerDurationField()
```

An answer to a duration field in a form.

**Attributes**:

- `asking` - How the question was asked, including the question text, help
  text, and other attributes of the question.
- `value` - The value of the answer, or None when the user did not fill in
  anything and the field is nullable.

<a id="wizard_ui_bridge.form_defs.PartFormValidationResult"></a>

## PartFormValidationResult Objects

```python
class PartFormValidationResult(NamedTuple)
```

Result of validating a partly filled form.

**Attributes**:

- `is_valid` - True when the form is valid, False when it is not valid.
- `message` - A message to be displayed to the user, explaining why the
  form is not valid. Empty string when the form is valid.
- `disable_row_idxs` - A tuple of row indexes that should be disabled in the
  form, because what has been filled in so far makes
  these rows irrelevant. For example if ouput format
  is set to some binary format, then the row(s) that
  ask for character encoding can be disabled, because
  they are irrelevant for the chosen output format.
  Actually disabling these rows is not strictly
  necessary, but it is a good user experience to do so.
- `prefill_values` - Values the validator asks the bridge to place into
  other rows' inputs, as a tuple of (row_index, value)
  pairs. Each value must match the answer type of the
  field in that row. A bridge applies each request
  during live editing as if the user had typed the
  value; setting a value equal to the one already there
  is a no-op, so a validator that emits a stable value
  does not loop. The validator owns idempotency: it
  should emit a prefill only when it means to fill or
  overwrite the target. A prefill aimed at the row that
  just changed is ignored, so writing back never fights
  the user's current edit. A prefill aimed at a disabled
  row is still applied, so the value shows in the greyed
  row and takes effect if the row is later enabled. A
  row index outside the form, or a value whose type does
  not match the field, raises an exception, since both
  are validator bugs. A choice or multi-choice value not
  among the field's choices, and any prefill of a
  sensitive field, are ignored. prefill_values is a
  live-editing convenience only and is ignored when the
  form is submitted, so an application must still apply
  the same default on submit.

<a id="wizard_ui_bridge.console"></a>

# wizard\_ui\_bridge.console

Console text user interface bridge for the configuration wizard.

This module provides the concrete console bridge used when the wizard
talks to a user through plain text streams. It recognises reserved
navigation tokens so a console user can step back, cancel the current
level or abandon the whole configuration.

<a id="wizard_ui_bridge.console.WizardUiBridgeConsole"></a>

## WizardUiBridgeConsole Objects

```python
class WizardUiBridgeConsole(WizardUiBridge)
```

Bridge between the wizard and the console text user interface.

<a id="wizard_ui_bridge.console.WizardUiBridgeConsole.__init__"></a>

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

<a id="wizard_ui_bridge.console.WizardUiBridgeConsole.ask_text"></a>

#### ask\_text

```python
def ask_text(question: str,
             re_ask_reason: Optional[str] = None,
             nullable: bool = False,
             *,
             default: Optional[str] = None,
             sensitive: bool = False) -> Optional[str]
```

Ask for free text on the console; see WizardUiBridge.ask_text.

<a id="wizard_ui_bridge.console.WizardUiBridgeConsole.supports_form_field"></a>

#### supports\_form\_field

```python
def supports_form_field(field: AskField) -> bool
```

Show every form field type; see WizardUiBridge.

The inherited base ask_form() asks each field with the typed ask
methods, so the console form handles the typed float, date, time,
date-time and duration fields as well as the original kinds.

<a id="wizard_ui_bridge.console.WizardUiBridgeConsole.ask_yes_no"></a>

#### ask\_yes\_no

```python
def ask_yes_no(question: str,
               default: bool,
               re_ask_reason: Optional[str] = None) -> bool
```

Ask a yes/no question on the console; see ask_yes_no.

<a id="wizard_ui_bridge.console.WizardUiBridgeConsole.ask_table"></a>

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

With both min_rows and max_rows given the table has a variable
number of rows, edited through a row-menu interface. Otherwise the
fixed rows in cells are filled one editable cell at a time.

<a id="wizard_ui_bridge.console.WizardUiBridgeConsole.ask_choice"></a>

#### ask\_choice

```python
def ask_choice(question: str,
               *,
               choices: Sequence[str],
               default: Optional[str] = None,
               re_ask_reason: Optional[str] = None) -> str
```

Ask one choice on the console; see WizardUiBridge.ask_choice.

<a id="wizard_ui_bridge.console.WizardUiBridgeConsole.ask_multi"></a>

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

<a id="wizard_ui_bridge.console.WizardUiBridgeConsole.error_file"></a>

#### error\_file

```python
def error_file() -> TextIO
```

Return the stream used for validation diagnostics.

<a id="wizard_ui_bridge.console.WizardUiBridgeConsole.show"></a>

#### show

```python
def show(message: str) -> None
```

Show a message to the user.

This method prints the message to the console.

**Arguments**:

- `message` - The message to show the user.

<a id="wizard_ui_bridge.arg_types"></a>

# wizard\_ui\_bridge.arg\_types

Types used as arguments to the WizardUiBridge class.

<a id="wizard_ui_bridge.arg_types.WizardNavigation"></a>

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

<a id="wizard_ui_bridge.arg_types.WizardBack"></a>

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

<a id="wizard_ui_bridge.arg_types.WizardCancelLevel"></a>

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
answers collected at the current level are not recorded as answers,
but a well crafted wizard keeps them in memory as drafts so that
they can be offered as defaults if the user returns to the level and
provided that answers to other questions have not invalidated them.

Each level's driver catches this from the level it opened and re-asks
the opening question. When the current level has no enclosing level,
the outermost driver cannot step out; following this contract it
re-asks the current question and tells the user there is no outer
level. Nesting may be arbitrarily deep: each driver either handles the
request for the level it opened or lets it propagate further out.

<a id="wizard_ui_bridge.arg_types.WizardAbort"></a>

## WizardAbort Objects

```python
class WizardAbort(WizardNavigation)
```

Request to abandon the whole configuration.

A bridge raises this when the user abandons configuration entirely.
The wizard does not catch it; it propagates out of the wizard call so
the application can stop the configuration session.

<a id="wizard_ui_bridge.arg_types.WizardPathKind"></a>

## WizardPathKind Objects

```python
class WizardPathKind(Enum)
```

Expected path type and existence for a path question.

<a id="wizard_ui_bridge.arg_types.PathAskOptions"></a>

## PathAskOptions Objects

```python
@dataclass(frozen=True)
class PathAskOptions()
```

Options for a path question.

<a id="wizard_ui_bridge.arg_types.TableColumn"></a>

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

<a id="wizard_ui_bridge.arg_types.TableCell"></a>

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

<a id="wizard_ui_bridge.form_helpers"></a>

# wizard\_ui\_bridge.form\_helpers

Helpers shared by the WizardUiBridge form question.

<a id="wizard_ui_bridge.form_helpers.initial_answer"></a>

#### initial\_answer

```python
def initial_answer(field: AskField) -> AnswerField
```

Return the starting answer for a field before the user edits it.

The value is the field's default, or the empty or not-yet-answered
state when the field has no default. A choice field with no default
starts as None, which tells a partial validator the choice is not
answered yet; a bridge must not leave that None in a submitted form.

<a id="wizard_ui_bridge.form_helpers.valid_prefills"></a>

#### valid\_prefills

```python
def valid_prefills(
        fields: Sequence[AskField], changed: int, prefill_values: PrefillValues
) -> Iterator[tuple[int, PrefillValueType]]
```

Yield the prefill requests a bridge should apply, validated.

Each yielded (index, value) pair is ready to place into the row's
input. A prefill aimed at the changed row is skipped, so writing back
never fights the user's current edit. A row index outside the form
raises IndexError and a value whose Python type does not match the
field raises TypeError, since both are validator bugs. A choice value
not among the field's choices, any prefill of a sensitive text field,
and a multi-choice value with no valid member, are dropped instead, so
a portable validator stays safe. A multi-choice value keeps only its
members that are valid choices.

<a id="wizard_ui_bridge.form_helpers.prefilled_field"></a>

#### prefilled\_field

```python
def prefilled_field(field: AskField, prefill: PrefillValueType) -> AskField
```

Return field with prefill as its default.

The console bridge offers a prefill as the row's default when the row
is asked. A prefill that cannot serve as a valid default, such as an
integer or date outside the field's bounds, is ignored so the field
keeps its own default. The prefill has already been checked against
the field type by valid_prefills().

<a id="wizard_ui_bridge.bridge"></a>

# wizard\_ui\_bridge.bridge

User interface bridge for the TableIO JSON configuration wizard.

This module defines the abstract bridge between the wizard and a user
interface, the navigation requests a bridge raises to steer wizard flow,
and the column and cell descriptors used by table questions. Concrete
console and graphical bridges derive from WizardUiBridge.

An application that drives the wizard is responsible for implementing
the typed ask methods of its bridge, together with show(). A concrete
bridge implements ask_text(), ask_choice(), ask_multi(), ask_yes_no()
and ask_table(); ask_path() has a permanent base implementation that a
bridge may override for a native file or directory picker. The low-level
ask() is deprecated: calling it, overriding it, and the typed-method
fallbacks written in terms of it each warn loudly. This is the LAST
release that supports ask(); the next release REMOVES it, dropping both
calling ask() and the fallbacks that let a bridge which only overrides
ask() keep working. Migrate every bridge to implement the typed methods
directly, or it will stop working.

A GUI, textual, curses or web application should override ask_form() to show
the whole form at once, so the user sees every question together and answers
them in any order. The base implementation is permanent and suitable for a
console text interface.

A GUI, textual, curses or web application should also override ask_path() to
provide a native file or directory picker. The base implementation asks for
text and validates the path.

<a id="wizard_ui_bridge.bridge.WizardUiBridge"></a>

## WizardUiBridge Objects

```python
class WizardUiBridge()
```

Bridge between the wizard and the user interface.

This is an abstract base class for a bridge between the wizard and
the user interface. Provide concrete classes of this bridge to allow
the wizard to use a console text user interface or a graphical user
interface.

A concrete bridge implements ask_text(), ask_choice(), ask_multi(),
ask_yes_no(), ask_table() and show(). It may override ask_path() for
a native file or directory picker; otherwise the base implementation
asks for text and validates the path. It may override ask_form() to
show the whole form at once, so the user sees every question together
and answers them in any order. Overriding ask_form() and ask_path()
is strongly recommended for a GUI, textual, curses or web application.

The low-level ask() is deprecated: calling it, overriding it, and the
typed-method fallbacks written in terms of it each warn loudly. This
is the LAST release that supports ask(); the next release REMOVES it,
dropping both the ability to call ask() and the fallbacks that let a
bridge which only overrides ask() keep working. Migrate every bridge
to implement ask_text(), ask_choice(), ask_multi(), ask_yes_no() and
ask_table() directly, or it will stop working.

Any ask method may raise a WizardNavigation subclass to request back,
cancel-level or abort instead of returning an answer.

<a id="wizard_ui_bridge.bridge.WizardUiBridge.ask"></a>

#### ask

```python
def ask(question: str,
        re_ask_reason: Optional[str] = None,
        choices: Optional[Sequence[str]] = None) -> str | int
```

Ask a question and return the user's answer.

Deprecated and REMOVED in the next release, after which this call
will stop working. Call ask_text() for free text or ask_choice()
for a single choice instead. This base implementation is temporary
plumbing: it warns loudly and then dispatches to ask_text() when no
choices are given and to ask_choice() otherwise, so existing
callers keep working for this last release.

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

<a id="wizard_ui_bridge.bridge.WizardUiBridge.ask_text"></a>

#### ask\_text

```python
def ask_text(question: str,
             re_ask_reason: Optional[str] = None,
             nullable: bool = False,
             *,
             default: Optional[str] = None,
             sensitive: bool = False) -> Optional[str]
```

Ask a free-text question and return the entered text.

The application is responsible for implementing this method with
a real text-entry control. As a temporary migration aid the base
class provides a fallback in terms of the deprecated ask(), so a
bridge that still overrides ask() keeps working for non-sensitive
questions.

**Arguments**:

- `question` - The question to ask the user.
- `re_ask_reason` - The reason for re-asking the question, for
  instance that the user's answer was invalid.
- `nullable` - When True an empty answer with no default is
  reported as None. When False an empty answer with
  no default is the empty string.
- `default` - The value returned by an empty answer, or None for
  no default.
- `sensitive` - True when the bridge must avoid echoing the
  entered text, such as for passwords. A default is
  not allowed for a sensitive question.
  

**Returns**:

  The entered text, default for an empty answer with a default,
  or None for an empty answer when nullable.

**Raises**:

- `ValueError` - default is given together with sensitive.
- `NotImplementedError` - The deprecated ask() fallback is used
  for sensitive input.
- `WizardBack` - The user asked to return to the previous question.
- `WizardCancelLevel` - The user cancelled the current level.
- `WizardAbort` - The user abandoned the whole configuration.

<a id="wizard_ui_bridge.bridge.WizardUiBridge.ask_int"></a>

#### ask\_int

```python
def ask_int(question: str,
            re_ask_reason: Optional[str] = None,
            *,
            nullable: bool = False,
            min_value: Optional[int] = None,
            max_value: Optional[int] = None,
            default: Optional[int] = None) -> Optional[int]
```

Ask for an integer, optionally within inclusive bounds.

The base implementation uses ask_text() and re-asks until the
answer is empty when allowed or parses as an integer in range. A
derived bridge may override it with a direct numeric control.

**Arguments**:

- `question` - The question to ask the user.
- `re_ask_reason` - The reason for re-asking the question, for
  instance that the user's answer was invalid.
- `nullable` - When True an empty answer is reported as None, so
  the caller can treat it as a request to use the
  default. When False an empty answer will be re-asked
  until a valid answer is entered.
- `min_value` - The minimum allowed value, or None for no lower bound.
  The min value is inclusive.
- `max_value` - The maximum allowed value, or None for no upper bound.
  The max value is inclusive.
- `default` - The value returned by an empty answer, or None for
  no default.
  

**Returns**:

  The entered integer, default for an empty answer with a
  default, or None for an empty answer when nullable.

**Raises**:

- `WizardBack` - The user asked to return to the previous question.
- `WizardCancelLevel` - The user cancelled the current level.
- `WizardAbort` - The user abandoned the whole configuration.

<a id="wizard_ui_bridge.bridge.WizardUiBridge.ask_path"></a>

#### ask\_path

```python
def ask_path(question: str,
             re_ask_reason: Optional[str] = None,
             *,
             options: Optional[PathAskOptions] = None) -> Optional[Path]
```

Ask a question for a path and return the accepted path.

A derived bridge may override this method to provide a native file
or directory picker. The base implementation is permanent and
asks for text through ask_text(), then validates the answer.

**Arguments**:

- `question` - The question to ask the user.
- `re_ask_reason` - The reason for re-asking the question.
- `options` - Path options. None only rejects existing directories.
  

**Returns**:

  The accepted path, a default path, or None when nullable.

**Raises**:

- `WizardBack` - The user asked to return to the previous question.
- `WizardCancelLevel` - The user cancelled the current level.
- `WizardAbort` - The user abandoned the whole configuration.

<a id="wizard_ui_bridge.bridge.WizardUiBridge.ask_yes_no"></a>

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

<a id="wizard_ui_bridge.bridge.WizardUiBridge.ask_choice"></a>

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

<a id="wizard_ui_bridge.bridge.WizardUiBridge.ask_multi"></a>

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

<a id="wizard_ui_bridge.bridge.WizardUiBridge.ask_table"></a>

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

<a id="wizard_ui_bridge.bridge.WizardUiBridge.ask_form"></a>

#### ask\_form

```python
def ask_form(
        long_question: str,
        ask_fields: AskFields,
        *,
        re_ask_reason: Optional[str] = None,
        partial_validator: Optional[PartialFormValidator] = None
) -> AnswerFields
```

Ask the user to fill in a form and return the answers.

The bridge shows a form whose fields are described by ask_fields.
The base implementation is permanent and suitable for a console
text interface: it shows long_question, then asks each field in
turn with the typed ask methods ask_text(), ask_int(),
ask_yes_no(), ask_path(), ask_choice() and ask_multi(), and
returns one AnswerField per field in the same order.

Any serious application or library using GUI, textual, curses or
web interfaces should override this method to show the whole form
at once, so the user sees every question together and answers them
in any order. In such an implementation ask_form is typically a
dialog or form window with long_question and re_ask_reason shown
above a grid with two columns: the left column a label with the
field's short question, and the right column an input widget.

See wizard_ui_bridge_form_defs.py for the AskFields, and the
description of how each field type is typically implemented in a GUI
or textual interface.

When partial_validator is given, the base implementation calls it
after each field is answered, passing the current answers and the
index of the field just answered. It shows the returned message and
skips asking the fields listed in disable_row_idxs, filling them
with their default or not-yet-answered value instead. WizardBack
steps to the previous asked field; from the first field it
propagates so the wizard steps to the previous question.

**Arguments**:

- `long_question` - The main question or instruction to the user,
  typically shown above the form. It may be long
  string that the UI bridge is responsible for
  wrapping and displaying nicely.
- `ask_fields` - Description of each field in the form.
- `re_ask_reason` - The reason for re-asking, for instance how a
  value failed validation.
- `partial_validator` - Optional callback for early per-field
  feedback. It receives the current answers
  and the changed field index, and returns a
  PartFormValidationResult.
  

**Returns**:

  One AnswerField per AskField, in the order of ask_fields.

**Raises**:

- `WizardBack` - The user asked to return to the previous question.
- `WizardCancelLevel` - The user cancelled the current level.
- `WizardAbort` - The user abandoned the whole configuration.

<a id="wizard_ui_bridge.bridge.WizardUiBridge.supports_form_field"></a>

#### supports\_form\_field

```python
def supports_form_field(field: AskField) -> bool
```

Return True when the bridge can show the given form field.

A bridge that overrides ask_form() may not yet support all
the AskField types. This method returns True when the bridge can
show the given field, and False when it cannot. The base implementation
returns True only for the field types that oldest form bridges support,
so a bridge that overrides ask_form() should override this method as
well.

**Arguments**:

- `field` - The form field to check.

**Returns**:

  True if the bridge can show the field, False otherwise.

<a id="wizard_ui_bridge.bridge.WizardUiBridge.ask_form_w_fake"></a>

#### ask\_form\_w\_fake

```python
def ask_form_w_fake(
        long_question: str,
        ask_fields: AskFields,
        *,
        re_ask_reason: Optional[str] = None,
        partial_validator: Optional[PartialFormValidator] = None
) -> AnswerFields
```

Ask the user to fill in a form faking unsupported field types.

This is a temporary migration aid for a wizard that uses field types
the bridge does not yet support. It replaces each unsupported field
with a supported field that asks the question and inserts a partial
form validator that guides the answer to something that can be
converted to the unsupported field type. ask_form() is then called
with the modified fields and validator, and the answers are converted
back to the original field types before returning.

**Arguments**:

- `long_question` - The main question or instruction to the user,
  typically shown above the form. It may be long
  string that the UI bridge is responsible for
  wrapping and displaying nicely.
- `ask_fields` - Description of each field in the form.
- `re_ask_reason` - The reason for re-asking, for instance how a
  value failed validation.
- `partial_validator` - Optional callback for early per-field
  feedback. It receives the current answers
  and the changed field index, and returns a
  PartFormValidationResult.
  

**Returns**:

  One AnswerField per AskField, in the order of ask_fields.

**Raises**:

- `WizardBack` - The user asked to return to the previous question.
- `WizardCancelLevel` - The user cancelled the current level.
- `WizardAbort` - The user abandoned the whole configuration.
- `RuntimeError` - The bridge cannot show any field type that would
  allow the requested field types to be faked, so
  the form cannot be shown at all.

<a id="wizard_ui_bridge.bridge.WizardUiBridge.error_file"></a>

#### error\_file

```python
def error_file() -> TextIO
```

Return the stream used for validation diagnostics.

<a id="wizard_ui_bridge.bridge.WizardUiBridge.show"></a>

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

<a id="wizard_ui_bridge.factory"></a>

# wizard\_ui\_bridge.factory

Factory selecting a text-mode user interface bridge.

The wizard talks to the user through a WizardUiBridge. This factory
returns a Textual full-screen bridge when Textual is installed and the
streams are a real terminal, and falls back to the console bridge
otherwise, such as when output is redirected, when running under tests,
or where Textual is not available. The fallback keeps the library
importable and usable even if Textual has been uninstalled.

Textual is an optional dependency, installed with the extra
`wizard-ui-bridge[textual]`. The Textual bridge is therefore imported
only when it is about to be used, and asking for it without Textual
installed raises ImportError instead of degrading silently.

This factory chooses between text-mode bridges only. An application
with a graphical user interface should provide and use its own
graphical bridge instead.

<a id="wizard_ui_bridge.factory.textual_installed"></a>

#### textual\_installed

```python
def textual_installed() -> bool
```

Return whether the optional textual package is installed.

<a id="wizard_ui_bridge.factory.load_textual_bridge"></a>

#### load\_textual\_bridge

```python
def load_textual_bridge() -> type[WizardUiBridge]
```

Return the Textual bridge class, importing it on demand.

Textual is only imported here, so that a program that never asks
for the Textual bridge never pays for importing Textual. The
availability check keeps the missing-package case a clear
ImportError, while any other import error in the Textual bridge
itself is still reported as the error it is.

**Raises**:

- `ImportError` - If the optional textual package is not installed.

<a id="wizard_ui_bridge.factory.UiBridgeType"></a>

## UiBridgeType Objects

```python
class UiBridgeType(Enum)
```

Type of wizard user interface bridge.

AUTO: Auto-select the best bridge based on the environment.
      This will use Textual if it is installed and the streams
      are a terminal, else a console bridge.
TEXTUAL: Use the Textual bridge, even if it might fail.
CONSOLE: Use the console bridge, even if Textual could be used.

<a id="wizard_ui_bridge.factory.make_text_ui_bridge"></a>

#### make\_text\_ui\_bridge

```python
def make_text_ui_bridge(
        stdout_file: TextIO,
        stdin_file: TextIO,
        stderr_file: TextIO,
        bridge_type: UiBridgeType = UiBridgeType.AUTO) -> WizardUiBridge
```

Return a Textual bridge for a terminal, else a console bridge.

**Arguments**:

- `stdout_file` - Stream the console bridge prints to, also checked
  for being a terminal.
- `stdin_file` - Stream the console bridge reads from, also checked
  for being a terminal.
- `stderr_file` - Stream the console bridge prints errors to.
- `bridge_type` - Type of bridge to use. Defaults to AUTO.
  If AUTO, select the best bridge based on the environment.
  If TEXTUAL, use the Textual bridge that might fail.
  If CONSOLE, use the console bridge.
  

**Raises**:

- `ImportError` - If TEXTUAL is asked for but textual is not installed.
  

**Returns**:

  A Textual bridge when Textual is installed and both streams are
  a terminal, otherwise a console bridge.

<a id="wizard_ui_bridge._parse"></a>

# wizard\_ui\_bridge.\_parse

Text parsing and formatting for the typed form fields.

The float, date, time, date-time and duration form fields all need to
turn user text into a typed value and a typed value back into text. This
module holds that shared conversion, together with the human-readable
hints and error messages, so the console form, the Textual form and the
ask_form_w_fake() fallback all agree on the accepted text.

A duration is written as an optional day count and a clock part,
``<days> d <hours>:<minutes>:<seconds>``, where the seconds may carry a
decimal fraction, or as a single non-negative number of seconds. Dates,
times and date-times use the ISO 8601 forms accepted by the standard
library fromisoformat() parsers.

<a id="wizard_ui_bridge._parse.NEW_FIELD_TYPES"></a>

#### NEW\_FIELD\_TYPES

The typed form field classes added on top of the original six.

<a id="wizard_ui_bridge._parse.parse_float"></a>

#### parse\_float

```python
def parse_float(text: str) -> Optional[float]
```

Return a finite float from text, or None when not a number.

<a id="wizard_ui_bridge._parse.parse_date"></a>

#### parse\_date

```python
def parse_date(text: str) -> Optional[date]
```

Return an ISO date from text, or None when not a valid date.

<a id="wizard_ui_bridge._parse.parse_time"></a>

#### parse\_time

```python
def parse_time(text: str) -> Optional[time]
```

Return an ISO time from text, or None when not a valid time.

<a id="wizard_ui_bridge._parse.parse_datetime"></a>

#### parse\_datetime

```python
def parse_datetime(text: str) -> Optional[datetime]
```

Return an ISO date-time from text, or None when not valid.

<a id="wizard_ui_bridge._parse.parse_duration"></a>

#### parse\_duration

```python
def parse_duration(text: str) -> Optional[timedelta]
```

Return a duration from text, or None when it is not valid.

A lone non-negative number is read as a count of seconds; otherwise
the text must be ``<hours>:<minutes>:<seconds>`` with an optional
``<days> d`` prefix, and the seconds may carry a decimal fraction.

<a id="wizard_ui_bridge._parse.format_duration"></a>

#### format\_duration

```python
def format_duration(value: timedelta) -> str
```

Return a duration as ``<days> d HH:MM:SS`` with any fraction.

<a id="wizard_ui_bridge._parse.format_new_value"></a>

#### format\_new\_value

```python
def format_new_value(value: object) -> str
```

Return the text a typed value would round-trip from.

<a id="wizard_ui_bridge._parse.ordered_range_error"></a>

#### ordered\_range\_error

```python
def ordered_range_error(minimum: Optional[object],
                        maximum: Optional[object]) -> str
```

Return the message shown when a typed value is out of range.

<a id="wizard_ui_bridge._parse.ask_typed"></a>

#### ask\_typed

```python
def ask_typed(ask_text: _AskText, field: _TypedField[_OrderedT],
              parse: Callable[[str], Optional[_OrderedT]],
              hint: str) -> Optional[_OrderedT]
```

Re-ask a typed field through ask_text until the value is usable.

The hint is shown in the question and repeated in the parse-error
message, so a console user learns the accepted text format. An empty
answer yields the field default, or None when the field is nullable.

<a id="wizard_ui_bridge._parse.resolve_new"></a>

#### resolve\_new

```python
def resolve_new(field: AskField,
                text: Optional[str]) -> tuple[Optional[object], Optional[str]]
```

Return the typed value for a typed field's text, and any error.

A None text is an empty nullable answer, which is valid and has no
value. Otherwise the text is parsed and range-checked for the field's
type; the error is the reason to re-ask when the value is not usable.

<a id="wizard_ui_bridge._parse.new_answer"></a>

#### new\_answer

```python
def new_answer(field: AskField, value: Optional[object]) -> AnswerField
```

Wrap a typed value in the answer matching a typed field.

<a id="wizard_ui_bridge._parse.field_hint"></a>

#### field\_hint

```python
def field_hint(field: AskField) -> str
```

Return the format hint shown for a typed field.

<a id="wizard_ui_bridge._parse.value_from_text"></a>

#### value\_from\_text

```python
def value_from_text(field: AskField, text: str) -> Optional[object]
```

Return the typed value of a typed field for widget text.

An empty text yields the field default, matching how the console form
treats an empty answer. A non-empty text is parsed; unparsable or
out-of-range text yields None, and the caller reports the error.

<a id="wizard_ui_bridge._parse.error_from_text"></a>

#### error\_from\_text

```python
def error_from_text(field: AskField, text: str) -> Optional[str]
```

Return the parse or range error of a typed field's widget text.

Empty text is accepted when the field is nullable or has a default,
and otherwise reports that a value is required.

<a id="wizard_ui_bridge._parse.fake_field"></a>

#### fake\_field

```python
def fake_field(field: AskField) -> AskTextField
```

Return the text field used to fake an unsupported typed field.

<a id="wizard_ui_bridge._form_prefill"></a>

# wizard\_ui\_bridge.\_form\_prefill

Apply a partial validator's prefills to a Textual form's widgets.

The Textual form bridge asks the partial validator after every change and
then places the prefill values it returns into the matching field widgets,
exactly as if the user had typed them. This module holds that write-back,
kept apart from the large Textual bridge module.

<a id="wizard_ui_bridge._form_prefill.apply_prefills"></a>

#### apply\_prefills

```python
def apply_prefills(form: DOMNode, fields: Sequence[AskField], changed: int,
                   prefill_values: PrefillValues) -> None
```

Write each valid prefill into its row's widget in form.

A disabled row is written too, so the value shows greyed and takes
effect if the row is later enabled. Writing a value equal to the one
already there is a no-op, so a stable validator does not loop.

<a id="wizard_ui_bridge._fake"></a>

# wizard\_ui\_bridge.\_fake

Fake unsupported typed form fields as text fields.

A wizard may use the float, date, time, date-time or duration form
fields with a bridge that overrides ask_form() but was written before
those field types existed. Such a bridge reports through
supports_form_field() that it cannot show them. This module lets the
wizard still use one form: each unsupported field is shown as a text
field, a wrapping validator parses the text and guides the user to a
convertible value, and the text answers are converted back to the
requested typed answers.

The whole form is shown once by the bridge's own ask_form(), so the user
still sees and edits every field together. The parsing, formatting and
range messages are shared with the console and Textual forms through the
_wizard_ui_bridge_parse module, so the faked fields accept exactly the
same text.

<a id="wizard_ui_bridge._fake.ask_form_faking"></a>

#### ask\_form\_faking

```python
def ask_form_faking(
        bridge: _FakeableBridge, long_question: str, ask_fields: AskFields, *,
        re_ask_reason: Optional[str],
        partial_validator: Optional[PartialFormValidator]) -> AnswerFields
```

Show a form, faking the fields the bridge cannot show as text.

Raises RuntimeError when a field is unsupported and cannot be faked.

<a id="wizard_ui_bridge.bridge_helpers"></a>

# wizard\_ui\_bridge.bridge\_helpers

Helpers for implementing a WizardUiBridge.

The names without a leading underscore are the public helpers a bridge
implementation can use to interpret raw user answers the same way the
bundled bridges do, and the messages those bridges show when an answer
is not accepted.

<a id="wizard_ui_bridge.bridge_helpers.check_text_args"></a>

#### check\_text\_args

```python
def check_text_args(default: Optional[str], sensitive: bool) -> None
```

Raise when text-question arguments are inconsistent.

<a id="wizard_ui_bridge.bridge_helpers.question_with_default"></a>

#### question\_with\_default

```python
def question_with_default(question: str, default: Optional[str]) -> str
```

Return question with a bracketed default when one is given.

<a id="wizard_ui_bridge.bridge_helpers.text_answer"></a>

#### text\_answer

```python
def text_answer(text: str, nullable: bool,
                default: Optional[str]) -> Optional[str]
```

Return the public text answer for raw text from a bridge.

<a id="wizard_ui_bridge.bridge_helpers.path_answer"></a>

#### path\_answer

```python
def path_answer(
        text: Optional[str],
        options: PathAskOptions) -> tuple[bool, Optional[Path], Optional[str]]
```

Return whether a path answer is final, its value, and retry reason.

<a id="wizard_ui_bridge.bridge_helpers.ask_yes_no"></a>

#### ask\_yes\_no

```python
def ask_yes_no(reader: Callable[[Optional[str]], str | int], default: bool,
               re_ask_reason: Optional[str]) -> bool
```

Re-ask through reader until a yes/no answer is understood.

<a id="wizard_ui_bridge.bridge_helpers.run_table"></a>

#### run\_table

```python
def run_table(
        ask: AskReader, show: Callable[[str], None],
        columns: Sequence[TableColumn], cells: list[list[TableCell]],
        question: str, re_ask_reason: Optional[str],
        partial_check: Optional[PartialCheck]) -> list[list[Optional[str]]]
```

Show one table question and fill its editable cells via ask.

The read-only cells stay fixed and only the editable cells are asked,
one at a time, through the ask reader. This is the shared core of the
console table interface and the deprecated base-class table fallback.

<a id="wizard_ui_bridge.bridge_helpers.fill_cell"></a>

#### fill\_cell

```python
def fill_cell(
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

<a id="wizard_ui_bridge.bridge_helpers.cell_checker"></a>

#### cell\_checker

```python
def cell_checker(
    table: list[list[Optional[str]]], position: tuple[int, int],
    partial_check: Optional[PartialCheck]
) -> Callable[[Optional[str]], Optional[str]]
```

Return a per-cell check that records a candidate and validates it.

<a id="wizard_ui_bridge.bridge_helpers.int_text"></a>

#### int\_text

```python
def int_text(text: str) -> Optional[int]
```

Return an integer from text, or None when text is not an integer.

<a id="wizard_ui_bridge.bridge_helpers.out_of_range"></a>

#### out\_of\_range

```python
def out_of_range(value: int, min_value: Optional[int],
                 max_value: Optional[int]) -> bool
```

Return whether value lies outside the inclusive bounds.

<a id="wizard_ui_bridge.bridge_helpers.range_error"></a>

#### range\_error

```python
def range_error(min_value: Optional[int], max_value: Optional[int]) -> str
```

Return the message shown when an integer is out of range.

<a id="wizard_ui_bridge.bridge_helpers.ask_one"></a>

#### ask\_one

```python
def ask_one(reader: Callable[[Optional[str]],
                             str | int], choices: Sequence[str],
            default: Optional[str], re_ask_reason: Optional[str]) -> str
```

Re-ask through reader until one valid choice is selected.

<a id="wizard_ui_bridge.bridge_helpers.ask_many"></a>

#### ask\_many

```python
def ask_many(reader: Callable[[Optional[str]], str | int],
             choices: Sequence[str], default: Optional[Sequence[str]],
             min_select: int, max_select: Optional[int],
             re_ask_reason: Optional[str], one_based: bool) -> list[str]
```

Re-ask through reader until a valid set of choices is selected.

<a id="wizard_ui_bridge.bridge_helpers.match_token"></a>

#### match\_token

```python
def match_token(token: str, choices: Sequence[str],
                one_based: bool) -> Optional[str]
```

Map one menu index or name to a choice, or None when no match.

<a id="wizard_ui_bridge.bridge_helpers.multi_count_error"></a>

#### multi\_count\_error

```python
def multi_count_error(min_select: int, max_select: Optional[int]) -> str
```

Return the message shown when the selected count is not allowed.

<a id="wizard_ui_bridge.textual_bridge"></a>

# wizard\_ui\_bridge.textual\_bridge

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

<a id="wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual"></a>

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

<a id="wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.__init__"></a>

#### \_\_init\_\_

```python
def __init__() -> None
```

Start with an empty diagnostics buffer and message list.

<a id="wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.ask_text"></a>

#### ask\_text

```python
def ask_text(question: str,
             re_ask_reason: Optional[str] = None,
             nullable: bool = False,
             *,
             default: Optional[str] = None,
             sensitive: bool = False) -> Optional[str]
```

Ask for free text; see WizardUiBridge.ask_text.

<a id="wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.ask_path"></a>

#### ask\_path

```python
def ask_path(question: str,
             re_ask_reason: Optional[str] = None,
             *,
             options: Optional[PathAskOptions] = None) -> Optional[Path]
```

Ask for a path with a directory tree and editable path input.

<a id="wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.ask_yes_no"></a>

#### ask\_yes\_no

```python
def ask_yes_no(question: str,
               default: bool,
               re_ask_reason: Optional[str] = None) -> bool
```

Ask a yes/no question; see WizardUiBridge.ask_yes_no.

<a id="wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.ask_choice"></a>

#### ask\_choice

```python
def ask_choice(question: str,
               *,
               choices: Sequence[str],
               default: Optional[str] = None,
               re_ask_reason: Optional[str] = None) -> str
```

Ask the user to pick one choice; see ask_choice.

<a id="wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.ask_multi"></a>

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

<a id="wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.ask_table"></a>

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

<a id="wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.ask_form"></a>

#### ask\_form

```python
def ask_form(
        long_question: str,
        ask_fields: AskFields,
        *,
        re_ask_reason: Optional[str] = None,
        partial_validator: Optional[PartialFormValidator] = None
) -> AnswerFields
```

Ask the user to fill a whole form on one screen; see ask_form.

<a id="wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.supports_form_field"></a>

#### supports\_form\_field

```python
def supports_form_field(field: AskField) -> bool
```

Show every form field type; see WizardUiBridge.

The Textual form has a widget for each field type, including a
text input for float, time and duration fields and a text input
with a calendar Pick button for date and date-time fields.

<a id="wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.error_file"></a>

#### error\_file

```python
def error_file() -> StringIO
```

Return the in-memory stream shown on the next screen.

<a id="wizard_ui_bridge.textual_bridge.WizardUiBridgeTextual.show"></a>

#### show

```python
def show(message: str) -> None
```

Buffer a message for the next question's screen.

A message shown when no further question follows is not
displayed, because only a Textual screen renders it.

