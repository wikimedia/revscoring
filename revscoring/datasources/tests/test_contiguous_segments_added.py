from deltas import Delete, Equal, Insert
from nose.tools import eq_

from ..contiguous_segments_added import contiguous_segments_added


def test_contiguous_segments_added():
    
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
    
    segments = contiguous_segments_added(revision_diff)
    
    eq_(segments[0], "and also")
