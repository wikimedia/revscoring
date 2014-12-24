import re

from ..datasources import revision_text
from .feature import feature_processor

WORD_RE = re.compile('\w+', re.UNICODE)

@feature_processor(returns=int,
                   depends_on=[revision_text])
def prev_words(revision_text):
    revision_text = revision_text or ''
    words = 0
    
    for m in WORD_RE.finditer(revision_text):
        
        words += 1
        
    return words
