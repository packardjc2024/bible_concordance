"""
This module opens the json files that were created and reads them into
dictionaries that will be used to read and search. It then calls the window
to initialize the GUI.
"""


import json
from pathlib import Path
from window import Window
from verse_lookup import VerseLookup
from word_lookup import WordLookup


# Read the three json files and get their dictionaries
bible_path = Path.joinpath(Path.cwd(), 'kjv_bible.json')
with open(bible_path, 'r') as bible_file:
    kjv_bible = json.load(bible_file)

summary_path = Path.joinpath(Path.cwd(), 'book_summary.json')
with open(summary_path, 'r') as summary_file:
    summary = json.load(summary_file)

concordance_path = Path.joinpath(Path.cwd(), 'concordance.json')
with open(concordance_path, 'r') as concordance_file:
    concordance = json.load(concordance_file)

# Create the old and new testament options
testaments = {}
index = list(kjv_bible.keys()).index('Matthew')
testaments['Old Testament'] = [key for key in list(kjv_bible.keys())[:index]]
testaments['New Testament'] = [key for key in list(kjv_bible.keys())[index:]]

# Create the window
root = Window(kjv_bible, summary, concordance, testaments)
verse_lookup = VerseLookup(root)
verse_lookup.initialize()
word_lookup = WordLookup(root, verse_lookup)
word_lookup.initialize()
root.initialize()
