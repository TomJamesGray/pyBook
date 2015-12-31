from app.db import dbConnection
from app import outputs
import sqlite3
def wizzard():
	name = input("What is their name: ")
	address = input("What is their address: ")
	telephone = input("What is their phone number: ")

	makeCustomer(name,address,telephone)
	
	outputs.decideWhatToDo()
def makeCustomer(name,address,telephone):
	# Insert Customer into database
	conn=dbConnection.connect()
	try:
		conn.execute("INSERT INTO customers (name,address,telephone) VALUES(?,?,?)",
			(name, address,telephone))
		conn.commit()
		print("Successfully created {}".format(name))
	except sqlite3.Error as e:
		print('Error: {}'.format(e))
	finally:
		conn.close()