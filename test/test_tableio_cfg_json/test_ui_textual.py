#! /usr/bin/env python3
"""Tests for the Textual user interface bridge."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

# pylint: disable=protected-access

import asyncio
import os
from pathlib import Path
from typing import Any, Optional, Sequence

import pytest
from textual.widgets import Button, Input, SelectionList, Static

from tableio_cfg_json import AskField, AskChoiceField, AskIntField, \
    AskMultiChoiceField, AskPathField, AskTextField, AskYesNoField, \
    AnswerTextField, PartialFormValidator, PathAskOptions, TableCell, \
    TableColumn, WizardAbort, WizardBack, WizardCancelLevel, \
    WizardNavigation, WizardPathKind, WizardUiBridgeTextual
from tableio_cfg_json.wizard_ui_bridge_form_defs import AnswerField
from tableio_cfg_json.wizard_ui_bridge_textual import _ChoiceApp, _FormApp, \
    _MultiApp, _NavApp, _PathApp, _TableApp, _TextApp, _browse_index, \
    _default_index, _field_index, _parse_cell_id, _preselected
from tableio_cfg_json._wizard_ui_bridge_path import _PickerScreen, \
    _selection_text
from tableio_cfg_json.wizard_ui_bridge_table import _new_row_template


def drive(app: _NavApp[Any], steps: Sequence[str]) -> _NavApp[Any]:
    """Run a screen headlessly, performing each step, and return it.

    A step starting with '#' is a click on that widget id; any other
    step is a single key press.
    """
    async def scenario() -> None:
        async with app.run_test() as pilot:
            for step in steps:
                if step.startswith('#'):
                    await pilot.click(step)
                else:
                    await pilot.press(step)
    asyncio.run(scenario())
    return app


class _CannedBridge(WizardUiBridgeTextual):
    """Textual bridge whose screens return scripted outcomes.

    Each scripted outcome is one of: a WizardNavigation subclass, which
    is recorded as the screen's navigation request; None, which acts as
    a screen closed with no value; or any other value, returned as the
    screen's result. The launched apps are kept so tests can inspect the
    messages they were given.
    """

    def __init__(self, outcomes: list[object]) -> None:
        """Store the scripted outcomes and an empty launch log."""
        super().__init__()
        self._outcomes = outcomes
        self.launched: list[_NavApp[Any]] = []

    def _launch(self, app: _NavApp[Any]) -> Any:
        """Record the app and return the next scripted outcome."""
        self.launched.append(app)
        outcome = self._outcomes.pop(0)
        if isinstance(outcome, type) and issubclass(outcome, WizardNavigation):
            app.nav = outcome
            return None
        return outcome


def test_text_returns_typed() -> None:
    """The text screen returns the characters the user typed."""
    app = drive(_TextApp('q', []), ['h', 'i', 'enter'])
    assert app.return_value == 'hi'


def test_text_empty() -> None:
    """The text screen returns an empty string for no input."""
    app = drive(_TextApp('q', []), ['enter'])
    assert app.return_value == ''


def test_text_prefilled() -> None:
    """The text screen starts with the given value."""
    app = drive(_TextApp('q', [], 'ready'), ['enter'])
    assert app.return_value == 'ready'


def test_text_back_nav() -> None:
    """ctrl+b records a back request and exits with no value."""
    app = drive(_TextApp('q', []), ['ctrl+b'])
    assert app.return_value is None
    assert app.nav is WizardBack


def test_text_cancel_nav() -> None:
    """ctrl+o records a cancel-level request and exits."""
    app = drive(_TextApp('q', []), ['ctrl+o'])
    assert app.return_value is None
    assert app.nav is WizardCancelLevel


def test_text_abort_quit() -> None:
    """The built-in ctrl+q quit exits with no value and no request."""
    app = drive(_TextApp('q', []), ['ctrl+q'])
    assert app.return_value is None
    assert app.nav is None


def test_path_submit(tmp_path: Path) -> None:
    """The path screen submits the editable path input."""
    path = tmp_path / 'config.json'
    app = _PathApp('q', [], PathAskOptions(), str(path))
    driven = drive(app, ['ctrl+s'])
    assert driven.return_value == str(path)


def test_path_default(tmp_path: Path) -> None:
    """The path screen starts from the default path."""
    path = tmp_path / 'config.json'
    options = PathAskOptions(default=path)
    app = _PathApp('q', [], options, None)
    assert app._start == tmp_path
    assert app._value == str(path)


@pytest.mark.parametrize('kind', [
    WizardPathKind.EXISTING_FILE,
    WizardPathKind.NON_EXISTING_FILE,
    WizardPathKind.FILE,
    WizardPathKind.NON_EXISTING_DIR,
    WizardPathKind.EXISTING_DIR,
    WizardPathKind.DIR])
def test_path_select_dir(tmp_path: Path, kind: WizardPathKind) -> None:
    """Directory selection becomes a value or child-name prefix."""
    path = tmp_path / 'selected'
    text = _selection_text(path, is_dir=True, kind=kind)
    if kind in (WizardPathKind.EXISTING_DIR, WizardPathKind.DIR):
        assert text == str(path)
    else:
        assert text == str(path) + os.sep


def test_path_select_file(tmp_path: Path) -> None:
    """File selection becomes the exact selected path."""
    path = tmp_path / 'chosen.json'
    assert _selection_text(path, is_dir=False,
                           kind=WizardPathKind.FILE) == str(path)


def test_choice_index() -> None:
    """The choice screen returns the index of the picked option."""
    app = drive(_ChoiceApp('q', ['a', 'b', 'c'], None, []), ['enter'])
    assert app.return_value == 0


def test_choice_default() -> None:
    """The choice screen highlights and returns the default option."""
    app = drive(_ChoiceApp('q', ['a', 'b', 'c'], 2, []), ['enter'])
    assert app.return_value == 2


def test_multi_indexes() -> None:
    """The multi screen returns the chosen indexes."""
    app = _MultiApp('q', ['a', 'b', 'c'], [0], 0, None, [])
    driven = drive(app, ['down', 'down', 'space', 'ctrl+s'])
    result = driven.return_value
    assert result is not None
    assert sorted(result) == [0, 2]


def test_multi_min() -> None:
    """The multi screen refuses to submit below the minimum count."""
    app = _MultiApp('q', ['a', 'b'], [], 1, None, [])
    driven = drive(app, ['ctrl+s', 'space', 'ctrl+s'])
    assert driven.return_value == [0]


def test_multi_button() -> None:
    """Clicking submit closes the multi screen with the selection."""
    app = _MultiApp('q', ['a', 'b'], [0], 0, None, [])
    driven = drive(app, ['#submit'])
    assert driven.return_value == [0]


def test_ask_text() -> None:
    """ask_text() returns the typed string."""
    bridge = _CannedBridge(['typed'])
    assert bridge.ask_text('q') == 'typed'


def test_ask_text_default() -> None:
    """ask_text() pre-fills and returns default for an empty answer."""
    bridge = _CannedBridge([''])
    assert bridge.ask_text('q', default='ready') == 'ready'
    app = bridge.launched[0]
    assert isinstance(app, _TextApp)
    assert app._value == 'ready'


def test_ask_text_nullable() -> None:
    """An empty nullable text answer with no default returns None."""
    bridge = _CannedBridge([''])
    assert bridge.ask_text('q', nullable=True) is None


def test_ask_text_sensitive() -> None:
    """Sensitive text uses password input mode."""
    bridge = _CannedBridge(['secret'])
    assert bridge.ask_text('q', sensitive=True) == 'secret'
    app = bridge.launched[0]
    assert isinstance(app, _TextApp)
    assert app._password is True


def test_text_secret_default() -> None:
    """Sensitive text questions reject defaults."""
    bridge = _CannedBridge(['secret'])
    with pytest.raises(ValueError, match='default'):
        bridge.ask_text('q', default='secret', sensitive=True)


def test_ask_path_value(tmp_path: Path) -> None:
    """ask_path() returns the validated path from the path screen."""
    path = tmp_path / 'config.json'
    path.write_text('{}', encoding='utf-8')
    options = PathAskOptions(kind=WizardPathKind.EXISTING_FILE)
    assert _CannedBridge([str(path)]).ask_path('q', options=options) == path


def test_ask_path_nullable() -> None:
    """ask_path() maps an empty nullable answer to None."""
    options = PathAskOptions(nullable=True)
    assert _CannedBridge(['']).ask_path('q', options=options) is None


def test_ask_path_retry(tmp_path: Path) -> None:
    """ask_path() re-asks with the invalid text still editable."""
    path = tmp_path / 'config.json'
    path.write_text('{}', encoding='utf-8')
    options = PathAskOptions(kind=WizardPathKind.EXISTING_FILE)
    bridge = _CannedBridge([str(tmp_path / 'missing.json'), str(path)])
    assert bridge.ask_path('q', options=options) == path
    first = bridge.launched[0]
    second = bridge.launched[1]
    assert isinstance(first, _PathApp) and isinstance(second, _PathApp)
    assert second._messages == ['Path does not exist.']
    assert second._value.endswith('missing.json')


def test_ask_path_default(tmp_path: Path) -> None:
    """ask_path() starts from and returns a default path."""
    path = tmp_path / 'config.json'
    path.write_text('{}', encoding='utf-8')
    options = PathAskOptions(kind=WizardPathKind.EXISTING_FILE, default=path)
    bridge = _CannedBridge([''])
    assert bridge.ask_path('q', options=options) == path
    app = bridge.launched[0]
    assert isinstance(app, _PathApp)
    assert app._value == str(path)


def test_dep_ask_dispatch() -> None:
    """The deprecated ask() dispatches to the typed Textual methods."""
    with pytest.warns(DeprecationWarning, match='deprecated'):
        assert _CannedBridge(['typed']).ask('q') == 'typed'
    with pytest.warns(DeprecationWarning, match='deprecated'):
        assert _CannedBridge([1]).ask('q', choices=['a', 'b', 'c']) == 'b'


def test_ask_choice_value() -> None:
    """ask_choice() maps the chosen index back to the choice."""
    bridge = _CannedBridge([2])
    assert bridge.ask_choice('q', choices=['a', 'b', 'c']) == 'c'


@pytest.mark.parametrize('index,expected', [(0, True), (1, False)])
def test_yes_no_map(index: int, expected: bool) -> None:
    """ask_yes_no() maps the yes index to True and the no index to False."""
    bridge = _CannedBridge([index])
    assert bridge.ask_yes_no('q', default=True) is expected


@pytest.mark.parametrize('default,index', [(True, 0), (False, 1)])
def test_yes_no_default_idx(default: bool, index: int) -> None:
    """ask_yes_no() highlights yes for a True default and no for False."""
    bridge = _CannedBridge([0])
    bridge.ask_yes_no('q', default=default)
    app = bridge.launched[0]
    assert isinstance(app, _ChoiceApp)
    assert app._default_index == index


def test_multi_map() -> None:
    """ask_multi() returns the chosen values in choices order."""
    bridge = _CannedBridge([[2, 0]])
    assert bridge.ask_multi('q', choices=['a', 'b', 'c']) == ['a', 'c']


def test_choice_default_idx() -> None:
    """ask_choice() highlights the default and None without a default."""
    with_default = _CannedBridge([0])
    with_default.ask_choice('q', choices=['a', 'b', 'c'], default='b')
    chosen = with_default.launched[0]
    assert isinstance(chosen, _ChoiceApp)
    assert chosen._default_index == 1
    without = _CannedBridge([0])
    without.ask_choice('q', choices=['a', 'b'])
    plain = without.launched[0]
    assert isinstance(plain, _ChoiceApp)
    assert plain._default_index is None


@pytest.mark.parametrize('nav', [WizardBack, WizardCancelLevel, WizardAbort])
def test_nav_reraised(nav: type[WizardNavigation]) -> None:
    """A recorded navigation request is re-raised by the bridge."""
    bridge = _CannedBridge([nav])
    with pytest.raises(nav):
        bridge.ask_text('q')


def test_quit_abort() -> None:
    """A screen that closes with no value is treated as an abort."""
    bridge = _CannedBridge([None])
    with pytest.raises(WizardAbort):
        bridge.ask_text('q')


def test_show_buffered() -> None:
    """A shown message appears on the next screen's header."""
    bridge = _CannedBridge(['x'])
    bridge.show('hello')
    bridge.ask_text('q')
    app = bridge.launched[0]
    assert isinstance(app, _TextApp)
    assert 'hello' in app._messages


