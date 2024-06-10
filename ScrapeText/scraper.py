"""
This module creates a class that converts a html file of the KJV version of
the Bible into a dictionary of dictionaries. The final result will be formatted
like this:
kjv_bible = {"Genesis": {"1:1": "text...", "1:2": "text", ...},
            "Exodus": {...}, ...}
The html can be read either by downloading the document and providing the path
or by using requests for the link from the website.
"""


from bs4 import BeautifulSoup
from shorten_names import ShortenNames
from clean_book import CleanBook
from pathlib import Path
import requests


class ScrapeHTMLBible:
    def __init__(self, source="file",
                 file_path=Path.joinpath(Path.cwd(), 'bible.html'),
                 url=r"https://www.gutenberg.org/cache/epub/10/pg10-images.html"):
        self.source = source
        self.bible_file = file_path
        self.url = url
        self.scraped_text = {}
        self.kjv_bible = {}

    def _scrape_document(self):
        """
        This method uses beautiful soup to scrape the text from either the
        document or the url. All books are under the div element with the name
        as a h2 element and all the verses as p elements.
        """
        if self.source == 'file':
            soup_obj = BeautifulSoup(open(self.bible_file, encoding='UTF-8'), 'html5lib')
        elif self.source == 'url':
            page = requests.get(self.url)
            soup_obj = BeautifulSoup(page.content, 'html.parser')
        else:
            print("The 'source' parameter must be 'file' or 'url'")
            exit()

        books = soup_obj.find_all('div', attrs={'class': 'chapter'})

        # I don't want to include the testament headers that are also h2 elements
        testaments = ['The New Testament of the King James Bible',
                      'The Old Testament of the King James Version of the Bible']

        for book in books:
            book_name = book.find('h2').text
            if book_name not in testaments:
                book_name = ShortenNames(book_name).shorten_name()
                self.scraped_text[book_name] = [p.text for p in book.find_all('p')]

    def _format_dict(self):
        """
        Convert to a dictionary in the format:
        book_name: {verse_number: verse_text}
        Note: Several books included an extra p element before the first verse
        with extended name details that has to be cut out.
        """
        for name, verses in self.scraped_text.items():
            if name in ('1 Kings', "2 Kings", "1 Samuel", "2 Samuel",
                        "Ecclesiastes"):
                verses = verses[2:]
            verses_dict = CleanBook(verses).return_dict()
            self.kjv_bible[name] = verses_dict

    def convert_to_dict(self):
        """
        Calls all the necessary methods in one method and returns the
        dictionary.
        """
        self._scrape_document()
        self._format_dict()
        return self.kjv_bible
