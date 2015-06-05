from .datasource import Datasource
from .util import WORD_RE

metadata = Datasource("parent_revision.metadata")
"""
Returns a :class:`~revscoring.datasources.types.RevisionMetadata` for the parent
revision.
"""

text = Datasource("parent_revision.text")
"""
Returns the text content of the parent revision.
"""

def process_words(parent_revision_text):
    parent_revision_text = parent_revision_text or ''
    return [match.group(0) for match in WORD_RE.finditer(parent_revision_text)]

words = Datasource("parent_revision.words", process_words,
                   depends_on=[text])
"""
Returns a list of word-like tokens in the content of the parent revision.
"""
