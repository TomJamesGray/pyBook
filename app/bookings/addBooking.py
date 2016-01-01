import sqlite3
from app.db import dbConnection
from app.helpers import helpers
from datetime import datetime
from app import outputs
def wizzard(name=None, address=None):
	nameInput=input("Customer name: ")

	if name != None and nameInput == "":
		print("Using name '{}' from previous add booking".format(name))
		print("And any address from previous add booking")
	elif nameInput != "":
		name = nameInput
		address=None
	else:
		print("No name provided")
		wizzard(name,address)
	# Use address here as it may be from a previous run of 
	# the function where the user may have put in an invalid date for example
	customerId = helpers.getCustomerId(name,address)

	if customerId == "ERROR:nameNotUnique":
		# Get address input as well, as name is not unique
		addressInput=input("Customer address: ")
		if address != None:
			print("Using address {} from previous add booking".format(address))
		elif addressInput != "":
			address = addressInput
		else:
			print("No address provided")
			wizzard(name,address)

		
		customerId = helpers.getCustomerId(name,address)
		if customerId == "ERROR:nameAndAddressNotUnique":
			print("Multiple records with the same name and address have been found\n")
			print("Possible duplicate records?")
			outputs.decideWhatToDo()
		elif customerId == "Error:noMatchingCustomer":
			print("No customer found")
			outputs.decideWhatToDo()
		elif str(customerId).startswith('ERROR'):
			# Catch errors, all will be sqlite related, unless a new
			# error code is used in getCustomerId() and hasn't been added here
			print("An unknown error occured: {}".format(e))
			outputs.decideWhatToDo()
	elif customerId == "ERROR:noMatchingCustomer":
		print("Name not recognised")
		outputs.decideWhatToDo()

	print(customerId)

	date=input("What day would you like to book (dd/mm/yyyy): ")
	try:
		bookingDate = datetime.strptime(date, '%d/%m/%Y')
	except ValueError:
		print("Invalid date")
		# Keep the same name and address values,
		# If input is blank then these values will be checked for
		wizzard(name,address)

	time=input("When would you like to book: ")
	try:
		bookingTime = datetime.strptime(time, '%H:%M').time()
	except ValueError:
		print("Invalid time")
		wizzard(name,address)

	# Concatenate date and time for easier storage
	timeDate = datetime.combine(bookingDate,bookingTime)

	reason=input("Booking reason: ")
	makeBooking(customerId,timeDate,reason)
	# Go back to start
	outputs.decideWhatToDo()
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