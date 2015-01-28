import re

from ..datasources import contiguous_segments_added
from .feature import Feature

WORD_RE = re.compile('\w+', re.UNICODE)

def process(language, contiguous_segments_added):
    
    badwords = 0
    
    for segment in contiguous_segments_added:
        words = (m.group(0) for m in WORD_RE.finditer(segment))
        for badword in language.badwords(words):
            badwords += 1
        
    
    return badwords

badwords_added = Feature("badwords_added", process, returns=int,
                         depends_on=["language", contiguous_segments_added])
