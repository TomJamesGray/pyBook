import sqlite3,os
from app.helpers.getConfig import getConfPart
def getDbPath():
	print(os.path.join(os.path.abspath(os.path.dirname(__file__)),getConfPart('dbFile')))
	return os.path.join(os.path.abspath(os.path.dirname(__file__)),getConfPart('dbFile'))

def connect(dbFile=getDbPath()):
	return sqlite3.connect(dbFile)