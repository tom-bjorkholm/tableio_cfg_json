#! /usr/bin/env python3
"""Open a stored configuration in an edit-cfg-json editor.

The earlier examples produced configuration files in two ways: built in code
(e01, e04, e05) and asked question by question with a wizard (e07 to e10).
This example shows the third way a stored configuration is changed, which is
a folding editor over the whole file at once.

The editor is the `edit-cfg-json` family. Its core discovers the editable
structure of a `config_as_json.Config` object by introspection, so an
application gets an editor for its configuration without writing any user
interface code and without describing its configuration a second time. The
core is what this example imports; the two editors an end user sees are the
separate packages `edit-cfg-json-tk` and `edit-cfg-json-textual`, and the
only difference between them here is which backend object is passed.

## What the editor works out, and what it has to be told

The editor reads the class: the docstring of `TioJsonConfig` and of each
nested section class, what kind of value each member holds, which members may
be left out of the file, and the names of an enum such as the CSV dialect. It
never reads a validator, and that is a deliberate decision of that library
rather than something not built yet, so nothing tells it which values
`format_name` or `table_alignment` accept.

That is what `tio_json_descriptions()` is for. It is the one source of truth
for how the TableIO configuration is described, so an application that stores
a `TioJsonConfig` does not write the TableIO documentation down a second time
and does not have it drift. What it says is what the editor cannot work out:
what each member is for, which values a plain string member accepts, what
those values mean, and which formats and implementations the member has any
effect for.

## The two shapes, and the two things this package offers

Class A of these examples stores one TableIO endpoint per file, so the whole
configuration is a `TioJsonConfig`. That class needs the runtime capabilities
and file access of the endpoint, which no configuration file could hold, so
the editor cannot construct it: `tio_json_loader()` is how the application
says how it is built. The descriptions are then `TIO_JSON_DESCRIPTIONS`,
which is `tio_json_descriptions()` with no prefix.

This example calls `tio_json_loader()`, because a real application usually
has capabilities of its own to ask for. A program that is told a name rather
than making a call uses one of the ready-made loaders instead:
`tio_json_read_loader`, `tio_json_create_loader` and
`tio_json_update_loader`, one per file access, each asking for no capability
beyond the access itself.

Class B stores an application configuration that owns several endpoints, and
`SplitCitiesConfig` from e05 is that shape. That class the editor constructs
itself, because its constructor takes only the arguments `config_as_json`
documents, so no loader is needed. What is needed is a prefix: a description
addresses the whole path to the member it is about, so the members of the
endpoint called `input` are described under `('input', ...)`. That is the one
argument `tio_json_descriptions()` takes, and an application with several
endpoints calls it once per endpoint and merges the results with whatever it
says about its own members.

## How much of an endpoint can be edited

A member that is not in the file is not a row in the editor, because the
editor is shown the JSON the object would write and an unset optional member
is not in it. A compact configuration file therefore opens with very few rows.

Which of the two happens is decided by whoever constructs the object. For a
single endpoint that is `tio_json_loader()`, and it builds on a complete set
of defaults by default, so every option is a row and the editor marks the ones
the file did not hold. For an application configuration it is the application
class: `SplitCitiesConfig` constructs its endpoints compactly, so its
endpoints open with the members its file holds and no more. Neither is wrong;
they are the same trade-off seen from two places, between a configuration file
that stays as small as it was and one that shows everything there is to set.

## Which backend this example runs

`DumpEditor` is the only backend the core ships. It prints the model once and
returns, there is nothing for a user to do while it runs and therefore no Save
to press, and that is why this example never writes the file back. It is used
here because it is the one backend that needs no user interface library, so
this example runs anywhere and in the test suite.

An application that wants a real editor changes the one argument that says
which backend to run, and nothing else on this page:

```python
from edit_cfg_json_textual import TextualEditor

saved = edit(config, TextualEditor(), descriptions=app_descriptions(),
             in_file=config_file)
```

`edit_cfg_json_tk.TkEditor` is the same thing in a desktop window. Neither
package is a dependency of `tableio-cfg-json`, so an application that wants
one declares it for itself.

## Why this example does not call edit()

`edit()` is the short door, and the snippet above is what an application with
a real editor writes: build the model, run the backend, hand back what was
saved. This example needs the long way round for one reason only. A container
large enough to flood a window opens folded, and a printout has no control to
press on it, so an application configuration would print its three endpoints
as three folded lines and none of the members this example is about. A program
that prints therefore builds the model itself and opens every container before
the backend runs. That is what `--unfold` of `python3 -m edit_cfg_json.dump`
does, and it is the whole of the difference. An interactive session wants the
folding and asks for none of this.

## Running it

```sh
python -m tableio_cfg_example.e11_config_editor --cfg split-cities.json
python -m tableio_cfg_example.e11_config_editor -e -r -c capitals-csv.json
```
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
from pathlib import Path
import sys
from typing import Optional, TextIO

from config_as_json import Config
from edit_cfg_json import ConfigLoader, Descriptions, DumpEditor, \
    EditorBackend, LoadPolicy, editor_model
from tableio import FileAccess, access_capabilities
from tableio_cfg_example.e05_app_config import SplitCitiesConfig
from tableio_cfg_json import TIO_JSON_DESCRIPTIONS, tio_json_config_default, \
    tio_json_descriptions, tio_json_loader

ENDPOINT_MEMBERS = ('input', 'less_than_output', 'not_less_than_output')
"""The members of SplitCitiesConfig that hold a TableIO endpoint."""

APP_DESCRIPTIONS: Descriptions = {
    ('split_column',): 'Column whose value decides which output a row goes '
                       'to. One of City, Country or Continent.',
    ('split_limit',): 'A row goes to the less-than output while the value in '
                      'that column sorts before this text.'}
"""What the application says about the two members that are its own.

