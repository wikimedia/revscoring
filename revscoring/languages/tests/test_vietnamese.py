from nose.tools import eq_

from .. import language
from ..vietnamese import (is_badword, is_informal_word, is_misspelled,
                          is_stopword)


def test_language():

    assert is_badword()("đít")
    assert is_badword()("ỉa")
    assert is_badword()("Ỉa")
    assert is_badword()("assface")
    assert not is_badword()("trứng")
    assert not is_badword()("bass")
    eq_(hash(is_badword), hash(language.is_badword))

    assert is_informal_word()("hehe")
    assert is_informal_word()("hihihihihihihihihi")
    assert is_informal_word()("Wá")
    assert not is_informal_word()("he")
    eq_(hash(is_informal_word), hash(language.is_informal_word))

    assert is_misspelled()("wjwkjb")
    assert is_misspelled()("đuờng")
    assert is_misspelled()("cug")
    assert not is_misspelled()("ấy")
    assert not is_misspelled()("giặt")

    # TODO: this fails with the most recent hunspell-vi package
    #assert not is_misspelled()("lũy")

    assert not is_misspelled()("luỹ")
    eq_(hash(is_misspelled), hash(language.is_misspelled))

    assert is_stopword()("như")
    assert is_stopword()("cái")
    assert is_stopword()("mà")
    assert not is_stopword()("chó")
    eq_(hash(is_stopword), hash(language.is_stopword))