def test_error_drained() -> None:
    """Diagnostics written to error_file() appear on the next screen."""
    bridge = _CannedBridge(['x'])
    bridge.error_file().write('diag line\n')
    bridge.ask_text('q')
    app = bridge.launched[0]
    assert isinstance(app, _TextApp)
    assert 'diag line' in app._messages


def test_reask_reason() -> None:
    """A re-ask reason is shown together with the question."""
    bridge = _CannedBridge(['x'])
    bridge.ask_text('q', 'bad value')
    app = bridge.launched[0]
    assert isinstance(app, _TextApp)
    assert 'bad value' in app._messages


def test_drained_once() -> None:
    """Buffered messages are shown once and not on later screens."""
    bridge = _CannedBridge(['x', 'y'])
    bridge.show('once')
    bridge.ask_text('q1')
    bridge.ask_text('q2')
    first = bridge.launched[0]
    second = bridge.launched[1]
    assert isinstance(first, _TextApp) and isinstance(second, _TextApp)
    assert 'once' in first._messages
    assert 'once' not in second._messages


def test_table_prefilled() -> None:
    """Submitting unchanged returns the pre-filled cells and headers."""
    columns = (TableColumn('Parameter', read_only=True),
               TableColumn('Value'))
    cells = [[TableCell(value='alpha'), TableCell(value='one')],
             [TableCell(value='beta'),
              TableCell(value='y', choices=('x', 'y'), nullable=True)]]
    driven = drive(_TableApp(columns, cells, 'q', [], None), ['ctrl+s'])
    assert driven.return_value == [['alpha', 'one'], ['beta', 'y']]


