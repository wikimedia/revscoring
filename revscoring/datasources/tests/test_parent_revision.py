from mw import Timestamp
from nose.tools import eq_

from .. import parent_revision
from ...dependent import solve


def test_metadata():
    cache = {
        parent_revision.doc: {
            "revid": 3456789,
            "comment": "Wat?",
            "timestamp": "2015-01-07T12:23:57Z"
        }
    }

    metadata = solve(parent_revision.metadata, cache=cache)

    eq_(metadata.rev_id, 3456789)
    eq_(metadata.parent_id, None)
    eq_(metadata.user_id, None)
    eq_(metadata.user_text, None)
    eq_(metadata.timestamp, Timestamp("2015-01-07T12:23:57Z"))
    eq_(metadata.comment,  "Wat?")
    eq_(metadata.page_id, None)
    eq_(metadata.page_namespace, None)
    eq_(metadata.page_title, None)

    metadata = solve(parent_revision.metadata,
                     cache={parent_revision.doc: None})
    eq_(metadata, None)


def test_text():

    text = solve(parent_revision.text,
                 cache={parent_revision.doc: {"*": "Some text"}})
    eq_(text, "Some text")

    text = solve(parent_revision.text,
                 cache={parent_revision.doc: None})
    eq_(text, None)


def test_words():

    words = solve(parent_revision.words,
                  cache={parent_revision.text: "Some text words 55."})
    eq_(words, ["Some", "text", "words"])

    words = solve(parent_revision.words,
                  cache={parent_revision.text: None})
    eq_(words, [])
