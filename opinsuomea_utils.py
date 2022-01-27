#File to hold base variable sructures and core functions of the Opin Suomea app

import json
import os
import sqlite3
from datetime import datetime

class lause:


    dbid = None
    unitid = None
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
    number = 0 #Number of the unit
    name = "" #name of the unit
    description = ""
    update_date = ""
    other_info = ""