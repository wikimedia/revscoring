from nose.tools import eq_

from .. import language
from ..english import is_badword, is_misspelled, is_stopword, stem_word


def test_language():

    eq_(stem_word()("shitting"), "shit")
    eq_(stem_word()("Shitting"), "shit")
    eq_(hash(stem_word), hash(language.stem_word))

    assert is_badword(stem_word())("shit")
    assert is_badword(stem_word())("shitty")
    assert is_badword(stem_word())("Shitty")
    assert not is_badword(stem_word())("hat")
    eq_(hash(is_badword), hash(language.is_badword))

    assert is_misspelled()("wjwkjb")
    assert not is_misspelled()("waffles")
    assert not is_misspelled()("Waffles")
    eq_(hash(is_misspelled), hash(language.is_misspelled))

    assert is_stopword()("A")
    assert is_stopword()("in")
    assert is_stopword()("about")
    assert not is_stopword()("waffles")
    eq_(hash(is_stopword), hash(language.is_stopword))
