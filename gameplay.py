#File to hold gameplay structure.

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

import random
import time
import config
import datetime
import statistics
import opinsuomea_utils as osu


def selectnum(lauset):
    print("We have {} setnences in this set".format(len(lauset)))
    #Select how many to do
    while True:
        numtodo = input("How many sentences do you want to do? (default: {}) ".format(config.jsonconfigdata['default_session_length']))
        if numtodo == "":
            max = config.jsonconfigdata['default_session_length']
            print("Okay, we will do {} sentences.".format(max))
            break
        try:
            max = int(numtodo)
            if max > 0:
                print("Okay, doing {} sentences.".format(max))
                break
            if max < 1:
                print ("Please enter a positive number.")
        except:
            print("You did not enter an integer.  Try again!")
    return max

def checkanswer(answer, vastaus):
    if not config.jsonconfigdata["check_case"]:
        answer = answer.lower()
        vastaus = vastaus.lower()
    if answer == vastaus:
        return True
    else:
        return False

def selectionalgorithm(lauselist, lausehistory):
    scores = []
    for lause in lauselist:
        scores.append(lause.points)

    #meanpoints = statistics.mean(scores)
    #print("Average value of points: ", meanpoints)
    tertilecutoffs = statistics.quantiles(scores, n=3)

    selectionlist = []
    for index, lause in enumerate(lauselist):
        #add sentence index to the selection list varying times based on score
        if lause.points <= tertilecutoffs[0]:
            #in lower tertile
            selectionlist += [index] * 3
        elif lause.points >= tertilecutoffs[1]:
            # in upper tertile
            selectionlist += [index] * 1
        else:
            #middle quartile
            selectionlist += [index] * 2

        #make unplayed sentences more likely
        if lause.timesplayed == 0:
            selectionlist += [index] * 4

    #print("Here is our randomization list:")
    #print(selectionlist)

    selectednumber = random.randint(0, len(selectionlist) - 1)
    lausetodo = selectionlist[selectednumber]
    #print("We seleced sentence number:", lausetodo)
    return lausetodo

def pickalause(lauselist, lausehistory):
    #This is where our magic comes in to be smart about selecting sentences.
    # This function handles the basic ideas - don't repeat sentences, maybe try to end with a sentence we failed on
    # selection algorithm is the actual math of picking a sentence.

    #lausetodo is the position of the sentence in lauselist.
    lausetodo = selectionalgorithm(lauselist, lausehistory)

    if lausetodo in lausehistory:
        count = 0
        while count < 7: # Try 7 times to get a sentence we haven't done this round yet. Give up after that.
            count += 1
            if lausetodo in lausehistory:
                lausetodo = selectionalgorithm(lauselist, lausehistory)
    lausehistory.append(lausetodo)
    return lausetodo, lausehistory