def test_table_clear_null() -> None:
    """A cleared nullable text cell is reported as None."""
    columns = (TableColumn('Value'),)
    cells = [[TableCell(value='one', nullable=True)]]
    driven = drive(_TableApp(columns, cells, 'q', [], None),
                   ['end', 'ctrl+u', 'ctrl+s'])
    assert driven.return_value == [[None]]


def test_table_empty_freetext() -> None:
    """A cleared non-nullable text cell is reported as an empty string."""
    columns = (TableColumn('Value'),)
    cells = [[TableCell(value='one')]]
    driven = drive(_TableApp(columns, cells, 'q', [], None),
                   ['end', 'ctrl+u', 'ctrl+s'])
    assert driven.return_value == [['']]


def test_table_select_blank() -> None:
    """A nullable drop-down left blank is reported as None."""
    columns = (TableColumn('Value'),)
    cells = [[TableCell(choices=('x', 'y'), nullable=True)]]
    driven = drive(_TableApp(columns, cells, 'q', [], None), ['ctrl+s'])
    assert driven.return_value == [[None]]


def test_table_select_pick() -> None:
    """Choosing a drop-down option returns that choice."""
    columns = (TableColumn('Value'),)
    cells = [[TableCell(choices=('x', 'y'), nullable=True)]]
    driven = drive(_TableApp(columns, cells, 'q', [], None),
                   ['enter', 'down', 'enter', 'ctrl+s'])
    assert driven.return_value == [['x']]


