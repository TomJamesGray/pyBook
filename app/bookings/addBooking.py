import sqlite3
from app.db import dbConnection
from app.helpers import helpers
from app.bookings import listBookings
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
	try:
		customerId = helpers.getCustomerId(name,address)
	except LookupError as e:
		print("Lookup error: {}".format(e))
		outputs.decideWhatToDo()
	except sqlite3.Error as e:
		print("Sqlite error: {}".format(e))
		outputs.decideWhatToDo()
	except Exception as e:
		print("An unexpected error occured: {}".format(e))
		outputs.decideWhatToDo()

	if len(customerId) > 1:
		# Get address input as well, as name is not unique
		addressInput=input("Customer address: ")
		if address != None:
			print("Using address {} from previous add booking".format(address))
		elif addressInput != "":
			address = addressInput
		else:
			print("No address provided")
			wizzard(name,address)
	
		try:
			customerId = helpers.getCustomerId(name,address)
		except LookupError as e:
			print("Lookup error: {}".format(e))
			outputs.decideWahtToDo()
		except sqlite3.Error as e:
			print("Sqlite error: {}".format(e))
			outputs.decideWhatToDo()
		except Exception as e:
			print("An unexpected error occured: {}".format(e))
			outputs.decideWhatToDo()
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
	#Check if a booking at the same time has already been made
	if listBookings.getBookings({'timeStampBook':timeDate}) != []:
		print("A booking already exists at this time")
		doubleBookVerif = input("Would you like to double book this time?(y/n)")
		if doubleBookVerif.lower() != "y":
			wizzard(name,address)
	reason=input("Booking reason: ")
	makeBooking(customerId[0][0],timeDate,reason)
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
