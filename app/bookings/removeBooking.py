import sqlite3
from app.helpers.helpers import getArgsBy,getCustomerInfoFromId,makeArgsDict
from app.helpers.getConfig import getConfPart
from app.db import dbConnection
from app import outputs
# Get arguments from config file to get from which attributes a 
# booking can be removed, then get the arguments provided by the 
# user, confirm the decision, then remove booking with remove()

def removeWizzard(argsString):
    if argsString == '' or not argsString:
        print("No arguments provided")
        outputs.decideWhatToDo()
    args = getArgsBy(argsString,',|=')
    if len(args) % 2 != 0:
        print("Insufficient arguments provided, odd number")
        outputs.decideWhatToDo()
    
    searchableArgs=getArgsBy(getConfPart('removeBy','bookings').strip(),',')
    #makeArgsDict includes LIMIT as an argument so that needs to be removed
    #so it can be used properly
    argsDict = makeArgsDict(args,searchableArgs)
    for i in range(0,len(args),2):
        if args[i].lower() == "limit":
            limit = int(args[i+1])
            #limit is would be in argsDict so remove it
            argsDict.pop('limit',0)
        else:
            limit = 1
    try:
        if remove(argsDict,limit):
            print("Succesfully removed booking")
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
    statement = "SELECT customerId,bookingId FROM bookings WHERE " + whereClause + " LIMIT ?"
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
            raise LookupError("More bookings found than specified limit")
        elif len(customerIds) == 0:
            raise LookupError("No bookings found")
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
                    #TODO - Show the time for the booking as the only time when multiple bookings
                    #matching the same whereClause is when there are multiple bookings from the same customer
                    print("Delete booking for {}, address {}".format(customerInfo[0],customerInfo[1]))
                    confirmDelete = input("(y/n): ")

                if confirmDelete.lower() == "y" or (confirm==False and confrimDelete==None):
                    bookingId = customerIds[i][1]
                    #Update where clause to just use the booking ID which is
                    #unique so only one booking can be deleted from the
                    #statement, which is what is wanted as at confirm
                    #is set to true
                    whereClause = "bookingId=?"
                    statement = "DELETE FROM bookings WHERE " + whereClause
                    print(statement)
                    deleteCursor = conn.execute(
                        statement,
                        (str(bookingId),)
                    )
                    conn.commit()
                else:
                    print("Booking not deleted")
        return 1
    except sqlite3.Error as e:
        raise sqlite3.Error(e)

