#! /usr/bin/env python3
"""Tests for the Textual option-form screen.

This covers the grid form of typed fields, its live and on-submit
validation, the directory picker opened from a path field and the
bridge method that maps the form outcome back to the wizard.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

# pylint: disable=protected-access

import asyncio
from pathlib import Path

import pytest
from textual.widgets import Button, Input, SelectionList, Static

from tableio_cfg_json import AskField, AskChoiceField, AskIntField, \
    AskMultiChoiceField, AskPathField, AskTextField, AskYesNoField, \
    AnswerTextField, PartialFormValidator, PathAskOptions, WizardBack, \
    WizardCancelLevel, WizardPathKind
from tableio_cfg_json.wizard_ui_bridge_textual import _FormApp, \
    _browse_index, _field_index
from .ui_textual_support import drive, open_picker, _CannedBridge, _submitted


def _sample_form() -> list[AskField]:
    """Return one field of each kind for the form screen tests."""
    return [
        AskTextField('Name', None, default='Tom'),
        AskIntField('Age', None, default=30),
        AskYesNoField('Sub?', None, True),
        AskChoiceField('Color', None, choices=('red', 'green', 'blue'),
                       default='green'),
        AskMultiChoiceField('Tags', None, choices=('a', 'b', 'c'),
                            default=('a',))]


def _status(app: _FormApp) -> str:
    """Return the text currently shown in the form status line."""
    return str(app.query_one('#form_status', Static).render())


def test_form_defaults() -> None:
    """Submitting a form unchanged returns each field's default."""
    driven = drive(_FormApp('H', _sample_form(), [], None), ['#submit'])
    assert [answer.value for answer in _submitted(driven)] == \
        ['Tom', 30, True, 'green', ['a']]


def test_form_text_typed() -> None:
    """A text field returns the characters typed into it."""
    fields: list[AskField] = [AskTextField('Name', None)]
    driven = drive(_FormApp('H', fields, [], None), ['h', 'i', '#submit'])
    assert _submitted(driven)[0].value == 'hi'


def test_form_yesno_toggle() -> None:
    """Toggling the check box flips the yes/no answer."""
    fields: list[AskField] = [AskYesNoField('Sub?', None, False)]
    driven = drive(_FormApp('H', fields, [], None), ['space', '#submit'])
    assert _submitted(driven)[0].value is True


def test_form_choice_pick() -> None:
    """Picking a drop-down option returns that choice."""
    fields: list[AskField] = [
        AskChoiceField('C', None, choices=('x', 'y', 'z'))]
    driven = drive(_FormApp('H', fields, [], None),
                   ['enter', 'down', 'enter', 'ctrl+s'])
    assert _submitted(driven)[0].value == 'x'


def test_form_multi_select() -> None:
    """A multi-choice field returns the selected values in order."""
    fields: list[AskField] = [
        AskMultiChoiceField('T', None, choices=('a', 'b', 'c'))]
    driven = drive(_FormApp('H', fields, [], None),
                   ['space', 'down', 'down', 'space', 'ctrl+s'])
    assert _submitted(driven)[0].value == ['a', 'c']


def test_form_blank_choice() -> None:
    """A choice with no default left blank refuses to submit."""
    fields: list[AskField] = [AskChoiceField('C', None, choices=('x', 'y'))]
    driven = drive(_FormApp('H', fields, [], None), ['#submit'])
    assert driven.return_value is None


def test_form_int_range() -> None:
    """An integer outside the field bounds refuses to submit."""
    fields: list[AskField] = [
        AskIntField('N', None, min_value=1, max_value=5)]
    driven = drive(_FormApp('H', fields, [], None), ['9', '#submit'])
    assert driven.return_value is None


def test_form_multi_min() -> None:
    """A multi-choice below its minimum count refuses to submit."""
    fields: list[AskField] = [
        AskMultiChoiceField('T', None, choices=('a', 'b'), min_select=1)]
    driven = drive(_FormApp('H', fields, [], None), ['#submit'])
    assert driven.return_value is None


def test_form_multi_fits() -> None:
    """A multi-choice list sits fully inside the grid, not clipped.

    The check-box list would otherwise inherit a parent-relative
    max-height that collapses its grid row to one line, leaving only the
    top border visible. The definite max-height in the form CSS lets the
    auto-height grid reserve the whole widget.
    """
    app = _FormApp('H', _sample_form(), [], None)

    async def scenario() -> tuple[int, int]:
        async with app.run_test(size=(80, 24)) as pilot:
            await pilot.pause()
            multi = app.query_one(SelectionList)
            grid = app.query_one('#form_grid')
            return (multi.region.bottom, grid.region.bottom)
    multi_bottom, grid_bottom = asyncio.run(scenario())
    assert multi_bottom <= grid_bottom


