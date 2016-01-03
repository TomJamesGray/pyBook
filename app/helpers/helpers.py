import re,sqlite3
from app.db import dbConnection
from app.helpers.getConfig import getConfPart
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
def getCustomerInfoFromId(customerId,attributesWanted=['name','address']):
	# Get a customers information, by default name and address
	# From their id, the attryibutes wanted are passed in through
	# a list
	
	statement = "SELECT "
	if len(attributesWanted)==1:
		statement += "? "
	elif len(attributesWanted)==0:
		return "ERROR:noAttributesToSelect"
	else:
		i=0
		while i<len(attributesWanted):
			# check the values provided by the user against
			# customers -> list by, in config, as '?' can't be used
			# for column names in sql
			searchableArgs = getArgsBy(getConfPart('listBy','customers').strip(),',')
			if attributesWanted[i] in searchableArgs:
				if i != len(attributesWanted)-1 :
					statement += attributesWanted[i] + ","
				else:
					statement += attributesWanted[i]
			else:
				return "ERROR:unknownAttributeWanted"
			i += 1
	# No need to check if customer is unique as id is used
	# And is marked so in the db
	statement += " FROM customers WHERE customerId=?"
	conn = dbConnection.connect()
	print(statement)
	try:
		cursor = conn.execute(
			statement,
			(customerId,)
		)
		customerInfo = cursor.fetchone()
		if customerInfo == [''] or customerInfo == None:
			return "Error:noMatchingCustomer"
		else:
			return customerInfo
	except sqlite3.Error as e:
		print("Error: {}".format(e))
		return "ERROR"
