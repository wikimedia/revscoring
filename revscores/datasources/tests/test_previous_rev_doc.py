from collections import namedtuple

from nose.tools import eq_

from ..previous_rev_doc import previous_rev_doc
from .test_rev_doc import FakeRevisions, FakeSession


def test_previous_rev_doc():
    FakeRevisionMeta = namedtuple("RevisionMeta", ['rev_id', 'parent_id'])
    rm = FakeRevisionMeta(302, 301)
    doc = {'revid': 301, 'comment': "foobar?"}
    session = FakeSession(doc)
    
    rd = previous_rev_doc(session, rm)
    
    eq_(rd, doc)
