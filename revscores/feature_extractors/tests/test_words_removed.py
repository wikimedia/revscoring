from collections import namedtuple

from nose.tools import eq_

from ..words_removed import words_removed


def test_words_removed():
    eq_(words_removed(["This is four words.", "And two."]), 6)
    eq_(words_removed(["Aqui há seis palavras.", "Não sete!"]), 6)
