#! /usr/bin/env python3
"""Tests for the wizard-ui-bridge teaching examples."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from io import StringIO
from pathlib import Path
from typing import Callable, Optional

import pytest
from wizard_ui_example import e01_one_question, e02_question_kinds, \
    e03_navigation, e04_table_question, e05_ask_form, e06_typed_form, \
    e07_custom_bridge
from wizard_ui_bridge import UiBridgeType, AskPathField, \
    AskMultiChoiceField, AskDateField, AskDateTimeField, AskDurationField, \
    WizardPathKind, TableColumn, TableCell


def _drive(collect: Callable[..., Optional[str]],
           lines: list[str]) -> tuple[Optional[str], str, str]:
    """Run one example's collect function on the console with scripted lines.

    Args:
        collect: The example's collect_* function; all of them accept the
                 same stream and bridge_type keyword arguments.
        lines: One scripted answer per line, in the order the console
               fallback asks the questions.
    Returns:
        The value the collect function returned, the stdout text and the
        stderr text.
    """
    out_file = StringIO()
    err_file = StringIO()
    result = collect(stdin_file=StringIO('\n'.join(lines) + '\n'),
                     stdout_file=out_file, stderr_file=err_file,
                     bridge_type=UiBridgeType.CONSOLE)
    return result, out_file.getvalue(), err_file.getvalue()


def test_greeting_full() -> None:
    """A name, nickname and code produce a full greeting."""
    greeting, output, _ = _drive(e01_one_question.collect_greeting,
                                 ['Alice', 'Ali', 'secret', ''])
    assert greeting is not None
    assert 'Hello, Alice, also known as Ali!' in greeting
    assert 'has 6 character(s)' in greeting
    assert 'Hello, Alice' in output
    # A question must follow show() so a textual/GUI bridge renders it.
    assert 'Press Enter to finish.' in output


def test_greeting_default() -> None:
    """An empty name falls back to the default 'World'."""
    greeting, _, _ = _drive(e01_one_question.collect_greeting,
                            ['', 'Ali', 'x', ''])
    assert greeting is not None
    assert 'Hello, World, also known as Ali!' in greeting


def test_greeting_no_nickname() -> None:
    """An omitted nickname reuses the name and notes it on error_file."""
    greeting, _, errors = _drive(e01_one_question.collect_greeting,
                                 ['Bob', '', 'x', ''])
    assert greeting is not None
    assert 'Hello, Bob, also known as Bob!' in greeting
    assert 'No nickname given' in errors


def test_greeting_cancel() -> None:
    """Aborting at the first question makes no greeting."""
    greeting, output, _ = _drive(e01_one_question.collect_greeting, [':q'])
    assert greeting is None
    assert 'cancelled' in output


def test_greeting_ui_note() -> None:
    """ui_note names the console bridge and the parser defaults to auto."""
    note = e01_one_question.ui_note(UiBridgeType.CONSOLE)
    assert 'console' in note.lower()
    assert e01_one_question.build_parser().parse_args([]).ui == 'auto'


def test_export_defaults(tmp_path: Path) -> None:
    """Accepting the defaults summarizes a full CSV export."""
    out_path = tmp_path / 'report.csv'
    lines = ['', '', str(out_path), '', '', '']
    summary, _, _ = _drive(e02_question_kinds.collect_and_summarize, lines)
    assert summary is not None
    assert 'Report title: Cities report' in summary
    assert 'Output format: CSV' in summary
    assert f'Output file: {out_path}' in summary
    assert 'Row limit: all rows' in summary
    assert 'Header row: included' in summary
    assert 'Columns: City, Country, Continent' in summary


def test_export_path_reask(tmp_path: Path) -> None:
    """A wrong output extension is reported and the path is re-asked."""
    bad = tmp_path / 'report.txt'
    good = tmp_path / 'report.csv'
    lines = ['', '', str(bad), str(good), '', '', '']
    summary, _, errors = _drive(e02_question_kinds.collect_and_summarize,
                                lines)
    assert summary is not None
    assert f'Output file: {good}' in summary
    assert 'should end with ".csv"' in errors


def test_export_excel_limit(tmp_path: Path) -> None:
    """Choosing Excel, a row limit and custom answers are summarized."""
    out_path = tmp_path / 'report.xlsx'
    lines = ['Cities', '2', str(out_path), '100', 'no', '1,2']
    summary, _, _ = _drive(e02_question_kinds.collect_and_summarize, lines)
    assert summary is not None
    assert 'Output format: Excel' in summary
    assert 'Row limit: 100' in summary
    assert 'Header row: omitted' in summary
    assert 'Columns: City, Country' in summary


def test_export_population(tmp_path: Path) -> None:
    """A non-default column selection reaches the summary."""
    out_path = tmp_path / 'report.csv'
    lines = ['', '', str(out_path), '', '', '1,4']
    summary, _, _ = _drive(e02_question_kinds.collect_and_summarize, lines)
    assert summary is not None
    assert 'Columns: City, Population' in summary


def test_export_cancel() -> None:
    """Aborting at the first question makes no summary."""
    summary, output, _ = _drive(e02_question_kinds.collect_and_summarize,
                                [':q'])
    assert summary is None
    assert 'cancelled' in output


def test_export_parser() -> None:
    """The question-kinds parser defaults to the auto UI bridge."""
    assert e02_question_kinds.build_parser().parse_args([]).ui == 'auto'


def test_form_csv(tmp_path: Path) -> None:
    """Accepting the defaults summarizes a full CSV export form."""
    out_path = tmp_path / 'report.csv'
    summary, _, _ = _drive(e05_ask_form.collect_and_summarize,
                           ['', str(out_path), '', '', '', '', ''])
    assert summary is not None
    assert 'Report title: Cities report' in summary
    assert f'Output file: {out_path}' in summary
    assert 'Output format: CSV' in summary
    assert 'CSV delimiter: ,' in summary
    assert 'Row limit: all rows' in summary
    assert 'Header row: included' in summary
    assert 'Columns: City, Country, Continent' in summary


def test_form_no_delim(tmp_path: Path) -> None:
    """A non-CSV format disables and hides the delimiter row."""
    out_path = tmp_path / 'report.xlsx'
    summary, _, _ = _drive(e05_ask_form.collect_and_summarize,
                           ['', str(out_path), '2', '', '', ''])
    assert summary is not None
    assert 'Output format: Excel' in summary
    assert 'CSV delimiter' not in summary


def test_form_reask(tmp_path: Path) -> None:
    """A bad CSV delimiter is reported and the form is re-asked."""
    out_path = tmp_path / 'report.csv'
    bad = ['', str(out_path), '', ';;', '', '', '']
    good = ['', str(out_path), '', ',', '', '', '']
    summary, output, _ = _drive(e05_ask_form.collect_and_summarize, bad + good)
    assert summary is not None
    assert 'CSV delimiter: ,' in summary
    assert 'exactly one character' in output


def test_form_cancel() -> None:
    """Aborting at the first field returns no summary."""
    summary, output, _ = _drive(e05_ask_form.collect_and_summarize, [':q'])
    assert summary is None
    assert 'cancelled' in output


def test_form_fields() -> None:
    """The form describes seven fields with a new-file path input."""
    fields = e05_ask_form.build_export_form()
    assert len(fields) == 7
    path_field = fields[1]
    assert isinstance(path_field, AskPathField)
    assert path_field.path_options.kind == WizardPathKind.NON_EXISTING_FILE
    columns_field = fields[6]
    assert isinstance(columns_field, AskMultiChoiceField)
    assert columns_field.min_select == 1
    assert e05_ask_form.build_parser().parse_args([]).ui == 'auto'


def test_schedule_prefill() -> None:
    """The end time is prefilled from the date, start and duration."""
    summary, _, _ = _drive(e06_typed_form.collect_and_summarize,
                           ['', '2024-06-15', '', '', '', '', ''])
    assert summary is not None
    assert 'Date: 2024-06-15' in summary
    assert 'Ends at: 2024-06-15 10:00:00' in summary
    assert 'Price: 0.0' in summary


def test_schedule_free() -> None:
    """A free event disables the price row and shows it as free."""
    summary, _, _ = _drive(e06_typed_form.collect_and_summarize,
                           ['', '2024-06-15', '', '', '', 'yes'])
    assert summary is not None
    assert 'Price: free' in summary
    assert 'Ends at: 2024-06-15 10:00:00' in summary


def test_schedule_duration() -> None:
    """A typed duration extends the computed end time."""
    lines = ['Talk', '2024-06-15', '10:00', '02:30:00', '', '', '5']
    summary, _, _ = _drive(e06_typed_form.collect_and_summarize, lines)
    assert summary is not None
    assert 'Ends at: 2024-06-15 12:30:00' in summary
    assert 'Price: 5.0' in summary


def test_schedule_date_reask() -> None:
    """A bad date is re-asked before the schedule is summarized."""
    lines = ['', 'not-a-date', '2024-06-15', '', '', '', '', '']
    summary, _, _ = _drive(e06_typed_form.collect_and_summarize, lines)
    assert summary is not None
    assert 'Date: 2024-06-15' in summary


def test_schedule_cancel() -> None:
    """Aborting at the first field returns no summary."""
    summary, output, _ = _drive(e06_typed_form.collect_and_summarize, [':q'])
    assert summary is None
    assert 'cancelled' in output


def test_schedule_fields() -> None:
    """The scheduling form has the typed field kinds in order."""
    fields = e06_typed_form.build_schedule_form()
    assert len(fields) == 7
    assert isinstance(fields[1], AskDateField)
    assert isinstance(fields[3], AskDurationField)
    assert isinstance(fields[4], AskDateTimeField)
    assert e06_typed_form.build_parser().parse_args([]).ui == 'auto'


def test_account_personal() -> None:
    """A personal account is summarized without organization details."""
    lines = ['alice', 'a@x.com', '', 'x']
    summary, _, _ = _drive(e03_navigation.collect_account, lines)
    assert summary is not None
    assert 'Username: alice' in summary
    assert 'Account type: Personal' in summary
    assert 'Password: 1 character(s)' in summary
    assert 'Organization' not in summary


def test_account_org() -> None:
    """An organization account collects the nested organization level."""
    lines = ['bob', 'b@x.com', '2', 'BobCorp', '50', 'pw']
    summary, _, _ = _drive(e03_navigation.collect_account, lines)
    assert summary is not None
    assert 'Account type: Organization' in summary
    assert 'Organization: BobCorp' in summary
    assert 'Members: 50' in summary


def test_account_defaults() -> None:
    """Empty answers fall back to the built-in defaults."""
    summary, _, _ = _drive(e03_navigation.collect_account, ['', '', '', 'x'])
    assert summary is not None
    assert 'Username: guest' in summary
    assert 'Email: guest@example.com' in summary
    assert 'Account type: Personal' in summary


def test_back_keeps_answer() -> None:
    """Stepping back offers the earlier answer as the new default."""
    lines = ['alice', ':b', '', 'a@x.com', '', 'x']
    summary, _, _ = _drive(e03_navigation.collect_account, lines)
    assert summary is not None
    assert 'Username: alice' in summary


def test_cancel_org() -> None:
    """Cancelling the org level returns to the account-type question."""
    lines = ['carol', 'c@x.com', '2', 'TmpCorp', ':c', '1', 'x']
    summary, _, _ = _drive(e03_navigation.collect_account, lines)
    assert summary is not None
    assert 'Account type: Personal' in summary
    assert 'Organization' not in summary


def test_cancel_org_remembers() -> None:
    """Re-entering a cancelled level offers its earlier answers as defaults."""
    lines = ['x', 'x@x.com', '2', 'ReCorp', ':c', '2', '', '7', 'pw']
    summary, _, _ = _drive(e03_navigation.collect_account, lines)
    assert summary is not None
    assert 'Organization: ReCorp' in summary
    assert 'Members: 7' in summary


def test_back_from_org_first() -> None:
    """Back from the org level's first question re-asks account type."""
    lines = ['dave', 'd@x.com', '2', ':b', '1', 'x']
    summary, _, _ = _drive(e03_navigation.collect_account, lines)
    assert summary is not None
    assert 'Account type: Personal' in summary


