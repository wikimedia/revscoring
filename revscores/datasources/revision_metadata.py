from collections import namedtuple

from mw import Timestamp

from ..util.dependencies import depends
from .rev_doc import rev_doc

RevisionMetadata = namedtuple("RevisionMetadata", ['rev_id',
                                                   'parent_id',
                                                   'user_text',
                                                   'user_id',
                                                   'timestamp',
                                                   'comment',
                                                   'page_id',
                                                   'page_namespace',
                                                   'page_title',
                                                   'bytes',
                                                   'minor'])

@depends(on=[rev_doc])
def revision_metadata(rev_doc):
    
    return convert_doc(rev_doc)
    


def convert_doc(rev_doc):
    
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
                            rev_doc['page'].get('title'),
                            rev_doc.get('size'),
                            'minor' in rev_doc)
