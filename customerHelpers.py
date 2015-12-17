from dbConnection import connect
import sqlite3
def customerAmountLookup(column, query):
	# Looks up customers based on a column and query
	# Returns the amount of matching customers
	conn = connect()
	try:
		cursor = conn.execute(
			"SELECT count(*) FROM customers WHERE (?)=(?)",
			(column,query))
		# get amount of rows returned
		return len(cursor.fetchall())
	except sqlite3.Error as e:
		print('Error: {}'.format(e))
def idLookup(name,address=None):
	conn = connect()
	# Check if address value provided
	if address != None:
		try:
			cursor = conn.execute(
				"SELECT id FROM customers WHERE name=(?) AND address=(?)",
				name,address)
			customerId=cursor.fetchone()[0]
		except sqlite3.Error as e:
			print("Error: {}".format(e))
			return "ERROR"
	else:
		try:
			cursor = conn.execute(
				"SELECT customerId FROM customers WHERE name=(?)",
				name)
			customerId=cursor.fetchone()[0]
		except sqlite3.Error as e:
			print("Error: {}".format(e))
			return "ERROR"
	return customerId
	conn.close()
if __name__ == "__main__":
	print(customerAmountLookup('name','q'))