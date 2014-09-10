from mw import Timestamp
from nose.tools import eq_

from ..revision_text import revision_text


def test_revision_text():
    doc = {
        "*": "This is some text."
    }
    
    text = revision_text(doc)
    
    eq_(text, doc['*'])
    
    
    null_doc = {}
    
    text = revision_text(null_doc)
    
    eq_(text, None)
