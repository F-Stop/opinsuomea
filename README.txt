Opin Suomea
Written by Marc Perkins.
February 5, 2022.

A small app to practice Finnish grammar by presenting the user with sentences that are missing one part of them and asking the user to type in the missing portion.  The program has the ability to create a database of sentences that are broken down into units; users select a unit, and then are prompted with the sentence in Finnish, its English translation, and (optionally) hints.  This app runs entirely locally - no internet connection is needed, and no data is sent to (or received from) the net at any time.

The program tracks which sentences have been played, and how often they have been answered correctly, to bias selection of sentences to those that have been gotten wrong more often (though any sentence in a unit can be chosen at any time).  More details on how this is done, below.

The program imports sentences from an Excel file (located in the data folder), so the user can customize the units entirely as they want.  Users can also share units easily.  Importing can either be done non-destructively (updating each sentence and/or adding new sentences, but not deleting user history data) or destructively (wiping all existing data from the database, including removing the play-history data for each question).

NOTE: While there are a few sample units included, they were written by a non-Finnish speaker and should not be trusted to be correct.  Make your own sentences!

Data is stored in a SQLLITE database contained in the "data" folder, allowing the program to save information from session to session.  If the database does not exist or gets corrupted somehow, use the in-program option to "wipe database and reload verbs", which will create a brand new database if none exists.  If you want to move data between devices, you will need to manually copy this database file to the new location.

The program allows users to choose whether the program shows various optional items (the verb in Finnish, hints for the sentence) and whether the program checks for case when evaluating answers (default: no case checking). Users can save these settings to a preferences file so they are maintained across sessions (or just edit the preferences file manually themselves, if they want).

Users can also store error reports if sentences have problems with them (typos, incorrect answers, etc.).  To do this type "error" after entering an incorrect answer.  These errors are stored locally in the database, not e-mailed or sent to anyone, so they are present solely for the user's own benefit in tracking which of their sentences / answers needs to be fixed.  You can display a list of sentences that have error reports in them via the database menu, and this same option allows you to clear all error reports from the database.  Simply importing updated versions of a sentence will NOT clear error reports, since I do not have a mechanism to determine whether updates to sentences actually fix the errors that are reported - that is up to you, fine user, to determine.

If you want to create your own units, or edit the sentences / verbs that are already in the program, open up the Excel spreadsheet file in the "data" directory.  Make any changes you want to that file (being careful to not change the formatting of the spreadsheet - see instructions in the sheet), save it with the same filename, and then "update" the database via the database menu in the program. This will add new sentences/verbs/units to the database, and update ones that have changed, without deleting your user data.  When you update the database, keep an eye out for warnings after importing - the program should handle most cases of errors without causing crashes, but may not do what you intended if things have been mis-formatted.  Errors print out after updating (scroll up if you miss them).


To run:
1) Install Python 3 (programmed using 3.10, but should work on earlier versions of 3) - https://www.python.org/downloads/
2) Open a terminal / command line window
3) If you haven't already, run the command "pip3 install openpyxl" or "pip install openpyxl"
4) Navigate to the directory this script is in.
5) Run the command "python3 opinsuomea.py"


SCORING DETAILS:
Sentences have a "score" calculated for them (which is hidden from the user prsently).  All sentences start at 0 when the database is wiped or when a sentence is imported for the first time (updates to sentences, like fixing a typo, leave sentence scores intact). Each time a sentence is answered correctly it gets 2 points, each time a sentence is gotten wrong it gets -1 points.  The program selects sentences from the lower tertile (of score ranges for the selected set of sentence) at triple the rate of sentences with scores in the upper tertile (the middle tertile is chosen at double the rate of hte upper tertile).  Sentences that have never been played get a 4x increase in liklehood of being chosen.  The program also tries to not select sentences that have been presented in the current round (though this may not be possible if sets are small or rounds are long).


PREFERENCES:

The following variables are available for use globally in the program (being read at program start from the configuration file):
Configuration file: opinsuomea_config.json

  "default_session_length" : 5  - the default number of questions asked in each session of the game
  "check_case" : false - whether case matters for determining if answers are correct or incorrect
  "show_hint": true - show the hint field when presenting a question (hint field is never shown for a particular sentence if there is no hint for it)
    "show_verbi": true, - show the Finnish language version of the verb to be used
    "show_verbi_eng": true, - show the English translation of the verb to be used (often duplicative of the English sentence translation)
    "data_folder": "data", - locatin of the data folder (contains the database and spreadsheet used for importing)
    "test_database": "test_opinsuomea_db", - name of the test database
    "prod_database": "opinsuomea_db", - name of the production database
    "Use_test_database": false - which database to use - false indicates that the production database should be used.
    "license_file" : "LICENSE.txt" - name of license file

  Not implemented yet in gameplay:
  "kirjakieli" : true  - whether to include kirjakieli lauset in the question pool
  "puhekieli" : true   - whether to include puhekieli lauset in the question pool


DISCLAIMER:

Marc Perkins is a hobby programmer who wrote this while starting to learn Finnish in Jyväskylä, Finland.

The programming is basic, and Marc apologizes in advance to skilled programmers who look over the code.

Sentences included are more for demonstration of the program's functioning than actual learning,
as they were written by Marc, who is probably at the A1 level of comprehension of Finnish.

DEPENDENCIES:

File Importer currently requires the following Python modules:
openpyxl

CONTRIBUTIONS:

Contributions, either to the sentence list or to the code, would be much appreciated.

See more at: https://github.com/F-Stop/opinsuomea

COPYRIGHT:

Copyright 2022 by Marc Perkins.

LICENSE:

This file is part of Opin Suomea.

Opin Suomea is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Opin Suomea is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Opin Suomea. If not, see <https://www.gnu.org/licenses/>.