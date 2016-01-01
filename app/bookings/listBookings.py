import sqlite3
from app.helpers.helpers import getArgsBy
from app.helpers.getConfig import getConfPart
from tabulate import tabulate
from app import outputs
from app.db import dbConnection
def list(argsString):
	conn = dbConnection.connect()
	args = getArgsBy(argsString,',|=')
	if args == [''] or not args:
		try:
			bookings=conn.execute("SELECT * FROM bookings")
			print(tabulate(bookings,
				headers=['Booking id','Customer id','Time','Reason'],
				tablefmt="fancy_grid"))
		except sqlite3.Error as e:
			print("Error: {}".format(e))
	elif len(args) % 2 != 0:
		# If args length is an uneven length then there is a argument without a pair
		# value and will mean the sql statement will get messed up
		print("Odd number of arguments supplied")
		print("Each argument must have a value eg. \n")
		print("lb key=value or")
		print("lb key=value,key2=value2\n")
		print("There can be no lone keys or values")

	else:
		searchableArgs = getArgsBy(getConfPart('listBy','bookings').strip(),',')
		argsFound = 0
		# Declare base statement then add to it if more args found
		statement = "SELECT * FROM bookings WHERE "
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
			# print(args)
		try:
			bookings=conn.execute(
				statement,
				vals)
			print(tabulate(bookings,
				headers=['Booking id','Customer id','Time','Reason'],
				tablefmt="fancy_grid"))
		except sqlite3.Error as e:
			print("Error: {}".format(e))
	# Go back to start
	outputs.decideWhatToDo()