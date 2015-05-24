from nose.tools import eq_

from .. import language
from ..french import is_badword, is_misspelled, is_stopword, stem_word


def test_language():

    eq_(stem_word()("merdique"), "merdiqu")
    eq_(stem_word()("Merdique"), "merdiqu")
    eq_(hash(stem_word), hash(language.stem_word))

    assert is_badword(stem_word())("merde")
    assert is_badword(stem_word())("merdique")
    assert is_badword(stem_word())("Merdique")
    assert not is_badword(stem_word())("Chapeau")
    eq_(hash(is_badword), hash(language.is_badword))

    assert is_misspelled()("wjwkjb")
    assert not is_misspelled()("gaufres")
    assert not is_misspelled()("Gaufres")
    eq_(hash(is_misspelled), hash(language.is_misspelled))

    assert is_stopword()("A")
    assert is_stopword()("dans")
    assert is_stopword()("notre")
    assert not is_stopword()("gaufres")
    eq_(hash(is_stopword), hash(language.is_stopword))
