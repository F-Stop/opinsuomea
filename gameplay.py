import random
import config
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

def playround(verbs, units, lauset, max):
    numcorrect = 0
    numwrong = 0
    for number in range(max):
        #print("run ", number)
        # Select a sentence
        lausetodo = random.randint(0,len(lauset)-1)
        currentlause = lauset[lausetodo]

        #display info and get input
        print("")
        print("")
        print("Verbi käyttää  :", currentlause.verbi_inf)
        print("Joka tarkoittaa:", verbs[currentlause.verbi_inf].englanniksi)
        print("")
        print("Lause on:       ", currentlause.lause)
        print("Englanniksi:    ", currentlause.lause_englanniksi)
        print("")
        answer = input("Type your answer: ")

        #check answer and act accordingly
        iscorrect = checkanswer(answer, currentlause.verbi_vastaus)
        if iscorrect:
            print("Woohoo!  You are correct!")
            numcorrect += 1
        else:
            print("Oh no!  Not quite right.")
            numwrong += 1
            print("Your entry:  ", answer)
            print("Correct ans: ", currentlause.verbi_vastaus)
            while True: #ask them to type it correctly, or enter to skip
                answer2 = input("\nType it correctly (enter to skip):")
                iscorrect2 = checkanswer(answer2, currentlause.verbi_vastaus)
                if iscorrect2:
                    print("Great job!")
                    break
                elif answer2 == "":
                    print("Yeah, that was a tough one.  Let's move on.")
                    break
                else:
                    print("Your entry:  ", answer)
                    print("Correct ans: ", currentlause.verbi_vastaus)
    return numcorrect, numwrong

def startgame(verbs, units, lauset):
    print("GAME ON!")
    while True:
        max = selectnum(lauset)
        numcorrect, numwrong = playround(verbs, units, lauset, max)
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