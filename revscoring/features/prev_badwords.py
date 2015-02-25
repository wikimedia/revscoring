import re

from ..datasources import previous_revision_text
from ..languages import is_badword
from .feature import Feature

WORD_RE = re.compile('\w+', re.UNICODE)

def process(is_badword, previous_revision_text):
    previous_revision_text = previous_revision_text or ''
    
    words = (match.group(0) for match in
                WORD_RE.finditer(previous_revision_text))
    
    return sum(is_badword(w) for w in words)

prev_badwords = Feature("prev_badwords", process,
                        returns=int,
                        depends_on=[is_badword, previous_revision_text])
