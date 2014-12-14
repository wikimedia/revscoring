from collections import namedtuple

from nose.tools import eq_

from ..prev_words import prev_words


def test_prev_words():
    
    revision_text = "This is werds. 7438 And stuff."
    eq_(prev_words(revision_text), 6)

    revision_text = "Luz, câmera, ação!"
    eq_(prev_words(revision_text), 3)
