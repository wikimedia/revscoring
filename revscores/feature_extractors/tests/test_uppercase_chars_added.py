from nose.tools import eq_

from ..uppercase_chars_added import uppercase_chars_added


def test_uppercase_chars_added():
    
    contiguous_segments_added = ["abcABC"]
    
    eq_(uppercase_chars_added(contiguous_segments_added), 3)
