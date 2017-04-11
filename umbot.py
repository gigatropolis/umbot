import os
import time
from slackclient import SlackClient
import brewdata


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
    *list*      hops|(ferm|fermentables|grains)|yeast|styles|recipes   [long]
    *explain*   hop|(ferm|fermentables|grains)|yeast|style|recipe  <name of ingredient, style, or recipe to explain>

      *Example:*
        \"@umbot help\"
        \"@umbot list hops\"
        \"@umbot list styles long\"
        \"@umbot explain hop Cascade\""""


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "ask umbot for help"
    words = command.split(" ")
    if command.startswith("help".lower()):
        response = GetHelp()

    elif command.startswith("explain".lower()):
        response = brewdata.handle_explain(command, channel)
        
    if command.startswith("list".lower()):
        response = brewdata.handle_list(command, channel)
    
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

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
                print("channel=%s  output=%s" % (output['channel'], output['text']))

            if output and 'text' in output and AT_BOT in output['text']:
                print(output)
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

