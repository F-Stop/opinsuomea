import opinsuomea_utils as osu
import file_importer as osfile
import gameplay as gp
import random
# See PyCharm help at https://www.jetbrains.com/help/pycharm/


#Things to add:
# Create config file
# Cofig file contains: default session length, whether to check for lower case, ...


def print_hi(name):
    print("Welcome to Opin Suomea - an app to help learn Finnish grammar.")
    print("Created by Marc Perkins")
    print("Currently this is a super-duper-mega-ultra Alpha")

def print_notes():
    print("NOTE: Current all comparisons are done in lower case.")


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
    q/Q - Quit""")

def mainmenu(verbs, units, lauset):
    while True:
        displaymainmenu()
        choice1 = input("Type the letter of your option: ")
        if choice1 == "1":
            gp.startgame(verbs, units, lauset)
        elif choice1.lower() == "v":
            print("List of verbs")
            for verb in verbs:
                print(verb, "---", verbs[verb].englanniksi)
        elif choice1.lower() == "s":
            print("List of sentences")
            for lause in lauset:
                print(lause.lause, "---", lause.verbi_inf, "---", lause.verbi_vastaus, "---", lause.lause_englanniksi)
        elif choice1.lower() == "o":
            optionsmenu()
        elif choice1.lower() == "q":
            print("Thanks for using the app!")
            exit()
        else:
            print("Hmm, I didn't quite understand that.  Please try again.")



#Main portion
if __name__ == '__main__':
    print_hi('Something')
    wb, verbsheet, unitsheets = osfile.openfile()
    verbs, units, lauset, errorlist = osfile.parsefile(wb, verbsheet, unitsheets)

    print_notes()

    mainmenu(verbs, units, lauset)

