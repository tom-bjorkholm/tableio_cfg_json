#! /usr/bin/env python3
"""Tests for the wizard UI bridge names that moved to wizard_ui_bridge.

The old names must keep working, so that applications built on the old
location keep running, while every use of them tells the maintainer of
that application to change the import.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import ast
import importlib
import warnings
from pathlib import Path

import pytest

import wizard_ui_bridge
import tableio_cfg_json
from tableio_cfg_json._moved import MOVED_NAMES, STRICT_ENV, \
    WizardUiBridgeMoved

SHIMS = {
    'wizard_ui_bridge': ('wizard_ui_bridge.bridge', 'WizardUiBridge'),
    'wizard_ui_bridge_arg_types': ('wizard_ui_bridge.arg_types',
                                   'WizardBack'),
    'wizard_ui_bridge_console': ('wizard_ui_bridge.console',
                                 'WizardUiBridgeConsole'),
    'wizard_ui_bridge_form_defs': ('wizard_ui_bridge.form_defs', 'AskField'),
    'wizard_ui_bridge_table': ('wizard_ui_bridge._table',
                               '_run_variable_table'),
    'wizard_ui_bridge_textual': ('wizard_ui_bridge.textual_bridge',
                                 'WizardUiBridgeTextual'),
    'wizard_ui_factory': ('wizard_ui_bridge.factory', 'make_text_ui_bridge'),
}


def _package_folder() -> Path:
    """Return the folder the installed tableio_cfg_json package is in."""
    assert tableio_cfg_json.__file__ is not None
    return Path(tableio_cfg_json.__file__).parent


def _stub_names(stub_file: Path) -> set[str]:
    """Return the names a type stub re-exports."""
    tree = ast.parse(stub_file.read_text(encoding='utf-8'))
    return {alias.asname or alias.name for node in tree.body
            if isinstance(node, ast.ImportFrom) for alias in node.names}


@pytest.mark.parametrize('name', sorted(MOVED_NAMES))
def test_moved_name(name: str) -> None:
    """Every moved name warns and is the object the new package has."""
    with pytest.warns(WizardUiBridgeMoved, match=name):
        moved = getattr(tableio_cfg_json, name)
    assert moved is getattr(wizard_ui_bridge, name)


@pytest.mark.parametrize('name', sorted(MOVED_NAMES))
def test_moved_message(name: str) -> None:
    """The warning names the import that replaces the old one."""
    with pytest.warns(WizardUiBridgeMoved) as records:
        getattr(tableio_cfg_json, name)
    assert f'from wizard_ui_bridge import {name}' in str(records[0].message)


@pytest.mark.parametrize('old,new,name', [
    (old, new, name) for old, (new, name) in SHIMS.items()])
def test_moved_module(old: str, new: str, name: str) -> None:
    """Every deprecated module warns and hands out the moved object."""
    shim = importlib.import_module(f'tableio_cfg_json.{old}')
    with pytest.warns(WizardUiBridgeMoved, match=name):
        moved = getattr(shim, name)
    assert moved is getattr(importlib.import_module(new), name)


def test_strict_package(monkeypatch: pytest.MonkeyPatch) -> None:
    """Strict mode turns a moved package name into an ImportError."""
    monkeypatch.setenv(STRICT_ENV, '1')
    with pytest.raises(ImportError, match='WizardUiBridge'):
        getattr(tableio_cfg_json, 'WizardUiBridge')


def test_strict_module(monkeypatch: pytest.MonkeyPatch) -> None:
    """Strict mode turns a deprecated module name into an ImportError."""
    monkeypatch.setenv(STRICT_ENV, '1')
    shim = importlib.import_module('tableio_cfg_json.wizard_ui_bridge_console')
    with pytest.raises(ImportError, match='WizardUiBridgeConsole'):
        getattr(shim, 'WizardUiBridgeConsole')


def test_unknown_name() -> None:
    """An unknown name is an AttributeError, not a moved name."""
    with pytest.raises(AttributeError):
        getattr(tableio_cfg_json, 'NoSuchName')


def test_shim_dunder() -> None:
    """A dunder lookup on a deprecated module does not warn."""
    shim = importlib.import_module('tableio_cfg_json.wizard_ui_bridge')
    with warnings.catch_warnings():
        warnings.simplefilter('error')
        with pytest.raises(AttributeError):
            getattr(shim, '__deprecated__')


def test_own_names_silent(recwarn: pytest.WarningsRecorder) -> None:
    """The names this package still owns are not deprecated."""
    assert tableio_cfg_json.TioJsonConfig is not None
    assert tableio_cfg_json.tio_json_config_wizard is not None
    assert not [record for record in recwarn
                if issubclass(record.category, WizardUiBridgeMoved)]


@pytest.mark.parametrize('old,new', [(old, new) for old, (new, _) in
                                     SHIMS.items()])
def test_stub_matches(old: str, new: str) -> None:
    """Every name a deprecated module's stub promises really exists."""
    module = importlib.import_module(new)
    for name in _stub_names(_package_folder() / f'{old}.pyi'):
        assert hasattr(module, name)


def test_all_is_complete() -> None:
    """The public name list is the own names plus the moved ones."""
    names = set(tableio_cfg_json.__all__)
    assert MOVED_NAMES < names
    assert 'TioJsonConfig' in names - MOVED_NAMES
