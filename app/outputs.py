# import getConfig,bookings,customer
# import helpers.getConfig
from app.helpers import getConfig
from app.helpers.helpers import getCustomerInfoFromId
from app.customer import addCustomer,listCustomer
from app.bookings import addBooking,listBookings,removeBooking
def welcome():
    print("Hello welcome to %s" % getConfig.getConfPart('name'))

def decideWhatToDo():
	decision = input("What would you like to do (h for help)?: ")
	if decision.lower() == "ab":
		addBooking.wizzard()
	elif decision.lower() == "ac":
		addCustomer.wizzard()
	elif decision.lower().startswith('lc'):
		# Remove lc (i.e remove first 2 chars) to leave arguments
		args = decision[2:]
		listCustomer.list(args)
	elif decision.lower().startswith('lb'):
		# Remove lb (i.e remove first 2 chars) to leave arguments
		args = decision[2:]
		listBookings.list(args)
	elif decision.lower().startswith('rb'):
		args = decision[2:]
		removeBooking.removeWizzard(args)
	elif decision.lower() == "h":
		showHelp()
	else:
		decideWhatToDo()

def showHelp():
	print("ab - add booking")
	print("ac - add customer")
	print("lc - lists all customers")
	print("lb - lists all bookings")
	print("h - displays this help message")
	print("rb - removes a booking")
	decideWhatToDo()
