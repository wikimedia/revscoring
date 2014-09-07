from ..dependencies import depends_on


@depends_on('rev_id', 'session')
def rev_doc(rev_id, session):
    doc = session.revisions.get(rev_id=rev_id,
                                properties={'ids', 'user', 'timestamp',
                                            'userid', 'comment', 'content',
                                            'flags', 'size'})
    
    if doc is None:
        raise RevisionDocumentNotFound(rev_id)
    else:
        return doc
