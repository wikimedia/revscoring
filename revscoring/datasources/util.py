import re

# Used to identify and extract words.
WORD_RE = re.compile('[^\W\d]+', re.UNICODE)
