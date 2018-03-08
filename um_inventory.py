import os
import time
import sqlite3 as lite
import calcbeer as beer
import um_beerdb as beerdb

SQLITE_DATABASE = r'./data/inventory/inventory.sqlite'

def  HandleInventory(command, channel):
    """
        List inventory ingredients
    """
    response = ""
    words = command.split(" ")
    print("words: %s" %(words))
    help = """
Inventory commands: help, list, delete, add, export, import

*list* - list sales

*add* - Addes a new sales transaction to inventory list:

    Message sent in format:  @umbot inventory add <amount> <Type> of <name> to <location> [from <name>]

    Type is 'sixtel', 'case', or 'half'

    Beer Name is one of:
    SAS    Stout as a service
    HS     Hismen Sii
    IPO    IPO IPA

    Example:

        @umbot inv add 3 Sixtle of SAS to Taplands from David

*delete* - delete an existing sales record

*export* - Export data to specified format

    EXCEL   Windows excel spreadsheet
    COMMA   Comma seperated list
     """
    cmd = words[1].lower()

    if cmd == "help" or cmd == "?":
        return help

    if cmd == "list":
        #return GetHopExplanation(command.split(words[1])[1].strip())
        return ListInventory()

    if cmd == "delete" or cmd == "del":
       return GetGrainExplanation(command.split(words[1])[1].strip())

    if cmd == "add":
       return AddSalesInventory(command)

    if cmd == "sales":
           return ListUserSales()

    if cmd == "export":
       return ExportSalesInventory(command.split(words[1])[1].strip())

    if cmd == "import":
        return GetRecipeExplanation(command.split(words[1])[1].strip())

    return help

def _GetQuery(query, *records):
    print("Query: ", query)
    print("*records", records)
    try:
        con = lite.connect(SQLITE_DATABASE)
        cur = con.cursor()
        if records:
            cur.execute(query, records)
        else:
            cur.execute(query)

        data = cur.fetchall()
        print("_GetQuery::data: ", data)
    except:
        data = None
    finally:
        if con:
            con.close()

    return data

def _GetSalesId(name):
    data = _GetQuery("SELECT ID FROM SalesPerson WHERE Name = ?", name) 
    if not data:
        print("_GetSalesId::No data")
        return 0

    salesId = int(data[0][0])
    #print("Sales id = ", salesId)    
    return salesId

def ListInventory(name = '', type = '', amount = ''):
    
    query = "SELECT SalesPerson.Name, SalesPerson.Area, Beer.Name, Beer.Type, Beer.Location, Beer.Amount FROM SalesPerson, Beer WHERE SalesPerson.ID = Beer.Sales_ID"
    data = _GetQuery(query)

    if data:
        response = ""
        for inv in data:
            (salesName, salesArea, beerName, beerType, beerLocation, beerAmount) = inv
            response += "%s %s %s %s %s %d\n" % (salesName, salesArea, beerName, beerType, beerLocation, beerAmount)
    else:
        response = "Could't list inventory"

    return response

def ListUserSales(name = ''):
    
    query = "SELECT SalesPerson.Name, Beer.Type, Beer.Location, SUM(Beer.Amount) AS 'Amount' FROM SalesPerson, Beer WHERE SalesPerson.ID = Beer.Sales_ID GROUP BY SalesPerson.Name, Beer.Type, Beer.Location ORDER BY Beer.Location, Amount DESC"
    data = _GetQuery(query)

    if data:
        response = ""
        for sales in data:
            (salesName, beerType, beerLocation, beerAmount) = sales
            response += "%s %s %s %d\n" % (salesName, beerType, beerLocation, beerAmount)
    else:
        response = "Couldn't list inventory"

    return response

def AddSalesInventory(command):

    response = ""
    words = command.split(" ")
    print("words: %s" %(words))
    help = """Add Sales transaction to inventory list:
    
    Message sent in format:  @umbot inventory add <amount> <Type> of <name> to <location> [from <name>]
    
     Type is 'sixtel', 'case', or 'half'

     Beer Name is one of:
        SAS    Stout as a service
        HS     Hismen Sii
        IPO    IPO IPA
     
         Example:

        @umbot inv add 3 Sixtle of SAS to Taplands from David

"""
    if len(words) < 8:
        return "Not enough words\n\n%s" % (help)

    if words[6].lower() != "to":
        return "Wrong format\n\n%s" % (help)

    print("len(words) = ", len(words))

    if len(words) > 8 and words[8] == "from":
        record = (_GetSalesId(words[9]), words[5], words[3], words[7], int(words[2]))
        query = "INSERT INTO Beer (Sales_ID, Name, Type, Location, Amount) VALUES (?,?,?,?,?)"
    else:
        record = (words[5], words[3], words[7], int(words[2]))
        query = "INSERT INTO Beer (Name, Type, Location, Amount) VALUES (?,?,?,?)"
       
    try:
        con = lite.connect(SQLITE_DATABASE)
        cur = con.cursor()
        cur.execute(query, record)

        con.commit()
        #print("data: ", data)
    except:
        raise #return "Couldn't add sales record to database\n\n%s" % (help)
    finally:
        if con:
            con.close()

    return "added sales record to database"
    
 
