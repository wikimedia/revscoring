import re

from ..datasources import contiguous_segments_added
from ..languages import is_badword
from .feature import Feature

WORD_RE = re.compile('\w+', re.UNICODE)

def process(is_badword, contiguous_segments_added):
    
    words_added = (match.group(0) for segment in contiguous_segments_added
                                  for match in WORD_RE.finditer(segment))
    return sum(is_badword(word) for word in words_added)

badwords_added = Feature("badwords_added", process, returns=int,
                         depends_on=[is_badword, contiguous_segments_added])
