import os
import time
from slackclient import SlackClient
import brewdata
import um_meetup
import um_untappd
import um_beerdb
import calcbeer

BOT_NAME = 'umbot'

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def GetHelp():
    return """
Current supported commands are 'help', 'list', 'explain', 'calc', and 'source'.
    
    *help*
    *list*      events|beer|brewery|hops|(ferm|fermentables|grains)|yeast|styles|recipes   [long]
    *explain*   hop|(ferm|fermentables|grains)|yeast|style|recipe  <name of ingredient, style, or recipe to explain>
    *calc*      OgToBrix|BrixToOg|RefactoToFg
    *source*    Show URL to umbot Source code on GitHub


      *Example:*
        "@umbot help"   -                    Show this message
        "@umbot list events"   -             List the next five upcoming events on meetup.com

        "@umbot list beer [beer name]"   -   List beers found on untappd.com. Leave beer name blank will search "umunhum brewing"

        "@umbot list brewery" or "list bry"  - List people on untappd.com drinking beer from Umunhum brewing

        "@umbot list hops"   -               List of all hops in database
        "@umbot list styles [long]"   -      List of beer styles in database
        "@umbot explain hop Cascade"   -     This will give a detaled explanation of hop Cascade
     """


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    exitRequested = False

    response = ""
    words = command.split(" ")
    
    if words[0].lower() == "help" or words[0].lower() == "?" or words[0].lower() == "h":
        response = GetHelp()
        
    elif words[0].lower() == "explain" or words[0].lower() == "ex":
        response = brewdata.handle_explain(command, channel)
        
    elif words[0].lower() == "list" or words[0].lower() == "ls":
        response = handle_list(command, channel)
        
    elif words[0].lower() == "update":
        response = um_beerdb.HandleUpdate(command, channel)
        
    elif words[0].lower() == "calc":
        response = calcbeer.HandleCalc(command, channel)
        
    elif command.lower() == "die umbot die":
        exitRequested = True
        response = "@umbot dead from neglect"
        
    elif command.lower() == "source":
        exitRequested = True
        response = "https://github.com/gigatropolis/umbot"
        
    if not response:
        response = GetHelp()

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

    return exitRequested

def handle_list(command, channel):
    """
        Find what is being listed and call appropriate handler 
    """
    response = ""
    words = command.split(" ")
    help = """ Use 'list to get names of beer ingredients and meetup events

  Current beer ingredients are 'hops', 'grains', and 'yeast'

  list events will give the next five upcoming meetups

  Type a command like \"@umbot list hops\"  or "@umbot list yeast\"
  """

    print("words: %s" %(words))
    if (len(words) < 2) or words[1].lower() == "help":
        return help
    if words[1].lower() == 'upcomming' or words[1].lower() == 'events':
        return um_meetup.handle_list(command, channel)

    if words[1].lower() == 'beer':
        return um_untappd.SearchBeer("umunhum brewing")

    if words[1].lower() == 'brewery' or words[1].lower() == 'bry':
        return um_untappd.ListBreweryActivity(206691)

    if not response:
        response = brewdata.handle_list(command, channel)
    
    if not response:
        return help

    return response

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:

            if output and 'text' in output:
                print(output)

            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip(), \
                       output['channel']
    return None, None

    
if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():

        print("Updating Hop Database...")
        print(um_beerdb.UpdateHops())

        print("umbot connected and running!")

        exitRequested = False

        while not exitRequested:
            
            command, channel = parse_slack_output(slack_client.rtm_read())

            if command and channel:
                exitRequested = handle_command(command, channel)

            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")

