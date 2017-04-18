import os
import datetime
import meetup.api

# MEETUP Token
MEETUP_TOKEN = os.environ.get("MEETUP_TOKEN")

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

def ShowEvents(events, max = 5):
    response = ""
    count = 1
    print(len(events))
    for event in events:
        #print(event)
        date = datetime.date.fromtimestamp(event['time']/1000).strftime("%B %d %Y")
        response += """*#%d  %s*

        located at %s   *date:*  %s

        RSVP: %d  Maybe: %d   Wait list: %d
 
        Address: %s, %s

       *Description:* %s

       %s

      --------------------------------------------------------------------

        """ % (count, event['name'], event['venue']['name'], date,
               event['yes_rsvp_count'], event['maybe_rsvp_count'], event['waitlist_count'],
               event['venue']['address_1'], event['venue']['city'],
               event['description'], event['event_url'])

        count += 1
        if count > max:
            break

    return response
    
def GetEvents(groupUrl, eventStatus='upcoming'):
    client = meetup.api.Client(MEETUP_TOKEN)
    #try:
    events_info = client.GetEvents(group_urlname=groupUrl, status=eventStatus)
    keys = events_info.__dict__.keys()
    if 'details' in keys:
        print(events_info.details)
        return None

    events = events_info.results
    #print(events)
    #except:
        

    return events




