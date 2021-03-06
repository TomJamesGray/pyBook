import re,sqlite3
from app.db import dbConnection
from app.helpers.getConfig import getConfPart
def getArgsBy(argString,regExp,strip=True):
    # Use regexp to split arguments into list
    if strip:
        argString = argString.strip()
    args = re.split(regExp,argString)

    return args

def makeArgsDict(args,searchableArgs):
    #Function to generate an dictinary with the arguments and values
    #It will go through the args and make sure they're searcable as well
    #Most likely to be used with functions that query the db
    argsDict = {}
    for i in range(0,len(args),2):
        if args[i] in searchableArgs:
            argsDict[args[i]] = args[i+1]
        else:
            raise ValueError("Invalid argument: {}".format(args[i]))
    return argsDict
def getCustomerId(name,address=None,limit=2):
    conn=dbConnection.connect()
    if address == None:
        try:
            # count(*) used as sqlite doesn't know rows returned without iterating
            # over it first
            cursor = conn.execute(
                "SELECT count(*) FROM customers WHERE name=? LIMIT ?",
                (name,limit)
            )
            rowsReturned = cursor.fetchone()[0]
            if rowsReturned > 0:
            # Get actual customer id
                cursor = conn.execute(
                    "SELECT customerId FROM customers WHERE name=? LIMIT ?",
                    (name,limit)
                )
                return cursor.fetchall()
            else:
                raise LookupError("No customer found")
        except sqlite3.Error as e:
            raise sqlite3.Error(e)
        finally:
            conn.close()
    elif address != None:
        try:
            # Basically the same as above just with an address, same checks 
            # But less likely to happen as it's v. unlikely two customers
            # will have the same name and address
            cursor = conn.execute(
                "SELECT count(*) FROM customers WHERE name=? AND address=? LIMIT ?",
                (name,address,limit)
            )
            rowsReturned = cursor.fetchone()[0]
            if rowsReturned > 0:
                # Get actual customer id
                # cursor = dbConnection.connect('bookings.db')
                cursor = conn.execute(
                    "SELECT customerId FROM  customers WHERE name=? AND address=? LIMIT ?",
                    (name,address,limit)
                )
                return cursor.fetchall()
            else:
                raise LookupError("No customer found")
        except sqlite3.Error as e:
            raise sqlite3.Error(e)
        finally:
            conn.close()
def getCustomerInfoFromId(customerId,attributesWanted=['name','address']):
    # Get a customers information, by default name and address
    # From their id, the attryibutes wanted are passed in through
    # a list
    
    statement = "SELECT "
    if len(attributesWanted)==1:
        statement += attributesWanted[0]
    elif len(attributesWanted)==0:
        raise ValueError("No attributes to select")
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
                raise ValueError("Unknown attribute required")
            i += 1
    # No need to check if customer is unique as id is used
    # And is marked so in the db
    statement += " FROM customers WHERE customerId=?"
    conn = dbConnection.connect()
    try:
        cursor = conn.execute(
            statement,
            (customerId,)
        )
        customerInfo = cursor.fetchone()
        if customerInfo == [''] or customerInfo == None:
            raise LookupError("No matching customer found")
        else:
            return customerInfo
    except sqlite3.Error as e:
        print("Error: {}".format(e))
