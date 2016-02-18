from app.db import dbConnection
from app.helpers.helpers import getArgsBy
from app.helpers.getConfig import getConfPart
from tabulate import tabulate
from app import outputs
import sqlite3
def list(argsString):
	# Get args
	args = getArgsBy(argsString,',|=')
	if args == [''] or not args:
		try:
			customers = getCustomers({})
		except sqlite3.Error as e:
			print("Sqlite error occured: {}".format(e))
	else:
		searchableArgs = getArgsBy(getConfPart('listBy','customers').strip(),',')
		# Declare base statement then add to it if more args found
		argsDict = {}
		for i in range(0,len(args),2):
			if args[i] in searchableArgs:
				argsDict[args[i]] = args[i+1]
			else:
				print("Invalid argument: {}".format(args[i]))
				outputs.decideWhatToDo()
		try:
			customers = getCustomers(argsDict)
		except sqlite3.Error as e:
			print("Sqlite error occured: {}".format(e))
	
	print(tabulate(customers,
		headers=['customerId','name','address','telephone'],
		tablefmt="fancy_grid"))
	# Return to start
	outputs.decideWhatToDo()
def getCustomers(argsDict,likeElems=[]):
	#Returns a list with all the bookings matching the parameters provided in the
	#dictionary. If no bookings are found it will return an empty list. This function
	#doesn't check whether the parameters are allowed in the config.ini
	valsList = []
	if len(argsDict) == 0:
		statement = "SELECT * FROM customers"

	else:
		i = 0
		statement = "SELECT * FROM customers WHERE "
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

