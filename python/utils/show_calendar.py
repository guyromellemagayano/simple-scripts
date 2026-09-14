#!/usr/bin/env python3
"""
Simple Calendar [v1.0]

Displays a calendar with adjustable values to update the calendar of your preference
"""

import calendar
from datetime import UTC, datetime

now = datetime.now(UTC).astimezone()
# Function to show calendar
def showCalendar(yy, mm):
    return(calendar.month(yy, mm))

print(showCalendar(now.year, now.month))
