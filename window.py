"""
This module is the window that will be used for the app.
"""

from tkinter import *
from tkinter import ttk
import textwrap
import re


class Window(Tk):
    def __init__(self, bible_dict, books_dict, concordance, testaments):
        super().__init__()
        self.bible_dict = bible_dict
        self.books_dict = books_dict
        self.concordance = concordance
        self.testaments = testaments

    def configure_window(self, window_width=700, window_height=500):
        """
        Configures all the tkinter window settings.
        """
        self.window_width = window_width
        self.window_height = window_height
        self.title('KJV Bible')

        # Set up the window geometry and center the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        y = screen_height // 2 - self.window_height // 2
        x = screen_width // 2 - self.window_width // 2
        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

        # Set up the window configuration
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0, minsize=200)

        # Set the style
        style = ttk.Style()
        style.theme_use('clam')

    def create_search_frame(self):
        """
        Creates the top frame for the window that will hold the search
        selection options.
        """
        self.search_frame = Frame(self, borderwidth=2, relief='sunken')
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
        Creates the testament box which will be a traced stringvar to
        determine which books appear in the books combobox
        """
        self.testament = StringVar(self.search_frame, value='Old Testament')
        self.testament.trace('w', self.choose_testament)

        testament_label = Label(self.search_frame, text='Testament')
        self.testament_box = ttk.Combobox(self.search_frame, values=['Old Testament',
                                                                  'New Testament'],
                                          textvariable=self.testament)
        testament_label.grid(row=1, column=0)
        self.testament_box.grid(row=1, column=1)

    def create_books_box(self):
        """
        Creates the books combo box to choose which book to search.
        """
        self.book_name = StringVar(self.search_frame, value='Genesis')
        self.book_name.trace('w', self.choose_book)

        books_label = Label(self.search_frame, text='Book')
        self.books = ttk.Combobox(self.search_frame, textvariable=self.book_name,
                                  values=[])
        books_label.grid(row=2, column=0)
        self.books.grid(row=2, column=1)

    def create_chapter_box(self):
        """
        Creates the combo box to choose the chapter
        """
        self.chapter = StringVar(self.search_frame, value="1")
        self.chapter.trace('w', self.choose_chapter)

        chapters_label = Label(self.search_frame, text='Chapter')
        self.chapters = ttk.Combobox(self.search_frame, textvariable=self.chapter,
                                     values=[])
        chapters_label.grid(row=3, column=0)
        self.chapters.grid(row=3, column=1)

    def create_verse_boxes(self):
        """
        Creates the combo box to choose the start and stop verses
        """
        self.start_verse = StringVar(self.search_frame, value="1")
        self.start_verse.trace('w', self.choose_verse)

        start_verse_label = Label(self.search_frame, text='Verse')
        self.verses = ttk.Combobox(self.search_frame, textvariable=self.start_verse,
                                   values=[])
        start_verse_label.grid(row=4, column=0)
        self.verses.grid(row=4, column=1)

    def choose_testament(self, *args):
        """
        This method is called when the testament stringvar is changed. It
        configures the books box based on the value of the stringvar.
        """
        testament = self.testament.get()
        self.books.configure(values=self.testaments[testament])
        self.books.current(0)

    def choose_book(self, *args):
        """
        Displays the chapters of a book based on the current value of the
        book_name stringvar.
        """
        book = self.book_name.get()
        self.chapters.configure(values=[str(i) for i in range(1, self.books_dict[book]['number_chapters'] + 1)])
        self.chapters.current(0)

    def choose_chapter(self, *args):
        """
        Displays the verses in the verses box based on the value of the
        chapter stringvar
        """
        chapter = self.chapter.get()
        verses = [str(i) for i in range(1, self.books_dict[self.book_name.get()]['chapter_verses'][chapter]+1)]
        self.verses.config(values=verses)
        self.verses.current(0)

    def choose_verse(self, *args):
        """
        Displays the verse text in the bottom frame based on the values in the
        string variables in the top frame.
        """
        book = self.book_name.get()
        chapter = self.chapter.get()
        start_verse = self.start_verse.get()
        formatted_start = f"{chapter}:{start_verse}"
        text = textwrap.fill(f"{formatted_start} {self.bible_dict[book][formatted_start]}", 90)
        self.text_label.configure(text=text)

    def create_verse_frame(self):
        """
        Creates the bottom frame that will display the selected text.
        """
        self.verse_frame = Frame(self, borderwidth=2, relief='sunken')
        self.verse_frame.grid(row=1, column=0, padx=5, pady=5, sticky='NEWS')

        self.text_label = Label(self.verse_frame, text="", justify=LEFT)
        self.text_label.grid(row=0, column=0, sticky='NEWS')

    def create_word_search(self):
        """
        Creates the top-right frame which will hold the word search options.
        """
        self.word_frame = Frame(self, borderwidth=2, relief='sunken')
        self.word_frame.grid(row=0, column=1, padx=5, pady=5, sticky='NEWS')
        self.word_frame.columnconfigure(0, weight=1)

        title = Label(self.word_frame, text="Choose a word to look up",
                      borderwidth=2, relief='raised')
        title.grid(row=0, column=0, sticky='NEWS')

        self.word_entry = Entry(self.word_frame)
        self.word_entry.grid(row=1, column=0, padx=5, pady=5, sticky='NEWS')

        button = Button(self.word_frame, text="Search",
                        command=self.choose_word)
        button.grid(row=2, column=0, padx=5, pady=5)
        self.word_entry.bind('<Return>', func=self.choose_word)

    def create_results_frame(self):
        """
        Creates the bottom-right frame that will hold the search results
        treeview.
        """
        self.results_frame = Frame(self, borderwidth=2, relief='sunken')
        self.results_frame.grid(row=1, column=1, sticky='NEWS')
        self.results_frame.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.results_frame.rowconfigure(0, weight=0)
        self.results_frame.rowconfigure(1, weight=0)
        self.results_frame.rowconfigure(2, weight=1)

        self.word_label = Label(self.results_frame, text="")
        self.word_label.grid(row=0, columnspan=2)

        self.results_label = Label(self.results_frame, text="")
        self.results_label.grid(row=1, columnspan=2)

        self.create_results_table()

    def create_results_table(self):
        """
        Creates the table to display the word search results using treeview.
        """
        self.results_table = ttk.Treeview(self.results_frame, selectmode='browse',
                                          show='headings')
        self.results_table['columns'] = ['Book', 'Verse']
        self.results_table.grid(row=2, column=0, sticky='NEWS')
        self.results_table.heading(0, text='Book')
        self.results_table.heading(1, text='Verse')
        self.results_table.column(column='Book', width=95)
        self.results_table.column(column='Verse', width=95)
        self.results_table.bind('<<TreeviewSelect>>', self.select_row)

        scrollbar = ttk.Scrollbar(self.results_frame, orient='vertical',
                                  command=self.results_table.yview)
        self.results_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=2, column=1, sticky='NEWS')

    def choose_word(self, *args):
        """
        Called when the search button is selected.
        """
        word = self.word_entry.get().strip().lower()
        if word not in self.concordance.keys():
            results_text = f'Not found. Try again.'
        else:
            occurrences = len(self.concordance[word])
            results_text = f'{occurrences} occurrences.'
            self.fill_table(word)

        self.word_label.configure(text=f'"{word.upper()}"')
        self.results_label.configure(text=results_text)
        self.word_entry.delete(0, END)
        self.word_entry.focus_set()

    def fill_table(self, word):
        """
        Fills the results table.
        """
        # Clear the table if there is anything in it
        for row in self.results_table.get_children():
            self.results_table.delete(row)

        # Get the list of verse occurrences
        verses = self.concordance[word]
        for verse in verses:
            self.results_table.insert("", 'end', values=verse,
                                      text="")

    def select_row(self, *args):
        """
        This method is called when the user selects a row in the treeview
        table. It gets the values and then changes the stringvars so that
        the verse automatically populates in the bottom left display frame.
        """
        row = self.results_table.selection()[0]
        verse = self.results_table.item(row)['values']
        book = verse[0]
        location = re.search(r'(\d+):(\d+)', verse[1])
        chapter = location.group(1)
        verse = location.group(2)

        if book in self.testaments['Old Testament']:
            self.testament.set('Old Testament')
        else:
            self.testament.set('New Testament')

        self.book_name.set(book)
        self.chapter.set(chapter)
        self.start_verse.set(verse)

    def initialize(self):
        """
        Creates the frame and entries and then starts the main loop.
        """
        self.configure_window()
        self.create_search_frame()
        self.create_verse_frame()
        self.choose_testament()
        self.choose_book()
        self.choose_chapter()
        self.choose_verse()
        self.create_word_search()
        self.create_results_frame()
        self.mainloop()
