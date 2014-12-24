import re

from ..datasources import contiguous_segments_added
from .feature import feature_processor

WORD_RE = re.compile('\w+')

@feature_processor(returns=int,
                   depends_on=["language", contiguous_segments_added])
def misspellings_added(language, contiguous_segments_added):
    
    misspellings = 0
    
    for segment in contiguous_segments_added:
        words = (m.group(0) for m in WORD_RE.finditer(segment))
        for misspelling in language.misspellings(words):
            misspellings += 1
        
    
    return misspellings
