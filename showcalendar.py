"""
Simple Calendar [v1.0]

Displays a calendar with adjustable values to update the calendar of your preference
"""

import calendar

# Function to show calendar
def showCalendar(yy, mm):
    return(calendar.month(yy, mm))

print(showCalendar(2016, 2))