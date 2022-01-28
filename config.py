import json
import os

# Configuration setting, including config file name, are found in config.py
#   Import into all files so this acts as a global config variable.
#   To pull config variable value, use config.jsonconfigdata['key']
#   To chagne config variable, call config.setconfigvariable(key, value)

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