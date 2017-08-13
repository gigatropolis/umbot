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
    response = "Try: \"list hops\""
    words = command.split(" ")
    print("words: %s" %(words))

    if words[1].lower() == 'upcoming' or words[1].lower() == 'events':
        events = GetEvents('umunhum', 'upcoming')
        response = ShowEvents(events)

    if response:
        return response

    return "events not found"    

def ListHops():
    response = "Have %d hops in database\n\n" % len(lstHops)
    for hop in lstHops:
        response += "'%s',  " % (hop["name"])
    
    return response

def  handle_Explain(command, channel):
    """
        Connects to data source to list beer related ingredient or recipe 
    """
    response = "Try: \"list hops\""
    words = command.split(" ")
    print("words: %s" %(words))

    if words[1].lower() == 'upcoming' or words[1].lower() == 'events':
        events = GetEvents('umunhum', 'upcoming')
        response = ShowEvents(events)

    if response:
        return response

    return "events not found"    

def SearchBeer(search):
    
    req = _GetRequest("search/beer", q=search,limit='3')
    beer = req.json()   

    if int(beer['meta']['code']) != 200:
       return "ERROR: " % (beer['meta']['error_type'])
    else:
        return beer['response']['beers']['items']

def ListBreweryActivity(breweryID):

    req = _GetRequest("brewery/checkins/%s" % (breweryID),limit='200')
    checkins = req.json()

    if int(checkins['meta']['code']) != 200:
        return "ERROR: %s\n" % (checkins['meta']['error_type'])

#['checkin_id', 'created_at', 'checkin_comment', 'rating_score', 'user', 'beer', 'brewery', 'venue', 'comments', 'toasts', 'media', 'source', 'badges']
 
    if not 'response' in checkins:
        return "No data returned"

    response = ""
    for item in checkins['response']['checkins']['items']:
        venue = "N/A"
        if venue in item:
            venue = item['venue']['venue_name']
        response += """--- %s  "%s"  at  %s
        rate: %d    comments: %s

        location: %s

        """ % (item['user']['user_name'], item['beer']['beer_name'], item['created_at'], item['rating_score'], item['checkin_comment'], venue)

    return response