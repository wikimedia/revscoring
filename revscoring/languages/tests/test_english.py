from nose.tools import eq_

from .. import english, language


def test_language():

    stem_word = english.solve(language.stem_word)

    eq_(stem_word("shitting"), "shit")
    eq_(stem_word("Shitting"), "shit")

    is_badword = english.solve(language.is_badword)

    assert is_badword("shit")
    assert is_badword("shitty")
    assert is_badword("Shitty")
    assert not is_badword("hat")

    is_informal_word = english.solve(language.is_informal_word)

    assert is_informal_word("kewlest")
    assert is_informal_word("won't")
    assert is_informal_word("cant")
    assert not is_informal_word("hat")

    is_misspelled = english.solve(language.is_misspelled)

    assert is_misspelled("wjwkjb")
    assert not is_misspelled("waffles")
    assert not is_misspelled("Waffles")

    is_stopword = english.solve(language.is_stopword)

    assert is_stopword("A")
    assert is_stopword("in")
    assert is_stopword("about")
    assert not is_stopword("waffles")
