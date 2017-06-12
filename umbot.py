import os
import time
from slackclient import SlackClient
import brewdata
import um_meetup
import um_untappd

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
Current supported commands are 'help', 'list', and 'explain'.
    
    *help*
    *list*      events|hops|(ferm|fermentables|grains)|yeast|styles|recipes   [long]
    *explain*   hop|(ferm|fermentables|grains)|yeast|style|recipe  <name of ingredient, style, or recipe to explain>

      *Example:*
        "@umbot help"
        "@umbot list events"   This will list the next five upcoming events on meetup
        "@umbot list hops"
        "@umbot list styles long"
        "@umbot explain hop Cascade"
     """


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = ""
    words = command.split(" ")
    
    if words[0].lower() == "help" or words[0].lower() == "?" or words[0].lower() == "h":
        response = GetHelp()

    elif words[0].lower() == "explain" or words[0].lower() == "ex":
        response = brewdata.handle_explain(command, channel)
        
    if words[0].lower() == "list" or words[0].lower() == "ls":
        response = handle_list(command, channel)
    
    if not response:
        response = GetHelp()

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

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

    if (len(words) < 2) or words[1].lower() == "help":
        return help
    if words[1].lower() == 'upcomming' or words[1].lower() == 'events':
        return um_meetup.handle_list(command, channel)

    if words[1].lower() == 'beer':
        return um_untappd.SearchBeer("umunhum brewing")

    if words[1].lower() == 'brewery' or words[1].lower() == 'bry':
        return um_untappd.ListBreweryActivity(206691)

    if not response:
        return help
    
    return brewdata.handle_list(command, channel)

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
        print("umbot connected and running!")
        while True:
            
            command, channel = parse_slack_output(slack_client.rtm_read())

            if command and channel:
                handle_command(command, channel)

            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")

