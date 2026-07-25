#! /usr/local/bin/python3
"""Deprecated location of the wizard UI bridge form fields.

This module moved to wizard_ui_bridge.form_defs. Importing from here still
works and warns, see tableio_cfg_json._moved for how to make it fail
instead.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from tableio_cfg_json._moved import moved_attr

_NEW_MODULE = 'wizard_ui_bridge.form_defs'


def __getattr__(name: str) -> object:
    """Return name from its new module, warning that it moved."""
    return moved_attr(__name__, _NEW_MODULE, name)