def playround(lauset, max, conn, cur):
    numcorrect = 0
    numwrong = 0
    lausehistory = []
    gotitright = False #flag for if the user got the answer correct.  We'll be pessimistic.
    for number in range(max):
        #print("run ", number)
        # Select a sentence
        lausetodo, lausehistory = pickalause(lauset, lausehistory)
        currentlause = lauset[lausetodo]

        #display info and get input
        print("")
        print("")
        print("")
        print("Englanniksi:    ", currentlause.lause_englanniksi)
        print("Lause on:       ", currentlause.lause)
        print("")
        if config.jsonconfigdata['show_verbi']:
            print("Verbi käyttää  :", currentlause.verbi_inf)
        if config.jsonconfigdata['show_verbi_eng']:
            print("Joka tarkoittaa:", currentlause.verbi_englanniksi)
        if config.jsonconfigdata['show_hint']:
            if currentlause.hint is not None:
                print("Vihje          :", currentlause.hint)



        if currentlause.puhekieli: print("CAUTION: Puhekieli!")
        print("")
        answer = input("Type your answer: ")

        #check answer and act accordingly
        iscorrect = checkanswer(answer, currentlause.vastaus)
        if iscorrect:
            print("Woohoo!  You are correct:", osu.assemblesentence(currentlause.lause, currentlause.vastaus) )
            numcorrect += 1
            gotitright = True
            time.sleep(0.5)
        else:
            print("Oh no!  Not quite right.")
            numwrong += 1
            gotitright = False
            print("Correct ans: ", currentlause.vastaus)
            print("Your entry:  ", answer)
            while True: #ask them to type it correctly, or enter to skip
                answer2 = input("\nType it correctly (enter to skip or 'error' to report an error): ")
                if answer2.lower() == "error":
                    print("\nOh no! Sorry about something being wrong.  Let's flag this question as having an error in the database.")
                    errortext = input("Please briefly summarize what is wrong with this sentence (enter to skip error report):")
                    if errortext == "":
                        print("Okay, not filing an error report.  Continuing!")
                        break
                    else:
                        currentlause.lause_reported = True
                        currentlause.lause_comments.append(errortext)
                        osu.reporterror(currentlause, conn, cur)
                        break
                iscorrect2 = checkanswer(answer2, currentlause.vastaus)
                if iscorrect2:
                    print("Great job!")
                    break
                elif answer2 == "":
                    print("Yeah, that was a tough one.  Let's move on.")
                    break
                else:
                    print("Your entry:  ", answer2)
                    print("Correct ans: ", currentlause.vastaus)

        #Process end of setnence here - update DB, etc.

        #Universal updates:
        currentlause.timesplayed += 1
        currentlause.lastplayed = datetime.datetime.now()

        if gotitright:
            currentlause.timescorrect += 1
            currentlause.points += 2
            currentlause.correctlastplay = True
        else:
            currentlause.timeswrong += 1
            currentlause.points -= 1
            currentlause.correctlastplay = False
            #Update currentlausevariable here.
            #Add to DB update code here

        #Store setnence back in memory Lause list:
        lauset[lausetodo] = currentlause

        #Store in DB:
        #store data in sentence table
        sqlstring = "UPDATE Lause SET timesplayed = ?, lastplayed = ?, points = ?, correctlastplay = ?, timescorrect = ?, timeswrong = ? WHERE id = ?"
        cur.execute(sqlstring, (currentlause.timesplayed, currentlause.lastplayed, currentlause.points, currentlause.correctlastplay, currentlause.timescorrect, currentlause.timeswrong, currentlause.dbid))

        #store data in history table
        wrongtext = None
        if gotitright is False:
            wrongtext = answer
        sqlstring = "INSERT OR IGNORE INTO Historia (lause_id, category_id, verbi_id, datetime, gotcorrect, wrongtext, json) VALUES (?, ?, ?, ?, ?, ?, ?)"
        cur.execute(sqlstring, (currentlause.dbid, currentlause.unitdbid, currentlause.verbi_dbid, currentlause.lastplayed, currentlause.correctlastplay, wrongtext, currentlause.jsondata))
        conn.commit()

        #Show correct sentence here:

    return lauset, numcorrect, numwrong

def startgame(conn, cur):

    #Start by choosing a unit or units to do.
    #then choose how many sentences to do

    doall = False   # flag to allow user to select wanting to do all of the units
    print("\nGAME ON!\n")

    unitlist = osu.pullunits(conn, cur)

    print("Here are the units we have:\n")
    print("# - Unit name - Unit Description")
    count = 1
    for unit in unitlist:
        print(count, "-", unit.name, "-", unit.description)
        count += 1
    while True:
        unitchoicetext = input("\nWhat unit would you like to play today? (# or enter to do ALL the units) ")
        if unitchoicetext == "":
            doall = True
            unitdbid = 0 #placeholder.
            break
        try:
            unitchoice = int(unitchoicetext)
            if unitchoice < 1:
                print("Please enter a valid number")
                continue
            chosenunit = unitlist[unitchoice - 1]
            unitdbid = chosenunit.dbid  #unit index is 0 based, whereas my display was 1 based
            break
        except:
            print("Please enter a valid number")

    if doall:
        print("Alright, we are going to do ALL units.  Have fun ;)")
    else:
        print("Alright, we are going to do unit: ", chosenunit.name)

    lauselist = osu.getlauselist(conn, cur, unitdbid, doall)

    while True:
        max = selectnum(lauselist)
        lauselist, numcorrect, numwrong = playround(lauselist, max, conn, cur)
        print("\nRESULTS:")
        print("Number correct: ", numcorrect)
        print("Number wrong: ", numwrong)
        while True:
            again = input("\nWant to play again? (y/n) ")
            if again.lower() == "y":
                break
            elif again.lower() == "n":
                return



if __name__ == "__main__":
    print("Executing this script directly, eh?  Try using opinsuomea.py - this isn't supposed to be run on its own.")