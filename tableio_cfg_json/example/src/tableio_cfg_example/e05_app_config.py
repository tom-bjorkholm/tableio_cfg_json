#! /usr/bin/env python3
"""Build an application config that owns several TableIO endpoints.

The Class A examples (e01-e04) each describe one TableIO endpoint: one
input or one output. A real program usually needs more than one endpoint
at once, plus a few settings that are the application's own and that
TableIO knows nothing about. This example shows that shape.

SplitCitiesConfig is a config-as-json application config. It owns three
nested TioJsonConfig endpoints (input, less_than_output and
not_less_than_output) and two application-owned members (split_column
and split_limit). The whole object validates and reads/writes itself as
one JSON file, and each nested endpoint keeps its own durable TableIO
choices, configured independently of the others.

This program builds that object directly in code, writes it as JSON, and
emits a plain text guide for later hand-editing. Building it in code
first makes an important point: the object is ordinary configuration
data. The interactive wizard shown in a later example is only one way to
produce the very same object; nothing about the config depends on a
wizard.

To make "configured independently" concrete, the two outputs here use
different formats: less_than_output is CSV and not_less_than_output is
ODS. Any endpoint could be any format TableIO supports; the split runner
(e06_split_cities) reads this one config and writes each output through
its own endpoint.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
from pathlib import Path
import sys
from textwrap import wrap
from typing import Optional, Sequence, TextIO, override

from config_as_json import Config, ConfigNesting, ConfigNestingKind, \
    MemberValidationStep, NestedConfigs, PathOrStr, StrLenValidator, \
    StrValidator, ValidationPlan
from tableio import Capabilities, FileAccess, access_capabilities
from tableio_cfg_json import TioJsonConfig, describe_config_members, \
    describe_config_reference, get_config_member_names, get_general_cfg_info, \
    tio_json_config_default


CITY_COLUMNS = ('City', 'Country', 'Continent')
"""Header row expected by this teaching example."""
_WIDTH = 79


class SplitCitiesConfig(Config):
    """Configuration for one run of the split-cities example program."""

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr) -> None:
        """Create or read the complete application configuration.

        Args:
            from_json_data_text: Optional JSON text to parse.
            from_json_filename: Optional JSON file to read.
            stderr_file: Stream receiving validation diagnostics.
        """
        # A config-as-json class is normally initialized to useful defaults.
        # Application code can then assign the specific values it wants before
        # writing JSON. build_app_config() below demonstrates that style, and
        # so does the interactive wizard example.
        self.input = _default_config(FileAccess.READ, stderr_file)
        self.less_than_output = _default_config(FileAccess.CREATE, stderr_file)
        self.not_less_than_output = _default_config(FileAccess.CREATE,
                                                    stderr_file)
        self.split_column = 'Country'
        self.split_limit = 'M'
        Config.__init__(self, from_json_data_text=from_json_data_text,
                        from_json_filename=from_json_filename,
                        stderr_file=stderr_file)

    @override
    def nested_configs(self) -> NestedConfigs:
        """Return nested TableIO config declarations for this config."""
        # The top-level application config owns three nested TioJsonConfig
        # objects. Each nested config needs a factory because the input member
        # is read-capable, while both output members are create-capable.
        input_nesting = ConfigNesting(kind=ConfigNestingKind.MEMBER,
                                      config_type=TioJsonConfig,
                                      factory_function=self._input_factory)
        create_nesting = ConfigNesting(kind=ConfigNestingKind.MEMBER,
                                       config_type=TioJsonConfig,
                                       factory_function=self._create_factory)
        return {
            'input': input_nesting,
            'less_than_output': create_nesting,
            'not_less_than_output': create_nesting
        }

    @override
    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return validation for the application-owned config values."""
        _ = stderr_file
        # We only validate the split column and split limit here because
        # the input and output configs are validated by the nested Configs.
        return [
            MemberValidationStep(
                member_names=['split_column'],
                validator=StrValidator(CITY_COLUMNS, ignore_case=False)),
            MemberValidationStep(
                member_names=['split_limit'],
                validator=StrLenValidator(min_length=1, max_length=None))
        ]

    def _input_factory(self, from_json_data_text: Optional[str] = None,
                       from_json_filename: Optional[PathOrStr] = None,
                       stderr_file: TextIO = sys.stderr) -> TioJsonConfig:
        """Create a nested read-capable TableIO config from JSON."""
        return _json_config(FileAccess.READ, from_json_data_text,
                            from_json_filename, stderr_file)

    def _create_factory(self, from_json_data_text: Optional[str] = None,
                        from_json_filename: Optional[PathOrStr] = None,
                        stderr_file: TextIO = sys.stderr) -> TioJsonConfig:
        """Create a nested create-capable TableIO config from JSON."""
        return _json_config(FileAccess.CREATE, from_json_data_text,
                            from_json_filename, stderr_file)


