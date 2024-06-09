"""
This module calls all the necessary classes and functions to scrape the text
and create the concordance. The result is a dictionary of the text and a
dictionary summarizing the text. Each dict will then be saved to a separate
json file.
"""


from scraper import ScrapeHTMLBible
from bible_summaries import BookSummary
import json


# Create the bible dictionary by scraping the html file
kjv_bible = ScrapeHTMLBible().convert_to_dict()

# Create the concordance
summary_dict = {}
for key, value in kjv_bible.items():
    summary_dict[key] = BookSummary(value, key).summarize()

# Save the bible dict to a json file
with open('kjv_bible.json', 'w') as bible_file:
    json.dump(kjv_bible, bible_file)

# Save the summary dict to a file
with open('summary.json', 'w') as summary_file:
    json.dump(summary_dict, summary_file)
