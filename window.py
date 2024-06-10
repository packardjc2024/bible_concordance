"""
This module is the window that will be used for the app.
"""

from tkinter import *
from tkinter import ttk
import textwrap


class Window(Tk):
    def __init__(self, bible_dict, books_dict, concordance, testaments):
        super().__init__()
        self.bible_dict = bible_dict
        self.books_dict = books_dict
        self.concordance = concordance
        self.testaments = testaments

    def configure_window(self, window_width=500, window_height=500):
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

    def create_search_frame(self):
        """
        Creates the top frame for the window that will hold the search
        selection options.
        """
        self.search_frame = Frame(self, borderwidth=2, relief='sunken')
        self.search_frame.grid(row=0, padx=5, pady=5)

        title = Label(self.search_frame, borderwidth=2, relief='raised',
                      text='Select from the boxes below to search.', )
        title.grid(row=0, columnspan=2)

        ###### change to optoin to choose search for passage or search for word
        ####### or word search be toplevel pop up---yes so can look at both at same time
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

    def create_bottom_frame(self):
        """
        Creates the bottom frame that will display the selected text.
        """
        self.bottom_frame = Frame(self, borderwidth=2, relief='sunken')
        self.bottom_frame.grid(row=1, columnspan=2, padx=5, pady=5, sticky='NEWS')

        self.text_label = Label(self.bottom_frame, text="", justify=LEFT)
        self.text_label.grid(row=0, column=0, sticky='NEWS')

    def initialize(self):
        """
        Creates the frame and entries and then starts the main loop.
        """
        self.configure_window()
        self.create_search_frame()
        self.create_bottom_frame()
        self.choose_testament()
        self.choose_book()
        self.choose_chapter()
        self.choose_verse()
        self.mainloop()