def build_app_config(stderr_file: TextIO) -> SplitCitiesConfig:
    """Build the split-cities application config directly in code.

    The object starts with defaults and then receives the specific values
    this example wants. Each endpoint is assigned its own TableIO default
    for a chosen format, which is why the two outputs can use different
    formats. The application-owned split_column and split_limit are plain
    Python values assigned the same way.

    Args:
        stderr_file: Stream receiving validation diagnostics.
    Returns:
        A validated SplitCitiesConfig ready to be written as JSON.
    """
    config = SplitCitiesConfig(stderr_file=stderr_file)
    # Each nested endpoint is its own TableIO endpoint config. Assigning a
    # differently-formatted default to each output shows that the outputs are
    # configured independently; the input is read-capable, the outputs are
    # create-capable.
    config.input = _default_config(FileAccess.READ, stderr_file, 'CSV')
    config.less_than_output = _default_config(FileAccess.CREATE, stderr_file,
                                              'CSV')
    config.not_less_than_output = _default_config(FileAccess.CREATE,
                                                  stderr_file, 'ODS')
    # These two are the application's own settings. TableIO reads and writes
    # tables, but it does not know which rows this program wants in each file.
    config.split_column = 'Country'
    config.split_limit = 'M'
    return config


def create_app_config_files(config_file: Path, syntax_file: Path,
                            stderr_file: Optional[TextIO] = None) -> None:
    """Build the application config and write the JSON and guide files.

    Unlike the wizard example there is no user interaction here, so this
    function needs no input stream: the values come from build_app_config.

    Args:
        config_file: JSON application configuration file to write.
        syntax_file: Plain text guide for later hand-editing.
        stderr_file: Optional diagnostic stream for TableIO/config errors.
    """
    err_file = sys.stderr if stderr_file is None else stderr_file
    config = build_app_config(err_file)
    config.write(to_json_filename=config_file, stderr_file=err_file)
    # The text file is for the human who later opens the JSON by hand. It is
    # intentionally broader than the specific choices made in code above.
    syntax_file.write_text(_syntax_text(config, err_file) + '\n',
                           encoding='utf-8')


def _default_config(file_access: FileAccess, stderr_file: TextIO,
                    format_name: Optional[str] = None) -> TioJsonConfig:
    """Return a default nested TableIO config for one file access mode.

    Passing format_name pins the endpoint to that format; leaving it None
    lets TableIO recommend a default, which is how the class initializes
    its members before the caller overrides them.
    """
    capabilities = access_capabilities(file_access, error_file=stderr_file)
    return tio_json_config_default(capabilities=capabilities,
                                   file_access=file_access,
                                   format_name=format_name)


def _json_config(file_access: FileAccess, from_json_data_text: Optional[str],
                 from_json_filename: Optional[PathOrStr],
                 stderr_file: TextIO) -> TioJsonConfig:
    """Read a nested TableIO config for one file access mode."""
    capabilities = access_capabilities(file_access, error_file=stderr_file)
    return TioJsonConfig(capabilities=capabilities, file_access=file_access,
                         from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file)


