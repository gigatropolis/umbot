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


| Name | Amount | time | Alpha | Use | IBU |
| -------------------- | ---------- | ---------- | ---------- | --------------- | ---------- |
Fuggles | 0.50oz | 7 days | 5.1% | Dry Hop | 0.0
Goldings, East Kent | 0.50oz | 7 days | 6.2% | Dry Hop | 0.0
Goldings, East Kent | 0.75oz | 15 min | 5.3% | Boil | 9.5
Fuggles | 0.50oz | 5 min | 5.1% | Boil | 3.8
Fuggles | 0.50oz | 1 min | 5.1% | Boil | 3.8
Goldings, East Kent | 0.50oz | 1 min | 5.3% | Boil | 3.9
