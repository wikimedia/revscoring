from nose.tools import eq_

from .. import language, hebrew


def test_language():

    is_misspelled = hebrew.solve(language.is_misspelled)

    assert is_misspelled("חטול")
    assert not is_misspelled("חתול")

    is_badword = hebrew.solve(language.is_badword)

    assert is_badword("שרמוטה")
    assert not is_badword("שימרותה")

    is_informal_word = hebrew.solve(language.is_informal_word)

    assert is_informal_word("בגללך")
<<<<<<< HEAD
    assert not is_informal_word("בגלל")
=======
    assert not is_informal_word("בגלל")
>>>>>>> 9a762e70c049be565ca16d3ede133ebd90e6f816
