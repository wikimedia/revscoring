from nose.tools import eq_

from .. import language, hebrew


def test_language():

    is_misspelled = hebrew.solve(language.is_misspelled)

    assert is_misspelled("חטול")
    assert not is_misspelled("חתול")

    is_badword = hebrew.solve(language.is_badword)

    assert is_badword("שרמוטה")
    assert not is_badword("שימרותה")
