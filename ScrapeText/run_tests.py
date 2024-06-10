"""
This module allows the user to run tests on the scraper using both the url link
and the downloaded html document. They can also use different books of the
Bible to run tests by changing that information in the config file.
"""


import subprocess
import configparser
from pathlib import Path
from scraper import ScrapeHTMLBible


def run_test():
    """Runs the pytest in verbose mode."""
    print(f"\n*****Running test for {source.upper()}.*****\n")
    subprocess.run(['pytest', '--verbose'])


def write_config():
    """Writes to the config file."""
    with open(config_path, 'w') as file:
        config.write(file)


# Define the details for the book to test the CleanBook class.
# A source like Bible Gateway (https://www.biblegateway.com/) can be used
# in order to independently verify the last verse number and text.
book = "Galatians"
last_verse_number = "6:18"
last_verse_text = "Brethren, the grace of our Lord Jesus Christ be with your spirit. Amen."
scraper = ScrapeHTMLBible()
scraper.convert_to_dict()
verse_list = scraper.scraped_text[book]

# Write the initial config file for the file test
config_path = Path.joinpath(Path.cwd(), 'config.ini')
config = configparser.ConfigParser()
source = "file"
config['source'] = {'source': source}
config['book'] = {'name': 'Galatians',
                  'last_verse_number': last_verse_number,
                  'last_verse_text': last_verse_text,
                  'verse_list': verse_list}
write_config()

# Run the file test
run_test()

# Change the source in the config file
config.read(config_path)
source = 'url'
config.set('source', 'source', source)
write_config()

# Re-run the test
run_test()




