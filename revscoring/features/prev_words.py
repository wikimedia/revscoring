import re

from ..datasources import previous_revision_text
from .feature import Feature

WORD_RE = re.compile('\w+', re.UNICODE)

def process(revision_text):
    revision_text = revision_text or ''
    words = 0

    for m in WORD_RE.finditer(revision_text):

        words += 1

    return words

prev_words = Feature("prev_words", process,
                     returns=int,
                     depends_on=[previous_revision_text])
