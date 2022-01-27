import os
import opinsuomea_utils as osu
from openpyxl import load_workbook

datafilename = "OpinSuomea - Lause tiedot.xlsx"
#datafilename = "OpinSuomea - Lause tiedot - error test.xlsx"

appfolder = os.path.dirname(__file__)
datafolder = os.path.join(appfolder, "data")
datafile = os.path.join(datafolder, datafilename)


def openfile():
    if os.path.exists(datafile):
         print("Data file '{}' exists.".format(datafile))
    else:
        print("It appears that the datafile does not exist.  Should have been:")
        print(datafile)
        exit()
    try:
        wb = load_workbook(filename = datafile)
        print("Workbook opened")
    except:
        print("Looks like workbook loading failed.")
        exit()
    print("\nHere are all the sheets we saw in the file")
    for sheet in wb:
        print(sheet.title)
    print("\nThis list should include only unit worksheets:")
    for sheet in wb:
        if sheet.title == "Template":
            continue
        if sheet.title == "Usage":
            continue
        if sheet.title == "Verbit":
            verbsheet = sheet
            print(sheet.title)
            continue
        #Everything else should be unit sheets
        unitsheets = []
        unitsheets.append(sheet)

    print("\nSheet info")
    print("Verb sheet:", verbsheet.title)
    print("Unit sheets:")
    for sheet in unitsheets:
        print(sheet.title)

    return wb, verbsheet, unitsheets

def parseverbs(verbsheet):
    verbdict = {}  #Dictionary of verbs - key is infinitive, item is the verb variable type.
    print("\nParsing verbs")

    for row in verbsheet.iter_rows(min_row=2):
        #print(row[0].value, row[1].value)
        currentverbi = osu.verbi()
        currentverbi.infinitive = row[0].value
        currentverbi.englanniksi = row[1].value
        #print("Current verb infinitive is ", currentverbi.infinitive)
        #print("Current verb englanniski is ", currentverbi.englanniksi)
        verbdict[currentverbi.infinitive] = currentverbi
        #print(verbdict[row[0].value], verbdict[row[0].value].infinitive, verbdict[row[0].value].englanniksi)
        #print(verbdict[currentverbi.infinitive].englanniksi)
    #print(verbdict)
    #print("asua returns", verbdict["asua"].englanniksi)
    #print("viedä returns", verbdict["viedä"].englanniksi)
    #for verb in verbdict:
    #    print(verb, "should match", verbdict[verb].englanniksi)
    print("Verb list parsing complete.")
    return verbdict

def parseunits(unitsheets, verbs):
    print("\nStarting unit parsing")
    units = []  #List of units.
    lauset = [] #list of lauset
    errorlist = []
    for unit in unitsheets:
        print("Current unit is:", unit)

        #first get basic info on unit:
        currentunit = osu.unit()
        if unit["A1"].value == "Unit number":
            currentunit.number = unit["B1"].value
        else:
            print("WARNING: No unit number detected")
            errorlist.append("Unit parsing error: No unit number detected for unit {}".format(unit))
        if unit["A2"].value == "Unit name":
            currentunit.name = unit["B2"].value
        else:
            print("WARNING: No unit name detected")
            errorlist.append("Unit parsing error: No unit name detected for unit {}".format(unit))
        if unit["A3"].value == "Unit description":
            currentunit.description = unit["B3"].value
        else:
            print("WARNING: No unit description detected")
            errorlist.append("Unit parsing error: No unit description detected for unit {}".format(unit))
        if unit["A4"].value == "Update date":
            currentunit.update_date = unit["B4"].value
        else:
            print("WARNING: No unit update date detected")
            errorlist.append("Unit parsing error: No unit update date detected for unit {}".format(unit))
        if unit["A5"].value == "Other info":
            currentunit.other_info = unit["B5"].value
        else:
            print("WARNING: No unit other info detected")
            errorlist.append("Unit parsing error: No unit other info detected for unit {}".format(unit))
        units.append(currentunit)
        print("Basic info for the unit imported.")

        print("Starting sentence import.")

        #Pull all sentences from the unit

        count = 0
        for row in unit.iter_rows(min_row=8):
            count += 1
            currentlause = osu.lause()
            #print(row[0].value, row[1].value)
            currentlause.unitid = currentunit.number
            if row[0].value.lower() == "kirjakieli":
                currentlause.kirjakieli = True
            elif row[0].value.lower() == "puhekieli":
                currentlause.kirjakieli = True
            else:
                print("WARNING: ei puhekili ta kirjakieli lausessa")
                errorlist.append("WARNING: ei puhekili ta kirjakieli lausessa for lause {}".format(row[3].value))

            currentlause.verbi_inf = row[1].value
            currentlause.verbi_vastaus = row[2].value
            currentlause.lause = row[3].value
            currentlause.lause_englanniksi = row[4].value

            # check and see if verb in the unit spreadsheet is in the verb dictionary
            try:
                english = verbs[currentlause.verbi_inf].englanniksi
            except:
                print("WARNING: Verb in the spreadsheet is not in the verb dictionary")
                errorlist.append(
                    "Unit parsing ERROR: No verb definition for a verb {} used in sentence: {}, ".format(currentlause.verbi_inf, currentlause.lause))

            lauset.append(currentlause)

        print("Finishing sentence import for that unit. We imported {} sentences for this unit.".format(count))

    print("\nUnit file parsing finished.  Here are all the units we imported:")
    for unit in units:
        print(unit.name)

    print("\nWe imported {} sentences.".format(len(lauset)))
    #print ("Here are the setnences we imported")
    #for lause in lauset:
    #    print(lause.lause, lause.lause_englanniksi)
    return units, lauset, errorlist


def parsefile(wb, verbsheet, unitsheets):
    verbs = parseverbs(verbsheet)
    units, lauset, errorlist = parseunits(unitsheets, verbs)

    if len(errorlist) == 0:
        print("No errors - Yay!")
    else:
        print("Here are errors and warnings from the import:")
        for item in errorlist:
            print(item)
    return verbs, units, lauset, errorlist


if __name__ == "__main__":
    print("Executing this script directly, eh?  Try using opinsuomea.py - this isn't supposed to be run on its own.")