from collections import namedtuple

from nose.tools import eq_

from ..prev_misspellings import prev_misspellings


def test_prev_misspellings():
    
    def is_misspelled(word): return word in {"werds", "erros", "digtiação"}
    
    revision_text = "This is werds. 7438 And stuff."
    eq_(prev_misspellings(is_misspelled, revision_text), 1)

    revision_text = "Texto com erros de digtiação."
    eq_(prev_misspellings(is_misspelled, revision_text), 2)
