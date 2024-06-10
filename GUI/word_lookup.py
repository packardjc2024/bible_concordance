"""
This module serves as the concordance (word search) for the app. It will create
two frames on the right side of the window. The top frame will be the word
search entry and the bottom frame will display the results in a treeview. When
a result verse is selected in the treeview, it will automatically populate the
verse in verse lookup frames on the right side of the window.
"""


from tkinter import *
from tkinter import ttk
import re


class WordLookup:
    def __init__(self, root, verse_lookup):
        """
        Both the root window and the verse lookup are passed to the class. The
        references to attributes in these parameter classes are then shortened
        for ease of use.
        """
        self.root = root
        self.verse_lookup = verse_lookup
        self.bible_dict = self.root.bible_dict
        self.books_dict = self.root.books_dict
        self.concordance = self.root.concordance
        self.testaments = self.root.testaments
        self.testament = self.verse_lookup.testament
        self.chapter = self.verse_lookup.chapter
        self.book_name = self.verse_lookup.book_name
        self.start_verse = self.verse_lookup.start_verse

    def create_word_search(self):
        """
        Creates the top-right frame which will hold the word search options.
        """
        self.word_frame = Frame(self.root, borderwidth=2, relief='sunken')
        self.word_frame.grid(row=0, column=1, padx=5, pady=5, sticky='NEWS')
        self.word_frame.columnconfigure(0, weight=1)

        title = Label(self.word_frame, text="Choose a word to look up",
                      borderwidth=2, relief='raised')
        title.grid(row=0, column=0, sticky='NEWS')

        self.word_entry = Entry(self.word_frame)
        self.word_entry.grid(row=1, column=0, padx=5, pady=5, sticky='NEWS')
        self.word_entry.bind('<Return>', func=self.choose_word)

        button = Button(self.word_frame, text="Search",
                        command=self.choose_word)
        button.grid(row=2, column=0, padx=5, pady=5)

    def create_results_frame(self):
        """
        Creates the bottom-right frame that will hold the search results
        treeview.
        """
        self.results_frame = Frame(self.root, borderwidth=2, relief='sunken')
        self.results_frame.grid(row=1, column=1, sticky='NEWS')
        self.results_frame.columnconfigure(0, weight=1)
        self.results_frame.columnconfigure(1, weight=0)
        self.results_frame.rowconfigure(0, weight=0)
        self.results_frame.rowconfigure(1, weight=0)
        self.results_frame.rowconfigure(2, weight=1)

        self.word_label = Label(self.results_frame, text="")
        self.word_label.grid(row=0, columnspan=2)

        self.results_label = Label(self.results_frame, text="")
        self.results_label.grid(row=1, columnspan=2)

    def create_results_table(self):
        """
        Creates the table to display the word search results using treeview and
        creates a scrollbar for viewing the results in the table.
        """
        self.results_table = ttk.Treeview(self.results_frame,
                                          selectmode='browse', show='headings')
        self.results_table['columns'] = ['Verse']
        self.results_table.grid(row=2, column=0, sticky='NEWS')
        self.results_table.heading(0, text='Verse')
        self.results_table.column(column='Verse', width=95)
        self.results_table.bind('<<TreeviewSelect>>', self.select_row)

        scrollbar = ttk.Scrollbar(self.results_frame, orient='vertical',
                                  command=self.results_table.yview)
        self.results_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=2, column=1, sticky='NEWS')

    def choose_word(self, *args):
        """
        This method is called when the search button is clicked or the user
        pressed Enter/Return while the cursor is in the word entry. It gets the
        word from the entry and displays the number of verses that word occurs
        and then calls the fill table method.
        """
        word = self.word_entry.get().strip().lower()
        if word not in self.concordance.keys():
            results_text = f'Not found. Try again.'
            self.clear_table()
        else:
            occurrences = len(self.concordance[word])
            results_text = f'{occurrences} occurrences.'
            self.fill_table(word)

        self.word_label.configure(text=f'"{word.upper()}"')
        self.results_label.configure(text=results_text)
        self.word_entry.delete(0, END)
        self.word_entry.focus_set()

    def clear_table(self):
        """
        Clears the results table.
        """
        for row in self.results_table.get_children():
            self.results_table.delete(row)

    def fill_table(self, word):
        """
        If the word is found in the Bible this method is called to get all
        the verse references from the concordance dictionary and insert them
        into the table.
        """
        self.clear_table()

        verses = self.concordance[word]
        for verse in verses:
            self.results_table.insert("", 'end', values=(verse,),
                                      text="")

    def select_row(self, *args):
        """
        This method is called when the user selects a row in the treeview
        table. It gets the values and then changes the string variables so that
        the verse automatically populates in the bottom left display frame.
        """
        # Get the book name, chapter number, and verse number from the table.
        row = self.results_table.selection()[0]
        verse = self.results_table.item(row)['values']
        location = re.search(r'(.*?)\s(\d+):(\d+)', verse[0])
        book = location.group(1)
        chapter = location.group(2)
        verse = location.group(3)

        # Reset the string variables to populate the verse
        if book in self.testaments['Old Testament']:
            self.testament.set('Old Testament')
        else:
            self.testament.set('New Testament')

        self.book_name.set(book)
        self.chapter.set(chapter)
        self.start_verse.set(verse)

    def initialize(self):
        """
        Calls all the methods necessary to create the frames for the class.
        """
        self.create_word_search()
        self.create_results_frame()
        self.create_results_table()
