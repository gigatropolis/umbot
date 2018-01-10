# umbot
## Slackbot for Umunhum Brewing 

    *help*
    *list*      events|beer|brewery|hops|(ferm|fermentables|grains)|yeast|styles|recipes   [long]
    *explain*   hop|(ferm|fermentables|grains)|yeast|style|recipe  <name of ingredient, style, or recipe to explain>
    *inventory* add|delete|list|expot|import

      *Example:*
        "@umbot help"   -                    Show this message
        "@umbot list events"   -             List the next five upcoming events on meetup.com

        "@umbot list beer [beer name]"   -   List beers found on untappd.com. Leave beer name blank will search "umunhum brewing"

        "@umbot list brewery" or "list bry"  - List people on untappd.com drinking beer from Umunhum brewing

        "@umbot list hops"   -               List of all hops in database
        "@umbot list styles [long]"   -      List of beer styles in database
        "@umbot explain hop Cascade"   -     This will give a detaled explanation of hop Cascade

### TODO:

Here are some ideas:
@umbot where to buy - gives a list of our customers or a link to a map of them
@umbot events - gives a list of the next 5 events from our meetup channel 
@umbot board - lists the slack names of the board members suitable for copying and pasting into a slack message
@umbot subcommittees - lists the slack channels (like #member-recruiting) that belong to the standing subcommittees.

