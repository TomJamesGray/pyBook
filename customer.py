import dbConnection,sqlite3,main
from tabulate import tabulate
from helpers import getArgsBy
from getConfig import getConfPart
def makeCustomerWizzard():
	name = input("What is their name: ")
	address = input("What is their address: ")
	telephone = input("What is their phone number: ")

	makeCustomer(name,address,telephone)
	# Go back to main part
	main.main()
def listCustomers(argsString):
	conn=dbConnection.connect('bookings.db')
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
	main.main()
def makeCustomer(name,address,telephone):
	# Insert Customer into database
	conn=dbConnection.connect('bookings.db')
	try:
		conn.execute("INSERT INTO customers (name,address,telephone) VALUES(?,?,?)",
			(name, address,telephone))
		conn.commit()
	except sqlite3.Error as e:
		print('Error: {}'.format(e))

	print("Successfully created {}".format(name))
	conn.close()
def getCustomerId(name,address=None):
	# 
	# TODO - 	Check amount of rows returned to see if name is unique
	# 			Carry on moving it away from OOP, i.e fix references to functions
	# 
	conn=dbConnection.connect('bookings.db')
	if address==None:
		try:
			# count(*) used as sqlite doesn't know rows returned without iterating
			# over it first
			cursor = conn.execute(
				"SELECT count(*) FROM customers WHERE name=? LIMIT 2",
				(name)
			)
			rowsReturned = cursor.fetchone()[0]
			print(rowsReturned)
		except sqlite3.Error as e:
			print("Error: {}".format(e))

if __name__ == "__main__":
    getCustomerId('q')