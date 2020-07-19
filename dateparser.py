from datetime import datetime 

now		= datetime.now()
month 	= str(now.month)
day		= str(now.day)
year	= str(now.year)
hour	= str(now.hour)
minute	= str(now.minute)
second	= str(now.second)

print(month + " / " + day + " / " + year + " - " + hour + ' : ' + minute + ' : ' + second)