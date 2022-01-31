Opin Suomea
Written by Marc Perkins.
January 31, 2022.

A small app to practice Finnish grammar by presenting the user sentences that are missing one part of them.  The program has a database of sentences that are broken down into units; users select a unit, and then are prompted with the sentence in Finnish, its English translation, and hints.

The program tracks which sentences have been played, and how often they have been answered correctly, to bias selection of chosen sentences to sentences that have been gotten wrong more often.

To import sentences it reads an Excel file (located in the data folder).


To run:
1) Install Python 3.10 or later - https://www.python.org/downloads/
2) Open a terminal / command line window
3) If you haven't already, run the command "pip3 install openpyxl" or "pip install openpyxl"
4) Navigate to the directory this script is in.
5) Run the command "python3 opinsuomea.py"


Additional details:
Sentences have a "score" calculated for them - each time a sentence is answered correctly it gets 2 points, each time it is gotten wrong it gets -1 points (all sentences start at 0).  The program selects sentences from the lower tertile (of score ranges for the selected set of sentence) at tripe the rate of sentences with scores in the upper tertile (with sentences that have never been played getting a 4x increase in liklihood of being chosen).  The program also tries to not select sentences that have been presented in the prior round (though this may not be possible if sets are small or rounds are long).


File Importer currently requires the following Python modules:
openpyxl

Configuration file: opinsuomea_config.json
  "default_session_length" : 2  - the default number of questions asked in each session of the game
  "check_case" : false - whether case matters for determining if answers are correct or incorrect

  Not implemented yet in gameplay:
  "kirjakieli" : true  - whether to include kirjakieli lauset in the question pool
  "puhekieli" : true   - whether to include puhekieli lauset in the question pool
