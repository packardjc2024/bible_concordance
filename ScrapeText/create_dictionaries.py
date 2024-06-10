"""
This module calls all the necessary classes and functions to scrape the text
and create the concordance. The result is a dictionary of the text, a
dictionary summarizing the text, and a dictionary summarizing each book.
Each dict will then be saved to a separate
json file.
"""


from ScrapeText.scraper import ScrapeHTMLBible
from ScrapeText.bible_summaries import BookSummary
from pathlib import Path
import json


def create_dictionaries(directory=Path.cwd().parent):
    """
    Creates the bible dictionary, summary dictionary, and concordance
    dictionaries. If called directly, uses the default directory path. If
    called from the main module, will use the passed directory path.
    """
    kjv_bible = ScrapeHTMLBible().convert_to_dict()

    # Create the books concordance
    book_summary_dict = {}
    for key, value in kjv_bible.items():
        book_summary_dict[key] = BookSummary(value, key).summarize()

    # Combine the books concordance into a single entire bible concordance
    concordance = {}
    for key, value in book_summary_dict.items():
        for word, verse_list in value['words_list'].items():
            if word not in concordance:
                concordance[word] = [f"{key} {verse}" for verse in verse_list]
            else:
                concordance[word].extend([f"{key} {verse}" for verse in verse_list])

    # Save the bible dict to a json file
    bible_path = Path.joinpath(directory, 'kjv_bible.json')
    with open(bible_path, 'w') as bible_file:
        json.dump(kjv_bible, bible_file)

    # Save the summary dict to a file
    summary_path = Path.joinpath(directory, 'book_summary.json')
    with open(summary_path, 'w') as summary_file:
        json.dump(book_summary_dict, summary_file)

    # Save the concordance to a file:
    concordance_path = Path.joinpath(directory, 'concordance.json')
    with open(concordance_path, 'w') as concordance_file:
        json.dump(concordance, concordance_file)


if __name__ == '__main__':
    create_dictionaries()
