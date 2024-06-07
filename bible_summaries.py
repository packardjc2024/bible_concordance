"""
This module gathers summaries about a book and returns a dictionary that can be
used in searching for specific chapters and verses.
"""


import re
from scraper import ScrapeHTMLBible


class BookSummary:
    def __init__(self, bible_dict, book_name):
        self.bible_dict = bible_dict
        self.book_name = book_name
        self.number_chapters = 0
        self.chapters_verses_dict = {}

    def get_chapters(self):
        """
        Returns a dictionary in the format chapter: number_verses
        """
        last_string = list(self.bible_dict[self.book_name].keys())[-1]
        self.number_chapters = int(re.search(r'(\d+):\d+', last_string).group(1))

    def get_chapters_verses(self):
        """
        Returns a dictionary with the format chapter: number_verses:
        """
        for i in range(1, self.number_chapters + 1):
            max_verse = 0
            for key in list(self.bible_dict[self.book_name].keys()):
                if int(re.search(r'(\d+):\d+', key).group(1)) == i:
                    verse = int(re.search(f"{i}:(\\d+)", key).group(1))
                    if verse > max_verse:
                        max_verse = verse
                self.chapters_verses_dict[i] = max_verse

    def summarize(self):
        """
        calls all the methods that gather the information and then returns
        the values.
        """
        self.get_chapters()
        self.get_chapters_verses()


bible_dict = ScrapeHTMLBible().convert_to_dict()

test = BookSummary(bible_dict, 'Galatians')
test.summarize()