import re

from ..datasources import contiguous_segments_added
from .feature import feature_processor

WORD_RE = re.compile('\w+', re.UNICODE)

@feature_processor(returns=int, 
                   depends_on=["language", contiguous_segments_added])
def badwords_added(language, contiguous_segments_added):
    
    badwords = 0
    
    for segment in contiguous_segments_added:
        words = (m.group(0) for m in WORD_RE.finditer(segment))
        for badword in language.badwords(words):
            badwords += 1
        
    
    return badwords
