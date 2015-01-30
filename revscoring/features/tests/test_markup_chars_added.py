from nose.tools import eq_

from ..markup_chars_added import markup_chars_added


def test_markup_chars_added():
    
    contiguous_segments_added = ["foobar {{herpaA}}", 'A[a]Aa[[Awu]]ta']
    
    eq_(markup_chars_added(contiguous_segments_added), 10)
