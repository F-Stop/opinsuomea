#File to hold base variable sructures and core functions of the Opin Suomea app

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
import json
import os
import sqlite3
import re
from datetime import datetime

class lause:
    dbid = None
    humanid = ""
    unitdbid = None
    unithumanid = None
    unitname = ""
    kirjakieli = False
    puhekieli = False
    type = None #Type of thing missing - 1 = verb, 2 = noun (not implemented), 3 = other
    lause = "" #sentence with the verb missing
    lause_englanniksi = "" #Sentence in English
    hint = "" #Hint field, especially for use with other-type sentences.
    lause_verbin_paikka = 0 #start position of verb in the sentence
    verbi_dbid = None
    vastaus = "" #verb conjugated correctly
    verbi_inf = ""  #verb infinitive form (suomeksi)
    verbi_englanniksi = "" #verb definition (englanniksi)
    points = None #track points assigned to sentence
    lastplayed = None #Date of the last play
    correctlastplay = None #track if the last play is correct
    timesplayed = None
    timescorrect = None
    timeswrong = None
    substantiivi_dbid = None #Unused now, but place to hold nouns
    substantiivi_inf = ""  #noun general form
    substantiivi_vastaus = "" #noun conjugated correctly
    substantiivi_englanniksi = "" #noun definition (englanniksi)
    lause_reported = False #Flag to track if user has reported an error with the sentence
    lause_comments = [] #user comments on the sentence - will be list of strings.
    errorflagindb = None #Flag to track if there is an error already recorded in the dB
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

    #This function serves two purposes:
    #    1) If the DB has been created fresh before this, it will insert everything new.
    #    2) If it is working on an existing DB, it just updates everything (assuming bits may be changed), but should not change the stats (to leave those intact)

    #Verb work first
    print("Inserting verbs")

    #First create a dummy record that has dashes, to prevent code blowups if accidentially searching this table for a sentence that has no verb
    #   As I have hard-coded in a value of "-" if a setnence is not a verb-containing one.
    cur.execute('''INSERT OR IGNORE INTO Verbi (infinitive, englanti, type) VALUES ("-", "-", "")''')
    for verb in verblist:
        #print(verb)
        #print(verblist[verb].englanniksi)
        cur.execute('''SELECT id FROM Verbi WHERE (infinitive) = ( ? )''', (verb,))
        result = cur.fetchone()
        if result:
            print(verb, "already exists in the database.  Updating.")
            verb_id = result[0]
            cur.execute('''UPDATE OR IGNORE Verbi SET infinitive = ?, englanti = ?, type = ? WHERE id = ?''', (verb,verblist[verb].englanniksi,verblist[verb].typpi, verb_id))
            conn.commit()
        else:
            print(verb, "is a new verb.  Inserting.")
            cur.execute('''INSERT OR IGNORE INTO Verbi (infinitive, englanti, type) VALUES (?, ?, ?)''', (verb,verblist[verb].englanniksi,verblist[verb].typpi))
            conn.commit()
            cur.execute('''SELECT id FROM Verbi WHERE (infinitive) = ( ? )''', (verb,))
            verb_id = cur.fetchone()[0]
        verblist[verb].dbid = verb_id
        #print("Verb dbID is:", verb_id)

    #insert categories / units
    for unit in unitlist:
        print("Working on unit: ", unit.humanid)
        cur.execute('''SELECT id FROM Kategoria WHERE (humanid) = ( ? )''', (unit.humanid,))
        result = cur.fetchone()
        if result:
            print(unit.humanid, unit.name, "already exists.  Updating.")
            unit_id = result[0]
            cur.execute('''UPDATE OR IGNORE Kategoria SET humanid = ?, name = ?, description = ?, updatedate = ?, otherinfo = ? WHERE id = ?''', (unit.humanid, unit.name, unit.description, unit.update_date, unit.other_info, unit_id))
            conn.commit()
        else:
            print(unit.humanid, unit.name, "is a new unit. Inserting.")
            cur.execute('''INSERT OR IGNORE INTO Kategoria (humanid, name, description, updatedate, otherinfo) VALUES (?, ?, ?, ?, ?)''', (unit.humanid, unit.name, unit.description, unit.update_date, unit.other_info))
            conn.commit()
            cur.execute('''SELECT id FROM Kategoria WHERE (humanid) = ( ? )''', (unit.humanid,))
            unit_id = cur.fetchone()[0]
        unit.dbid = unit_id
        #print("Unit dbID is:", unit_id)

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
            print(lause.humanid, "already exists.  Updating.")
            lause_dbid = result[0]
            cur.execute('''UPDATE OR IGNORE Lause SET humanid = ?, kategoria_id = ?, verbi_id = ?, lause = ?, lause_eng = ?, vastaus = ?, kirjakieli = ?, puhekieli = ?, type = ?, hint = ? WHERE id = ?''', (lause.humanid, unit_dbid, verb_dbid, lause.lause, lause.lause_englanniksi, lause.vastaus, lause.kirjakieli, lause.puhekieli, lause.type, lause.hint, lause_dbid))
            conn.commit()
        else:
            print(lause.humanid, "is a new lause.  Inserting.")
            cur.execute('''INSERT OR IGNORE INTO Lause (humanid, kategoria_id, verbi_id, lause, lause_eng, vastaus, kirjakieli, puhekieli, type, hint) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (lause.humanid, unit_dbid, verb_dbid, lause.lause, lause.lause_englanniksi, lause.vastaus, lause.kirjakieli, lause.puhekieli, lause.type, lause.hint))
            conn.commit()
            cur.execute('''SELECT id FROM Lause WHERE (humanid) = ( ? )''', (lause.humanid,))
            lause_dbid = cur.fetchone()[0]
        lause.dbid = lause_dbid
        #print("Lause ID is:", lause.dbid)

    conn.commit()
    print("Completed database import/update.")

    return verblist, unitlist, lauselist, errorlist



def pullverbs(conn, cur):
    cur.execute('''SELECT id, infinitive, englanti, type, json FROM Verbi''')
    result = cur.fetchall()
    verbitlist = []
    for item in result:
        currentverb = verbi()
        currentverb.dbid = item[0]
        currentverb.infinitive = item[1]
        currentverb.englanniksi = item[2]
        currentverb.typpi = item[3]
        currentverb.jsondata = item[4]
        verbitlist.append(currentverb)
    return verbitlist

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


def getlauselist(conn, cur, unitdbid, allunits = False, dbwhereclause = ""):
    #dbwhere clause MUST start with "AND" or the like to form a legal SQL statement.
    if allunits:
        dbunitclause = ""
    else:
        dbunitclause = "AND Lause.kategoria_id = {} ".format(unitdbid)  # This may be a security risk if this is ever published online.

    sqlstring = """SELECT Verbi.infinitive, Verbi.englanti, Verbi.id, Kategoria.humanid, Kategoria.name, Lause.id, Lause.humanid, Lause.kategoria_id, Lause.lause, Lause.lause_eng, Lause.vastaus, Lause.kirjakieli, Lause.puhekieli, Lause.points, Lause.correctlastplay, Lause.timesplayed, Lause.timescorrect, Lause.timeswrong, Lause.lastplayed, Lause.errorflag, Lause.json, Lause.type, Lause.hint, Lause.errortext 
    FROM Verbi, Lause, Kategoria
    WHERE  Lause.verbi_id = Verbi.id AND Lause.kategoria_id = Kategoria.id {} {}
    ORDER BY Kategoria.humanid, Lause.humanid
    """.format(dbunitclause, dbwhereclause)

    cur.execute(sqlstring)
    results = cur.fetchall()

    lauselist = []
    for result in results:
        tamalause = lause()
        #print(result)
        tamalause.verbi_inf = result[0]
        tamalause.verbi_englanniksi = result[1]
        tamalause.verbi_dbid = result[2]
        tamalause.unithumanid = result[3]
        tamalause.unitname = result[4]
        tamalause.dbid = result[5]
        tamalause.humanid = result[6]
        tamalause.unitdbid = result[7]
        tamalause.lause = result[8]
        tamalause.lause_englanniksi = result[9]
        tamalause.vastaus = result[10]
        tamalause.kirjakieli = result[11]
        tamalause.puhekieli = result[12]
        tamalause.points =  result[13]
        tamalause.correctlastplay =  result[14]
        tamalause.timesplayed = result[15]
        tamalause.timescorrect =  result[16]
        tamalause.timeswrong =  result[17]
        tamalause.lastplayed =  result[18]
        tamalause.errorflagindb =  result[19]
        tamalause.jsondata =  result[20]
        tamalause.type = result[21]
        tamalause.hint = result[22]
        if result[23] is not None:
            tamalause.lause_comments = json.loads(result[23])
        lauselist.append(tamalause)

    return lauselist

def printimporterrorlist(errorlist):
    if len(errorlist) == 0:
        print("\nNo errors in the import - Yay!")
    else:
        print("\nHere are errors and warnings from the import:")
        for item in errorlist:
            print(item)


def assemblesentence(lause, vastaus):
    if re.search('###', lause) is None:  # check if there are three ###'s
        return lause #just return the sentence as found in database if there are no ###'s
    sentence = re.sub('(###)', vastaus, lause)
    return sentence

def reporterror(lause, conn, cur):
    sqlstring = "UPDATE Lause SET errorflag = ?, errortext = ? WHERE id = ?"
    cur.execute(sqlstring, (lause.lause_reported, json.dumps(lause.lause_comments), lause.dbid))
    conn.commit()
    print("Error report saved.  Thank you for reporting this, and we apologize for the trouble!")
    print("\nNote: error reports are not automatically emailed to anyone - they are just saved in your local database file.")
    print("You will need to manually make changes yourself, or email the db file to someone, to actually fix the issue.")