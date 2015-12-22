import dbConnection, sqlite3, main
from tabulate import tabulate
from helpers import getArgsBy
from getConfig import getConfPart
def makeCustomerWizzard():
	name = input("What is their name: ")
	address = input("What is their address: ")
	telephone = input("What is their phone number: ")

	# Create instance of Customer class
	customer=Customer(name,address,telephone)
	# Insert it into db
	customer.makeCustomer()
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
class Customer:
	def __init__(self,name,address,telephone=None):
		self.name=name
		self.address=address
		# Telephone isn't required to allow getCustomerId
		self.telephone=telephone
	def makeCustomer(self):
		# Insert Customer into database
		conn=dbConnection.connect('bookings.db')
		try:
			conn.execute("INSERT INTO customers (name,address,telephone) VALUES(?,?,?)",
				(self.name, self.address,self.telephone))
			conn.commit()
		except sqlite3.Error as e:
			print('Error: {}'.format(e))

		print("Successfully created {}".format(self.name))
		conn.close()

	def getCustomerId(self):	
		# Retrieve customer id making sure it matches name and address
		conn=dbConnection.connect('bookings.db')
		try:
			cursor = conn.execute(
				"SELECT customerId FROM customers WHERE name=? AND address=? LIMIT 1",
				(self.name,self.address)
			)
			# Fetch just the one value
			customerId = cursor.fetchone()[0]
		except (sqlite3.Error,TypeError) as e:
			print("Error: {}".format(e))
			return "ERROR"
			pass
		finally:
			conn.close()


		return customerId