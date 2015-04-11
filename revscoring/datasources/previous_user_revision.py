from . import revision
from .datasource import Datasource
from .types import RevisionMetadata


def process_doc(session, revision_metadata):

    if revision_metadata.user_text is not None:
        docs = session.user_contribs.query(user={revision_metadata.user_text},
                                           properties={'ids', 'timestamp'},
                                           limit=1,
                                           direction="older",
                                           start=revision_metadata.timestamp-1)
        docs = list(docs)
        if len(docs) > 0:
            return docs[0]
        else:
            return None
    else:
        return None

doc = Datasource("previous_user_revision.doc", process_doc,
                 depends_on=['session', revision.metadata])


def process_metadata(previous_user_revision_doc):
    return RevisionMetadata.from_doc(previous_user_revision_doc) \
        if previous_user_revision_doc is not None else None

metadata = Datasource("previous_user_revision.metadata", process_metadata,
                      depends_on=[doc])
