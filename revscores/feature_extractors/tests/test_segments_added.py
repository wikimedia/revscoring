from nose.tools import eq_

from ..segments_added import segments_added


def test_segments_added():
    
    contiguous_segments_added = ["foobar {{herpaA}}", 'A[a]Aa[[Awu]]ta']
    
    eq_(segments_added(contiguous_segments_added), 2)
