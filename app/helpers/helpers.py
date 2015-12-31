import re,sqlite3
from app.db import dbConnection
def getArgsBy(argString,regExp,strip=True):
	# Use regexp to split arguments into list
	if strip:
		argString = argString.strip()
	args = re.split(regExp,argString)

	return args

def getCustomerId(name,address=None):
	conn=dbConnection.connect()
	if address == None:
		try:
			# count(*) used as sqlite doesn't know rows returned without iterating
			# over it first
			# AND comma at end of name makes it a tuple, otherwise sql complains
			cursor = conn.execute(
				"SELECT count(*) FROM customers WHERE name=? LIMIT 2",
				(name,)
			)
			rowsReturned = cursor.fetchone()[0]
			if rowsReturned == 2:
				return "ERROR:nameNotUnique"
			elif rowsReturned == 1:
				# Get actual customer id
				# cursor = dbConnection.connect('bookings.db')
				cursor = conn.execute(
					"SELECT customerId FROM  customers WHERE name=?",
					(name,)
				)
				return cursor.fetchone()[0]
			else:
				return "ERROR:noMatchingCustomer"
		except sqlite3.Error as e:
			print("Error: {}".format(e))
			return "ERROR"
		finally:
			conn.close()
	elif address != None:
		try:
			# Basically the same as above just with an address, same checks 
			# But less likely to happen as it's v. unlikely two customers
			# will have the same name and address
			cursor = conn.execute(
				"SELECT count(*) FROM customers WHERE name=? AND address=? LIMIT 2",
				(name,address)
			)
			rowsReturned = cursor.fetchone()[0]
			if rowsReturned == 2:
				return "ERROR:nameAndAddressNotUnique"
			elif rowsReturned == 1:
				# Get actual customer id
				# cursor = dbConnection.connect('bookings.db')
				cursor = conn.execute(
					"SELECT customerId FROM  customers WHERE name=? AND address=?",
					(name,address)
				)
				return cursor.fetchone()[0]
			else:
				return "ERROR:noMatchingCustomer"
		except sqlite3.Error as e:
			print("Error: {}".format(e))
			return "ERROR"
		finally:
			conn.close()