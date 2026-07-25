#! /usr/bin/env python3
"""Tests that the bridge keeps its dependency footprint small.

The point of this package being separate from tableio_cfg_json is that
a wizard that does not use TableIO shall not pull in TableIO and its
dependencies, and that a wizard that only uses the console bridge shall
not pull in Textual. Both are checked in a fresh interpreter, because
the test session itself imports both.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import subprocess
import sys

_REPORT = ("import sys\n"
           "print(' '.join(sorted({name.split('.')[0] "
           "for name in sys.modules})))")


def _imported(statement: str) -> set[str]:
    """Return the top-level modules a fresh interpreter ends up with."""
    result = subprocess.run([sys.executable, '-c', f'{statement}\n{_REPORT}'],
                            check=True, capture_output=True, text=True)
    return set(result.stdout.split())


def test_no_tableio_import() -> None:
    """Importing the package does not import TableIO."""
    assert 'tableio' not in _imported('import wizard_ui_bridge')


def test_no_textual_import() -> None:
    """Importing the package does not import the optional Textual."""
    assert 'textual' not in _imported('import wizard_ui_bridge')


def test_console_no_textual() -> None:
    """Building and using a console bridge does not import Textual."""
    statement = ('import sys\n'
                 'from wizard_ui_bridge import WizardUiBridgeConsole\n'
                 'WizardUiBridgeConsole(sys.stdout, sys.stdin, sys.stderr)')
    assert 'textual' not in _imported(statement)


def test_textual_imported() -> None:
    """Asking for the Textual bridge does import Textual."""
    statement = 'from wizard_ui_bridge import WizardUiBridgeTextual'
    assert 'textual' in _imported(statement)