Only these two are written here. Everything below the three endpoint members
belongs to `tableio-cfg-json` and is asked for instead of repeated, which is
the whole point of this example.
"""


def app_descriptions() -> Descriptions:
    """Return what to tell an editor about a SplitCitiesConfig.

    The application describes its own two members, and asks
    tio_json_descriptions() for each of its three endpoints. The prefix is
    the name of the member holding that endpoint, because a description
    addresses the whole path to the member it is about: the format of the
    input endpoint is ('input', 'format_name') and the CSV dialect of the
    less-than output is ('less_than_output', 'csv', 'dialect').

    Returns:
        What every member of the application configuration means.
    """
    described = dict(APP_DESCRIPTIONS)
    for member in ENDPOINT_MEMBERS:
        # Merging is ordinary dict work. The three calls cannot collide,
        # because each of them puts its paths below a different member.
        described.update(tio_json_descriptions((member,)))
    return described


def edit_app_config(config_file: Path, backend: EditorBackend,
                    stderr_file: TextIO) -> bool:
    """Edit a stored SplitCitiesConfig and report whether it was saved.

    No loader is passed. SplitCitiesConfig takes only the arguments that
    config_as_json documents, so the editor constructs it by reading its
    signature, and the nested endpoints are made by the factory functions
    that class already declares for reading a file.

    Args:
        config_file: JSON application configuration file to edit.
        backend: User interface backend that runs the editing session.
        stderr_file: Stream receiving diagnostics.
    Returns:
        Whether the session wrote the file.
    """
    config = SplitCitiesConfig(stderr_file=stderr_file)
    return _printed_session(config, backend, app_descriptions(), config_file,
                            None, stderr_file)


def edit_endpoint(config_file: Path, file_access: FileAccess,
                  backend: EditorBackend, stderr_file: TextIO) -> bool:
    """Edit a stored one-endpoint TableIO config and report the outcome.

    This is the Class A shape, where the whole configuration file is one
    TioJsonConfig. Two things are needed that the application configuration
    above needed neither of: a loader, because the class takes the runtime
    capabilities and file access that no file holds, and nothing in front of
    the description paths, because there is no member above them.

    Args:
        config_file: JSON endpoint configuration file to edit.
        file_access: Access mode the configuration is meant for. It is the
            application's own knowledge and is not in the file.
        backend: User interface backend that runs the editing session.
        stderr_file: Stream receiving diagnostics.
    Returns:
        Whether the session wrote the file.
    """
    capabilities = access_capabilities(file_access, error_file=stderr_file)
    # The object passed to edit() is what the session starts from when there
    # is no file. The loader is what reads the file itself, and it is the
    # loader that decides how much of the configuration is editable.
    config = tio_json_config_default(capabilities, file_access,
                                     include_all_options=True,
                                     stderr_file=stderr_file)
    loader = tio_json_loader(capabilities, file_access)
    return _printed_session(config, backend, TIO_JSON_DESCRIPTIONS,
                            config_file, loader, stderr_file)


# pylint: disable=too-many-arguments,too-many-positional-arguments
def _printed_session(config: Config, backend: EditorBackend,
                     descriptions: Descriptions, config_file: Path,
                     loader: Optional[ConfigLoader],
                     stderr_file: TextIO) -> bool:
    """Run one editing session over a whole file and report the outcome.

    This is `edit_cfg_json.edit()` written out, with the one extra step a
    printing backend needs. See the section of the module docstring about
    not calling edit() for why that step is here and why an application
    with a real editor calls edit() instead.

    Args:
        config: Object saying which class to edit and what it declares.
        backend: User interface backend that runs the editing session.
        descriptions: What to tell the editor about the members.
        config_file: JSON configuration file to edit.
        loader: How to construct the class, or None when the editor can
            construct it from the signature it declares.
        stderr_file: Stream receiving diagnostics.
    Returns:
        Whether the session wrote the file.
    """
    # LoadPolicy.DEFAULTS lets the declared values fill in what the file
    # leaves out, and the editor marks every member that was filled in, so
    # an older or hand-trimmed file still opens.
    model = editor_model(config, descriptions=descriptions,
                         in_file=config_file, loader=loader,
                         policy=LoadPolicy.DEFAULTS, stderr_file=stderr_file)
    # no_more_folding keeps a container open that the validation pass the
    # backend makes before it prints would otherwise fold away again.
    model.open_all(no_more_folding=True)
    backend.run_editor(model)
    return model.saved_config is not None


# ---------------------------------------------------------------------------
# Only command line handling below this line.


def build_parser() -> argparse.ArgumentParser:
    """Build the command line parser for the editor example.

    Returns:
        Parser for command line arguments.
    """
    parser = argparse.ArgumentParser(
        description='Edit a stored tableio-cfg-json configuration.')
    parser.add_argument('-c', '--cfg', dest='config_file', required=True,
                        type=Path, help='JSON configuration file to edit.')
    parser.add_argument('-e', '--endpoint', action='store_true',
                        help='The file holds one TableIO endpoint config.')
    access_group = parser.add_mutually_exclusive_group()
    for short_name, long_name, help_text in [
            ('-r', '--read', 'The endpoint is read-capable.'),
            ('-w', '--write', 'The endpoint is write-capable.')]:
        access_group.add_argument(short_name, long_name, action='store_true',
                                  help=help_text)
    return parser


def main(args: Optional[list[str]] = None) -> int:
    """Parse command line arguments and run the requested editor.

    Args:
        args: Optional command line argument list. ``None`` means
            ``sys.argv[1:]``.
    Returns:
        Process exit code.
    """
    parsed = build_parser().parse_args(args)
    # The whole of what running a real editor instead would change: an
    # instance of TkEditor or TextualEditor in place of this one.
    backend: EditorBackend = DumpEditor()
    if parsed.endpoint:
        file_access = FileAccess.READ if parsed.read else FileAccess.CREATE
        edit_endpoint(parsed.config_file, file_access, backend, sys.stderr)
    else:
        edit_app_config(parsed.config_file, backend, sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
