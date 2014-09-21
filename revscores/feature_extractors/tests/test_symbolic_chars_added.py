from nose.tools import eq_

from ..symbolic_chars_added import symbolic_chars_added


def test_symbolic_chars_added():
    
    contiguous_segments_added = [":;'.,[]{}<>?/|\\\"\'!@#$%^&*()~-=+`"]
    
    eq_(symbolic_chars_added(contiguous_segments_added), 32)
