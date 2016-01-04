import sqlite3
from app.helpers.helpers import getArgsBy,getCustomerInfoFromId
from app.helpers.getConfig import getConfPart
from app.db import dbConnection
from tabulate import tabulate
from app import outputs
# Get arguments from config file to get from which attributes a 
# booking can be removed, then get the arguments provided by the 
# user, confirm the decision, then remove booking with remove()

def removeWizzard(argsString):
	if argsString == '' or not argsString:
		print("No arguments provided")
		outputs.decideWhatToDo()
	else:
		args = getArgsBy(argsString,',|=')
		searchableArgs = getArgsBy(getConfPart('removeBy','bookings').strip(),',')
		# Where clause will be used in both select and delete statement so
		# is made up here
		whereClause = ""
		unChecked=True
		argsFound=0
		i=0
		vals=[]
		while unChecked:
			if args[i] in searchableArgs:
				if argsFound >= 1:
					whereClause += "AND " + args[i] + '=? '
				else:
					whereClause += args[i] + '=?'
				# i+1 is the value corresponding to the argument
				# and is removed so it won't be treated as an argument
				# in the next run
				vals.append(args[i+1])
				args.remove(args[i+1])
				argsFound += 1
			else:
				print("Invalid argument: {}".format(args[i]))
				outputs.decideWhatToDo()
			i+=1
			if i >= len(args):
				unChecked = False
	#Select the booking using the statement and make sure it is unique
	#Then ask for confirmation before executing the DELETE statement
	conn = dbConnection.connect()
	statement = "SELECT count(*),customerId FROM bookings WHERE " + whereClause + " LIMIT 2"
	print(statement)
	try:
		cursor = conn.execute(
			statement,
			tuple(vals),
		)
		countAndCustomerId = cursor.fetchone()
		if countAndCustomerId[0] == 2:
			print("Booking not unique")
			outputs.decideWhatToDo()
		elif countAndCustomerId[0] == 0:
			print("No matching booking")
			outputs.decideWhatToDo()
		else:
			#There is only one booking, so confirm deletion with 
			#customer details using their id
			customerInfo = getCustomerInfoFromId(countAndCustomerId[1])
			print(customerInfo)
			print("Delete booking for {}, address {}".format(customerInfo[0],customerInfo[1]))
			confirmDelete = input("(y/n): ")
			if confirmDelete.lower() == "y":
				deleteCursor = conn.execute(
					"DELETE FROM bookings WHERE " + whereClause,
					tuple(vals),
				)
				conn.commit()
			elif confirmDelete.lower() == "n":
				outputs.decideWhatToDo()
			else:
				print("Unregcognized command")
				outputs.decideWhatToDo()
	except sqlite3.Error as e:
		print("Error: {}".format(e))
	outputs.decideWhatToDo()	
