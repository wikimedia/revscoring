from nose.tools import eq_

from ..segments_removed import segments_removed


def test_segments_removed():
    
    contiguous_segments_removed = ["foobar {{herpaA}}", 'A[a]Aa[[Awu]]ta']
    
    eq_(segments_removed(contiguous_segments_removed), 2)
