import sqlite3
from app.helpers.helpers import getArgsBy,getCustomerInfoFromId
from app.helpers.getConfig import getConfPart
from app.db import dbConnection
from app import outputs
# Get arguments from config file to get from which attributes a 
# booking can be removed, then get the arguments provided by the 
# user, confirm the decision, then remove booking with remove()

def removeWizzard(argsString):
	if argsString == '' or not argsString:
		print("No arguments provided")
		outputs.decideWhatToDo()
	args = getArgsBy(argsString,',|=')
	if len(args) % 2 != 0:
		print("Insufficient arguments provided, odd number")
	attributes = []
	values = []
	for i in range(0,len(args)):
		if i%2 == 0:
			attributes.append(args[i])
		else:
			values.append(args[i])
	remove(attributes,values)
	outputs.decideWhatToDo()
def remove(attributes,values,confirm=True):
	#First check that values is a list and that it has the same length
	#As attributes
	if not isinstance(values,list):
		return "ERROR:valuesNotList"
	elif len(attributes) != len(values):
		return "ERROR:attributesLengthNotEqualValuesLength"
	whereClause = ""
	unChecked=True
	argsFound,i=0,0
	searchableArgs=getArgsBy(getConfPart('removeBy','bookings').strip(),',')
	while unChecked:
		if attributes[i] in searchableArgs:
			if argsFound >= 1:
				whereClause += "AND " + attributes[i] + '=? '
			else:
				whereClause += attributes[i] + '=?'
				argsFound += 1
		else:
			return "ERROR:attributeNotInSearchableArgs"
		i+=1
		if i >= len(attributes):
			unChecked = False

	conn = dbConnection.connect()
	statement = "SELECT count(*),customerId FROM bookings WHERE " + whereClause + " LIMIT 2"
	print(statement)
	print("These are the Values: {}".format(values))
	print(tuple(values))
	try:
		cursor = conn.execute(
			statement,
			tuple(values)
		)
		countAndCustomerId = cursor.fetchone()
		print(countAndCustomerId)
		if countAndCustomerId[0] == 2:
			return "ERROR:bookingNotUnique"
		elif countAndCustomerId[0] == 0:
			return "ERROR:noBookingFound"
		else:
			# By defualt this will happen as confirm defualts to True
			# However in the future this may not be desired and so can 
			# be set to remove without customer detail confrimation
			confirmDelete=None
			if confirm:
				customerInfo = getCustomerInfoFromId(countAndCustomerId[1])
				print(customerInfo)
				print("Delete booking for {}, address {}".format(customerInfo[0],customerInfo[1]))
				confirmDelete = input("(y/n): ")
			if confirmDelete.lower() == "y" or (confirm==False and confrimDelete==None):
				deleteCursor = conn.execute(
					"DELETE FROM bookings WHERE " + whereClause,
					tuple(values),
				)
				conn.commit()
			elif confirmDelete.lower() == "n":
				return "deleteCanceled"
			else:
				return "invalidInput"
	except sqlite3.Error as e:
		print("Error: {}".format(e))