def test_back_within_org() -> None:
    """Back inside the org level re-asks its previous question."""
    lines = ['eve', 'e@x.com', '2', 'EveCo', ':b', '', '10', 'x']
    summary, _, _ = _drive(e03_navigation.collect_account, lines)
    assert summary is not None
    assert 'Organization: EveCo' in summary
    assert 'Members: 10' in summary


def test_account_abort() -> None:
    """Aborting at the first question abandons the whole wizard."""
    summary, output, _ = _drive(e03_navigation.collect_account, [':q'])
    assert summary is None
    assert 'abandoned' in output


def test_top_cancel_note() -> None:
    """Cancelling at the top level re-asks with a note about no outer."""
    lines = ['frank', ':c', 'f@x.com', '', 'x']
    summary, output, _ = _drive(e03_navigation.collect_account, lines)
    assert summary is not None
    assert 'nothing to cancel out to' in output
    assert 'Email: f@x.com' in summary


def test_back_at_top_first() -> None:
    """Back at the very first question re-asks it with a note."""
    lines = [':b', 'gina', 'g@x.com', '', 'x']
    summary, output, _ = _drive(e03_navigation.collect_account, lines)
    assert summary is not None
    assert 'nothing to go back to' in output
    assert 'Username: gina' in summary


def test_nav_parser() -> None:
    """The navigation parser defaults to the auto UI bridge."""
    assert e03_navigation.build_parser().parse_args([]).ui == 'auto'


