#File to create the database structure

import sqlite3
import os
import config

def dbselector():
    #For running the script manually
    print("\nThis creates the database structure for the Opin Suomea app.  \n")
    print("This program creates brand-new databases and/or clears existing datases.  Run with care.  If in doubt, exit now!")

    #Database selector
    while True:
        dbfilename = input("What database do you want to work with today? 1 - {} 2 - {} q / quit = exit ".format(config.jsonconfigdata["test_database"], config.jsonconfigdata["prod_database"]))
        if dbfilename == "1":
            dbfilename = config.jsonconfigdata["test_database"]
            break
        if dbfilename == "2":
            dbfilename = config.jsonconfigdata["prod_database"]
            break
        if dbfilename.lower() == "q" or dbfilename.lower() == "quit":
            print("Allright, quitting")
            exit()
        if len(dbfilename) == 0:
            print("I didn't understand that boss.  Try again.")
        else:
            break
    return dbfilename


def createnewdb(dbfilename, calledfromothermodule = False):
    #Returns True if dbs were updated, False if dbs were not udpated.
    if dbfilename == "USEDEFAULTDB":
        if config.jsonconfigdata["Use_test_database"]:
            dbfilename = config.jsonconfigdata["test_database"]
        else:
            dbfilename = config.jsonconfigdata["prod_database"]

    appfolder = os.path.dirname(__file__)
    datafolder = os.path.join(appfolder, config.jsonconfigdata["data_folder"])
    dbfile = os.path.join(datafolder, dbfilename)

    if os.path.isfile(dbfile):
        choice = input("\nWARNING: The file {} already exists; \nare you sure you want to delete this file and overwrite it? (y/yes vs. anything else) ".format(dbfile))
        if choice.lower() == "y" or choice.lower() == "yes":
            print("Okay, we'll reset the database for ya, boss.")
        else:
            if calledfromothermodule:
                print("Okay, going back to main menu without updating database.")
                return(False) #indicating the dbs were not wiped-
            else:
                print("Okay, quitting.")
                exit()
    else:
        print("No existing file found - we'll create a new DB file for ya, boss.")

    try:
        conn = sqlite3.connect(dbfile)
        cur = conn.cursor()
        print("Connected to", dbfile)
    except:
        print("Error connecting to database.  Exiting.")
        exit()

    #Delete tables
    cur.execute('DROP TABLE IF EXISTS Verbi')
    cur.execute('DROP TABLE IF EXISTS Kategoria')
    cur.execute('DROP TABLE IF EXISTS Lause')
    cur.execute('DROP TABLE IF EXISTS Historia')
    conn.commit()
    print("Tables deleted.")

    cur.execute("""
        CREATE TABLE Verbi (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            infinitive TEXT UNIQUE,
            englanti TEXT,
            type TEXT,
            json TEXT
        );
    """)

    #allowing category number to include letters, so like 1a, 1bg, etc
    cur.execute("""
        CREATE TABLE Kategoria (
            id INTEGER NOT NULL PRIMARY KEY,
            humanid TEXT, 
            name TEXT,
            description TEXT,
            updatedate TEXT,
            otherinfo TEXT,
            json TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE Lause (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            humanid TEXT,
            kategoria_id INTEGER NOT NULL,
            verbi_id INTEGER NOT NULL,
            type INT,  
            lause TEXT,
            lause_eng TEXT,
            vastaus TEXT,
            kirjakieli BOOLEAN,
            puhekieli BOOLEAN,
            hint TEXT,
            points INTEGER DEFAULT 0,
            correctlastplay BOOLEAN,
            timesplayed INTEGER DEFAULT 0,
            timescorrect INTEGER DEFAULT 0, 
            timeswrong INTEGER DEFAULT 0,
            lastplayed DATETIME,
            errorflag BOOLEAN,
            errortext TEXT,
            json TEXT
        );
    """)


    cur.execute("""
        CREATE TABLE Historia (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            lause_id INTEGER,
            category_id INTEGER,
            verbi_id INTEGER,
            datetime DATE,
            gotcorrect BOOLEAN,
            wrongtext TEXT,
            json TEXT
        );
    """)


    conn.commit()
    conn.close()

    print("Tables formed all fresh and new for you in {}.  Have a nice day!".format(dbfile))

    return(True) # True means we did wipe the DB.

# Main portion
if __name__ == '__main__':
    dbfilename = dbselector()
    createnewdb(dbfilename)