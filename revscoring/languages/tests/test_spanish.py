import pickle

from nose.tools import eq_

from .. import language, spanish


def test_language():

    stem_word = spanish.solve(language.stem_word)

    eq_(stem_word("Huevos"), "huev")
    eq_(stem_word("Vamar"), "vam")

    is_badword = spanish.solve(language.is_badword)

    assert is_badword("huevos")
    assert is_badword("mamon")
    assert is_badword("Mamón")
    assert not is_badword("hat")

    is_informal_word = spanish.solve(language.is_informal_word)

    assert is_informal_word("jaja")
    assert is_informal_word("jejejejeje")
    assert is_informal_word("Chido")
    assert not is_informal_word("Mamón")

    is_misspelled = spanish.solve(language.is_misspelled)

    assert is_misspelled("wjwkjb")
    assert not is_misspelled("que")
    assert not is_misspelled("Que")

    is_stopword = spanish.solve(language.is_stopword)

    assert is_stopword("que")
    assert is_stopword("el")
    assert is_stopword("por")
    assert not is_stopword("waffles")

    pickled_spanish = pickle.loads(pickle.dumps(spanish))
    eq_(pickled_spanish, spanish)
