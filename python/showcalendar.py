"""
Simple Calendar [v1.0]

Displays a calendar with adjustable values to update the calendar of your preference
"""

from datetime import datetime
import calendar

now = datetime.now()
# Function to show calendar
def showCalendar(yy, mm):
    return(calendar.month(yy, mm))

print(showCalendar(now.year, now.month))