def test_table_nav_back() -> None:
    """ctrl+b in the table records a back request and exits."""
    columns = (TableColumn('Value'),)
    cells = [[TableCell(value='one')]]
    driven = drive(_TableApp(columns, cells, 'q', [], None), ['ctrl+b'])
    assert driven.return_value is None
    assert driven.nav is WizardBack


def test_table_partial_check() -> None:
    """The partial check sees each cell change with the changed position."""
    columns = (TableColumn('Value'),)
    cells = [[TableCell(nullable=True)]]
    calls: list[tuple[list[list[Optional[str]]], tuple[int, int]]] = []

    def check(table: list[list[Optional[str]]],
              position: tuple[int, int]) -> tuple[bool, str]:
        calls.append(([row[:] for row in table], position))
        value = table[position[0]][position[1]]
        return (value != 'bad', '' if value != 'bad' else 'no good')
    app = _TableApp(columns, cells, 'q', [], check)
    driven = drive(app, ['b', 'a', 'd', 'end', 'ctrl+u', 'o', 'k', 'ctrl+s'])
    assert driven.return_value == [['ok']]
    assert ([['bad']], (0, 0)) in calls
    assert ([['ok']], (0, 0)) in calls


def test_ask_table_canned() -> None:
    """ask_table() returns the table the screen produced."""
    columns = (TableColumn('Value'),)
    cells = [[TableCell(value='one')]]
    bridge = _CannedBridge([[['one']]])
    assert bridge.ask_table(columns, cells, 'q') == [['one']]


