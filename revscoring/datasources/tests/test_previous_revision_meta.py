from mw import Timestamp
from nose.tools import eq_

from ..previous_revision_metadata import previous_revision_metadata


def test_previous_revision_metadata():
    
    previous_rev_doc = {
        "revid": 3456789,
        "comment": "Wat?"
    }
    
    rm = previous_revision_metadata(previous_rev_doc)
    
    eq_(rm.rev_id, previous_rev_doc['revid'])
    eq_(rm.parent_id, None)
    eq_(rm.user_id, None)
    eq_(rm.user_text, None)
    eq_(rm.timestamp, None)
    eq_(rm.comment,  previous_rev_doc['comment'])
    eq_(rm.page_id, None)
    eq_(rm.page_namespace, None)
    eq_(rm.page_title, None)
