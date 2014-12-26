import re

from ..datasources import contiguous_segments_added
from .feature import Feature

WORD_RE = re.compile('\w+', re.UNICODE)

def process(contiguous_segments_added):
    
    return sum(len(WORD_RE.findall(segment))
               for segment in contiguous_segments_added)

words_added = Feature("words_added", process,
                      returns=int, depends_on=[contiguous_segments_added])
