import os
import time
import sqlite3 as lite
from slackclient import SlackClient


BOT_NAME = 'umbot'

SQLITE_DATABASE = r'C:\Users\gigatropolis\Documents\GitHub\build\src\Data\database2.sqlite'

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

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
        response = handle_explain(command, channel)
        
    if command.startswith("list".lower()):
        response = handle_list(command, channel)
    
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

def GetHelp():
    return """
Current supported commands are 'help', 'list', and 'explain'.
    
    *help*
    *list*      hops|(ferm|fermentables|grains)|yeast|styles
    *explain*   hop|(ferm|fermentables|grains)|yeast|style  <name of ingredient or style to explain>

      *Example:*
        \"umbot help\"
        \"umbot list hops\"
        \"umbot explain hop Cascade\""""

def  handle_explain(command, channel):
    """
        Connects to data source to explain beer related ingredient or recipe 
    """
    response = "Try: \"explain hop hopname\""
    words = command.split(" ")
    print("words: %s" %(words))

    if words[1] == "help":
        return """ Use 'explain to get more detail about a beer ingredient or style.

  Current supported ingredient types or 'hop', 'grain', 'yeast', and 'style'

  Type a command like \"umbot explain hop Centennial\" or "umbot explain grain Vienna\"
  """
    if words[1] == "hop":
        return GetHopExplanation(command.split("hop")[1].strip())

    if words[1] == "grain" or words[1] == "ferm" or words[1] == "fermentable":
       return GetGrainExplanation(command.split(word[1])[1].strip())

    if words[1] == "yeast":
       return GetYeastExplanation(command.split("yeast")[1].strip())

    if words[1] == "style":
       return GetStyleExplanation(command.split("style")[1].strip())

def _getIngredient(query):
     try:
        con = lite.connect(SQLITE_DATABASE)

        cur = con.cursor()
        print(query)    
        cur.execute(query)

        data = cur.fetchone()
        print("data: ", data)

     except:
        data = None
 
     finally:
        if con:
            con.close()

     return data

def _listIngredient(name):
    try:
        con = lite.connect(SQLITE_DATABASE)

        cur = con.cursor()
        cur.execute("SELECT DISTINCT name FROM %s" %(name))

        data = cur.fetchall()
        #print("data: ", data)

    except:
        data = None

    finally:
        if con:
            con.close()

    if data:
        response = ", ".join((str(d[0]) for d in data))
    else:
        response = "Could't list %s" % (name)

    return response
 
def ListHops():
    return _listIngredient("hop")

def ListFerms():
    return _listIngredient("fermentable")

def ListYeast():
    return _listIngredient("yeast")

def ListStyles():
    return _listIngredient("style")

def GetHopExplanation(name):
    
    query = "SELECT name, alpha, beta, notes, origin FROM hop where name like '%%%s%%'" % (name)
    data = _getIngredient(query)

    if data:
        response = "Found: _*%s*_\nalpha=%0.1f%%\nbeta=%0.1f%%\nOrigin=%s\nExplanation: %s\n" % (data[0], data[1], data[2], data[4], data[3])
    else:
        response = "No hop information found for hop '%s' try 'list hops' for list of available hops" % (name)

    return response

def GetGrainExplanation(name):

    query = "SELECT name, yield, color, supplier, notes, origin FROM fermentable where name like '%%%s%%'" % (name)
    data = _getIngredient(query)

    if data:
        response = "Found: _*%s*_\nyield=%d\color=%d\nOrigin=%s\nSupplier=%s\nExplanation: %s\n" % (data[0], data[1], data[2], data[5], data[3], data[4])
    else:
        response = "No information found for fermentable '%s' try 'list ferm' for list of available fermentables" % (name)

    return response

    
def GetYeastExplanation(name):

    query = "SELECT name, ytype, form, min_temperature, max_temperature, flocculation, attenuation, notes FROM yeast where name like '%%%s%%'" % (name)
    data = _getIngredient(query)

    if data:
        response = "Found: _*%s*_\ntype=%s\nform=%s\nTemp %d to %d\nflocculation=%s\nattenuation=%d\nExplanation: %s\n" % (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
    else:
        response = "No information found for yeast '%s' try 'list yeast' for list of available yeast" % (name)

    return response

def GetStyleExplanation(name):
    
    query = "SELECT name, s_type, category, category_number, style_letter, og_min, og_max, fg_min, fg_max, ibu_min, ibu_max, color_min, color_max, abv_min, abv_max, notes, profile, ingredients, examples FROM style where name like '%%%s%%'" % (name)
    data = _getIngredient(query)

    if data:
        response = """ Found Style:  _*%s*_
    
    *type:* %s    *cat:* %s (%s%s)
        
    *OG:* %0.4f - %0.4f     *FG:* %0.4f - %0.4f
    
    *IBU:* %d - %d    *Color (SRM):* %d - %d
    
    *ABV:* %0.1f - %0.1f
    
    *Notes:*
    
       %s
       
    *Profile:*
    
       %s
       
    *Ingredients:*
    
       %s
       
    *Examples:*
    
       %s   """ % (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8],
        data[9], data[10], data[11], data[12], data[13], data[14], data[15], data[16], data[17], data[18])
    else:
        response = "No style information found for style '%s' try 'list styles' for list of available styles" % (name)

    return response
    
def  handle_list(command, channel):
    """
        Connects to data source to list beer related ingredient or recipe 
    """
    response = "Try: \"list hops\""
    words = command.split(" ")
    print("words: %s" %(words))

    if words[1] == "help":
        return """ Use 'list to get names of beer ingredients

  Current supported ingredients are 'hops', 'grains', and 'yeast'

  Type a command like \"umbot list hops\" or "umbot list yeast\"
  """
    if words[1] == "hops":
        response =  ListHops()

    if words[1] == "ferm" or words[1] == "grains" or words[1] == "fermentables":
        response =  ListFerms()

    if words[1] == "yeast":
        response =  ListYeast()

    if words[1] == "styles":
        response =  ListStyles()

    return response

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

