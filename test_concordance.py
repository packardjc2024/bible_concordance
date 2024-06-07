"""
This module uses pytest to ensure that all the text was scraped and converted
correctly. If the file is run directly from the terminal instead of using the
run_tests module, then it will run one time for which ever source and book is
set up in the config file.
"""


import pytest
import pandas
from pathlib import Path
import configparser

from scraper import ScrapeHTMLBible
from shorten_names import ShortenNames


##############################################################################
# Set up the variables
##############################################################################
def get_verses_total(book_name):
    """
    This method gets the total number of verses from a book in the Bible.
    """
    return len(bible_dict[book_name].keys())


# Read the config file
config_path = Path.joinpath(Path.cwd(), 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)
source = config.get('source', 'source')
test_book = config.get('book', 'name')
last_number = config.get('book', 'last_verse_number')
last_text = config.get('book', 'last_verse_text')
book_verse_list = config.get('book', 'verse_list')

# Get the scraper dictionary results
bible_dict = ScrapeHTMLBible(source).convert_to_dict()

# Get the verified number of verses dictionary from the Excel file
filepath = Path.joinpath(Path.cwd(), "bible verses.xlsx")
df = pandas.read_excel(filepath)
verified_dict = {row['Book']: row['Verses'] for index, row in df.iterrows()}

# Create the parameterize list comparing the two dictionaries
parameterize_list = [(get_verses_total(key), verified_dict[key]) for key in verified_dict.keys()]

##############################################################################
# Tests
##############################################################################


class TestNumberNames:
    """
    This class tests to make sure that all the names that included numbers
    were correctly shortened.
    """
    samuel_long_name = "The First Book of Samuel"
    samuel_shortened = ShortenNames(samuel_long_name).shorten_name()
    samuel_pass = '1 Samuel'
    samuel_fail = 'First Samuel'

    def test_number_shouldpass(self):
        """
        Calls the shorten name function on the original string and compares
        it to the desired formated result.
        """
        assert self.samuel_shortened == self.samuel_pass

    @pytest.mark.xfail
    def test_number_shouldfail(self):
        """
        Calls the shorten name function on the original string and compares
        it to an incorrectly formated string so that it should fail.
        """
        assert self.samuel_shortened == self.samuel_fail


class TestCleanBook:
    """
    This class tests that the clean_book_strings class correctly returns a list
    of tuples (verse number, verse text).
    """
    original_list = book_verse_list
    number_verses = verified_dict[test_book]
    last_verse_number = last_number
    last_verse_string = last_text
    book_dict = bible_dict[test_book]

    def test_cleanbook_shouldpass(self):
        """
        Checks that the number of keys is equal to the total amount of verses
        in the Book of Galatians.
        """
        assert len(self.book_dict) == self.number_verses

    def test_cleanbook_last_number_shouldpass(self):
        """
        Checks that the last key in the list is the last verse in the Book of
        Galatians.
        """
        last_number = list(self.book_dict.keys())[-1]
        assert last_number == self.last_verse_number

    def test_cleanbook_last_verse_shouldpass(self):
        """
        Checks that the verse text in the last value in the list is the same as
        the desired result for the last verse in the Book of Galatians.
        """
        last_verse = list(self.book_dict.values())[-1]
        assert last_verse == self.last_verse_string


class TestBibleDict:
    """
    This class tests the resultant dictionary of the entire Bible to make sure
    that all the books and the correct number of verses were copied.
    """
    total_verses_verified = sum(list(verified_dict.values()))
    total_books_verified = len(verified_dict.keys())

    def test_scraper_total_books_shouldpass(self):
        """
        Tests that the resultant dictionary has the correct number of books.
        """
        assert len(bible_dict.keys()) == self.total_books_verified

    def test_scraper_total_verses_shouldpass(self):
        """
        Test that the total number of verses in the resultant dictionary
        matches the expected result.
        """
        result_total = sum([get_verses_total(book) for book in bible_dict.keys()])
        assert result_total == self.total_verses_verified

    @pytest.mark.parametrize("input,expected", parameterize_list)
    def test_scraper_book_verses_shouldpass(self, input, expected):
        """
        Checks each individual book to verify that the correct number of verses
        were copied.
        """
        assert input == expected
