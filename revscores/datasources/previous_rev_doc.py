from ..util.dependencies import depends_on
from .revision_metadata import revision_metadata


@depends_on('session', revision_metadata)
def previous_rev_doc(session, revision_metadata):
    if revision_metadata.parent_id is not None:
        doc = session.revisions.get(rev_id=revision_metadata.parent_id,
                                    properties={'ids', 'user', 'timestamp',
                                                'userid', 'comment', 'content',
                                                'flags', 'size'})
        return doc
    else:
        return None
