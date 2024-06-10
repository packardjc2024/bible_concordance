"""
This module is the main GUI window that will be used for the app. It will be
passed as root to the word_lookup and verse_lookup classes.
"""

from tkinter import *
from tkinter import ttk


class Window(Tk):
    def __init__(self, bible_dict, books_dict, concordance, testaments):
        super().__init__()
        """
        The window class is an instance of the main Tkinter window class and
        takes the dictionaries and testament list created in the main module
        so that they can be accessed by the other classes that take this class
        as a parameter. 
        """
        self.bible_dict = bible_dict
        self.books_dict = books_dict
        self.concordance = concordance
        self.testaments = testaments
        self.title('KJV Bible')

    def set_geometry(self, window_width=700, window_height=500):
        """
        Sets up the geometry of the window.
        """
        self.window_width = window_width
        self.window_height = window_height

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        y = screen_height // 2 - self.window_height // 2
        x = screen_width // 2 - self.window_width // 2
        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

    def set_grid(self):
        """
        Sets up the grid configuration to have the concordance related frames
        only use as much space as necessary and the verse lookup frames use the
        remainder of the window.
        """
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0, minsize=200)

    def set_style(self):
        """
        Sets the style for the window using ttk styles.
        """
        self.style = ttk.Style()
        self.style.theme_use('clam')

    def initialize(self):
        """
        Calls all the methods to set up the window and then starts the window
        by running the mainloop.
        """
        self.set_geometry()
        self.set_grid()
        self.set_style()
        self.mainloop()
