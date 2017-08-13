import os
import requests


def _GetRequest(name, **kwargs):
    
    url = 'https://api.untappd.com/v4/%s' %(name)
    data = {'client_id' : os.environ.get("UNTAPPD_ID"), 'client_secret' : os.environ.get("UNTAPPD_SECRET"),}
    if kwargs:
        data.update(kwargs)

    return requests.get(url, params=data) 


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