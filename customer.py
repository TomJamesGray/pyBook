import dbConnection, sqlite3, main
from tabulate import tabulate
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
def listCustomers():
	conn=dbConnection.connect('bookings.db')
	try:
		customers=conn.execute("SELECT * FROM customers")
	except sqlite3.Error as e:
		print("Error: {}".format(e))

	# Print customers nicely
	print(tabulate(customers))


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
