#! /usr/bin/env python3
"""Shared helpers for the interactive wizard test modules.

These provide a scripted UI bridge, console runners and the scripted
answer builders that several wizard test modules reuse to drive one
endpoint configuration.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

# pylint: disable=protected-access

from io import StringIO
from typing import Callable, Optional, Sequence

from tableio import CsvDialect, FileAccess, access_capabilities, \
    add_access_capabilities, list_implementations_tableio, \
    list_registered_tableio
from tableio_cfg_json import TioJsonConfig, WizardUiBridge, \
    WizardUiBridgeConsole, get_config_member_names, tio_json_config_wizard, \
    TableCell, TableColumn, PartialCheck
from tableio_cfg_json._wizard_ui_bridge_helpers import ask_many, ask_one, \
    ask_yes_no, run_table
import tableio_cfg_json.wizard as wizard_module


class _ScriptedBridge(WizardUiBridge):
    """Wizard UI bridge that returns scripted answers for tests.

    The bridge implements the typed ask methods directly, like a real
    bridge, by feeding scripted raw answers into the shared answer
    interpreters. A scripted answer that is an exception is raised
    instead, which lets tests drive navigation requests.
    """

    def __init__(self, answers: Sequence[str | int | BaseException]) -> None:
        """Store raw answers returned in order to the ask methods."""
        self.answers: list[str | int | BaseException] = list(answers)
        self.calls: list[
            tuple[str, Optional[str], Optional[tuple[str, ...]]]] = []
        self.messages: list[str] = []
        self.stderr_file = StringIO()

    def _next(self) -> str | int:
        """Return the next scripted answer, raising scripted exceptions."""
        if not self.answers:
            raise EOFError('No scripted answer left.')
        answer = self.answers.pop(0)
        if isinstance(answer, BaseException):
            raise answer
        return answer

    def _reader(self, question: str, choices: Optional[Sequence[str]]
                ) -> Callable[[Optional[str]], str | int]:
        """Return a reader that records each call and pops an answer."""
        choice_tuple = None if choices is None else tuple(choices)

        def read(reason: Optional[str]) -> str | int:
            self.calls.append((question, reason, choice_tuple))
            return self._next()
        return read

    def ask_text(self, question: str, re_ask_reason: Optional[str] = None,
                 nullable: bool = False, *, default: Optional[str] = None,
                 sensitive: bool = False) -> Optional[str]:
        """Return the next scripted answer as text."""
        if sensitive and default is not None:
            raise ValueError('default is not allowed for sensitive input')
        self.calls.append((question, re_ask_reason, None))
        answer = self._next()
        text = answer if isinstance(answer, str) else str(answer)
        if text == '' and default is not None:
            return default
        return None if (nullable and text == '') else text

    def ask_choice(self, question: str, *, choices: Sequence[str],
                   default: Optional[str] = None,
                   re_ask_reason: Optional[str] = None) -> str:
        """Pick one scripted choice; see WizardUiBridge.ask_choice."""
        return ask_one(self._reader(question, choices), choices, default,
                       re_ask_reason)

    # pylint: disable-next=too-many-arguments
    def ask_multi(self, question: str, *, choices: Sequence[str],
                  default: Optional[Sequence[str]] = None, min_select: int = 0,
                  max_select: Optional[int] = None,
                  re_ask_reason: Optional[str] = None) -> list[str]:
        """Pick several scripted choices; see WizardUiBridge.ask_multi."""
        return ask_many(self._reader(question, choices), choices, default,
                        min_select, max_select, re_ask_reason, one_based=False)

    def ask_yes_no(self, question: str, default: bool,
                   re_ask_reason: Optional[str] = None) -> bool:
        """Answer a scripted yes/no question; see ask_yes_no."""
        return ask_yes_no(self._reader(question, ('yes', 'no')), default,
                          re_ask_reason)

    # pylint: disable-next=too-many-arguments
    def ask_table(self, columns: Sequence[TableColumn],
                  cells: list[list[TableCell]], question: str, *,
                  re_ask_reason: Optional[str] = None,
                  partial_check: Optional[PartialCheck] = None,
                  min_rows: Optional[int] = None,
                  max_rows: Optional[int] = None) -> list[list[Optional[str]]]:
        """Fill a table from scripted answers; see ask_table."""
        _ = (min_rows, max_rows)
        return run_table(self._cell_reader, self.show, columns, cells,
                         question, re_ask_reason, partial_check)

    def _cell_reader(self, prompt: str, re_ask_reason: Optional[str] = None,
                     choices: Optional[Sequence[str]] = None) -> str | int:
        """Record one table-cell prompt and return the next answer."""
        choice_tuple = None if choices is None else tuple(choices)
        self.calls.append((prompt, re_ask_reason, choice_tuple))
        return self._next()

    def error_file(self) -> StringIO:
        """Return the stream used for validation diagnostics."""
        return self.stderr_file

    def show(self, message: str) -> None:
        """Store a shown message."""
        self.messages.append(message)


def _run_wizard(file_access: FileAccess, answer_lines: list[str]
                ) -> tuple[TioJsonConfig, str, str]:
    """Run the wizard with scripted answers."""
    stdin_file = StringIO('\n'.join(answer_lines) + '\n')
    stdout_file = StringIO()
    stderr_file = StringIO()
    ui_bridge = WizardUiBridgeConsole(stdout_file, stdin_file, stderr_file)
    capabilities = access_capabilities(file_access, error_file=stderr_file)
    config = tio_json_config_wizard(capabilities, file_access, ui_bridge)
    return config, stdout_file.getvalue(), stderr_file.getvalue()


def _run_bridge(file_access: FileAccess,
                ui_bridge: WizardUiBridge) -> TioJsonConfig:
    """Run the wizard through a supplied bridge."""
    capabilities = access_capabilities(file_access,
                                       error_file=ui_bridge.error_file())
    return tio_json_config_wizard(capabilities, file_access, ui_bridge)


def _wizard_lines(format_name: str, file_access: FileAccess,
                  impl_answer: Optional[str] = None,
                  member_answers: Optional[dict[str, list[str]]] = None
                  ) -> list[str]:
    """Return scripted answers for one format and optional member values."""
    capabilities = access_capabilities(file_access)
    match_caps = add_access_capabilities(file_access, capabilities)
    format_names = list_registered_tableio(capabilities=match_caps)
    impl_names = list_implementations_tableio(format_name=format_name,
                                              capabilities=match_caps)
    answer_map = {} if member_answers is None else member_answers
    lines = [_menu_number(format_name, format_names)]
    implementation = None
    if len(impl_names) > 1:
        impl_menu = (wizard_module._AUTO_IMPL,) + tuple(impl_names)
        lines.append('' if impl_answer is None else impl_answer)
        if impl_answer is not None and impl_answer != '':
            implementation = impl_menu[int(impl_answer) - 1]
    for member_name in _optional_names(format_name, file_access,
                                       implementation):
        lines.extend(answer_map.get(member_name, ['']))
    return lines


def _optional_names(format_name: str, file_access: FileAccess,
                    implementation: Optional[str]) -> tuple[str, ...]:
    """Return optional wizard member names for one scripted selection."""
    capabilities = access_capabilities(file_access)
    member_names = get_config_member_names(capabilities=capabilities,
                                           file_access=file_access,
                                           format_name=format_name,
                                           implementation=implementation)
    return tuple(name for name in member_names
                 if name not in ('format_name', 'implementation'))


def _menu_number(choice: str, choices: Sequence[str]) -> str:
    """Return the one-based menu number for a known choice."""
    return str(choices.index(choice) + 1)


def _format_index(format_name: str, file_access: FileAccess) -> int:
    """Return the 0-based index of one format for scripted answers."""
    capabilities = access_capabilities(file_access)
    match_caps = add_access_capabilities(file_access, capabilities)
    return list_registered_tableio(capabilities=match_caps).index(format_name)


def _member_answer_lines(format_name: str, file_access: FileAccess,
                         implementation: Optional[str] = None,
                         member_answers: Optional[dict[str, list[str | int]]]
                         = None) -> list[str | int]:
    """Return scripted answers for optional members."""
    answer_map = {} if member_answers is None else member_answers
    lines: list[str | int] = []
    for member_name in _optional_names(format_name, file_access,
                                       implementation):
        lines.extend(answer_map.get(member_name, ['']))
    return lines


def assert_csv_core(config: TioJsonConfig) -> None:
    """Assert the CSV option values shared by several wizard tests."""
    assert config.character_encoding == 'utf-8'
    assert config.csv is not None
    assert config.csv.dialect == CsvDialect.UNIX
    assert config.csv.delimiter == ';'
