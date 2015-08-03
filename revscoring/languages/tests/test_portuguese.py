from nose.tools import eq_

from .. import language, portuguese


def test_language():

    stem_word = portuguese.solve(language.stem_word)

    eq_(stem_word("merda"), "merd")
    eq_(stem_word("Merda"), "merd")

    is_badword = portuguese.solve(language.is_badword)

    assert is_badword("merda")
    assert is_badword("merdar")
    assert is_badword("Merdar")
    assert not is_badword("arvere")

    is_misspelled = portuguese.solve(language.is_misspelled)

    assert is_misspelled("wjwkjb")
    assert not is_misspelled("Esta")

    is_stopword = portuguese.solve(language.is_stopword)

    assert is_stopword("A")
    assert is_stopword("o")
    assert not is_stopword("arvere")
