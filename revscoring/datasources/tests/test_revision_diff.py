from deltas import Delete, Equal, Insert
from nose.tools import eq_

from ..revision_diff import revision_diff


def test_revision_diff():
    
    previous_revision_text = "foo bar herp derp?"
    revision_text = "herp derp and also?"
    
    operations, a, b = revision_diff(previous_revision_text, revision_text)
    
    eq_(operations, [Delete(a1=0, a2=4, b1=0, b2=0),
                     Equal(a1=4, a2=7, b1=0, b2=3),
                     Insert(a1=3, a2=7, b1=3, b2=7),
                     Equal(a1=7, a2=8, b1=7, b2=8)])
    
    eq_(a, ["foo", " ", "bar", " ", "herp", " ", "derp", "?"])
    
    eq_(b, ['herp', ' ', 'derp', ' ', 'and', ' ', 'also', '?'])
