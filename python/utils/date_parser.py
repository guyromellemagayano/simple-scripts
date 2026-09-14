#!/usr/bin/env python3
from datetime import UTC, datetime

now		= datetime.now(UTC).astimezone()
month 	= str(now.month)
day		= str(now.day)
year	= str(now.year)
hour	= str(now.hour)
minute	= str(now.minute)
second	= str(now.second)

print(month + " / " + day + " / " + year + " - " + hour + ' : ' + minute + ' : ' + second)
