
from nose.tools import eq_

from ..chars_added import chars_added


def test_is_section_comment():
    contiguous_segments_added = ["1234", "56", "7"]
    
    eq_(chars_added(contiguous_segments_added), 7)
