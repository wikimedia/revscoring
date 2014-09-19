from nose.tools import eq_

from ..symbol_chars_added import symbol_chars_added


def test_symbol_chars_added():
    
    contiguous_segments_added = [":;'.,[]{}<>?/|\\\"\'!@#$%^&*()~-=+`"]
    
    eq_(symbol_chars_added(contiguous_segments_added), 32)
