from mw import Timestamp
from nose.tools import eq_

from .. import previous_user_revision
from ...dependent import solve


def test_metadata():
    cache = {
        previous_user_revision.doc: {
            "revid": 3456789,
            "comment": "Wat?",
            "timestamp": "2015-01-07T12:23:57Z"
        }
    }

    metadata = solve(previous_user_revision.metadata, cache=cache)

    eq_(metadata.rev_id, 3456789)
    eq_(metadata.parent_id, None)
    eq_(metadata.user_id, None)
    eq_(metadata.user_text, None)
    eq_(metadata.timestamp, Timestamp("2015-01-07T12:23:57Z"))
    eq_(metadata.comment,  "Wat?")
    eq_(metadata.page_id, None)
    eq_(metadata.page_namespace, None)
    eq_(metadata.page_title, None)

    metadata = solve(previous_user_revision.metadata,
                     cache={previous_user_revision.doc: None})
    eq_(metadata, None)
