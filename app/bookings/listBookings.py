import sqlite3
from app.helpers.helpers import getArgsBy,makeArgsDict
from app.helpers.getConfig import getConfPart
from tabulate import tabulate
from app import outputs
from app.db import dbConnection
from datetime import datetime,timedelta
def listWizzard(argsString):
	args = getArgsBy(argsString, ',|=')
	if args == [''] or not args:
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
		argsDict = makeArgsDict(args,searchableArgs)
		try:
			bookings = getBookings(argsDict)
		except sqlite3.Error as e:
			print("Sqlite error occured: {}".format(e))

	print(tabulate(bookings,
		headers=['Booking id','Customer id','Time','Reason'],
		tablefmt="fancy_grid"))
	outputs.decideWhatToDo()
def getBookings(argsDict,likeElems=[]):
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
				#If i needs to be queried by like then put 'LIKE' in statement else use normal '='
				statement += "AND " + key +("LIKE ? " if (i in likeElems) else'=? ')
			else:
				statement += key + (" LIKE ? " if (i in likeElems) else"=? ")
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
		#Sets both variable to be equal to the original dateTime
		openTime, absOpenTime = (datetime.strptime(openTimes[0],'%H:%M'),)*2
		closeTime, absCloseTime = (datetime.strptime(openTimes[1],'%H:%M'),)*2
		#If 'today' is supplied as an argument then change it to be equal to the actual date
		if 'today' in args:
			args = [arg.replace('today',datetime.today().strftime('%d/%m/%Y')) for arg in args]
		if args == ['']:
			date = datetime.today()
		elif len(args) == 1:
			#Use date from args, ValueError will be made if invalid date is used
			date = datetime.strptime(args[0],'%d/%m/%Y').date()
		elif len(args) == 2:
			#Just 'times' supplied, so use that and todays date
			date = datetime.today()
			if args[0] == 'times':
				openTime = datetime.strptime(getArgsBy(args[1],'-')[0],'%H:%M')
				closeTime = datetime.strptime(getArgsBy(args[1],'-')[1],'%H:%M')
			else:
				print("Invalid argument '{}'  supplied, was expecting times".format(args[0]))
				outputs.decideWhatToDo()
		elif len(args) == 3:
			#Use date from args and get and use time args
			if args[1] == 'times':
				# In form `lba 1/1/1970 times=0:00-5:00`
				date = datetime.strptime(args[0],'%d/%m/%Y').date()
				openTime = datetime.strptime(getArgsBy(args[2],'-')[0],'%H:%M')
				closeTime = datetime.strptime(getArgsBy(args[2],'-')[1],'%H:%M')
			elif args[0] == 'times':
				# In form `lba times=0:00-5:00 1/1/1970`
				date = datetime.strptime(args[2],'%d/%m/%Y').date()
				openTime = datetime.strptime(getArgsBy(args[1],'-')[0],'%H:%M')
				closeTime = datetime.strptime(getArgsBy(args[1],'-')[1],'%H:%M')
			else:
				print("Expected times argument, none given")
				outputs.decideWhatToDo()
		else:
			#If nothing usable was supplied then give an error
			print("Invalid arguments supplied")
			outputs.decideWhatToDo()
	except ValueError as e:
		print("Error getting date: {}".format(e))
		outputs.decideWhatToDo()
	print(date.strftime('%Y-%m-%d'))
	#timeStampBook is to be queried by LIKE hence the [0] as it's the first elem in the dict
	bookings = getBookings({'timeStampBook':str(date.strftime('%Y-%m-%d'))+'%'},[0])
	bookingTimes = []
	for i in range(0,len(bookings)):
		#Remove date and append to booking times
		bookingTimes.append(bookings[i-1][2][11:])
	curTime = openTime
	if openTime <= absOpenTime:
		curTime = absOpenTime
	if closeTime >= absCloseTime:
		closeTime = absCloseTime
	
	while curTime <= closeTime:
		#Loop through bookings, increment 1 bookingLength at a time
		#If it matches a booking then don't add that time to the list
		if str(curTime.time()) not in bookingTimes:
			print("Aavailable: {}".format(curTime.time()))
		curTime = curTime + timedelta(minutes=int(bookingLength))
	outputs.decideWhatToDo() 