def test_ask_table_nav() -> None:
    """ask_table() re-raises a navigation request from the screen."""
    columns = (TableColumn('Value'),)
    cells = [[TableCell(value='one')]]
    bridge = _CannedBridge([WizardCancelLevel])
    with pytest.raises(WizardCancelLevel):
        bridge.ask_table(columns, cells, 'q')


def test_new_row_uniform() -> None:
    """A new row keeps the members shared across each template column."""
    columns = (TableColumn('P', read_only=True), TableColumn('V'))
    cells = [[TableCell(value='p', choices=('a', 'b'), nullable=True),
              TableCell(value='x', choices=('a', 'b'), nullable=True)],
             [TableCell(value='p', choices=('a', 'b'), nullable=True),
              TableCell(value='y', choices=('a', 'b'), nullable=True)]]
    new_row = _new_row_template(columns, cells)
    assert new_row[0].value == 'p'
    assert new_row[0].choices == ('a', 'b')
    assert new_row[0].nullable is True
    assert new_row[1].value == ''
    assert new_row[1].choices == ('a', 'b')


def test_new_row_defaults() -> None:
    """Differing template members fall back to '', None and False."""
    columns = (TableColumn('V'),)
    cells = [[TableCell(value='x', choices=('a',), nullable=True)],
             [TableCell(value='y', choices=('a', 'b'), nullable=False)]]
    new_row = _new_row_template(columns, cells)
    assert new_row[0].value == ''
    assert new_row[0].choices is None
    assert new_row[0].nullable is False


def test_new_row_none() -> None:
    """A uniformly None value stays None in added rows."""
    columns = (TableColumn('V'),)
    cells = [[TableCell(value=None, nullable=True)],
             [TableCell(value=None, nullable=True)]]
    new_row = _new_row_template(columns, cells)
    assert new_row[0].value is None
    assert new_row[0].nullable is True


