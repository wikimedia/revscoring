import pickle

from nose.tools import eq_

from .. import indonesian, language


def test_language():

    is_badword = indonesian.solve(language.is_badword)

    assert is_badword("gestapo")
    assert is_badword("geftapo")
    assert is_badword("Gestapo")
    assert not is_badword("hat")

    is_misspelled = indonesian.solve(language.is_misspelled)

    assert is_misspelled("mungkinkahSAKJDHAKS")
    assert not is_misspelled("mungkinkah")
    assert not is_misspelled("Mungkinkah")

    is_stopword = indonesian.solve(language.is_stopword)

    assert is_stopword("mungkinkah")
    assert is_stopword("siapa")
    assert not is_stopword("belajar")

    pickled_indonesian = pickle.loads(pickle.dumps(indonesian))
    eq_(pickled_indonesian, indonesian)
