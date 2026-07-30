#! /usr/bin/env python3
"""Tests for the wizard-ui-bridge teaching examples."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from io import StringIO
from pathlib import Path
from typing import Callable, Optional

from wizard_ui_example import e01_one_question, e02_question_kinds, \
    e05_ask_form, e06_typed_form
from wizard_ui_bridge import UiBridgeType, AskPathField, \
    AskMultiChoiceField, AskDateField, AskDateTimeField, AskDurationField, \
    WizardPathKind


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
