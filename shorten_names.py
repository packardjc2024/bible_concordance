"""
This class takes the long book name from the KJV Bible and shortens the
name to make it quicker and easier to search.
"""

import re


class ShortenNames:
    def __init__(self, long_name: str):
        self.long_name = long_name

    def number(self) -> str:
        """
        Changes the number from a word to a number.
        """
        book = re.search(r'(\w+)$', self.long_name).group(1)
        number = re.search(r'^The (\w+)', self.long_name).group(1)
        if number == 'First':
            number = '1'
        elif number == 'Second':
            number = '2'
        elif number == 'Third':
            number = '3'
        return f"{number} {book}"

    def last_word(self) -> str:
        """
        Keeps only the last word of the book name string
        """
        return re.search(r'(\w+)$', self.long_name).group(1)

    def shorten_name(self) -> str:
        """
        Filters through all the possibilities to send the name to the correct
        method and then returns the shortened name.
        """
        if 'Revelation' in self.long_name:
            new_name = 'Revelation'
        elif 'Acts' in self.long_name:
            new_name = 'Acts'
        elif 'Lamentations' in self.long_name:
            new_name = 'Lamentations'
        elif 'Solomon' in self.long_name:
            new_name = 'Song of Songs'
        elif 'Moses' in self.long_name:
            new_name = self.last_word()
        elif 'First' in self.long_name:
            new_name = self.number()
        elif 'Second' in self.long_name:
            new_name = self.number()
        elif 'Third' in self.long_name:
            new_name = self.number()
        else:
            new_name = self.last_word()

        return new_name

