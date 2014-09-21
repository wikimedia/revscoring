from collections import namedtuple

from nose.tools import eq_

from ..words_removed import words_removed


def test_words_removed():
    eq_(words_removed(["This is four words.", "And two."]), 6)
