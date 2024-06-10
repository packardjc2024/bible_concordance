"""
This class takes a list of strings in a book and cleans it so that it
returns a dictionary of 'chapter:verse': 'verse_text'. This is necessary
because the strings in the <p> html elements are not grouped by single verses.
"""

import re


class CleanBook:
    def __init__(self, strings_list: list[str]):
        self.__strings_list = strings_list
        self.__book_string = ""
        self.__tuples_list = []
        self.__dictionary = {}

    def _remove_newlines(self):
        """
        Removes the new lines from the list of strings
        """
        self.__strings_list = [i.replace('\n', ' ').strip() for i in self.__strings_list]

    def _convert_list_to_string(self):
        """
        Converts the list of strings to a single string using join:
        """
        self.__book_string = ' '.join(self.__strings_list)

    def _convert_to_tuples(self):
        """
        Converts the single string to a list of tuples where 0 is the verse
        number and 1 is the verse text
        """
        # Divide the book string into a list of verse numbers and strings
        pattern = re.compile(r'(\d+:\d+)')
        result_list = pattern.split(self.__book_string)

        # Remove any empty values
        self.__tuples_list = [value for value in result_list if value != '']

    def _create_dict(self):
        """
        Converts the list of tuples to the desired dictionary format.
        """
        number_index = 0
        while number_index < len(self.__tuples_list) - 1:
            verse_index = number_index + 1
            self.__dictionary[self.__tuples_list[number_index]] = self.__tuples_list[verse_index].strip()
            number_index += 2

    def return_dict(self) -> dict:
        """
        Calls all the methods and returns the dictionary.
        """
        self._remove_newlines()
        self._convert_list_to_string()
        self._convert_to_tuples()
        self._create_dict()
        return self.__dictionary
