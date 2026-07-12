#! /usr/bin/env python3
"""Tests for the single-screen Textual widgets and ask dispatch.

This covers the free-text, path, choice and multi-choice screens, the
directory picker screen and the bridge methods that map their outcomes
back to the wizard.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

# pylint: disable=protected-access

import asyncio
import os
from pathlib import Path

import pytest
from textual.widgets import Button, DirectoryTree, Input

from tableio_cfg_json import AskPathField, PathAskOptions, WizardAbort, \
    WizardBack, WizardCancelLevel, WizardNavigation, WizardPathKind
from tableio_cfg_json.wizard_ui_bridge_textual import _ChoiceApp, _FormApp, \
    _MultiApp, _PathApp, _TextApp, _default_index, _preselected
from tableio_cfg_json._wizard_ui_bridge_path import _PickerScreen, \
    _PathPick, _selection_text, _start_dir
from .ui_textual_support import drive, open_picker, _CannedBridge, _submitted


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


def test_path_submit_button(tmp_path: Path) -> None:
    """Clicking the path screen's Submit button confirms the input."""
    path = tmp_path / 'config.json'
    app = _PathApp('q', [], PathAskOptions(), str(path))
    driven = drive(app, ['#submit'])
    assert driven.return_value == str(path)


def test_path_tree_selects(tmp_path: Path) -> None:
    """Tree file and directory selections fill the editable input."""
    chosen = tmp_path / 'chosen.csv'
    chosen.write_text('x')
    app = _PathApp('q', [], PathAskOptions(kind=WizardPathKind.FILE),
                   str(tmp_path))

    async def scenario() -> tuple[str, str]:
        async with app.run_test() as pilot:
            tree = app.query_one(DirectoryTree)
            await pilot.pause()
            app._file_selected(DirectoryTree.FileSelected(tree.root, chosen))
            file_val = app.query_one('#path_input', Input).value
            app._dir_selected(
                DirectoryTree.DirectorySelected(tree.root, tmp_path))
            dir_val = app.query_one('#path_input', Input).value
            return (file_val, dir_val)
    file_val, dir_val = asyncio.run(scenario())
    assert file_val == str(chosen)
    assert dir_val == str(tmp_path) + os.sep


@pytest.mark.parametrize('button_id, keeps_default', [
    ('submit', False), ('cancel', True)])
def test_picker_buttons(tmp_path: Path, button_id: str,
                        keeps_default: bool) -> None:
    """The picker Submit returns the pick; Cancel keeps the default."""
    target = tmp_path / 'out.csv'
    picked = tmp_path / 'picked.csv'
    field = AskPathField('File', None, PathAskOptions(default=target))
    app = _FormApp('H', [field], [], None)

    async def scenario() -> None:
        async with app.run_test() as pilot:
            screen = await open_picker(pilot, str(picked))
            await pilot.click(screen.query_one(f'#{button_id}', Button))
            await pilot.pause()
            await pilot.click('#submit')
    asyncio.run(scenario())
    assert _submitted(app)[0].value == (target if keeps_default else picked)


def test_pathpick_confirm() -> None:
    """The shared _PathPick base leaves _confirm to the host screen."""
    with pytest.raises(NotImplementedError):
        _PathPick()._confirm('value')


def test_start_dir_unusable(monkeypatch: pytest.MonkeyPatch) -> None:
    """A default whose existence check fails roots the tree at cwd."""
    def boom(self: Path) -> bool:
        """Fail every existence check with an OSError."""
        _ = self
        raise OSError('unusable')
    monkeypatch.setattr(Path, 'exists', boom)
    assert _start_dir(Path('/whatever/here')) == Path.cwd()


def test_start_dir_no_parent(tmp_path: Path) -> None:
    """A default under a missing parent roots the tree at cwd."""
    assert _start_dir(tmp_path / 'missing' / 'child') == Path.cwd()
