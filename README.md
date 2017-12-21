# umbot
Slackbot for Umunhum Brewing 

  

Current supported commands:

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

