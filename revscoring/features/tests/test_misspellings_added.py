from nose.tools import eq_

from ..misspellings_added import misspellings_added


def test_misspellings_added():
    
    def is_misspelled(word): return word in {"werds", "erros", "digtiação"}
    
    contiguous_segments_added = ["This is werds. 7438", "And stuff."]
    eq_(misspellings_added(is_misspelled, contiguous_segments_added), 1)
