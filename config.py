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

import json
import os

# Configuration setting, including config file name, are found in config.py
#   Import into all files so this acts as a global config variable.
#   To pull config variable value, use config.jsonconfigdata['key']
#   To chagne config variable, call config.setconfigvariable(key, value)

# ********** Version number *************
version = "0.1"

# ********** Configuration file ************
#Written in JSON.  {"key" : "value"}
configfilename = 'opinsuomea_config.json'

appfolder = os.path.dirname(__file__)
configfile = os.path.join(appfolder, configfilename)

if os.path.exists(configfile):
    print("Config file '{}' exists.".format(configfile))
else:
    print(
        "It appears that the configuration file does not exist.  This file should be in the root directory of the app:")
    print(filename)
    exit()

try:
    rawconfigdata = open(configfile, 'rb').read()
    print("Configuration file opened.")
except:
    print("Configuration file is not openable, boss.  Try again.")
    print("Please ensure that a configuration file with this name is in the root directory of hte app:", filename)
    exit()

try:
    jsonconfigdata = json.loads(rawconfigdata)
    print("Config JSON parsed.")
except:
    print("Config file  JSON parsing error.  Quitting.")
    print("Here's what we saw in the file:")
    print(rawconfigdata)
    exit()

def setconfigvariable(key, value):
    #Function to change config variables easily
    #  confirmed that it changes them globally if called from a function in another file.
    print(key, "was set at", jsonconfigdata[key])
    jsonconfigdata[key] = value
    print(key, "is now set at", jsonconfigdata[key])


def saveupdatedconfigtofile():
    try:
        f = open(configfile, 'w')
    except:
        print("Could open preferences file {} to write to it.  Updated preferences were not saved.".format(configfile))
        return
    try:
        f.write(json.dumps(jsonconfigdata, indent=4))
        f.close()
        print("\nPreferences file {} successfully saved.".format(configfile))
    except:
        print("Could open save preferences to file {}.  Updated preferences were not saved.".format(configfile))
        return
    return

def printsummary():
    print("Opin Suomea - a program to help users learn Finnish grammar")

def printcopyright():
    print("Opin Suomea Copyright Marc Perkins 2022")

def printcontactinfo():
    print("To contact Marc Perkins, e-mail him at mperkinsphoto@gmail.com")

def printcopyrightandlicensestatement():
    print("\n\n\n")
    printsummary()
    printcopyright()
    printcontactinfo()

    try:
        appfolder = os.path.dirname(__file__)
        licensefile = os.path.join(appfolder, jsonconfigdata['license_file'])
        lf = open(licensefile, 'r')
        #print("License file opened.")
        for line in lf.readlines():
            print(line, end =" ")
        print("\n\n")
        printcopyright()
        printcontactinfo()
    except:
        print("\nLicense file is not openable, boss.  Something is wrong.  We'll print out basic license info here, but the license file should be at:", licensefile)
        print("\nThis program is licensed under the GNU GPLv3 license.")
        print("""    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.""")
        print("\n\n")
        printcopyright()
        printcontactinfo()


