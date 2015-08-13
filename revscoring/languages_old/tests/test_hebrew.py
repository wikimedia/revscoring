import pickle

from nose.tools import eq_

from .. import hebrew, language


def test_language():

    is_misspelled = hebrew.solve(language.is_misspelled)

    assert is_misspelled("חטול")
    assert not is_misspelled("חתול")

    is_badword = hebrew.solve(language.is_badword)

    assert is_badword("שרמוטה")
    assert not is_badword("שימרותה")

    is_informal_word = hebrew.solve(language.is_informal_word)

    assert is_informal_word("בגללך")  # Because of you
    assert not is_informal_word("בגלל")  # Because

    pickled_hebrew = pickle.loads(pickle.dumps(hebrew))
    eq_(pickled_hebrew, hebrew)
