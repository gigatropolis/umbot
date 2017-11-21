import os
import time
import sqlite3 as lite
import calcbeer as beer
import um_beerdb as beerdb

SQLITE_DATABASE = r'./brewdata.sqlite'
#SQLITE_DATABASE = r'./database.sqlite'

def  handle_list(command, channel):
    """
        Connects to data source to list beer related ingredient or recipe 
    """
    print("in list()")

    help = """ Use 'list to get names of beer ingredients

  Current supported ingredients are 'hops', 'grains', and 'yeast'

  Type a command like \"umbot list hops\" or "umbot list yeast\"
  """
    response = ""
    words = command.split(" ")
    print("words: %s" %(words))

    if words[1] == "help":
        return help

    if words[1] == "hops":
        #response =  ListHops()
        response =  beerdb.ListHops()

    if words[1] == "ferm" or words[1] == "grains" or words[1] == "fermentables":
        response =  ListFerms()

    if words[1] == "yeast":
        response =  ListYeast()

    if words[1] == "styles":
        if len(words) <= 2:
            response =  ListStyles()
        else:
            if words[2].lower() == "long":
                response = ListStylesLong(command)

    if words[1] == "recipes" or words[1] == "rec":
        print("In Recipe")
        response =  ListRecipes()

    if not response:
        print("no response")
        response = help

    return response

def  handle_explain(command, channel):
    """
        Connects to data source to explain beer related ingredient or recipe 
    """
    response = ""
    words = command.split(" ")
    print("words: %s" %(words))
    help = """ Use 'explain to get more detail about a beer ingredient or style.

  Current supported ingredient types or 'hop', 'grain', 'yeast', 'recipe', and 'style'

  Type a command like \"@umbot explain hop Centennial\" or "@umbot explain grain Vienna\"
  """
    it = words[1].lower()

    if it == "help" or it == "?":
        return help

    if it == "hop":
        #return GetHopExplanation(command.split(words[1])[1].strip())
        return beerdb.GetHopExplanation(command.split(words[1])[1].strip())

    if it == "grain" or it == "ferm" or it == "fermentable":
       return GetGrainExplanation(command.split(words[1])[1].strip())

    if it == "yeast":
       return GetYeastExplanation(command.split(words[1])[1].strip())

    if it == "style":
       return GetStyleExplanation(command.split(words[1])[1].strip())

    if it == "recipe" or it == "rec":
        return GetRecipeExplanation(command.split(words[1])[1].strip())

    return help

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

def _GetAllRecords(query):
     try:
        con = lite.connect(SQLITE_DATABASE)

        cur = con.cursor()
        print(query)    
        cur.execute(query)

        data = cur.fetchall()
        print("data: ", data)

     except:
        data = None
 
     finally:
        if con:
            con.close()

     return data
 
def ListHops():
    return _listIngredient("hop")

def ListFerms():
    return _listIngredient("fermentable")

def ListYeast():
    return _listIngredient("yeast")

def ListStyles():
    return _listIngredient("style")

def ListRecipes():
    response = "Unable to get Recipe list from database"
    con = None
    query = "SELECT DISTINCT recipe.id, recipe.name, style.name, recipe.og, recipe.fg FROM recipe, style WHERE recipe.style_id = style.id"
    try:
        print("trying..")
        con = lite.connect(SQLITE_DATABASE)
        cur = con.cursor()
        cur.execute(query)

        recipes = cur.fetchall()
        print("recipes: ", recipes)

    except:
        recipes = None
    finally:
        if con:
            con.close()

    if not recipes:
        return response

    response = ""

    for recipe in recipes:
        response += "(%d) %s (%s) OG: %0.3f FG: %0.3f\n" % (recipe[0], recipe[1], recipe[2], recipe[3], recipe[4])
    print("in end")
    return response
 
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
        response = "Found: _*%s*_\nyield=%d\ncolor=%d\nOrigin=%s\nSupplier=%s\nExplanation: %s\n" % (data[0], data[1], data[2], data[5], data[3], data[4])
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

def ListStylesLong(command):
    query = "SELECT DISTINCT name, s_type, category, category_number, style_letter, og_min, og_max, fg_min, fg_max, ibu_min, ibu_max, color_min, color_max, abv_min, abv_max FROM style"
    styles = _GetAllRecords(query)
 
    if not styles:
        return "No styles found listing with long option"

    response = ""
    for style in styles:
        name, s_type, category, category_number, style_letter, og_min, og_max, fg_min, fg_max, ibu_min, ibu_max, color_min, color_max, abv_min, abv_max = style
        response += "%s%s %s - %s:  %s:  OG: %0.3f - %0.3f  FG: %0.3f - %0.3f IBU: %d - %d  SRM: %d - %d  %0.1f%% - %0.1f%%\n" % (category_number, style_letter, s_type, category,
                      name, og_min, og_max, fg_min, fg_max, ibu_min, ibu_max, color_min, color_max, abv_min, abv_max)

    return response

