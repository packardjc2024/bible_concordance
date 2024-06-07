"""

"""


import re
from scraper import ScrapeHTMLBible


bible_dict = ScrapeHTMLBible().convert_to_dict()

words = []
verses = 0
for verses_dict in bible_dict.values():
    for verse_text in verses_dict.values():
        words_list = re.findall(r'[\w-]+', verse_text)
        words.extend(words_list)
        verses += 1


galatians = []
for verse in bible_dict['Galatians'].values():
    words_list = re.findall(r'[\w-]+', verse)
    galatians.extend(words_list)

print('total words:', len(words))  # Should be 783,137
print('galatians words:', len(galatians))
print('verses:', verses)
print('books:', len(bible_dict))

my_count = {}
for key, value in bible_dict.items():
    my_count[key] = len(value.keys())
