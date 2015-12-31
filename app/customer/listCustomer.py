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
				args.remove(args[i])
				# And remove other val relating to the initial invalid value
				# using i again as previous one has already removed 
				args.remove(args[i])
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