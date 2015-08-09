import pickle

from nose.tools import eq_

from .. import language, vietnamese
from .util import all_false, all_true


def test_language():

    is_badword = vietnamese.solve(language.is_badword)

    all_true(is_badword, ["đít", "ỉa", "Ỉa", "assface", "trứng"])
    all_false(is_badword, ["bass", "ai", "bằng", "bị", "bộ", "cho", "chưa",
                           "chỉ", "cuối", "cuộc"])

    is_informal_word = vietnamese.solve(language.is_informal_word)

    assert is_informal_word("hehe")
    assert is_informal_word("hihihihihihihihihi")
    assert is_informal_word("Wá")
    assert not is_informal_word("he")

    is_misspelled = vietnamese.solve(language.is_misspelled)

    assert is_misspelled("wjwkjb")
    assert is_misspelled("đuờng")
    assert is_misspelled("cug")
    assert not is_misspelled("ấy")
    assert not is_misspelled("giặt")

    # TODO: this fails with the most recent hunspell-vi package
    #assert not is_misspelled("lũy")

    assert not is_misspelled("luỹ")

    is_stopword = vietnamese.solve(language.is_stopword)

    assert is_stopword("như")
    assert is_stopword("cái")
    assert is_stopword("mà")
    assert not is_stopword("chó")

    pickled_vietnamese = pickle.loads(pickle.dumps(vietnamese))
    eq_(pickled_vietnamese, vietnamese)
