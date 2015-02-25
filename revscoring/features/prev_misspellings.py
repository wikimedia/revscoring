import re

from ..datasources import previous_revision_text
from ..languages import is_misspelled
from .feature import Feature

WORD_RE = re.compile('\w+', re.UNICODE)

def process(is_misspelled, previous_revision_text):
    previous_revision_text = previous_revision_text or ''
    
    words = (match.group(0) for match in
             WORD_RE.finditer(previous_revision_text))

    return sum(is_misspelled(w) for w in words)

prev_misspellings = Feature("prev_misspellings", process,
                            returns=int,
                            depends_on=[is_misspelled, previous_revision_text])
