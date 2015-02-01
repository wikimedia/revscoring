from nose.tools import eq_

from ..longest_repeated_char_added import longest_repeated_char_added


def test_longest_repeated_char_added():
    
    contiguous_segments_added = ["foobar herpaA", 'AaAaAwuta']
    
    eq_(longest_repeated_char_added(contiguous_segments_added), 5)
