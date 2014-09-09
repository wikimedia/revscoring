from mw import Timestamp
from nose.tools import eq_

from ..revision_metadata import convert_doc, revision_metadata


def test_convert_doc():
    doc = {
        "revid": 624484477,
        "parentid": 624165266,
        "user": "AreaMan",
        "userid": 10297969,
        "timestamp": "2014-09-07T01:15:33Z",
        "comment": "/* Usage in speech */   Introduce some synonyms.",
        "page": {
            "pageid": 11178,
            "ns": 0,
            "title": "Foobar"
        }
    }
    
    rm = convert_doc(doc)
    
    eq_(rm.rev_id, doc['revid'])
    eq_(rm.parent_id, doc['parentid'])
    eq_(rm.user_id, doc['userid'])
    eq_(rm.user_text, doc['user'])
    eq_(rm.timestamp, Timestamp(doc['timestamp']))
    eq_(rm.comment, doc['comment'])
    eq_(rm.page_id, doc['page']['pageid'])
    eq_(rm.page_namespace, doc['page']['ns'])
    eq_(rm.page_title, doc['page']['title'])

def test_revision_metadata():
    
    doc = {
        "revid": 3456789
    }
    
    rm = revision_metadata(doc)
    
    eq_(rm.rev_id, doc['revid'])
    eq_(rm.parent_id, None)
    eq_(rm.user_id, None)
    eq_(rm.user_text, None)
    eq_(rm.timestamp, None)
    eq_(rm.comment, None)
    eq_(rm.page_id, None)
    eq_(rm.page_namespace, None)
    eq_(rm.page_title, None)
