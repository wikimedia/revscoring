from nose.tools import eq_

from ..num_segments_removed import num_segments_removed


def test_num_segments_removed():
    
    contiguous_segments_removed = ["foobar {{herpaA}}", 'A[a]Aa[[Awu]]ta']
    
    eq_(num_segments_removed(contiguous_segments_removed), 2)
