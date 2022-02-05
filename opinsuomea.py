#    Opin Suomea - a program to help people learn Finnish grammar
#    Copyright (C) 2022 Marc Perkins
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#    Contact Marc at the email address specified in config.printcontactinfo()

import config
import time
import opinsuomea_utils as osu
import file_importer as osfile
import gameplay as gp
import db_creator
import pprint
import random





# Configuration setting, including config file name, are found in config.py
#   To pull config variable value, use config.jsonconfigdata['key']
#   To chagne config variable, call config.setconfigvariable(key, value)




def print_hi():
    config.printsummary()
    config.printcopyright()
    print("""\n         This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
         without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
         See the GNU General Public License for more details.
         This is free software, and you are welcome to redistribute it
         under certain conditions; type `c' for details.""")
    print("")
    print("Welcome to Opin Suomea - an app to help learn Finnish grammar.")
    print("Created by Marc Perkins")




def print_notes():
    print("Currently this is a pre-release; I hope it is helpful, but nothing is guaranteed.")
    print("Version: ", config.version)
    return

def wipe_and_reload_db_from_file():
    wb, verbsheet, unitsheets = osfile.openfile()
    verblist, unitlist, lauselist, errorlist = osfile.parsefile(wb, verbsheet, unitsheets)
    wasdbwiped = db_creator.createnewdb("USEDEFAULTDB", True) #passing fake name to get that function to use the default db selected in preferences
    if wasdbwiped:
        conn, cur = osu.connectdb()
        verblist, unitlist, lauselist, errorlist = osu.populate_dbs(verblist, unitlist, lauselist, errorlist, conn, cur)
        osu.printimporterrorlist(errorlist)
        print("\nAlright, you've got a nice fresh set of databases with new data loaded from the Excel file to use!")
    else:
        #DB wiping was aborted by the user, so skip updating setences.
        print("Databases were left intact - no changes made.")



def update_db_from_file():
    wb, verbsheet, unitsheets = osfile.openfile()
    verblist, unitlist, lauselist, errorlist = osfile.parsefile(wb, verbsheet, unitsheets)
    conn, cur = osu.connectdb()
    verblist, unitlist, lauselist, errorlist = osu.populate_dbs(verblist, unitlist, lauselist, errorlist, conn, cur)
    osu.printimporterrorlist(errorlist)
    print("\nVerbs, Units, and Sentences were updated using the Excel file; your history data should still be intact.")



def preferencesmenu():
    while True:
        print("\n\n                   PREFERENCES MENU\n")
        print("Note: Some sets may be built to require showing of hints or verb in Finnish. YMMV.")
        print("             Configuration Variable                           Current Value")
        print("    1 - change default session length                           ", config.jsonconfigdata['default_session_length'])
        print("    2 - change setting of 'show hint'                           ", config.jsonconfigdata['show_hint'])
        print("    3 - change setting of 'show verb in Finnish'                ", config.jsonconfigdata['show_verbi'])
        print("    4 - change setting of 'show verb's English translation'     ", config.jsonconfigdata['show_verbi_eng'])
        print("    5 - change setting of 'case matters when checking answers'  ", config.jsonconfigdata['check_case'])
        print("    s - Save updated preferences to file (for use in future sessions)")
        choice1 = input("\nType the letter of your selection (or enter to return to main menu): ")
        if choice1.lower() == "1":
            while True:
                numqs = input("How many questions would you like to do in each session? ")
                try:
                    numqsint = int(numqs)
                except:
                    print("Please enter a valid integer greater than 0.")
                    continue
                if numqsint < 1:
                    print("Please enter a valid integer greater than 0.")
                    continue
                break
            config.jsonconfigdata['default_session_length'] = numqsint
            print("Okay - we changed the default session length to:", config.jsonconfigdata['default_session_length'])
        elif choice1.lower() == "2":
            if config.jsonconfigdata['show_hint'] == True: config.jsonconfigdata['show_hint'] = False
            elif config.jsonconfigdata['show_hint'] == False: config.jsonconfigdata['show_hint'] = True
            print("Got it, boss!")
            continue
        elif choice1.lower() == "3":
            if config.jsonconfigdata['show_verbi'] == True: config.jsonconfigdata['show_verbi'] = False
            elif config.jsonconfigdata['show_verbi'] == False: config.jsonconfigdata['show_verbi'] = True
            print("Got it, boss!")
            continue
        elif choice1.lower() == "4":
            if config.jsonconfigdata['show_verbi_eng'] == True: config.jsonconfigdata['show_verbi_eng'] = False
            elif config.jsonconfigdata['show_verbi_eng'] == False: config.jsonconfigdata['show_verbi_eng'] = True
            print("Got it, boss!")
            continue
        elif choice1.lower() == "5":
            if config.jsonconfigdata['check_case'] == True: config.jsonconfigdata['check_case'] = False
            elif config.jsonconfigdata['check_case'] == False: config.jsonconfigdata['check_case'] = True
            print("Got it, boss!")
            continue
        elif choice1.lower() == "s": #save preferences to file.
            config.saveupdatedconfigtofile()
            time.sleep(0.5)
            continue
        elif choice1.lower() == "":
            print("Back to main menu!")
            return()
        else:
            print("Hmm, I didn't quite understand that.  Please try again.")

