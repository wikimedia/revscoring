from .datasource import Datasource
from .revision_metadata import revision_metadata


def process(session, revision_metadata):
    if revision_metadata.parent_id is not None and \
       revision_metadata.parent_id > 0:
        doc = session.revisions.get(rev_id=revision_metadata.parent_id,
                                    properties={'ids', 'user', 'timestamp',
                                                'userid', 'comment', 'content',
                                                'flags', 'size'})
        return doc
    else:
        return {}

previous_rev_doc = Datasource("previous_rev_doc", process,
                              depends_on=['session', revision_metadata])
