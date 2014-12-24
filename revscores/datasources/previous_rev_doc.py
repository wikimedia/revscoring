from .datasource import datasource_processor
from .revision_metadata import revision_metadata


@datasource_processor(['session', revision_metadata])
def previous_rev_doc(session, revision_metadata):
    if revision_metadata.parent_id is not None and \
       revision_metadata.parent_id > 0:
        doc = session.revisions.get(rev_id=revision_metadata.parent_id,
                                    properties={'ids', 'user', 'timestamp',
                                                'userid', 'comment', 'content',
                                                'flags', 'size'})
        return doc
    else:
        return {}