def test_table_add_row() -> None:
    """Adding a row, filling it, and submitting returns the new row."""
    columns = (TableColumn('V'),)
    cells = [[TableCell(value='a')], [TableCell(value='b')]]
    app = _TableApp(columns, cells, 'q', [], None, 2, 4)

    async def scenario() -> None:
        async with app.run_test() as pilot:
            await pilot.click('#add_row')
            await pilot.pause()
            app.query_one('#cell_2_0').focus()
            await pilot.press('c')
            await pilot.click('#submit')
    asyncio.run(scenario())
    assert app.return_value == [['a'], ['b'], ['c']]


def test_add_row_readonly() -> None:
    """A read-only column becomes editable in an added row."""
    columns = (TableColumn('P', read_only=True), TableColumn('V'))
    cells = [[TableCell(value='p1'), TableCell(value='x')],
             [TableCell(value='p2'), TableCell(value='y')]]
    app = _TableApp(columns, cells, 'q', [], None, 2, 4)

    async def scenario() -> None:
        async with app.run_test() as pilot:
            await pilot.click('#add_row')
            await pilot.pause()
            app.query_one('#cell_2_0').focus()
            await pilot.press('z')
            await pilot.click('#submit')
    asyncio.run(scenario())
    assert app.return_value == [['p1', 'x'], ['p2', 'y'], ['z', '']]


def test_table_remove_row() -> None:
    """Removing the last row drops it from the result."""
    columns = (TableColumn('V'),)
    cells = [[TableCell(value='a')], [TableCell(value='b')]]
    app = _TableApp(columns, cells, 'q', [], None, 1, 3)

    async def scenario() -> None:
        async with app.run_test() as pilot:
            await pilot.click('#remove_row')
            await pilot.pause()
            await pilot.click('#submit')
    asyncio.run(scenario())
    assert app.return_value == [['a']]


def test_table_row_bounds() -> None:
    """The table will not shrink below min_rows or grow past max_rows."""
    columns = (TableColumn('V'),)
    cells = [[TableCell(value='a')]]
    app = _TableApp(columns, cells, 'q', [], None, 1, 2)

    async def scenario() -> None:
        async with app.run_test() as pilot:
            await pilot.click('#remove_row')
            await pilot.pause()
            await pilot.click('#add_row')
            await pilot.pause()
            await pilot.click('#add_row')
            await pilot.pause()
            await pilot.click('#submit')
    asyncio.run(scenario())
    result = app.return_value
    assert result is not None
    assert len(result) == 2


def test_fixed_no_buttons() -> None:
    """A fixed table has no Add row or Remove row button."""
    columns = (TableColumn('V'),)
    cells = [[TableCell(value='a')]]
    app = _TableApp(columns, cells, 'q', [], None)

    async def scenario() -> tuple[int, int]:
        async with app.run_test():
            return (len(app.query('#add_row')), len(app.query('#remove_row')))
    assert asyncio.run(scenario()) == (0, 0)


def test_ask_table_variable() -> None:
    """ask_table passes the row bounds through to the table screen."""
    columns = (TableColumn('V'),)
    cells = [[TableCell(value='a')]]
    bridge = _CannedBridge([[['a']]])
    bridge.ask_table(columns, cells, 'q', min_rows=1, max_rows=3)
    app = bridge.launched[0]
    assert isinstance(app, _TableApp)
    assert app._variable is True
    assert (app._min_rows, app._max_rows) == (1, 3)


def test_header_messages() -> None:
    """Buffered messages are rendered above the question."""
    app = drive(_TextApp('q', ['note one', 'note two']), ['enter'])
    assert app.return_value == ''


def test_preselected_default() -> None:
    """Default values map to indexes, and no default maps to empty."""
    assert _preselected(('a', 'b', 'c'), ('a', 'c')) == [0, 2]
    assert _preselected(('a', 'b'), None) == []


def test_default_idx_missing() -> None:
    """A default outside the choices highlights no option."""
    assert _default_index(('a', 'b'), 'zzz') is None
    assert _default_index(('a', 'b'), None) is None


