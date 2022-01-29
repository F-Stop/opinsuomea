#File to hold base variable sructures and core functions of the Opin Suomea app

import config
import json
import os
import sqlite3
from datetime import datetime

class lause:
    dbid = None
    humanid = ""
    unitdbid = None
    unithumanid = None
    unitname = ""
    kirjakieli = False
    puhekieli = False
    lause = "" #sentence with the verb missing
    lause_englanniksi = "" #Sentence in English
    lause_verbin_paikka = 0 #start position of verb in the sentence
    verbi_dbid = None
    verbi_vastaus = "" #verb conjugated correctly
    verbi_inf = ""  #verb infinitive form (suomeksi)
    verbi_englanniksi = "" #verb definition (englanniksi)
    substantiivi_dbid = None #Unused now, but place to hold nouns
    substantiivi_inf = ""  #noun general form
    substantiivi_vastaus = "" #noun conjugated correctly
    substantiivi_englanniksi = "" #noun definition (englanniksi)
    lause_reported = False #Flag to track if user has reported an error with the sentence
    lause_comments = [] #user comments on the sentence - will be list of strings.
    need_to_update = False #Flag to track if this sentence needs to be updated in dB (i.e., new user error report)
    väärä_vastaus = "" #place to track wrong answers
    jsondata = None  #always store this as DB-friendly JSON data, and parse it out when needed.

class user:
    dbid = None
    etunimi = ""
    sukunimi = ""
    email = ""
    learning = None #JSON data, stored as DB-friendly JSON data, to allow flexible changing of learning data tracked

class verbi:
    dbid = None
    infinitive = "" # infinitive form
    englanniksi = "" # English definition
    typpi = "" # verb type
    jsondata = None  #JSON data, stored as DB-friendly JSON data, to allow flexible info on verbs to be stored

class unit:
    dbid = None
    humanid = "" #Number of the unit, which can include letters
    name = "" #name of the unit
    description = ""
    update_date = ""
    other_info = ""
    json = ""

def connectdb():
    #connect to db
    if config.jsonconfigdata["Use_test_database"]:
        dbfilename = config.jsonconfigdata["test_database"]
    else:
        dbfilename = config.jsonconfigdata["prod_database"]

    appfolder = os.path.dirname(__file__)
    datafolder = os.path.join(appfolder, config.jsonconfigdata["data_folder"])
    dbfile = os.path.join(datafolder, dbfilename)

    if os.path.isfile(dbfile):
        try:
            conn = sqlite3.connect(dbfile)
            cur = conn.cursor()
            print("Connected to", dbfile)
        except:
            print("No existing database file found when trying to open database.  Exiting.  Database should have been at: ", dbfile)
            exit()
    else:
        print("No existing database file found when trying to open database.  Exiting.  Database should have been at: ", dbfile)
        exit()
    return conn, cur

def populate_dbs(verblist, unitlist, lauselist, errorlist, conn, cur):
    #Assuming that we are populating from scratch or just adding in new ones
    #NOT updating existing sentences.  Consider adding that in future.

    #Verb work first
    print("Inserting verbs")
    for verb in verblist:
        #print(verb)
        #print(verblist[verb].englanniksi)
        cur.execute('''SELECT id FROM Verbi WHERE (infinitive) = ( ? )''', (verb,))
        result = cur.fetchone()
        if result:
            # print("Verb already exists")
            verb_id = result[0]
        else:
            print(verb, "is a new verb.  Inserting.")
            cur.execute('''INSERT OR IGNORE INTO Verbi (infinitive, englanti, type) VALUES (?, ?, ?)''', (verb,verblist[verb].englanniksi,verblist[verb].typpi))
            conn.commit()
            cur.execute('''SELECT id FROM Verbi WHERE (infinitive) = ( ? )''', (verb,))
            verb_id = cur.fetchone()[0]
        verblist[verb].dbid = verb_id
        print("Verb dbID is:", verb_id)

    #insert categories / units
    for unit in unitlist:
        print("Working on unit: ", unit.humanid)
        cur.execute('''SELECT id FROM Kategoria WHERE (humanid) = ( ? )''', (unit.humanid,))
        result = cur.fetchone()
        if result:
            print("Unit already exists")
            unit_id = result[0]
        else:
            print(unit.humanid, unit.name, "is a new unit. Inserting.")
            cur.execute('''INSERT OR IGNORE INTO Kategoria (humanid, name, description, updatedate, otherinfo) VALUES (?, ?, ?, ?, ?)''', (unit.humanid, unit.name, unit.description, unit.update_date, unit.other_info))
            conn.commit()
            cur.execute('''SELECT id FROM Kategoria WHERE (humanid) = ( ? )''', (unit.humanid,))
            unit_id = cur.fetchone()[0]
        unit.dbid = unit_id
        print("Unit dbID is:", unit_id)

    #insert lauset
    for lause in lauselist:
        print("Working on Lause: ", lause.humanid)

        cur.execute('''SELECT id FROM Verbi WHERE (infinitive) = ( ? )''', (lause.verbi_inf,))
        verb_dbid = cur.fetchone()[0]

        cur.execute('''SELECT id FROM Kategoria WHERE (humanid) = ( ? )''', (lause.unithumanid,))
        unit_dbid = cur.fetchone()[0]

        cur.execute('''SELECT id FROM Lause WHERE (humanid) = ( ? )''', (lause.humanid,))
        result = cur.fetchone()
        if result:
            print("Luase already exists")
            lause_dbid = result[0]
        else:
            print(lause.humanid, "is a new lause.  Inserting.")
            cur.execute('''INSERT OR IGNORE INTO Lause (humanid, kategoria_id, verbi_id, lause, lause_eng, vastaus, kirjakieli, puhekieli) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (lause.humanid, unit_dbid, verb_dbid, lause.lause, lause.lause_englanniksi, lause.verbi_vastaus, lause.kirjakieli, lause.puhekieli))
            conn.commit()
            cur.execute('''SELECT id FROM Lause WHERE (humanid) = ( ? )''', (lause.humanid,))
            lause_dbid = cur.fetchone()[0]
        lause.dbid = lause_dbid
        print("Lause ID is:", lause.dbid)

    print("Completed database import.")

    return verblist, unitlist, lauselist, errorlist

def pullunits(conn, cur):
    cur.execute('''SELECT id, humanid, name, description, updatedate, otherinfo, json FROM Kategoria''')
    result = cur.fetchall()
    unitlist = []
    for item in result:
        currentunit = unit()
        currentunit.dbid = item[0]
        #print(currentunit.dbid)
        currentunit.humanid = item[1]
        #print(currentunit.humanid)
        currentunit.name = item[2]
        #print(currentunit.name)
        currentunit.description = item[3]
        currentunit.update_date = item[4]
        currentunit.other_info = item[5]
        currentunit.json = item[6]
        unitlist.append(currentunit)

    return unitlist