_FIXED_DEFAULTS = ['', '', '', '', '', '']


def test_tables_defaults() -> None:
    """Accepting both tables summarizes their starting content."""
    summary, _, _ = _drive(e04_table_question.collect_and_summarize,
                           _FIXED_DEFAULTS + [''])
    assert summary is not None
    assert 'city -> city (text)' in summary
    assert 'population -> population (number)' in summary
    assert 'founded -> founded (date)' in summary
    assert 'Alex: 2 seat(s)' in summary
    assert 'Bo: 3 seat(s)' in summary


def test_rename_custom() -> None:
    """Editing free-text cells renames the chosen columns."""
    fixed = ['City', '', '', '', 'Year', '']
    summary, _, _ = _drive(e04_table_question.collect_and_summarize,
                           fixed + [''])
    assert summary is not None
    assert 'city -> City (text)' in summary
    assert 'founded -> Year (date)' in summary


def test_rename_type() -> None:
    """Picking a choice cell changes that column's data type."""
    fixed = ['', '2', '', '', '', '']
    summary, _, _ = _drive(e04_table_question.collect_and_summarize,
                           fixed + [''])
    assert summary is not None
    assert 'city -> city (number)' in summary


def test_guest_add() -> None:
    """Adding a row extends the guest list."""
    variable = [':+', 'Cleo', '4', '']
    summary, _, _ = _drive(e04_table_question.collect_and_summarize,
                           _FIXED_DEFAULTS + variable)
    assert summary is not None
    assert 'Cleo: 4 seat(s)' in summary
    assert 'Alex: 2 seat(s)' in summary


