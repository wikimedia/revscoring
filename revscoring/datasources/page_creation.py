from . import revision
from ..errors import RevisionDocumentNotFound
from .datasource import Datasource
from .types import RevisionMetadata


def process_doc(session, revision_metadata):
    docs = session.revisions.query(pageids={revision_metadata.page_id},
                                   direction="newer",
                                   limit=1,
                                   properties={'ids', 'user', 'timestamp',
                                               'userid', 'comment',
                                               'flags', 'size'})
    docs = list(docs)

    if len(docs) == 1:
        return docs[0]
    else:
        raise RevisionDocumentNotFound({'page_id': revision_metadata.page_id})

doc = Datasource("page_creation.doc", process_doc,
                 depends_on=['session', revision.metadata])


def process_metadata(page_creation_doc):
    return RevisionMetadata.from_doc(page_creation_doc)

metadata = Datasource("page_creation.metadata", process_metadata,
                      depends_on=[doc])
