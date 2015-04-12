from deltas import Delete, Equal, Insert
from mw import Timestamp
from nose.tools import eq_

from .. import page_creation
from ...dependent import solve


def test_metadata():
    cache = {
        page_creation.doc: {
            "revid": 3456789,
            "comment": "Wat?",
            "timestamp": "2015-01-07T12:23:57Z"
        }
    }

    metadata = solve(page_creation.metadata, cache=cache)

    eq_(metadata.rev_id, 3456789)
    eq_(metadata.parent_id, None)
    eq_(metadata.user_id, None)
    eq_(metadata.user_text, None)
    eq_(metadata.timestamp, Timestamp("2015-01-07T12:23:57Z"))
    eq_(metadata.comment,  "Wat?")
    eq_(metadata.page_id, None)
    eq_(metadata.page_namespace, None)
    eq_(metadata.page_title, None)
