import sqlite3,outputs,dbConnection,main,customer
from datetime import datetime
from tabulate import tabulate
from getConfig import getConfPart
from helpers import getArgsBy

def makeBookingWizzard(name=None, address=None):
	nameInput=input("Customer name: ")

	# Check if no input and no former value used
	if nameInput == "" and name == "":
		print("No name provided")
		makeBookingWizzard(name, address)

	name = nameInput
	customerId = customer.getCustomerId(name)

	if customerId == "ERROR:nameNotUnique":
		# Get address input as well as name is not unique
		addressInput=input("Customer address: ")
		if addressInput == "" and address == "":
			print("No address provided")
			makeBookingWizzard(name, address)
		elif address != "":
			address = addressInput

		print("Name: {}, address: {}".format(name,address))
		
		customerId = customer.getCustomerId(name,address)
		if customerId == "ERROR":
			outputs.decideWhatToDo();
	elif customerId == "ERROR:noMatchingCustomer":
		print("Name not recognised")
		makeBookingWizzard(None,address)

	print(customerId)

	date=input("What day would you like to book (dd/mm/yyyy): ")
	try:
		bookingDate = datetime.strptime(date, '%d/%m/%Y')
	except ValueError:
		print("Invalid date")
		# Keep the same name and address values,
		# If input is blank then these values will be checked for
		makeBookingWizzard(name,address)

	time=input("When would you like to book: ")
	try:
		bookingTime = datetime.strptime(time, '%H:%M').time()
	except ValueError:
		print("Invalid time")

	# Concatenate date and time for easier storage
	timeDate = datetime.combine(bookingDate,bookingTime)

	reason=input("Booking reason: ")
	makeBooking(customerId,timeDate,reason)
	# Go back to start
	main.main()
def makeBooking(customerId,bookingDateTime,reason):
	conn = dbConnection.connect()
	try:
		curson = conn.execute(
			"INSERT INTO bookings (customerId,timeStampBook,reason) VALUES(?,?,?)",
			(customerId,bookingDateTime,reason))
		conn.commit()
	except sqlite3.Error as e:
		print('Error: {}'.format(e))
	finally:
		conn.close()
def listBookings(argsString):
	conn = dbConnection.connect()
	args = getArgsBy(argsString,',|=')
	if args == [''] or not args:
		try:
			bookings=conn.execute("SELECT * FROM bookings")
			print(tabulate(bookings,
				headers=['Booking id','Customer id','Time','Reason'],
				tablefmt="fancy_grid"))
		except sqlite3.Error as e:
			print("Error: {}".format(e))
	else:
		searchableArgs = getArgsBy(getConfPart('listBy','bookings').strip(),',')
		argsFound = 0
		# Declare base statement then add to it if more args found
		statement = "SELECT * FROM bookings WHERE "
		unSorted=True
		i=0
		vals=[]
		while unSorted:
			if args[i] in searchableArgs:
				if argsFound >= 1:
					statement += "AND " + args[i] + '=? '	
				else:
					statement += args[i] + '=? '
				vals.append(args[i+1])
				args.remove(args[i+1])
				argsFound += 1
			else:
				args.remove(args[i])
				# And remove other val relating to the initial invalid value
				# using i again as previous one has already removed 
				args.remove(args[i])
			i+=1
			if i >= len(args):
				unSorted = False
		try:
			bookings=conn.execute(
				statement,
				vals)
			print(tabulate(bookings,
				headers=['Booking id','Customer id','Time','Reason'],
				tablefmt="fancy_grid"))
		except sqlite3.Error as e:
			print("Error: {}".format(e))
	# Go back to start
	main.main()
