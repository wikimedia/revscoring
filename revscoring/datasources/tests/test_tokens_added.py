from deltas import Delete, Equal, Insert
from nose.tools import eq_

from ..tokens_added import tokens_added


def test_tokens_added():
    
    a = ["foo", " ", "bar",
         " ",
         "herp", " ", "derp",
         "?"]
    b = ["herp", " ", "derp",
         " ",
         "and", " ", "also",
         "?"]
    
    operations = [Delete(0, 3, 0, 0),
                  Equal(4, 7, 0, 3),
                  Equal(3, 4, 3, 4),
                  Insert(4, 4, 4, 7),
                  Equal(7, 8, 7, 8)]
    
    revision_diff = operations, a, b
    
    eq_(tokens_added(revision_diff), ["and", " ", "also"])