def databasemenu():
    while True:
        print("\n\n        DATABASE TOOLS MENU\n")
        print("    v - Print list of verbs")
        print("    l - Print list of sentences")
        print("    e - Print list of sentences that have error reports")
        print("    u - Update database with refreshed sentence/unit/verb data from Excel file (leaves history data intact)")
        print("    d - Wipe database and reload verbs, units, and sentences from the Excel file (deletes all history data and creates a brand new database file)")
        choice1 = input("\nType the letter of your selection (or enter to return to main menu): ")

        if choice1.lower() == "v": #list all verbs.
            print("\nHere are all the verbs in our database:")
            verbitlist = osu.pullverbs(conn, cur)
            print("")
            print("Infinitive  -  Englanniksi")
            for verbi in verbitlist:
                if verbi.infinitive == "-": continue
                print(verbi.infinitive, "  -  ", verbi.englanniksi)

            # for verb in verbs:
            #    print(verb, "---", verbs[verb].englanniksi)
        elif choice1.lower() == "l": #list all sentences.  Currently very ugly formatting and sorting.
            print("\nHere are all the sentences")
            lauselist = osu.getlauselist(conn, cur, "not used", True)
            print("")
            print(" ID   - Sentence           -  Answer")
            for lause in lauselist:
                print(lause.humanid, " - ", lause.lause, " - ", lause.vastaus)
        elif choice1.lower() == "e": #Show, and offer option to clear, error reports.
            lauselist = osu.getlauselist(conn, cur, "not used", True, "AND errorflag = true")
            if len(lauselist) == 0:
                print("\nNo errors found in the database.  Yippee!")
                time.sleep(0.5)
            else:
                print("\nHere are all the sentences with error reports")
                print("")
                print(" ID   - Sentence    -  Answer    -   Comments")
                for lause in lauselist:
                    print(lause.humanid, " - ", lause.lause, " - ", lause.vastaus, " - ", lause.lause_comments)
                print("\nSend this list of sentences to your friendly neighborhood developer to fix them")
                print("Or edit them in the spreadsheet (found in the 'data' folder) and then re-import the sentences")
                clearchoice = input("\nDo you want to delete these reports from the database? (i.e., you or someone else fixed them) - y/n")
                if clearchoice.lower() == "y":
                    for lause in lauselist:
                        sqlstring = "UPDATE Lause SET errorflag = false, errortext = null WHERE id = ?"
                        cur.execute(sqlstring, (lause.dbid,))
                        conn.commit()
                    print("OK - all error reports have been cleared from the database.")
                else:
                    print("Leaving error reports intact, boss.  Note that error reports are not cleared when importing - they must be manually cleared via this menu option.")
        elif choice1.lower() == "u": #Update database nondestructively from Excel file, leaving gameplay data intact.
            update_db_from_file()
        elif choice1.lower() == "d": #Update database destructively, wiping database clean before re-importing from Excel file.
            wipe_and_reload_db_from_file()
        elif choice1.lower() == "":
            print("Back to main menu!")
            return()
        else:
            print("Hmm, I didn't quite understand that.  Please try again.")

def displaymainmenu():
    print("""\n      MAIN MENU
    1 - Play game
    p - Preferences and display options
    d - Database tools
    c - Copyright and license info
    q - Quit""")

def mainmenu(conn, cur):
    while True:
        displaymainmenu()
        choice1 = input("Type the letter of your choice: ")
        if choice1 == "1":
            gp.startgame(conn, cur)
        elif choice1.lower() == "p":
            preferencesmenu()
        elif choice1.lower() == "d":
            databasemenu()
        elif choice1.lower() == "q":
            print("Thanks for using the app!  Hope it was helpful! Onnea!")
            config.printcontactinfo()
            exit()
        elif choice1.lower() == "c":
            config.printcopyrightandlicensestatement()
        else:
            print("Hmm, I didn't quite understand that.  Please try again.")



#Main portion
if __name__ == '__main__':
    conn, cur = osu.connectdb()
    print_hi()
    print_notes()
    mainmenu(conn, cur)

