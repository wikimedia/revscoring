from collections import namedtuple

from mw import Timestamp

from ..errors import RevisionDocumentNotFound
from .datasource import Datasource
from .types import RevisionMetadata


def process_doc(rev_id, session):
    try:
        doc = session.revisions.get(rev_id=rev_id,
                                    properties={'ids', 'user', 'timestamp',
                                                'userid', 'comment', 'content',
                                                'flags', 'size'})
        return doc
    except KeyError:
        raise RevisionDocumentNotFound({'rev_id': rev_id})

doc = Datasource("revision.doc", process, depends_on=['rev_id', 'session'])

def process_metadata(revision_doc):
    return RevisionMetadata.from_doc(revision_doc)

metadata = Datasource("revision.metadata", process_metadata, depends_on=[doc])

def process_text(revision_doc):
    return revision_doc.get("*")

text = Datasource("revision.text", process_metadata, depends_on=[doc])
