import re

from ..datasources import revision_text
from .feature import feature_processor

WORD_RE = re.compile('\w+', re.UNICODE)

@feature_processor(returns=int,
                   depends_on=["language", revision_text])
def prev_badwords(language, revision_text):
    
    badwords = 0
    
    words = (m.group(0) for m in WORD_RE.finditer(revision_text))
    for badword in language.badwords(words):
        badwords += 1
        
    return badwords
