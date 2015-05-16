from . import revision
from .datasource import Datasource
from .types import RevisionMetadata
from .util import WORD_RE


def process_metadata():
    raise NotImplementedError()

metadata = Datasource("parent_revision.metadata", process_metadata)


def process_text():
    raise NotImplementedError()

text = Datasource("parent_revision.text", process_text)


def process_words(parent_revision_text):
    parent_revision_text = parent_revision_text or ''
    return [match.group(0) for match in WORD_RE.finditer(parent_revision_text)]

words = Datasource("parent_revision.words", process_words,
                   depends_on=[text])
