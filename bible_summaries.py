"""
This module gathers summaries about a book and returns a dictionary that can be
used in searching for specific chapters and verses.
"""

import re
from scraper import ScrapeHTMLBible


class BookSummary:
    def __init__(self, book_dict, book_name):
        self.book_dict = book_dict
        self.book_name = book_name
        self.number_chapters = 0
        self.chapters_verses_dict = {}
        self.words = {}
        self.words_count = {}
        self.summary = {}

    def get_chapters(self):
        """
        Returns a dictionary in the format chapter: number_verses
        """
        last_string = list(self.book_dict.keys())[-1]
        self.number_chapters = int(re.search(r'(\d+):\d+', last_string).group(1))

    def get_chapters_verses(self):
        """
        Returns a dictionary with the format chapter: number_verses:
        """
        for i in range(1, self.number_chapters + 1):
            max_verse = 0
            for key in list(self.book_dict.keys()):
                if int(re.search(r'(\d+):\d+', key).group(1)) == i:
                    verse = int(re.search(f"{i}:(\\d+)", key).group(1))
                    if verse > max_verse:
                        max_verse = verse
                self.chapters_verses_dict[i] = max_verse

    def get_words(self):
        """
        Returns a dictionary of the words in the book in the format:
        word: [verses where occurs]
        """
        for key, value in self.book_dict.items():
            words_list = re.findall(r'[\w-]+', value)
            for word in words_list:
                if word.lower() not in self.words.keys():
                    self.words[word.lower()] = [key]
                else:
                    self.words[word.lower()].append(key)

    def calculate_words_count(self):
        """
        Returns a dictionary with the count of words and each word's count in
        the book.
        """
        for key, value in self.words.items():
            self.words_count[key] = len(value)

    def summarize(self):
        """
        Calls all the methods that gather the information and then returns
        a dictionary of all the values.
        """
        self.get_chapters()
        self.get_chapters_verses()
        self.get_words()
        self.calculate_words_count()
        self.summary.update({'number_chapters': self.number_chapters,
                             'chapter_verses': self.chapters_verses_dict,
                             'words_count': self.words_count,
                             'words_list': self.words})
        return self.summary
