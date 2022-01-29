import config
import opinsuomea_utils as osu
import file_importer as osfile
import gameplay as gp
import db_creator
import random
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# Configuration setting, including config file name, are found in config.py
#   To pull config variable value, use config.jsonconfigdata['key']
#   To chagne config variable, call config.setconfigvariable(key, value)




def print_hi(name):
    print("Welcome to Opin Suomea - an app to help learn Finnish grammar.")
    print("Created by Marc Perkins")
    print("Currently this is a super-duper-mega-ultra Alpha")

def print_notes():
    return

def wipe_and_reload_db_from_file():
    wb, verbsheet, unitsheets = osfile.openfile()
    verblist, unitlist, lauselist, errorlist = osfile.parsefile(wb, verbsheet, unitsheets)
    db_creator.createnewdb("USEDEFAULTDB") #passing fake name to get that function to use the default db selected in preferences
    conn, cur = osu.connectdb()
    verblist, unitlist, lauselist, errorlist = osu.populate_dbs(verblist, unitlist, lauselist, errorlist, conn, cur)
    print("\nAlright, you've got a nice fresh set of databases with new data loaded from the Excel file to use!")


def optionsmenu():
    while True:
        print("""\nOPTIONS MENU
    x - Placeholder
    blank line - return to main""")
        choice1 = input("Type the letter of your option: ")
        if choice1.lower() == "x":
            print("Probably have stuff on importing and exporting here.")
        elif choice1.lower() == "":
            print("Back to main menu!")
            return()
        else:
            print("Hmm, I didn't quite understand that.  Please try again.")

def displaymainmenu():
    print("""\nMAIN MENU
    1 - Play game
    v - Print list of verbs
    s - Print list of sentences
    o - See options
    d - Wipe database and reload verbs, units, and sentences from the Excel file
    q/Q - Quit""")

def mainmenu(conn, cur):
    while True:
        displaymainmenu()
        choice1 = input("Type the letter of your option: ")
        if choice1 == "1":
            gp.startgame(conn, cur)
        elif choice1.lower() == "v":
            print("List of verbs")
            #for verb in verbs:
            #    print(verb, "---", verbs[verb].englanniksi)
        elif choice1.lower() == "s":
            print("List of sentences")
            #for lause in lauset:
            #    print(lause.lause, "---", lause.verbi_inf, "---", lause.verbi_vastaus, "---", lause.lause_englanniksi)
        elif choice1.lower() == "o":
            optionsmenu()
        elif choice1.lower() == "d":
            wipe_and_reload_db_from_file()
        elif choice1.lower() == "q":
            print("Thanks for using the app!")
            exit()
        else:
            print("Hmm, I didn't quite understand that.  Please try again.")



#Main portion
if __name__ == '__main__':
    print_hi('Something')
    print_notes()
    conn, cur = osu.connectdb()
    mainmenu(conn, cur)