def test_parse_cell_id() -> None:
    """A cell id parses to its position; other ids parse to None."""
    assert _parse_cell_id('cell_2_3') == (2, 3)
    assert _parse_cell_id(None) is None
    assert _parse_cell_id('submit') is None


def test_make_select_nonnull() -> None:
    """A non-nullable empty drop-down defaults to its first choice."""
    columns = (TableColumn('Value'),)
    cells = [[TableCell(choices=('x', 'y'))]]
    driven = drive(_TableApp(columns, cells, 'q', [], None), ['ctrl+s'])
    assert driven.return_value == [['x']]


def test_focus_empty_rows() -> None:
    """A table with no rows mounts and submits an empty result."""
    columns = (TableColumn('Value'),)
    driven = drive(_TableApp(columns, [], 'q', [], None, 0, 2), ['ctrl+s'])
    assert driven.return_value == []


def test_focus_all_readonly() -> None:
    """A first row of only read-only cells leaves nothing focused."""
    columns = (TableColumn('P', read_only=True),)
    cells = [[TableCell(value='x')]]
    driven = drive(_TableApp(columns, cells, 'q', [], None), ['ctrl+s'])
    assert driven.return_value == [['x']]


def test_recheck_none() -> None:
    """A cell change with no parsed position is ignored."""
    columns = (TableColumn('Value'),)
    app = _TableApp(columns, [[TableCell(value='a')]], 'q', [], None)
    app._recheck(None)
    assert app._table == [['a']]


def test_add_past_max() -> None:
    """Adding beyond max_rows is refused and the row count holds."""
    columns = (TableColumn('Value'),)
    cells = [[TableCell(value='a')]]
    app = _TableApp(columns, cells, 'q', [], None, 1, 2)

    async def scenario() -> int:
        async with app.run_test() as pilot:
            app._add_row()
            await pilot.pause()
            app._add_row()
            await pilot.pause()
            return len(app._rows)
    assert asyncio.run(scenario()) == 2


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


def _submitted(app: _NavApp[Any]) -> list[AnswerField]:
    """Return the answers a submitted form produced, asserting success."""
    result = app.return_value
    assert isinstance(result, list)
    return result


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


def test_path_enter_submits(tmp_path: Path) -> None:
    """Pressing Return in the path input submits its value."""
    path = tmp_path / 'config.json'
    app = _PathApp('q', [], PathAskOptions(), str(path))

    async def scenario() -> None:
        async with app.run_test() as pilot:
            app.query_one('#path_input', Input).focus()
            await pilot.press('enter')
    asyncio.run(scenario())
    assert app.return_value == str(path)


def test_path_fill_input(tmp_path: Path) -> None:
    """A tree selection fills the editable path input."""
    sub = tmp_path / 'sub'
    sub.mkdir()
    app = _PathApp('q', [], PathAskOptions(kind=WizardPathKind.DIR), None)

    async def scenario() -> str:
        async with app.run_test():
            app._fill_input(sub, is_dir=True)
            return app.query_one('#path_input', Input).value
    assert asyncio.run(scenario()) == str(sub)


def test_picker_seed(tmp_path: Path) -> None:
    """The picker roots at the typed folder, else at the default."""
    options = PathAskOptions(default=tmp_path / 'out.csv')
    empty = _PickerScreen(options, '')
    assert empty._start == tmp_path
    assert empty._value == ''
    typed = _PickerScreen(options, str(tmp_path))
    assert typed._start == tmp_path
    assert typed._value == str(tmp_path)


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
            await pilot.click('#browse_0')
            await pilot.pause()
            screen = app.screen
            assert isinstance(screen, _PickerScreen)
            screen.query_one('#path_input', Input).value = str(picked)
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
            await pilot.click('#browse_0')
            await pilot.pause()
            screen = app.screen
            assert isinstance(screen, _PickerScreen)
            screen.query_one('#path_input', Input).value = str(tmp_path)
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
