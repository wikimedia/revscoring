from nose.tools import eq_

from ..numeric_chars_added import numeric_chars_added


def test_numeric_chars_added():
    
    contiguous_segments_added = ["foobar123 {{herpaA}}", 'A[a]Aa[456[Awu]]ta']
    
    eq_(numeric_chars_added(contiguous_segments_added), 6)
