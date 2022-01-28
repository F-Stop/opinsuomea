Opin Suomea
Written by Marc Perkins.
January 28, 2022.

A small app to practice Finnish grammar.

Currently reads an Excel file (located in the data folder) to import sentences.
Will eventually have a pre-built database of sentences, if we ever get that far.

File Importer currently requires the following modules:
openpyxl

To run:
1) Install Python 3.10 or later - https://www.python.org/downloads/

2) Open a terminal / command line window

3) Run the command "pip install openpyxl" or "pip3 install openpyxl"

4) Navigate to the directory this script is in.

5) Run the command "python3 opinsuomea.py"


Configuration file: opinsuomea_config.json
  "default_session_length" : 2  - the default number of questions asked in each session of the game
  "check_case" : false - whether case matters for determining if answers are correct or incorrect
  "kirjakieli" : true  - whether to include kirjakieli lauset in the question pool
  "puhekieli" : true   - whether to include puhekieli lauset in the question pool
