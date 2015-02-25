from nose.tools import eq_

from ..portuguese import is_badword, is_misspelled, is_stopword, stem_word


def test_language():
    
    eq_(stem_word()("merda"), "merd")
    eq_(stem_word()("Merda"), "merd")
    
    assert is_badword(stem_word())("merda")
    assert is_badword(stem_word())("merdar")
    assert is_badword(stem_word())("Merdar")
    assert not is_badword(stem_word())("arvere")
    
    assert is_misspelled()("wjwkjb")
    assert not is_misspelled()("Esta")
    
    assert is_stopword()("A")
    assert is_stopword()("o")
    assert not is_stopword()("arvere")
