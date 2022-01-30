import random
import time
import config
import datetime
import opinsuomea_utils as osu


def selectnum(lauset):
    print("We have {} setnences in this set".format(len(lauset)))
    #Select how many to do
    while True:
        numtodo = input("How many sentences do you want to do? (default: {})".format(config.jsonconfigdata['default_session_length']))
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

def pickalause(lauselist, lausehistory):
    #This is where our magic comes in to be smart about selecting sentences.

    topscore = None
    bottomscore = None
    for lause in lauselist:
        if topscore == None: topscore = lause.points
        if bottomscore == None: bottomscore = lause.points
        if topscore < lause.points: topscore = lause.points
        if bottomscore > lause.points: bottomscore = lause.points

    #Add in mechanism here to scale liklihood each sentence is picked by score.

    lausetodo = random.randint(0, len(lauselist) - 1)  #if we get complicated selection, break this out.
    if lausetodo in lausehistory:
        count = 0
        while count < 7: # Try 7 times to get a sentence we haven't done this round yet. Give up after that.
            count += 1
            if lausetodo in lausehistory:
                lausetodo = random.randint(0, len(lauselist) - 1)
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
        print("Verbi käyttää  :", currentlause.verbi_inf)
        print("Joka tarkoittaa:", currentlause.verbi_englanniksi)
        if currentlause.hint is not None:
            print("Vihje          :", currentlause.hint)
        print("")
        print("Lause on:       ", currentlause.lause)
        print("Englanniksi:    ", currentlause.lause_englanniksi)
        if currentlause.puhekieli: print("CAUTION: Puhekieli!")
        print("")
        answer = input("Type your answer: ")

        #check answer and act accordingly
        iscorrect = checkanswer(answer, currentlause.vastaus)
        if iscorrect:
            print("Woohoo!  You are correct!")
            numcorrect += 1
            gotitright = True
            time.sleep(0.5)
        else:
            print("Oh no!  Not quite right.")
            numwrong += 1
            gotitright = False
            print("Your entry:  ", answer)
            print("Correct ans: ", currentlause.vastaus)
            while True: #ask them to type it correctly, or enter to skip
                answer2 = input("\nType it correctly (enter to skip):")
                iscorrect2 = checkanswer(answer2, currentlause.vastaus)
                if iscorrect2:
                    print("Great job!")
                    break
                elif answer2 == "":
                    print("Yeah, that was a tough one.  Let's move on.")
                    break
                else:
                    print("Your entry:  ", answer)
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
        sqlstring = "UPDATE Lause SET timesplayed = ?, lastplayed = ?, points = ?, correctlastplay = ?, timescorrect = ?, timeswrong = ? WHERE id = ?"
        cur.execute(sqlstring, (currentlause.timesplayed, currentlause.lastplayed, currentlause.points, currentlause.correctlastplay, currentlause.timescorrect, currentlause.timeswrong, currentlause.dbid))
        conn.commit()
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
        print(count, "-", unit.humanid, "",unit.name, "-", unit.description)
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
            again = input("\nWant to play again? (y/n)")
            if again.lower() == "y":
                break
            elif again.lower() == "n":
                return



if __name__ == "__main__":
    print("Executing this script directly, eh?  Try using opinsuomea.py - this isn't supposed to be run on its own.")