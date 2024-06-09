"""

"""


import json
from pathlib import Path


bible_path = Path.joinpath(Path.cwd(), 'kjv_bible.json')
with open(bible_path, 'r') as bible_file:
    kjv_bible = json.load(bible_file)

summary_path = Path.joinpath(Path.cwd(), 'summary.json')
with open(summary_path, 'r') as summary_file:
    summary = json.load(summary_file)

concordance_path = Path.joinpath(Path.cwd(), 'concordance.json')
with open(concordance_path, 'r') as concordance_file:
    json.load(concordance_file)
