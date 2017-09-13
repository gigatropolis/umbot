import os
import requests
import pickle

lstHops = []

def _GetRequest(name, **kwargs):
    
    url = 'https://api.brewerydb.com/v2/%s' % (name)
    data = {'key' : os.environ.get("BEER_DB_KEY"),}
    if kwargs:
        data.update(kwargs)

    return requests.get(url, params=data) 

def HandleUpdate(command, channel):
    """
        Update from beerdb 
    """
    help = "Try: \"update hops\""
    words = command.split(" ")
    print("words: %s" %(words))

    if words[1].lower() == 'hops':
        response = UpdateHops(True)

    if not response:
        response = help

    return response   
   
def UpdateHops(renew = False):
    """ 
    Grap hops list from beerdb.com and keep in a list
    """
    global lstHops

    if not renew:
        try:
            with open('hops.pickle', 'rb') as handle:
                hops = pickle.load(handle)
                lstHops = hops
                return "Got hops data from file hops.pickle"
        except:
            pass

    req = _GetRequest("hops")
    hops = req.json()
    #print(hops)
    if not "numberOfPages" in hops:
        return ""

    numPages = hops["numberOfPages"]
    lstHops = hops["data"]
    for pageNum in range(2,numPages+1):
        reqPage = _GetRequest("hops", p=pageNum)
        page = reqPage.json()
        if not "currentPage" in page:
            return ""
        lstHops += page["data"]

    if lstHops:        
        with open('hops.pickle', 'wb') as handle:
            pickle.dump(lstHops, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return "Updated Hop List in memory from beerdb.com"

def FindHopsByName(name):
    global lstHops
    hops = []
    for hop in lstHops:
        if hop["name"].lower().find(name.lower()) >= 0:
            hops.append(hop)

    return hops
        
def GetHopExplanation(name):
    " Explain hop passed in by name"
    response = ""

    hops = FindHopsByName(name)
    if not hops:
        return "No hops found searching name '%s'" % (name)

    response = "Found %d matches for name '%s':" % (len(hops), name)
    print(hops)
    for hop in hops:
        description = "None"
        if "description" in hop:
            description = hop["description"]

        response += "\n\n   name: %s  %s\n" %(hop["name"], ("\nDescription: %s" % (description) if description != "None" else "\nDescription: N/A"))

    print(response)
    return response      

def  handle_list(command, channel):
    """
        Connects to data source to list beer related ingredient or recipe 
    """
    help = "Try: \"list hops\""
    words = command.split(" ")
    print("words: %s" %(words))

    if words[1].lower() == 'upcoming' or words[1].lower() == 'events':
        events = GetEvents('umunhum', 'upcoming')
        response = ShowEvents(events)

    if response:
        response = help

    return response    

def ListHops():
    response = "Have %d hops in database\n\n" % len(lstHops)
    for hop in lstHops:
        response += "'%s',  " % (hop["name"])
    
    return response
