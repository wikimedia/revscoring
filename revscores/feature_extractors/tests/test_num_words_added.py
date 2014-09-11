from collections import namedtuple

from nose.tools import eq_

from ..num_words_added import num_words_added


def test_num_words_added():
    eq_(num_words_added(["This is four words.", "And two."]), 6)
