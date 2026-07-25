#! /usr/local/bin/python3
"""Support for names that moved to the wizard_ui_bridge package.

The wizard user interface bridge used to be part of tableio_cfg_json.
It is now the separate package wizard_ui_bridge, which does not depend
on TableIO. The old names still work here, so applications keep
running, but each use warns so that maintainers know to change the
import.

The warning is a DeprecationWarning subclass, which Python hides from
end users by default while pytest and unittest show it by default. A
maintainer who wants the stale imports to fail instead of warn can set
the environment variable named by STRICT_ENV to any non-empty value.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import warnings
from importlib import import_module
from os import environ
import wizard_ui_bridge

STRICT_ENV = 'WIZARD_UI_BRIDGE_STRICT'
"""Set this environment variable to make a moved name raise ImportError."""

REMOVED_IN = 'tableio-cfg-json 2.0'
"""The release that removes the deprecated re-exports named here."""

_NEVER_HERE = ('textual_installed', 'load_textual_bridge')

MOVED_NAMES = frozenset(name for name in wizard_ui_bridge.__all__
                        if name not in _NEVER_HERE)
"""The wizard UI bridge names this package used to define itself."""


class WizardUiBridgeMoved(DeprecationWarning):
    """Warns that a name moved to the wizard_ui_bridge package.

    Being its own category lets a maintainer turn just these warnings
    into errors, by running pytest with
    `-W error::tableio_cfg_json.WizardUiBridgeMoved`. The interpreter's
    own -W and PYTHONWARNINGS cannot name this category, because they
    are resolved before this package can be imported; STRICT_ENV works
    there instead.
    """


def moved_attr(old_module: str, new_module: str, name: str) -> object:
    """Return name from new_module, warning that it moved there.

    Dunder names are rejected without warning, so that attribute
    lookups made by the interpreter and by tools do not import the new
    module and do not warn.

    Args:
        old_module: Deprecated module the name was looked up in.
        new_module: Module the name lives in now.
        name: Name that was looked up.

    Raises:
        AttributeError: If name is a dunder name.
        ImportError: If strict mode is on, see STRICT_ENV.
    """
    if name.startswith('__'):
        raise AttributeError(
            f'module {old_module!r} has no attribute {name!r}')
    message = (f'{old_module}.{name} has moved to {new_module}.{name}. '
               f'Change the import to: from {new_module} import {name} . '
               f'The name is deprecated in {old_module} and is removed '
               f'in {REMOVED_IN}.')
    if environ.get(STRICT_ENV):
        raise ImportError(message)
    warnings.warn(message, WizardUiBridgeMoved, stacklevel=3)
    return getattr(import_module(new_module), name)
