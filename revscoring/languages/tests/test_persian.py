from nose.tools import eq_

from .. import language, persian


def test_language():

    is_badword = persian.solve(language.is_badword)

    assert is_badword("کیرم")
    assert is_badword("madar ghahbeh")
    assert not is_badword("hat")

    is_informal_word = english.solve(language.is_informal_word)

    assert is_informal_word("شادروان")
    assert is_informal_word("خدا بیامرز")
    assert not is_informal_word("hat")

    is_misspelled = persian.solve(language.is_misspelled)

    assert is_misspelled("Notafarsiword")
    assert not is_misspelled("مهم")
