import sqlite3,outputs,getConfig,customerHelpers
from customer import Customer
from datetime import datetime
from dbConnection import connect

def makeBookingWizzard(name=None, address=None):
	nameInput=input("Customer name: ")

	# Check if no input and no former value used
	if nameInput == "" and name == "":
		print("No name provided")
		makeBookingWizzard(name, address)
	elif name != "":
		name = nameInput
		# Check if this person is not the only person with the name
		# then get address input
		if customerHelpers.customerAmountLookup('name',name) >= 2:
			addressInput=input("Customer address: ")
			if addressInput == "" and address == "":
				print("No address provided")
				makeBookingWizzard(name, address)
			elif address != "":
				address = addressInput

	# print("Name: {}, address: {}".format(name,address))
	
	customerId = customerHelpers.idLookup(name)
	if customerId == "ERROR":
		outputs.decideWhatToDo();

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

def makeBooking(customerId,bookingDateTime,reason):
	conn = connect()
	try:
		curson = conn.execute(
			"INSERT INTO bookings (customerId,timeStampBook,reason) VALUES(?,?,?)",
			(customerId,bookingDateTime,reason))
		conn.commit()
	except sqlite3.Error as e:
		print('Error: {}'.format(e))
	finally:
		conn.close()