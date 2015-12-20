import getConfig,bookings,customer
def welcome():
    print("Hello welcome to %s" % getConfig.getConfPart('name'))

def decideWhatToDo():
	decision = input("What would you like to do (h for help)?: ")
	if decision.lower() == "ab":
		bookings.makeBookingWizzard()
	elif decision.lower() == "ac":
		customer.makeCustomerWizzard()
	elif decision.lower() == "lc":
		customer.listCustomers()
		print("TestPlz")
	elif decision.lower() == "h":
		showHelp()
	else:
		decideWhatToDo()

def showHelp():
	print("ab - add booking")
	print("ac - add customer")
	print("lc - lists all customers")
	print("h - displays this help message")
	decideWhatToDo()