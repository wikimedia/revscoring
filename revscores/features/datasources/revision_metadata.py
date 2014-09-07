from mw import Timestamp

from .rev_doc import rev_doc

RevisionMetadata = namedtuple("RevisionMetadata", ['id',
                                                   'parent_id',
                                                   'user_text',
                                                   'user_id',
                                                   'timestamp',
                                                   'comment',
                                                   'page_id',
                                                   'page_ns',
                                                   'page_title'])

@depends_on(rev_doc)
def revision_metadata(rev_doc):
    
    try:
        timestamp = Timestamp(rev_doc.get('timestamp'))
    except ValueError:
        timestamp = None
    
    return RevisionMetadata(rev_doc.get('revid'),
                            rev_doc.get('parentid'),
                            rev_doc.get('user'),
                            rev_doc.get('userid'),
                            timestamp,
                            rev_doc.get('comment'),
                            rev_doc['page'].get('pageid'),
                            rev_doc['page'].get('ns'),
                            rev_doc['page'].get('title'))

@depends_on(rev_doc)
def revision_text(rev_doc):
    return rev_doc.get("*")