def _syntax_text(config: SplitCitiesConfig, stderr_file: TextIO) -> str:
    """Build the plain text guide written next to the JSON config."""
    read_caps = access_capabilities(FileAccess.READ, error_file=stderr_file)
    create_caps = access_capabilities(FileAccess.CREATE,
                                      error_file=stderr_file)
    name_lists = [
        _member_names(read_caps, FileAccess.READ),
        _member_names(create_caps, FileAccess.CREATE)]
    less_intro = ('This output receives rows with the selected value below '
                  'the split limit.')
    not_less_intro = 'This output receives the remaining data rows.'
    parts = [
        get_general_cfg_info(),
        _application_guide(),
        _endpoint_guide('input', 'The input endpoint reads the city table.',
                        config.input, read_caps, FileAccess.READ, stderr_file),
        _endpoint_guide('less_than_output', less_intro,
                        config.less_than_output, create_caps,
                        FileAccess.CREATE, stderr_file),
        _endpoint_guide('not_less_than_output', not_less_intro,
                        config.not_less_than_output, create_caps,
                        FileAccess.CREATE, stderr_file),
        'Configuration member reference\n\n'
        + describe_config_reference(member_names=_unique_names(name_lists))]
    return '\n\n'.join(parts)


def _application_guide() -> str:
    """Return the application-owned part of the syntax guide."""
    text = (
        'Split-cities application configuration\n\n'
        'The top-level JSON object has five members. The members input, '
        'less_than_output and not_less_than_output are nested TableIO '
        'endpoint configurations. The member split_column selects one of '
        'City, Country or Continent. The member split_limit is a normal '
        'Python string, and the example compares strings case-sensitively.')
    title, paragraph = text.split('\n\n', maxsplit=1)
    return title + '\n\n' + _paragraph(paragraph)


# pylint: disable-next=too-many-arguments,too-many-positional-arguments
def _endpoint_guide(member_name: str, intro_text: str, config: TioJsonConfig,
                    capabilities: Capabilities, file_access: FileAccess,
                    stderr_file: TextIO) -> str:
    """Return the syntax guide for one nested TableIO endpoint config."""
    format_name = _format_name(config)
    member_text = describe_config_members(capabilities=capabilities,
                                          file_access=file_access)
    selected_text = config.as_json_string(stderr_file=stderr_file)
    intro = _paragraph(
        f'{intro_text} It currently uses the {format_name} format.')
    return (
        f'{member_name}\n\n'
        + intro
        + '\n\nEditable endpoint choices and members:\n\n'
        + member_text
        + '\n\nCurrently selected endpoint JSON:\n\n'
        + selected_text)


def _member_names(capabilities: Capabilities,
                  file_access: FileAccess) -> list[str]:
    """Return relevant TableIO member names for one endpoint config."""
    member_names = get_config_member_names(capabilities=capabilities,
                                           file_access=file_access)
    return list(member_names)


def _format_name(config: TioJsonConfig) -> str:
    """Return the required format name from a validated config object."""
    assert isinstance(config.format_name, str)
    return config.format_name


def _unique_names(name_lists: Sequence[Sequence[str]]) -> list[str]:
    """Return unique names in first-seen order."""
    member_names: list[str] = []
    for name_list in name_lists:
        for member_name in name_list:
            if member_name not in member_names:
                member_names.append(member_name)
    return member_names


def _paragraph(text: str) -> str:
    """Return one wrapped plain text paragraph."""
    return '\n'.join(wrap(text, width=_WIDTH))


# ---------------------------------------------------------------------------
# Only command line handling below this line.


def build_parser() -> argparse.ArgumentParser:
    """Build the command line parser for the application config example."""
    parser = argparse.ArgumentParser(
        description='Build the split-cities application config in code.')
    parser.add_argument('-c', '--cfg', dest='config_file', required=True,
                        type=Path, help='JSON configuration file to write.')
    parser.add_argument('-t', '--txt', dest='syntax_file', required=True,
                        type=Path, help='Plain text syntax guide to write.')
    return parser


def main(args: Optional[list[str]] = None) -> int:
    """Parse command line arguments and write the application config files."""
    parsed = build_parser().parse_args(args)
    create_app_config_files(config_file=parsed.config_file,
                            syntax_file=parsed.syntax_file)
    return 0


if __name__ == '__main__':
    sys.exit(main())