def test_guest_remove() -> None:
    """Removing a row drops that guest from the list."""
    variable = [':- 2', '']
    summary, _, _ = _drive(e04_table_question.collect_and_summarize,
                           _FIXED_DEFAULTS + variable)
    assert summary is not None
    assert 'Alex: 2 seat(s)' in summary
    assert 'Bo:' not in summary


def test_guest_partial_check() -> None:
    """A blank name and an out-of-range seat count are re-asked."""
    variable = [':+', '', 'Dana', '99', '2', '']
    summary, _, errors = _drive(e04_table_question.collect_and_summarize,
                                _FIXED_DEFAULTS + variable)
    assert summary is not None
    assert 'guest name' in errors
    assert 'Seats must be' in errors
    assert 'Dana: 2 seat(s)' in summary


def test_guest_final_verify() -> None:
    """A duplicate name passes per-cell checks but fails final verify."""
    variable = [':+', 'Alex', '2', '', '3', 'Cara', '', '']
    summary, _, errors = _drive(e04_table_question.collect_and_summarize,
                                _FIXED_DEFAULTS + variable)
    assert summary is not None
    assert 'share a name' in errors
    assert 'Cara: 2 seat(s)' in summary


def test_guest_min() -> None:
    """Deleting below the minimum row count is refused."""
    variable = [':- 1', ':- 1', '']
    summary, _, errors = _drive(e04_table_question.collect_and_summarize,
                                _FIXED_DEFAULTS + variable)
    assert summary is not None
    assert 'At least 1' in errors
    assert 'Bo: 3 seat(s)' in summary
    assert 'Alex' not in summary


def test_tables_cancel() -> None:
    """Aborting at the first cell cancels the whole program."""
    summary, output, _ = _drive(e04_table_question.collect_and_summarize,
                                [':q'])
    assert summary is None
    assert 'cancelled' in output


def test_table_shape() -> None:
    """The rename table has one read-only column and a choice cell."""
    columns = e04_table_question.RENAME_COLUMNS
    assert columns[0].read_only
    assert not columns[1].read_only
    cells = e04_table_question.build_rename_cells()
    assert len(cells) == 3
    assert cells[0][2].choices == ('text', 'number', 'date')
    assert e04_table_question.build_parser().parse_args([]).ui == 'auto'


