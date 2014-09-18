from ..util.dependencies import depends
from .revision_metadata import revision_metadata


@depends(on=['session', revision_metadata])
def first_rev_doc(session, revision_metadata):
    docs = session.revisions.query(pageids={revision_metadata.page_id},
                                   direction="newer",
                                   limit=1,
                                   properties={'ids', 'user', 'timestamp',
                                              'userid', 'comment', 'content',
                                              'flags', 'size'})
    docs = list(docs)
    
    if len(docs) == 1:
        return docs[0]
    else:
        raise RevisionNotFoundError({'page_id': revision_metadata.page_id})
