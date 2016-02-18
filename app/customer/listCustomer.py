from app.db import dbConnection
from app.helpers.helpers import getArgsBy
from app.helpers.getConfig import getConfPart
from tabulate import tabulate
from app import outputs
import sqlite3
def list(argsString):
	conn=dbConnection.connect()
	# Get args
	args = getArgsBy(argsString,',|=')
	if args == [''] or not args:
		try:
			customers=conn.execute("SELECT * FROM customers")
			print(tabulate(customers,
				headers=['Customer id','Name','Address','Telephone'],
				tablefmt="fancy_grid"))
		except sqlite3.Error as e:
			print("Error: {}".format(e))
	else:
		searchableArgs = getArgsBy(getConfPart('listBy','customers').strip(),',')
		argsFound = 0
		# Declare base statement then add to it if more args found
		statement = "SELECT * FROM customers WHERE "
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
				print("Invalid argument: {}".format(args[i]))
				outputs.decideWhatToDo()
			i+=1
			if i >= len(args):
				unSorted = False
		try:
			customers=conn.execute(
				statement,
				vals)
			print(tabulate(customers,
				headers=['customerId','name','address','telephone'],
				tablefmt="fancy_grid"))
		except sqlite3.Error as e:
			print("Error: {}".format(e))	

	# Return to start
	outputs.decideWhatToDo()
def getCustomer(argsDict,likeElems=[]):
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

