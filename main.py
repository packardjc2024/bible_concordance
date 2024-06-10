"""
This module opens the json files that were created and reads them into
dictionaries that will be used to read and search. It then calls the window
and word and verse classes to initialize the GUI.
"""


import json
from pathlib import Path
from window import Window
from verse_lookup import VerseLookup
from word_lookup import WordLookup


def create_bible_dict(bible_path=Path.joinpath(Path.cwd(), 'kjv_bible.json')):
    """
    Reads the JSON file and returns it as a dictionary.
    """
    with open(bible_path, 'r') as bible_file:
        return json.load(bible_file)


def create_summary_dict(summary_path=Path.joinpath(Path.cwd(), 'book_summary.json')):
    """
    Reads the JSON file and returns it as a dictionary.
    """
    with open(summary_path, 'r') as summary_file:
        return json.load(summary_file)


def create_concordance(concordance_path=Path.joinpath(Path.cwd(), 'concordance.json')):
    """
    Reads the JSON file and returns it as a dictionary.
    """
    with open(concordance_path, 'r') as concordance_file:
        return json.load(concordance_file)


def create_testaments_dict(bible_dict):
    """
    Creates a dictionary with two keys. Each contains a list of the books in the
    old and new testaments. This will be used for populating the testaments box in
    the verse_lookup frame.
    """
    testaments = {}
    index = list(bible_dict.keys()).index('Matthew')
    testaments['Old Testament'] = [key for key in list(bible_dict.keys())[:index]]
    testaments['New Testament'] = [key for key in list(bible_dict.keys())[index:]]
    return testaments


def create_gui_window(bible_dict, summary_dict, concordance_dict, testaments_dict):
    """
    Creates the main window using all the necessary imported modules and passes
    the values of all dictionaries to the root window.
    """
    root = Window(bible_dict, summary_dict, concordance_dict, testaments_dict)
    verse_lookup = VerseLookup(root)
    verse_lookup.initialize()
    word_lookup = WordLookup(root, verse_lookup)
    word_lookup.initialize()
    root.initialize()


if __name__ == '__main__':
    bible = create_bible_dict()
    summary = create_summary_dict()
    concordance = create_concordance()
    testaments = create_testaments_dict(bible)
    create_gui_window(bible, summary, concordance, testaments)
