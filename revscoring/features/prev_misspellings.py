import re

from ..datasources import previous_revision_text
from .feature import Feature

WORD_RE = re.compile('\w+', re.UNICODE)


def process(language, revision_text):
    revision_text = revision_text or ''
    misspellings = 0

    words = (m.group(0) for m in WORD_RE.finditer(revision_text))
    for misspelling in language.misspellings(words):
        misspellings += 1

    return misspellings

prev_misspellings = Feature("prev_misspellings", process,
                            returns=int,
                            depends_on=["language", previous_revision_text])
