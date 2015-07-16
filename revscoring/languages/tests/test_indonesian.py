from nose.tools import eq_

from .. import language
from ..indonesian import is_badword, is_misspelled, is_stopword


def test_language():

    assert is_badword()("gestapo")
    assert is_badword()("geftapo")
    assert is_badword()("Gestapo")
    assert not is_badword()("hat")
    eq_(hash(is_badword), hash(language.is_badword))

    assert is_misspelled()("mungkinkahSAKJDHAKS")
    assert not is_misspelled()("mungkinkah")
    assert not is_misspelled()("Mungkinkah")
    eq_(hash(is_misspelled), hash(language.is_misspelled))

    assert is_stopword()("mungkinkah")
    assert is_stopword()("siapa")
    assert not is_stopword()("belajar")
    eq_(hash(is_stopword), hash(language.is_stopword))
