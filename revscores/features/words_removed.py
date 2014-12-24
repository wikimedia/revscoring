import re

from ..datasources import contiguous_segments_removed
from .feature import Feature

WORD_RE = re.compile('\w+', re.UNICODE)

def process(contiguous_segments_removed):
    
    return sum(len(WORD_RE.findall(segment))
               for segment in contiguous_segments_removed)

words_removed = Feature("words_removed", process,
                        returns=int, depends_on=[contiguous_segments_removed])
