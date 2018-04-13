# umbot
## Slackbot for Umunhum Brewing 

  **help**

  **Example**
---
      "@umbot help"   -        show this message
---

  **list**      events|beer|brewery|hops|(ferm|fermentables|grains)|yeast|styles|recipes   [long]

  **Example:**

----
      "@umbot list hops"   -               List of all hops in database
      "@umbot list styles long"   -      List of beer styles in database. "long" adds details not just names
      "@umbot list events"   -             List the next five upcoming events on meetup.com

      "@umbot list beer [beer name]"   -   List beers found on untappd.com. Leave beer name blank will search "umunhum brewing"

      "@umbot list brewery" or "list bry"  - List people on untappd.com drinking beer from Umunhum brewing

---

  **explain**   hop|(ferm|fermentables|grains)|yeast|style|recipe  <name of ingredient, style, or recipe to explain>

  **Example:**

---
      "@umbot explain hop Cascade"   -     This will give a detaled explanation of hop Cascade
      "@umbot ex ferm Vienna         -     Details on grain of type Vienna. "ex" abbv for explanation
---

  **inventory** add|delete|list|expot|import

  **list** - list sales

  **add** - Addes a new sales transaction to inventory list:

          Add format:  @umbot inventory add <amount> <type> of <name> to <location> [from <first name>]

          <type> is 'sixtel', 'case', or 'half'

          <name> is code name for beer:
          SAS    Stout as a service
          HS     Hismen Sii
          IPO    IPO IPA

  **Example:**

---
            @umbot inventory add 3 Sixtle of SAS to Taplands from David
            @umbot inv add 6 case of IPO to Loft from Juelles
---

  **delete** - (Not Supported Yet) delete an existing sales record

  **export** - (Not Supported Yet) Export data to specified format

          EXCEL   Windows excel spreadsheet
          COMMA   Comma seperated list

---
  **calc**      OgToBrix|BrixToOg|RefactoToFg

      RefactoToFg - takes original Brix and Final Brix measured from refractometer and returns the actual brix
        RefactoToFg <brix Og> <brix Fg>


  **Example:**

---
      "@umbot calc ogtobrix 1.089"   (returns "Brix is 21.35")
      "@umbot calc BrixToOg 21.35"   (Returns "Original Gravity is 1.0890")
      "@umbot calc RefractoToFg 19.3 11.3"  (Returns "Final gravity is 1.0228")

---    

  **source**    Show URL to umbot Source code on GitHub

---
    @umbot source

    >> https://github.com/gigatropolis/umbot
---

### TODO:

Here are some ideas:
- [ ] @umbot where to buy - gives a list of our customers or a link to a map of them
- [x] @umbot events - gives a list of the next 5 events from our meetup channel 
- [ ] @umbot board - lists the slack names of the board members suitable for copying and pasting into a slack message
- [ ] @umbot subcommittees - lists the slack channels (like #member-recruiting) that belong to the standing subcommittees.

