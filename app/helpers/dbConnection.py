import sqlite3
from getConfig import getConfPart
def connect(dbFile=getConfPart('dbFile')):
	return sqlite3.connect(dbFile)