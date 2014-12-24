from .datasource import Datasource


def process(rev_id, session):
    try:
        doc = session.revisions.get(rev_id=rev_id,
                                    properties={'ids', 'user', 'timestamp',
                                                'userid', 'comment', 'content',
                                                'flags', 'size'})
        return doc
    except KeyError:
        raise RevisionDocumentNotFound({'rev_id': rev_id})

rev_doc = Datasource("rev_doc", process, depends_on=['rev_id', 'session'])
