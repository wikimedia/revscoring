from nose.tools import eq_

from ..num_segments_added import num_segments_added


def test_num_segments_added():
    
    contiguous_segments_added = ["foobar {{herpaA}}", 'A[a]Aa[[Awu]]ta']
    
    eq_(num_segments_added(contiguous_segments_added), 2)
