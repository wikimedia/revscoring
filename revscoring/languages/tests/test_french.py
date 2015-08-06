import pickle

from nose.tools import eq_

from .. import french, language


def test_language():

    stem_word = french.solve(language.stem_word)

    eq_(stem_word("merdique"), "merdiqu")
    eq_(stem_word("Merdique"), "merdiqu")

    is_badword = french.solve(language.is_badword)

    assert is_badword("merde")
    assert is_badword("merdique")
    assert is_badword("Merdique")
    assert not is_badword("Chapeau")

    is_misspelled = french.solve(language.is_misspelled)

    assert is_misspelled("wjwkjb")
    assert not is_misspelled("gaufres")
    assert not is_misspelled("Gaufres")

    is_stopword = french.solve(language.is_stopword)

    assert is_stopword("A")
    assert is_stopword("dans")
    assert is_stopword("notre")
    assert not is_stopword("gaufres")

    pickled_french = pickle.loads(pickle.dumps(french))
    eq_(pickled_french, french)
