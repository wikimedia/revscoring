from collections import namedtuple

from nose.tools import eq_

from ..num_words_removed import num_words_removed


def test_num_words_removed():
    eq_(num_words_removed(["This is four words.", "And two."]), 6)