def test_form_partial_disable(toggle_fields: list[AskField],
                              toggle_validator: PartialFormValidator) -> None:
    """A disabled row's widgets are disabled and skip validation."""
    app = _FormApp('H', toggle_fields, [], toggle_validator)

    async def scenario() -> bool:
        async with app.run_test() as pilot:
            app.query_one('#field_0').focus()
            await pilot.press('space')
            await pilot.pause()
            disabled = app.query_one('#field_1').disabled
            await pilot.click('#submit')
            return disabled
    assert asyncio.run(scenario()) is True
    assert _submitted(app)[1].value is None


def test_form_live_path_error(tmp_path: Path) -> None:
    """An existing file shows an error while editing, then clears.

    On the console the path is re-asked at once, so the form gives the
    same immediate feedback instead of only reporting it on submit.
    """
    existing = tmp_path / 'there.csv'
    existing.write_text('x')
    field = AskPathField('File', None, PathAskOptions(
        kind=WizardPathKind.NON_EXISTING_FILE))
    app = _FormApp('H', [field], [], None)

    async def scenario() -> tuple[str, str]:
        async with app.run_test() as pilot:
            app.query_one('#field_0', Input).value = str(existing)
            await pilot.pause()
            shown = _status(app)
            app.query_one('#field_0', Input).value = str(tmp_path / 'new.csv')
            await pilot.pause()
            return (shown, _status(app))
    error, cleared = asyncio.run(scenario())
    assert error == 'Path already exists.'
    assert cleared == ''


def test_form_live_int_error() -> None:
    """An out-of-range integer shows its error while editing."""
    fields: list[AskField] = [
        AskIntField('N', None, min_value=1, max_value=5)]
    app = _FormApp('H', fields, [], None)

    async def scenario() -> str:
        async with app.run_test() as pilot:
            app.query_one('#field_0', Input).value = '9'
            await pilot.pause()
            return _status(app)
    assert 'between 1 and 5' in asyncio.run(scenario())


def test_form_live_disabled(toggle_fields: list[AskField],
                            toggle_validator: PartialFormValidator) -> None:
    """A disabled field shows no live error of its own."""
    app = _FormApp('H', toggle_fields, [], toggle_validator)

    async def scenario() -> str:
        async with app.run_test() as pilot:
            app.query_one('#field_0').focus()
            await pilot.press('space')
            await pilot.pause()
            app._changed('field_1')
            await pilot.pause()
            return _status(app)
    assert asyncio.run(scenario()) == ''


def test_form_help_tooltip() -> None:
    """A field's help text becomes the tooltip of its widget and label."""
    fields: list[AskField] = [AskTextField('Name', 'your full name')]
    app = _FormApp('H', fields, [], None)

    async def scenario() -> tuple[object, object]:
        async with app.run_test():
            return (app.query_one('#field_0').tooltip,
                    app.query_one('#label_0').tooltip)
    assert asyncio.run(scenario()) == ('your full name', 'your full name')


def test_form_nav_back() -> None:
    """ctrl+b on the form records a back request and exits."""
    fields: list[AskField] = [AskTextField('Name', None)]
    driven = drive(_FormApp('H', fields, [], None), ['ctrl+b'])
    assert driven.return_value is None
    assert driven.nav is WizardBack


def test_ask_form_canned() -> None:
    """ask_form returns the answers produced by the form screen."""
    field = AskTextField('Name', None)
    answers = [AnswerTextField(field, 'typed')]
    bridge = _CannedBridge([answers])
    assert bridge.ask_form('H', [field]) == answers


def test_ask_form_nav() -> None:
    """ask_form re-raises a navigation request from the screen."""
    bridge = _CannedBridge([WizardCancelLevel])
    with pytest.raises(WizardCancelLevel):
        bridge.ask_form('H', [AskTextField('Name', None)])


def test_ask_form_messages() -> None:
    """A re-ask reason and a shown message reach the form header."""
    field = AskTextField('Name', None)
    bridge = _CannedBridge([[AnswerTextField(field, 'x')]])
    bridge.show('note')
    bridge.ask_form('H', [field], re_ask_reason='bad value')
    app = bridge.launched[0]
    assert isinstance(app, _FormApp)
    assert 'note' in app._messages
    assert 'bad value' in app._messages


