from collections import namedtuple

from mw import Timestamp

from .datasource import Datasource
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
def process(rev_doc):
    
    return convert_doc(rev_doc)
    

revision_metadata = Datasource("revision_metadata", process,
                               depends_on=[rev_doc])

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
                            rev_doc.get('page', {}).get('pageid'),
                            rev_doc.get('page', {}).get('ns'),
                            rev_doc.get('page', {}).get('title'),
                            rev_doc.get('size'),
                            'minor' in rev_doc)
