#! /usr/bin/env python3
"""Tests for the wizard-ui-bridge teaching examples."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from io import StringIO
from pathlib import Path
from typing import Optional

from wizard_ui_example import e01_ask_form, e02_schedule_form
from wizard_ui_bridge import UiBridgeType, AskPathField, \
    AskMultiChoiceField, AskDateField, AskDateTimeField, AskDurationField, \
    WizardPathKind


def _run_form(lines: list[str]) -> tuple[Optional[str], str]:
    """Run the ask_form example on the console with scripted answers.

    Args:
        lines: One scripted answer per line, in the order the console
               fallback asks the form fields.
    Returns:
        The summary returned by the example and the full console output.
    """
    out_file = StringIO()
    summary = e01_ask_form.collect_and_summarize(
        stdin_file=StringIO('\n'.join(lines) + '\n'), stdout_file=out_file,
        stderr_file=StringIO(), bridge_type=UiBridgeType.CONSOLE)
    return summary, out_file.getvalue()


def test_form_csv(tmp_path: Path) -> None:
    """Accepting the defaults summarizes a full CSV export form."""
    out_path = tmp_path / 'report.csv'
    summary, _ = _run_form(['', str(out_path), '', '', '', '', ''])
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
    summary, _ = _run_form(['', str(out_path), '2', '', '', ''])
    assert summary is not None
    assert 'Output format: Excel' in summary
    assert 'CSV delimiter' not in summary


def test_form_reask(tmp_path: Path) -> None:
    """A bad CSV delimiter is reported and the form is re-asked."""
    out_path = tmp_path / 'report.csv'
    bad = ['', str(out_path), '', ';;', '', '', '']
    good = ['', str(out_path), '', ',', '', '', '']
    summary, output = _run_form(bad + good)
    assert summary is not None
    assert 'CSV delimiter: ,' in summary
    assert 'exactly one character' in output


def test_form_cancel() -> None:
    """Aborting at the first field returns no summary."""
    summary, output = _run_form([':q'])
    assert summary is None
    assert 'cancelled' in output


def test_form_fields() -> None:
    """The form describes seven fields with a new-file path input."""
    fields = e01_ask_form.build_export_form()
    assert len(fields) == 7
    path_field = fields[1]
    assert isinstance(path_field, AskPathField)
    assert path_field.path_options.kind == WizardPathKind.NON_EXISTING_FILE
    columns_field = fields[6]
    assert isinstance(columns_field, AskMultiChoiceField)
    assert columns_field.min_select == 1
    assert e01_ask_form.build_parser().parse_args([]).ui == 'auto'


def _run_schedule(lines: list[str]) -> tuple[Optional[str], str]:
    """Run the scheduling-form example on the console with scripted lines."""
    out_file = StringIO()
    summary = e02_schedule_form.collect_and_summarize(
        stdin_file=StringIO('\n'.join(lines) + '\n'), stdout_file=out_file,
        stderr_file=StringIO(), bridge_type=UiBridgeType.CONSOLE)
    return summary, out_file.getvalue()


def test_schedule_prefill() -> None:
    """The end time is prefilled from the date, start and duration."""
    summary, _ = _run_schedule(['', '2024-06-15', '', '', '', '', ''])
    assert summary is not None
    assert 'Date: 2024-06-15' in summary
    assert 'Ends at: 2024-06-15 10:00:00' in summary
    assert 'Price: 0.0' in summary


def test_schedule_free() -> None:
    """A free event disables the price row and shows it as free."""
    summary, _ = _run_schedule(['', '2024-06-15', '', '', '', 'yes'])
    assert summary is not None
    assert 'Price: free' in summary
    assert 'Ends at: 2024-06-15 10:00:00' in summary


def test_schedule_duration() -> None:
    """A typed duration extends the computed end time."""
    lines = ['Talk', '2024-06-15', '10:00', '02:30:00', '', '', '5']
    summary, _ = _run_schedule(lines)
    assert summary is not None
    assert 'Ends at: 2024-06-15 12:30:00' in summary
    assert 'Price: 5.0' in summary


def test_schedule_date_reask() -> None:
    """A bad date is re-asked before the schedule is summarized."""
    lines = ['', 'not-a-date', '2024-06-15', '', '', '', '', '']
    summary, _ = _run_schedule(lines)
    assert summary is not None
    assert 'Date: 2024-06-15' in summary


def test_schedule_cancel() -> None:
    """Aborting at the first field returns no summary."""
    summary, output = _run_schedule([':q'])
    assert summary is None
    assert 'cancelled' in output


def test_schedule_fields() -> None:
    """The scheduling form has the typed field kinds in order."""
    fields = e02_schedule_form.build_schedule_form()
    assert len(fields) == 7
    assert isinstance(fields[1], AskDateField)
    assert isinstance(fields[3], AskDurationField)
    assert isinstance(fields[4], AskDateTimeField)
    assert e02_schedule_form.build_parser().parse_args([]).ui == 'auto'