def test_field_index() -> None:
    """A field id parses to its index; other ids parse to None."""
    assert _field_index('field_4') == 4
    assert _field_index(None) is None
    assert _field_index('label_2') is None


def test_browse_index() -> None:
    """A browse id parses to its index; other ids parse to None."""
    assert _browse_index('browse_3') == 3
    assert _browse_index(None) is None
    assert _browse_index('field_1') is None


def test_form_path_default(tmp_path: Path) -> None:
    """A form path field submits its default path unchanged."""
    target = tmp_path / 'out.csv'
    field = AskPathField('File', None, PathAskOptions(default=target))
    driven = drive(_FormApp('H', [field], [], None), ['#submit'])
    assert _submitted(driven)[0].value == target


def test_form_browse_fills(tmp_path: Path) -> None:
    """Submitting the picker fills the form path field."""
    picked = tmp_path / 'picked.csv'
    field = AskPathField('File', None, PathAskOptions())
    app = _FormApp('H', [field], [], None)

    async def scenario() -> None:
        async with app.run_test() as pilot:
            await open_picker(pilot, str(picked))
            await pilot.press('ctrl+s')
            await pilot.pause()
            await pilot.click('#submit')
    asyncio.run(scenario())
    assert _submitted(app)[0].value == picked


def test_form_browse_cancel(tmp_path: Path) -> None:
    """Cancelling the picker leaves the field at its default."""
    target = tmp_path / 'out.csv'
    field = AskPathField('File', None, PathAskOptions(default=target))
    app = _FormApp('H', [field], [], None)

    async def scenario() -> None:
        async with app.run_test() as pilot:
            await open_picker(pilot, str(tmp_path))
            await pilot.press('escape')
            await pilot.pause()
            await pilot.click('#submit')
    asyncio.run(scenario())
    assert _submitted(app)[0].value == target


def test_form_browse_disabled() -> None:
    """Disabling a path row also disables its Browse button."""
    field = AskPathField('File', None, PathAskOptions())
    app = _FormApp('H', [field], [], None)

    async def scenario() -> bool:
        async with app.run_test():
            app._apply_disabled((0,))
            return app.query_one('#browse_0', Button).disabled
    assert asyncio.run(scenario()) is True


def test_form_no_fields() -> None:
    """A form with no fields mounts and submits an empty answer list."""
    driven = drive(_FormApp('H', [], [], None), ['#submit'])
    assert driven.return_value == []


def test_change_not_ready() -> None:
    """A field change before the form is ready is ignored."""
    app = _FormApp('H', [AskTextField('Name', None)], [], None)
    app._changed('field_0')
    assert app._last_changed == 0


def test_form_browse_bad_id() -> None:
    """A browse press whose id is not a browse id opens no picker."""
    field = AskPathField('File', None, PathAskOptions())
    app = _FormApp('H', [field], [], None)

    async def scenario() -> int:
        async with app.run_test():
            app._browse_clicked(Button.Pressed(Button('x', id='submit')))
            return len(app.screen_stack)
    assert asyncio.run(scenario()) == 1


def test_int_empty_default() -> None:
    """An integer field cleared to blank falls back to its default."""
    fields: list[AskField] = [AskIntField('N', None, default=5)]
    app = _FormApp('H', fields, [], None)

    async def scenario() -> None:
        async with app.run_test() as pilot:
            app.query_one('#field_0', Input).value = ''
            await pilot.pause()
            await pilot.click('#submit')
    asyncio.run(scenario())
    assert _submitted(app)[0].value == 5


def test_int_required_empty() -> None:
    """A required integer field left empty refuses to submit."""
    fields: list[AskField] = [AskIntField('N', None)]
    driven = drive(_FormApp('H', fields, [], None), ['#submit'])
    assert driven.return_value is None


def test_form_int_not_number() -> None:
    """A non-numeric integer field refuses to submit."""
    fields: list[AskField] = [AskIntField('N', None)]
    app = _FormApp('H', fields, [], None)

    async def scenario() -> None:
        async with app.run_test() as pilot:
            app.query_one('#field_0', Input).value = 'abc'
            await pilot.pause()
            await pilot.click('#submit')
    asyncio.run(scenario())
    assert app.return_value is None
