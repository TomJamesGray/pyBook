import sqlite3,outputs
from customer import Customer
from datetime import datetime

def makeBookingWizzard(name=None, address=None):
	nameInput=input("Customer name: ")
	# Check if no input and no former value used
	if nameInput == "" and name == "":
		print("No name provided")
		makeBookingWizzard(name, address)
	elif name != "":
		name = nameInput

	addressInput=input("Customer address: ")
	if addressInput == "" and address == "":
		print("No address provided")
		makeBookingWizzard(name, address)
	elif address != "":
		address = addressInput
	print("Name: {}, address: {}".format(name,address))
	customer = Customer(name,address)
	customerId = Customer.getCustomerId(customer)
	if customerId == "ERROR":
		outputs.decideWhatToDo();

	print(customerId)

	date=input("What day would you like to book (dd/mm/yyyy): ")
	try:
		bookingDay = datetime.strptime(date, '%d/%m/%Y')
	except ValueError:
		print("Invalid date")
		# Keep the same name and address values,
		# If input is blank then these values will be checked for
		makeBookingWizzard(name,address)

	time=input("When would you like to book: ")
	try:
		bookingTime = datetime.strptime(time, '%H:%M')
	except ValueError:
		print("Invalid time")

	timeDate = date + time