def _drive_e07(lines: list[str], ui: str = 'custom'
               ) -> tuple[Optional[str], str, str]:
    """Run the custom-bridge example on scripted lines, capturing streams.

    The example builds its own bridge from a ``ui`` string rather than a
    UiBridgeType, so it needs a driver of its own; 'custom' selects the
    teleprinter bridge and 'console' a built-in bridge for contrast.
    """
    out_file = StringIO()
    err_file = StringIO()
    result = e07_custom_bridge.collect_and_summarize(
        stdin_file=StringIO('\n'.join(lines) + '\n'), stdout_file=out_file,
        stderr_file=err_file, ui=ui)
    return result, out_file.getvalue(), err_file.getvalue()


def test_e07_folds_output(tmp_path: Path) -> None:
    """The teleprinter bridge folds every printed line into its glyphs."""
    out_path = tmp_path / 'report.csv'
    summary, output, _ = _drive_e07(['', '', str(out_path), '', '', '', ''])
    assert summary is not None
    assert 'Report title: Cities report' in summary  # returned unfolded
    assert output == output.upper()  # nothing lowercase reaches the device
    assert 'REPORT TITLE: CITIES REPORT' in output  # the folded summary
    assert '0) CSV' in output  # choices become a numbered menu
    assert 'AT LEAST 1' in output  # the ask_int override names its range
    assert '?' in output  # a path separator folds to the replacement mark


def test_e07_choice_number(tmp_path: Path) -> None:
    """Numbered menus let the teleprinter pick a choice by its index."""
    out_path = tmp_path / 'report.xlsx'
    lines = ['Cities', '1', str(out_path), '100', '1', '0,1', '']
    summary, _, _ = _drive_e07(lines)
    assert summary is not None
    assert 'Output format: Excel' in summary
    assert 'Row limit: 100' in summary
    assert 'Header row: omitted' in summary
    assert 'Columns: City, Country' in summary


def test_e07_console_wizard(tmp_path: Path) -> None:
    """The same wizard runs unfolded on the built-in console bridge."""
    out_path = tmp_path / 'report.csv'
    summary, output, _ = _drive_e07(['', '', str(out_path), '', '', '', ''],
                                    ui='console')
    assert summary is not None
    assert 'Report title: Cities report' in output  # not folded to uppercase


def test_e07_cancel() -> None:
    """Aborting at the first question makes no summary."""
    summary, output, _ = _drive_e07([':q'])
    assert summary is None
    assert 'CANCELLED' in output


def test_e07_table_choice() -> None:
    """The mandatory ask_table fills fixed rows, choice cells by number."""
    answers = StringIO('Anna\n1\nBo\n0\n')
    bridge = e07_custom_bridge.TeleprinterBridge(StringIO(), answers,
                                                 StringIO())
    columns = [TableColumn('name'), TableColumn('kind')]
    kinds = ('text', 'number')
    cells = [[TableCell('x'), TableCell(None, choices=kinds)],
             [TableCell('y'), TableCell(None, choices=kinds)]]
    result = bridge.ask_table(columns, cells, 'edit')
    assert result == [['Anna', 'number'], ['Bo', 'text']]


def test_e07_table_var() -> None:
    """A variable-row table is refused: adding rows needs bridge support."""
    bridge = e07_custom_bridge.TeleprinterBridge(StringIO(), StringIO(),
                                                 StringIO())
    columns = [TableColumn('guest')]
    cells = [[TableCell('Ann')]]
    with pytest.raises(NotImplementedError):
        bridge.ask_table(columns, cells, 'guests', min_rows=1, max_rows=5)


def test_e07_fold_rule() -> None:
    """show() uppercases letters and replaces unsupported glyphs."""
    out_file = StringIO()
    bridge = e07_custom_bridge.TeleprinterBridge(out_file, StringIO(),
                                                 StringIO())
    bridge.show('a/b=c é')
    assert out_file.getvalue() == 'A?B?C ?\n'


def test_e07_parser() -> None:
    """The custom-bridge parser defaults to the teleprinter bridge."""
    assert e07_custom_bridge.build_parser().parse_args([]).ui == 'custom'
    parsed = e07_custom_bridge.build_parser().parse_args(['--ui', 'console'])
    assert parsed.ui == 'console'
