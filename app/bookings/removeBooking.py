import sqlite3
from app.helpers import getArgsBy
from app.helpers.getConfig import getConfPart
from app.db import dbConnection
from tabulate import tabulate
# Get arguments from config file to get from which attributes a 
# booking can be removed, then get the arguments provided by the 
# user, confirm the decision, then remove booking with remove()

def removeWizzard(argsString):
	if argsString == '' or not argsString:
		print("No arguments provided")
		outputs.decideWhatToDo()
	else:
		args = getArgsBy(argsString,',|=')
		searchableArgs = getArgsBy(getConfPart('removeBy','bookings').strip(),',')
		# Where clause will be used in both select and delete statement so
		# is made up here
		whereClause = ""
		unChecked=True
		i=0
		vals=[]
		while unChecked:
			if args[i] in searchableArgs:
				if argsFound >= 1:
					whereClause += "AND " + args[i] + '=? '
				else:
					whereClause += agrs[i] + '=?'
				# i+1 is the value corresponding to the argument
				# and is removed so it won't be treated as an argument
				# in the next run
				vals.append(args[i+1])
				agrs.remove(agrs[i+1])
			else:
				print("Invalid argument: {}".format(args[i]))
				outputs.decideWhatToDo()
			i+=1
			if i >= len(args):
				unChecked = False