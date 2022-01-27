import opinsuomea_utils as osu
import random

defaultmax = 2 # default number of sentences to do

def selectnum(lauset):
    print("We have {} setnences in this set".format(len(lauset)))
    #Select how many to do
    while True:
        numtodo = input("How many sentences do you want to do? (default: {})".format(defaultmax))
        if numtodo == "":
            max = defaultmax
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

def playround(verbs, units, lauset, max):
    numcorrect = 0
    numwrong = 0
    for number in range(max):
        #print("run ", number)
        print("")
        print("")
        lausetodo = random.randint(0,len(lauset)-1)
        currentlause = lauset[lausetodo]
        print("Verb to use:", currentlause.verbi_inf)
        print("Which means:", verbs[currentlause.verbi_inf].englanniksi)
        print("Lause on:   ", currentlause.lause)
        print("Englanniksi:", currentlause.lause_englanniksi)
        answer = input("Type your answer: ")
        if answer.lower() == currentlause.verbi_vastaus.lower():
            print("Woohoo!  You are correct!")
            numcorrect += 1
        else:
            numwrong += 1
            print("Your entry:  ", answer)
            print("Correct ans: ", currentlause.verbi_vastaus)
            while True:
                answer2 = input("\nType it correctly:")
                if answer2.lower() == currentlause.verbi_vastaus.lower():
                    print("Great job")
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