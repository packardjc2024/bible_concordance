"""
This module serves as the main program for the app. It contains the main
function which reads the json files, creates a testament dictionary, and then
creates the main window and passes it all the dictionaries. When called as the
main program it first checks if a json concordance exists. If not it runs the
setup modules to scrape the html and create the dictionaries and then calls the
main function.
"""


import json
from pathlib import Path
from GUI.window import Window
from GUI.verse_lookup import VerseLookup
from GUI.word_lookup import WordLookup
from ScrapeText.create_dictionaries import create_dictionaries


def main():
    """
    Reads all the json files, converts them to a dictionary, creates the
    testaments dictionary, and then creates the root window and passes the
    dictionaries to start the app.
    """
    # Read the bible json and convert to dictionary
    bible_path = Path.joinpath(Path.cwd(), 'kjv_bible.json')
    with open(bible_path, 'r') as bible_file:
        bible =  json.load(bible_file)

    # Read the summary json and convert to dictionary
    summary_path = Path.joinpath(Path.cwd(), 'book_summary.json')
    with open(summary_path, 'r') as summary_file:
        summary =  json.load(summary_file)

    # Read the concordance and convert to dictionary
    concordance_path = Path.joinpath(Path.cwd(), 'concordance.json')
    with open(concordance_path, 'r') as concordance_file:
        concordance = json.load(concordance_file)

    # Create the testaments dictionary
    testaments = {}
    index = list(bible.keys()).index('Matthew')
    testaments['Old Testament'] = [key for key in list(bible.keys())[:index]]
    testaments['New Testament'] = [key for key in list(bible.keys())[index:]]

    # Create the window to start the app
    root = Window(bible, summary, concordance, testaments)
    verse_lookup = VerseLookup(root)
    verse_lookup.initialize()
    word_lookup = WordLookup(root, verse_lookup)
    word_lookup.initialize()
    root.initialize()


if __name__ == '__main__':
    if Path.exists(Path.joinpath(Path.cwd(), 'concordance.json')):
        main()
    else:
        directory = Path.cwd()
        create_dictionaries(directory)
        main()



