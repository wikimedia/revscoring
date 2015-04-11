from . import revision
from .datasource import Datasource
from .types import RevisionMetadata
from .util import WORD_RE


def process_doc(session, revision_metadata):
    if revision_metadata.parent_id is not None and \
            revision_metadata.parent_id > 0:
        rev_id = revision_metadata.parent_id
        try:
            doc = session.revisions.get(rev_id=rev_id,
                                        properties={'ids', 'user', 'timestamp',
                                                    'userid', 'comment',
                                                    'content', 'flags', 'size'}
                                        )
            return doc
        except KeyError:
            return None
    else:
        return None

doc = Datasource("parent_revision.doc", process_doc,
                 depends_on=['session', revision.metadata])


def process_metadata(parent_revision_doc):
    return RevisionMetadata.from_doc(parent_revision_doc) \
        if parent_revision_doc is not None else None

metadata = Datasource("parent_revision.metadata", process_metadata,
                      depends_on=[doc])


def process_text(parent_revision_doc):
    return parent_revision_doc.get("*") \
        if parent_revision_doc is not None else None

text = Datasource("parent_revision.text", process_text,
                  depends_on=[doc])


def process_words(parent_revision_text):
    parent_revision_text = parent_revision_text or ''
    return [match.group(0) for match in WORD_RE.finditer(parent_revision_text)]

words = Datasource("parent_revision.words", process_words,
                   depends_on=[text])
