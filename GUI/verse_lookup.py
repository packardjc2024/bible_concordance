"""
This module creates the class that serves as the verse lookup. It encompasses
the left side of the window with a top frame for the search options and a
bottom frame that displays those options.
"""


from tkinter import ttk
from tkinter import *
import textwrap


class VerseLookup:
    def __init__(self, root):
        """
        Shorten the names of the dictionaries from the root window.
        """
        self.root = root
        self.bible_dict = self.root.bible_dict
        self.books_dict = self.root.books_dict
        self.concordance = self.root.concordance
        self.testaments = self.root.testaments

    def create_search_frame(self):
        """
        Creates the top-left frame for the window that will hold the search
        selection options.
        """
        self.search_frame = Frame(self.root, borderwidth=2, relief='sunken')
        self.search_frame.grid(row=0, column=0, padx=5, pady=5)

        title = Label(self.search_frame, borderwidth=2, relief='raised',
                      text='Select a verse to view')
        title.grid(row=0, columnspan=2, sticky='NEWS')

        self.create_testament_box()
        self.create_books_box()
        self.create_chapter_box()
        self.create_verse_boxes()

    def create_testament_box(self):
        """
        Creates the testament box which will be combo box that is traced by
        the string variable that will change the books list.
        """
        self.testament = StringVar(self.search_frame, value='Old Testament')
        self.testament.trace('w', self.choose_testament)

        testament_label = Label(self.search_frame, text='Testament')
        self.testament_box = ttk.Combobox(self.search_frame,
                                          values=['Old Testament', 'New Testament'],
                                          textvariable=self.testament)
        testament_label.grid(row=1, column=0)
        self.testament_box.grid(row=1, column=1)

    def create_books_box(self):
        """
        Creates the books combo box to choose which book to search. It will be
        traced by a string variable that will populate the chapters box.
        """
        self.book_name = StringVar(self.search_frame, value='Genesis')
        self.book_name.trace('w', self.choose_book)

        books_label = Label(self.search_frame, text='Book')
        self.books = ttk.Combobox(self.search_frame,
                                  textvariable=self.book_name,
                                  values=[])
        books_label.grid(row=2, column=0)
        self.books.grid(row=2, column=1)

    def create_chapter_box(self):
        """
        Creates the combo box to choose the chapter. It will be traced by a
        string variable that will populate the verses box.
        """
        self.chapter = StringVar(self.search_frame, value="1")
        self.chapter.trace('w', self.choose_chapter)

        chapters_label = Label(self.search_frame, text='Chapter')
        self.chapters = ttk.Combobox(self.search_frame,
                                     textvariable=self.chapter,
                                     values=[])
        chapters_label.grid(row=3, column=0)
        self.chapters.grid(row=3, column=1)

    def create_verse_boxes(self):
        """
        Creates the combo box to choose the verse to view. It is traced by a
        string variable that will display the selected verse in the bottom
        frame.
        """
        self.start_verse = StringVar(self.search_frame, value="1")
        self.start_verse.trace('w', self.choose_verse)

        start_verse_label = Label(self.search_frame, text='Verse')
        self.verses = ttk.Combobox(self.search_frame,
                                   textvariable=self.start_verse,
                                   values=[])
        start_verse_label.grid(row=4, column=0)
        self.verses.grid(row=4, column=1)

    def choose_testament(self, *args):
        """
        This method is called when the testament string variable is changed. It
        configures the books box based on the value of the string variable.
        """
        testament = self.testament.get()
        self.books.configure(values=self.testaments[testament])
        self.books.current(0)

    def choose_book(self, *args):
        """
        Displays the chapters of a book based on the current value of the
        book_name string variable.
        """
        book = self.book_name.get()
        chapters = [str(i) for i in range(1, self.books_dict[book]['number_chapters'] + 1)]
        self.chapters.configure(values=chapters)
        self.chapters.current(0)

    def choose_chapter(self, *args):
        """
        Displays the verses in the verses box based on the value of the chapter
        string variable.
        """
        chapter = self.chapter.get()
        verses = [str(i) for i in range(1, self.books_dict[self.book_name.get()]['chapter_verses'][chapter]+1)]
        self.verses.config(values=verses)
        self.verses.current(0)

    def choose_verse(self, *args):
        """
        Displays the verse text in the bottom-left frame based on the values in
        the string variables in the top frame.
        """
        book = self.book_name.get()
        chapter = self.chapter.get()
        start_verse = self.start_verse.get()
        formatted_start = f"{chapter}:{start_verse}"
        text = textwrap.fill(f"{formatted_start} {self.bible_dict[book][formatted_start]}", 90)
        self.text_label.configure(text=text)

    def create_verse_frame(self):
        """
        Creates the bottom-left frame that will display the selected text.
        """
        self.verse_frame = Frame(self.root, borderwidth=2, relief='sunken')
        self.verse_frame.grid(row=1, column=0, padx=5, pady=5, sticky='NEWS')

        self.text_label = Label(self.verse_frame, text="", justify=LEFT)
        self.text_label.grid(row=0, column=0, sticky='NEWS')

    def initialize(self):
        """
        Calls all the necessary methods to set up the class.
        """
        self.create_search_frame()
        self.create_verse_frame()
        self.choose_testament()
        self.choose_book()
        self.choose_chapter()
        self.choose_verse()
