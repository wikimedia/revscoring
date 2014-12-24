import re

from ..datasources import revision_text
from .feature import feature_processor

WORD_RE = re.compile('\w+', re.UNICODE)

@feature_processor(returns=int,
                   depends_on=["language", revision_text])
def prev_misspellings(language, revision_text):
    revision_text = revision_text or ''
    misspellings = 0
    
    words = (m.group(0) for m in WORD_RE.finditer(revision_text))
    for misspelling in language.misspellings(words):
        misspellings += 1
        
    return misspellings
