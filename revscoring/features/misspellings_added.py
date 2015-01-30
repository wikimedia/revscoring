import re

from ..datasources import contiguous_segments_added
from .feature import Feature

WORD_RE = re.compile('\w+')

def process(language, contiguous_segments_added):
    
    misspellings = 0
    
    for segment in contiguous_segments_added:
        words = (m.group(0) for m in WORD_RE.finditer(segment))
        for misspelling in language.misspellings(words):
            misspellings += 1
        
    
    return misspellings

misspellings_added = Feature("misspellings_added", process,
                             returns=int,
                             depends_on=["language", contiguous_segments_added])
