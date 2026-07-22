#! /usr/local/bin/python3
"""A modal month calendar for the Textual date and date-time fields.

A date field, and the date part of a date-time field, are shown in the
Textual form as a text input paired with a Pick button. Pressing that
button, or typing the '?' token into the input, opens this modal
calendar. The user steps between months and years, moves between the
days of the shown month with the arrow keys, and clicks a day to return
it; Escape or the Cancel button returns nothing so the input is left
unchanged. Days outside a field's inclusive bounds are shown disabled,
so the calendar only offers acceptable dates.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from __future__ import annotations
import calendar
from datetime import date
from typing import ClassVar, Iterator, Optional
from textual import on
from textual.app import ComposeResult
from textual.binding import BindingType
from textual.containers import Grid, Horizontal
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Button, Footer, Static
from tableio_cfg_json.wizard_ui_bridge_form_defs import value_out_of_range

_WEEKDAYS = ('Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su')
_NAV = ('prev_year', 'prev_month', 'next_month', 'next_year')


def _shift(year: int, month: int, action: str) -> tuple[int, int]:
    """Return the year and month reached by one navigation action."""
    if action == 'prev_year':
        year -= 1
    elif action == 'next_year':
        year += 1
    elif action == 'prev_month':
        year, month = (year, month - 1) if month > 1 else (year - 1, 12)
    else:
        year, month = (year, month + 1) if month < 12 else (year + 1, 1)
    return (min(max(year, date.min.year), date.max.year), month)


class _CalendarScreen(ModalScreen[Optional[date]]):
    """Modal month calendar returning the date the user clicks.

    The screen opens on a seed month and offers day buttons for that
    month, greying the days outside the inclusive minimum and maximum.
    Month and year buttons move the view, a day button returns its date,
    and Escape or Cancel returns None so the field keeps its value. The
    seed day is focused on opening and the arrow keys move the focus
    between the enabled days of the shown month, so a day can be picked
    without the mouse.
    """

    BINDINGS: ClassVar[list[BindingType]] = [
        ('escape', 'cancel', 'Cancel'),
        ('left', 'step_day(-1)', 'Prev day'),
        ('right', 'step_day(1)', 'Next day'),
        ('up', 'step_day(-7)', 'Prev week'),
        ('down', 'step_day(7)', 'Next week')]
    CSS = '#cal_grid { height: auto; grid-size: 7; }'

    def __init__(self, seed: date, minimum: Optional[date],
                 maximum: Optional[date]) -> None:
        """Store the seed month, its day and the inclusive day bounds."""
        super().__init__()
        self._year = seed.year
        self._month = seed.month
        self._seed_day = seed.day
        self._minimum = minimum
        self._maximum = maximum

    def compose(self) -> ComposeResult:
        """Lay out the title, the navigation, the day grid and footer."""
        yield Static(id='cal_title')
        with Horizontal(id='cal_nav'):
            yield Button('<< year', id='prev_year')
            yield Button('< month', id='prev_month')
            yield Button('month >', id='next_month')
            yield Button('year >>', id='next_year')
        yield Grid(id='cal_grid')
        yield Button('Cancel', id='cancel')
        yield Footer()

    async def on_mount(self) -> None:
        """Fill the day grid and focus the seed month's starting day."""
        await self._show_month()
        self._focus_start_day()

    async def _show_month(self) -> None:
        """Show the current month's title and rebuild the day grid.

        The old day widgets are removed before the new ones are mounted,
        so navigating to another month never leaves two cells sharing a
        day id.
        """
        title = f'{calendar.month_name[self._month]} {self._year}'
        self.query_one('#cal_title', Static).update(title)
        grid = self.query_one('#cal_grid', Grid)
        await grid.remove_children()
        await grid.mount(*self._grid_widgets())

    def _grid_widgets(self) -> Iterator[Widget]:
        """Yield the weekday headers and then one widget per day cell."""
        for name in _WEEKDAYS:
            yield Static(name)
        weeks = calendar.Calendar().monthdayscalendar(self._year, self._month)
        for week in weeks:
            for day in week:
                yield self._day_widget(day)

    def _day_widget(self, day: int) -> Widget:
        """Return a blank cell for a padding day, else a day button."""
        if day == 0:
            return Static('')
        return Button(str(day), id=f'day_{day}',
                      disabled=self._day_disabled(day))

    def _day_disabled(self, day: int) -> bool:
        """Return whether a day of the shown month is out of bounds."""
        in_month = date(self._year, self._month, day)
        return value_out_of_range(in_month, self._minimum, self._maximum)

    @on(Button.Pressed)
    async def _pressed(self, event: Button.Pressed) -> None:
        """Route a button press to navigation, a day, or cancel."""
        button_id = event.button.id
        if button_id == 'cancel':
            self.action_cancel()
        elif button_id in _NAV:
            self._year, self._month = _shift(self._year, self._month,
                                             button_id)
            await self._show_month()
        elif button_id is not None and button_id.startswith('day_'):
            self.dismiss(date(self._year, self._month, int(button_id[4:])))

    def action_cancel(self) -> None:
        """Close the calendar without returning a date."""
        self.dismiss(None)

    def action_step_day(self, delta: int) -> None:
        """Move focus by delta days within the shown month, if possible.

        The arrow keys step one day left or right and one week up or
        down. A step off the month, or onto a disabled day, is ignored,
        so the focus stays on a selectable day of the shown month.
        """
        current = self._focused_day()
        if current is not None:
            self._focus_day(current + delta)

    def _focus_start_day(self) -> None:
        """Focus the seed day, or the nearest enabled day of the month."""
        day = self._nearest_enabled(self._seed_day)
        if day is not None:
            self._focus_day(day)

    def _focused_day(self) -> Optional[int]:
        """Return the day number of the focused day button, or None."""
        focused = self.focused
        if isinstance(focused, Button) and focused.id is not None \
                and focused.id.startswith('day_'):
            return int(focused.id[4:])
        return None

    def _focus_day(self, day: int) -> None:
        """Focus a day's button when it is in the month and enabled."""
        last = calendar.monthrange(self._year, self._month)[1]
        if 1 <= day <= last and not self._day_disabled(day):
            self.query_one(f'#day_{day}', Button).focus()

    def _nearest_enabled(self, target: int) -> Optional[int]:
        """Return the enabled day nearest target, or None when none are."""
        last = calendar.monthrange(self._year, self._month)[1]
        enabled = [day for day in range(1, last + 1)
                   if not self._day_disabled(day)]
        if not enabled:
            return None
        return min(enabled, key=lambda day: abs(day - target))
