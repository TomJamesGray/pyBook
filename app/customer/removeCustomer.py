import sqlite3
from app.helpers.helpers import getArgsBy,getCustomerInfoFromId,makeArgsDict
from app.helpers.getConfig import getConfPart
from app.db import dbConnection
from app import outputs

def removeWizzard(argsString):
    if argsString == "" or not argsString:
        print("No arguments provided")
        outputs.decideWhatToDo()
    args = getArgsBy(argsString,',|=')
    print(args)
    if len(args) % 2 != 0:
        print("Insuficient arguments providied, odd number")
        outputs.decideWhatToDo()
    searchableArgs=getArgsBy(getConfPart('removeBy','customers').strip(),',')
    try:
        argsDict = makeArgsDict(args,searchableArgs)
    except ValueError as e:
        print("Value error: {}".format(e))
        outputs.decideWhatToDo()
    try:
        remove(argsDict)
    except ValueError as e:
        print("Value error: {}".format(e))
    except TypeError as e:
        print("Type error: {}".format(e))
    except LookupError as e:
        print("Lookup error: {}".format(e))
    outputs.decideWhatToDo()
def remove(argsDict,limit=1,confirm=True):
    #Deletes bookings matching parameters given, if the amount of bookings matching the
    #parameters exceedes the limit then a ValueError will be thrown
    #Also by defualt a confirm message will come up
    i = 0
    whereClause = ""
    valsList = []
    #First check generate a where clause that can be used across both the select and
    #remove statements
    for key,value in argsDict.items():
        if i >=1:
            whereClause += "AND " + key + "=? "
        else:
            whereClause += key + "=? "
        valsList.append(value)
        i += 1
    #Append limit +1 to check if too many results are returned
    valsList.append(str(limit+1))
    conn = dbConnection.connect()
    statement = "SELECT customerId FROM customers WHERE " + whereClause + " LIMIT ?"
    print(statement)
    #print(valsList)
    try:
        cursor = conn.execute(
            statement,
            valsList
        )
        customerIds = cursor.fetchall()
        print(customerIds)
        #outputs.decideWhatToDo()
        if len(customerIds) > limit:
            raise LookupError("More customers found than specified limit")
        elif len(customerIds) == 0:
            raise LookupError("No customers found")
        else:
            confirmDelete=None
            #Loop through all the bookings returned and as it's a nested tuple list
            #it's in the form customerIds[i][0]
            for i in range(0,len(customerIds)):
                # By defualt this will happen as confirm defualts to True
                # However in the future this may not be desired and so can
                # be set to remove without customer detail confrimation
                if confirm:
                    try:
                        #Loop through
                        customerInfo = getCustomerInfoFromId(customerIds[i][0])
                    except ValueError as e:
                        print("Value error: {}".format(e))
                        outputs.decideWhatToDo()
                    except LookupError as e:
                        print("Lookup error: {}".format(e))
                        outputs.decideWhatToDo()
                    except Exception as e:
                        print("Unexpected error: {}".format(e))
                        outputs.decideWhatToDo()
                    print("Delete customer {}, address {}".format(customerInfo[0],customerInfo[1]))
                    confirmDelete = input("(y/n): ")

                if confirmDelete.lower() == "y" or (confirm==False and confirmDelete==None):
                        print(customerIds[i][0])
                        whereClause = "customerId=?"
                        statement = "DELETE FROM customers WHERE " + whereClause
                        print(statement)
                        conn.execute(
                                statement,
                                (str(customerIds[i][0]),)
                        )
                        conn.commit()
                else:
                        print("Booking not deleted")
                return 1
    except sqlite3.Error as e:
        raise sqlite3.Error(e)
