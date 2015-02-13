import re

from ..datasources import previous_revision_text
from .feature import Feature

WORD_RE = re.compile('\w+', re.UNICODE)

def process(language, revision_text):
    revision_text = revision_text or ''
    badwords = 0

    words = (m.group(0) for m in WORD_RE.finditer(revision_text))
    for badword in language.badwords(words):
        badwords += 1

    return badwords

prev_badwords = Feature("prev_badwords", process,
                        returns=int,
                        depends_on=["language", previous_revision_text])
