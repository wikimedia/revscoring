from nose.tools import eq_

from .. import language
from ..spanish import (is_badword, is_informal_word, is_misspelled,
                       is_stopword, stem_word)


def test_language():

    eq_(stem_word()("Huevos"), "huev")
    eq_(stem_word()("Vamar"), "vam")
    eq_(hash(stem_word), hash(language.stem_word))

    assert is_badword()("huevos")
    assert is_badword()("mamon")
    assert is_badword()("Mamón")
    assert not is_badword()("hat")
    eq_(hash(is_badword), hash(language.is_badword))

    assert is_informal_word()("jaja")
    assert is_informal_word()("jejejejeje")
    assert is_informal_word()("Chido")
    assert not is_informal_word()("Mamón")
    eq_(hash(is_informal_word), hash(language.is_informal_word))

    assert is_misspelled()("wjwkjb")
    assert not is_misspelled()("que")
    assert not is_misspelled()("Que")
    eq_(hash(is_misspelled), hash(language.is_misspelled))

    assert is_stopword()("que")
    assert is_stopword()("el")
    assert is_stopword()("por")
    assert not is_stopword()("waffles")
    eq_(hash(is_stopword), hash(language.is_stopword))
