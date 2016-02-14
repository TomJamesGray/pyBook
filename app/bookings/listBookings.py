import sqlite3
from app.helpers.helpers import getArgsBy
from app.helpers.getConfig import getConfPart
from tabulate import tabulate
from app import outputs
from app.db import dbConnection
from datetime import datetime,timedelta
def listWizzard(argsString):
	args = getArgsBy(argsString, ',|=')
	if args == [''] or not args:
		getBookings({})
		try:
			bookings = getBookings({})
		except sqlite3.Error as e:
			print("Sqlite error occured: {}".format(e))
	elif len(args) % 2 != 0:
		# If args length is an uneven length then there is a argument without a pair
		# value and will mean the sql statement will get messed up
		print("Odd number of arguments supplied")
		print("Each argument must have a value eg. \n")
		print("lb key=value or")
		print("lb key=value,key2=value2\n")
		print("There can be no lone keys or values")
	else:
		# Check the arguments are valid then put them into a dictionary to be passed
		# to getBookings()
		searchableArgs = getArgsBy(getConfPart('listBy','bookings').strip(),',')
		argsDict = {}
		# Iterate by 2 to ignore the values of the args
		for i in range(0,len(args),2):
			if args[i] in searchableArgs:
				argsDict[args[i]] = args[i+1]
			else:
				print("Invalid argument: {}".format(args[i]))
				outputs.decideWhatToDo()
		try:
			bookings = getBookings(argsDict)
		except sqlite3.Error as e:
			print("Sqlite error occured: {}".format(e))

	print(tabulate(bookings,
		headers=['Booking id','Customer id','Time','Reason'],
		tablefmt="fancy_grid"))
	outputs.decideWhatToDo()
def getBookings(argsDict):
	# Returns a list with all the bookings matching the parameters provided in the
	# dictionary. If no bookings are found it will return an empty list. This fuction
	# doesn't check whether the parameters are allowed in config.ini	
	valsList = []
	if len(argsDict) == 0:
		statement = "SELECT * FROM bookings"
		
	else:
		i = 0
		statement = "SELECT * FROM bookings WHERE "
		for key,value in argsDict.items():
			if i >= 1:
				statement += "AND " + key + "=? "
			else:
				statement += str(key) + "=? "
			valsList.append(value)
			i += 1
	try:
		conn = dbConnection.connect()
		if len(valsList) == 0:
			cursor = conn.execute(statement)
		else:
			cursor = conn.execute(
				statement,
				valsList)
		return cursor.fetchall()
	except sqlite3.Error:
		raise
def listAvailable(argsString):
	# If args is blank then assume that today was wanted
	args = getArgsBy(argsString,',|=| ')
	conn = dbConnection.connect()
	openTimes = getArgsBy(getConfPart('openTimes'),',')
	bookingLength = getConfPart('bookingLength')
	try:
		openTime = datetime.strptime(openTimes[0],'%H:%M')
		closeTime = datetime.strptime(openTimes[1],'%H:%M')
		if args == [''] or 'today' in args:
			date = datetime.today()
		elif len(args) == 1:
			#Use date from args, ValueError will be made if invalid date is used
			date = datetime.strptime(args[0],'%d/%m/%Y').date()
		elif len(args) == 2:
			#Just 'times' supplied, so use that and todays date
			print("Two args")
			date = datetime.today()
			if args[0] == 'times':
				openTime = datetime.strptime(getArgsBy(args[1],'-')[0],'%H:%M')
				closeTime = datetime.strptime(getArgsBy(args[1],'-')[1],'%H:%M')
			else:
				print("Invalid argument '{}'  supplied, was expecting times".format(args[0]))
		elif len(args) == 3:
			#Use date from args and get and use time args
			date = datetime.strptime(args[0],'%d/%m/%Y').date()
			if args[1] == 'times':
				openTime = datetime.strptime(getArgsBy(args[2],'-')[0],'%H:%M')
				closeTime = datetime.strptime(getArgsBy(args[2],'-')[1],'%H:%M')
		else:
			#If nothing usable was supplied then give an error
			print("Invalid arguments supplied")
			outputs.decideWhatToDo()
	except ValueError as e:
		print("Error getting date: {}".format(e))
		outputs.decideWhatToDo()
	print(date.strftime('%Y-%m-%d'))
	cursor = conn.execute(
		"SELECT timeStampBook FROM bookings WHERE timeStampBook LIKE ?",
		(str(date.strftime('%Y-%m-%d'))+'%',)
	)
	bookings = cursor.fetchall()
	bookingTimes = []
	for i in range(0,len(bookings)):
		#Remove date and append to booking times
		bookingTimes.append(bookings[i][0][11:])
	curTime = openTime
	while curTime <= closeTime:
		#Loop through bookings, increment 1 bookingLength at a time
		#If it matches a booking then don't add that time to the list
		if str(curTime.time()) not in bookingTimes:
			print("Aavailable: {}".format(curTime.time()))
		curTime = curTime + timedelta(minutes=int(bookingLength))
	outputs.decideWhatToDo() 
