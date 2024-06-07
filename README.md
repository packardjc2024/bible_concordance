# Description
This program converts and HTML of the KJV Bible into a dictionary of books
with each book being a dictionary of verse_number: verse_text pairs. The html
comes from the Project Gutenberg website (https://www.gutenberg.org/ebooks/10).
The html can either be accessed using requests or the downloadable html file. 

## Testing
Using the run_tests file and adding books to the book_string_lists file will
allow the user to run tests on other books. Galatians was randomly chosen for
the original test. 

When running the tests the program is set up to run in one of two ways:

1. If pytest is called directly, the tests will be run one time for whichever
source and book is in the config file. 
2. If the run_tests.py file is called, then the test will run one time each for
using the html download and using requests with the url.