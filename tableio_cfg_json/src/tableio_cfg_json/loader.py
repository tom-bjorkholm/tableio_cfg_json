#! /usr/local/bin/python3
"""How a configuration editor constructs a TioJsonConfig.

An edit-cfg-json editor constructs the configuration class itself, from the
keyword arguments config-as-json documents. TioJsonConfig takes two more than
that: the runtime capabilities and the file access of the endpoint, which are
the application's and which nothing in a configuration file could supply. An
``edit_cfg_json.ConfigLoader`` is how an application says how its class is
built, and this module is that loader for TioJsonConfig.

The defaults TableIO recommends depend on the chosen format, so the format
and the implementation are read out of the JSON text before the defaults are
asked for. Without that, a file selecting CSV would be built on the defaults
of another format and refused for an implementation the user never wrote.

A ready-made loader is offered for each file access, for a program that needs
a name to point at rather than a call to make, which is what the ``--loader``
option of ``python3 -m edit_cfg_json.dump`` takes. There are three of them and
not one, because the file access is not in the configuration file and picking
the wrong one is not harmless: READ matches only the formats that can be read,
while CREATE matches every registered format, and the implementation that the
defaults fill in for one access is not the one the other access would choose.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import json
import sys
from typing import Optional, TextIO

from config_as_json import Config, PathOrStr
from edit_cfg_json import ConfigLoader
from tableio import Capabilities, FileAccess
from tableio_cfg_json.config import TioJsonConfig

NO_FILE_NAME = ('The editor reads the configuration file itself, so this '
                'loader is given JSON text and not a file name.')
"""Message of the refusal of a file name given to this loader."""


def _json_member(text: Optional[str], name: str,
                 fallback: Optional[str]) -> Optional[str]:
    """Return one top-level string member of JSON text, or a fallback.

    Only which defaults to build on is decided here, so anything that is not
    a JSON object holding that member as a string is left to the parse step,
    which reports what is wrong with it properly.

    Args:
        text: JSON text to look in, or None when there is none.
        name: Name of the top-level member to look for.
        fallback: Value to use when the text does not answer.
    Returns:
        The value of that member, or the fallback.
    """
    if text is None:
        return fallback
    try:
        data = json.loads(text)
    except ValueError:
        return fallback
    if not isinstance(data, dict):
        return fallback
    value = data.get(name)
    return value if isinstance(value, str) else fallback


def tio_json_loader(capabilities: Capabilities, file_access: FileAccess,
                    format_name: Optional[str] = None,
                    implementation: Optional[str] = None,
                    include_all_options: bool = True) -> ConfigLoader:
    """Get a loader that constructs a TioJsonConfig for a config editor.

    Pass the result as the ``loader`` argument of ``edit_cfg_json.edit()``,
    ``editor_model()`` or ``load_config()``. An application that edits its own
    configuration class needs no loader from here: it is the class holding the
    TioJsonConfig members that the editor is given, and constructing that one
    is the application's own to describe.

    ``include_all_options`` is what decides how much of a TableIO
    configuration an editing session can reach. A configuration file normally
    stores only the durable choices that have to be fixed, and an option that
    is not in the file is not a row in the editor, so the default here is to
    build on a complete set of defaults and let the editor mark every value
    the file did not hold. The cost is that saving then writes all of them,
    which turns a compact configuration file into a full one and fixes the
    implementation that TableIO would otherwise choose at runtime. Pass False
    to keep an edited file as compact as it was.

    Args:
        capabilities: Runtime capabilities requested by the application.
        file_access: Runtime file access requested by the application.
        format_name: Optional preferred TableIO format name, used only when
            the edited JSON text does not select one.
        implementation: Optional preferred TableIO implementation name, used
            only when the edited JSON text does not select one.
        include_all_options: Whether the editor should offer every option as
            a row rather than only the options the file holds.
    Returns:
        A loader for TioJsonConfig, satisfying ``edit_cfg_json.ConfigLoader``.
    """
    def load(*, from_json_data_text: Optional[str] = None,
             from_json_filename: Optional[PathOrStr] = None,
             ok_to_use_defaults: bool = False,
             stderr_file: TextIO = sys.stderr) -> Config:
        """Construct the configuration that the editor asked for.

        Args:
            from_json_data_text: JSON text to apply, or None for the values
                that TableIO recommends.
            from_json_filename: Refused, because the editor reads its own
                input files and never passes this.
            ok_to_use_defaults: Whether the recommended values may fill in
                the members that the JSON text does not hold.
            stderr_file: Stream receiving user-facing diagnostics.
        Raises:
            ValueError: A file name was given, or TableIO cannot recommend a
                configuration for the requested runtime values.
            KeyError: The JSON text has missing, unknown or misplaced keys.
            ConfigBadJson: The JSON text is not usable as configuration JSON.
            InvalidConfiguration: The resulting values fail validation.
        Returns:
            One TioJsonConfig holding the values of that JSON text.
        """
        if from_json_filename is not None:
            raise ValueError(NO_FILE_NAME)
        config = TioJsonConfig(
            capabilities=capabilities, file_access=file_access,
            format_name=_json_member(from_json_data_text, 'format_name',
                                     format_name),
            implementation=_json_member(from_json_data_text, 'implementation',
                                        implementation),
            include_all_options=include_all_options, stderr_file=stderr_file)
        if from_json_data_text is not None:
            config.parse_json(from_json_text=from_json_data_text,
                              ok_to_use_defaults=ok_to_use_defaults,
                              stderr_file=stderr_file)
        return config
    return load


tio_json_read_loader: ConfigLoader = tio_json_loader(Capabilities(),
                                                     FileAccess.READ)
"""Ready-made loader for a configuration of an endpoint that is read."""

tio_json_create_loader: ConfigLoader = tio_json_loader(Capabilities(),
                                                       FileAccess.CREATE)
"""Ready-made loader for a configuration of an endpoint that is written."""

tio_json_update_loader: ConfigLoader = tio_json_loader(Capabilities(),
                                                       FileAccess.UPDATE)
"""Ready-made loader for an endpoint that is both read and written.

The three ready-made loaders ask for no capability beyond the access itself,
so they match every backend that can do that access. An application that needs
more than that, or that wants an edited file to stay as compact as it was,
calls ``tio_json_loader()`` with what it needs.
"""
