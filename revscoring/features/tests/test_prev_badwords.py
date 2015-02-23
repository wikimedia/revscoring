from collections import namedtuple

from nose.tools import eq_

from ..prev_badwords import prev_badwords


def test_prev_badwords():
    
    def is_badword(w): return w in {"badword", "bad", "word"}
    
    revision_text = "This is word. 7438 And stuff."
    eq_(prev_badwords(is_badword, revision_text), 1)
    
    revision_text = "Texto com bad badword digtiação."
    eq_(prev_badwords(is_badword, revision_text), 2)