def GetStyleExplanation(name):
    
    query = "SELECT name, s_type, category, category_number, style_letter, og_min, og_max, fg_min, fg_max, ibu_min, ibu_max, color_min, color_max, abv_min, abv_max, notes, profile, ingredients, examples FROM style where name like '%%%s%%'" % (name)
    data = _getIngredient(query)
    name, s_type, category, category_number, style_letter, og_min, og_max, fg_min, fg_max, ibu_min, ibu_max, color_min, color_max, abv_min, abv_max, notes, profile, ingredients, examples = data

    if data:
        response = """ Found Style:  _*%s*_
    
    *type:* %s    *cat:* %s (%s%s)
        
    *OG:* %0.3f - %0.3f     *FG:* %0.3f - %0.3f
    
    *IBU:* %d - %d    *Color (SRM):* %d - %d
    
    *ABV:* %0.1f - %0.1f
    
    *Notes:*
    
       %s
       
    *Profile:*
    
       %s
       
    *Ingredients:*
    
       %s
       
    *Examples:*
    
       %s   """ % (name, s_type, category, category_number, style_letter, og_min, og_max, fg_min, fg_max, ibu_min, ibu_max, color_min, color_max,
                   abv_min, abv_max, notes, profile, ingredients, examples)
    else:
        response = "No style information found for style '%s' try 'list styles' for list of available styles" % (name)

    return response

def GetRecipeExplanation(name):
    
    query = "SELECT id from recipe WHERE name like '%%%s%%'" % (name)
    recID = _getIngredient(query)

    if not recID:
        return "Can't find recipe name '%s'" % (name)
    
    recID = recID[0]
   
    query = "SELECT hop.name, hop.amount, hop.time, hop.alpha, hop.use FROM hop, hop_in_recipe WHERE hop_in_recipe.recipe_id=%d AND hop.id = hop_in_recipe.hop_id" % (recID)
    hops = _GetAllRecords(query)

    query = "SELECT fermentable.name, fermentable.amount, fermentable.yield, fermentable.color FROM fermentable, fermentable_in_recipe WHERE fermentable_in_recipe.recipe_id = %d AND fermentable.id =  fermentable_in_recipe.fermentable_id" % (recID)
    ferms = _GetAllRecords(query)

    query = "SELECT recipe.name, style.name, recipe.og, recipe.fg, recipe.batch_size, recipe.boil_size, recipe.boil_time, recipe.efficiency, recipe.notes, recipe.taste_notes FROM recipe, style WHERE recipe.style_id = style.id AND recipe.id = %d" % (recID)
    data = _getIngredient(query)

    if not data:
        return "No recipe information found for recipe '%s'" % (name)
    
    name, style, og, fg, batch_size, boil_size, boil_time, efficiency, notes, taste_notes = data
    batch_size = beer.KilToGal(batch_size)
    boil_size = beer.KilToGal(boil_size)
    ibuTotal, SRM, abv = 0, 0.0, beer.ABV(og, fg)

    if hops:
        #strHops = "| Name                       | Amount | Yield | Color |\n"
        #strHops += "|----------------------------|--------|-------|-------|---|\n"
 
        nLen = 0
        for hop in hops:
            actLen = len(hop[0])
            if actLen > nLen:
                nLen = actLen

        nLen += 1
        strHops = "%s %s %10s %10s %10s %15s %10s\n\n" % ("_" * (nLen - 4), "Name", "Amount", "time", "Alpha", "Use", "IBU") 

        for hop in hops:
            hopName, hopAmount, hopTime, hopAlpha, hopUse = hop
            hopAmount = beer.KilToOz(hopAmount)
            if hopUse.lower() == "dry hop":
                hopTime = hopTime/60/24

            bTime = hopTime
            if hopUse.lower() == "first wort" or hopUse.lower() == "wort" or hopUse.lower() == "mash":
                bTime = 20

            if hopUse.lower() != "dry hop":
                ibu = beer.getIBU(batch_size, bTime, hopAmount, hopAlpha, og, boil_size)
                ibuTotal += ibu
            else:
                ibu = 0
            
            strHops += "%s %s %10.2foz %10d%s %10.1f%% %15s %10.1f\n" % ("_" * (nLen - len(hopName)), hopName, hopAmount, hopTime,
                                                    ("days" if hopUse.lower() == "dry hop" else "min"), 
                                                    hopAlpha, hopUse, ibu)
            #strHops += "| %s | %0.2foz | %dmin | %0.1f%%|\n" % (hopName, hopAmount, hopTime, hopAlpha)

    else:
        strHops = ""

    if ferms:
        strFerms = "%40s %10s %10s %10s\n\n" % ("Name", "Amount", "Yield", "Color")
        mcu = 0.0
        for ferm in ferms:
            fermName, fermAmount, fermYield, fermColor = ferm
            fermAmount = beer.KilToLb(fermAmount)

            mcu += fermAmount * fermColor / batch_size

            strFerms += "%40s %10.2flb %10.1f %10.1f\n" % (fermName, fermAmount, fermYield, fermColor)

        SRM = beer.McuToSrm(mcu)
    else:
        strFerms = ""

    response = """Found Recipe:  _*%s*_    Style: %s
    
    *OG:* %0.3f     *FG:* %0.3f     *IBU:* %d    *Color (SRM):* %0.1f
    
    *ABV:* %0.1f%%
    
    *Batch Size:*  %0.2f gal     *Boil Size:*  %0.2f gal     *Boil Time:*  %d min     *Mash efficiency:*  %d%%

    *Hops:*
    
%s

    *Fermentables:*

%s

    *Brew Notes:*
    
       %s
       
    *Tasting Notes:*
    
       %s 
""" % (name, style, og, fg, ibuTotal, SRM, abv, batch_size, boil_size, boil_time, efficiency,
        strHops, strFerms, notes, taste_notes)
    
    return response

