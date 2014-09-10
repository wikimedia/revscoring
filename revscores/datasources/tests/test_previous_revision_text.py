from mw import Timestamp
from nose.tools import eq_

from ..previous_revision_text import previous_revision_text


def test_previous_revision_text():
    previous_rev_doc = {
        "*": "This is some text."
    }
    
    text = previous_revision_text(previous_rev_doc)
    
    eq_(text, previous_rev_doc['*'])
    
    
    previous_rev_doc = {}
    
    text = previous_revision_text(previous_rev_doc)
    
    eq_(text, None)
