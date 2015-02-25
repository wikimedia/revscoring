import re

from ..datasources import contiguous_segments_added
from ..languages import is_misspelled
from .feature import Feature

WORD_RE = re.compile('\w+')

def process(is_misspelled, contiguous_segments_added):
    words_added = (match.group(0) for segment in contiguous_segments_added
                                  for match in WORD_RE.finditer(segment))
    return sum(is_misspelled(word) for word in words_added)

misspellings_added = Feature("misspellings_added", process,
                             returns=int,
                             depends_on=[is_misspelled, contiguous_segments_added])
