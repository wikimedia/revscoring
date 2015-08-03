from nose.tools import eq_

from .. import language, vietnamese


def test_language():

    is_badword = vietnamese.solve(language.is_badword)

    assert is_badword("đít")
    assert is_badword("ỉa")
    assert is_badword("Ỉa")
    assert is_badword("assface")
    assert not is_badword("trứng")
    assert not is_badword("bass")

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
