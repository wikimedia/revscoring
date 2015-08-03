from nose.tools import eq_

from .. import language, turkish


def test_language():

    is_badword = turkish.solve(language.is_badword)

    assert is_badword("Mal")
    assert is_badword("orospu çocuğu")
    assert not is_badword("Resim")

    is_stopword = turkish.solve(language.is_stopword)

    assert is_stopword("bazı")
    assert is_stopword("O")
    assert not is_stopword("Güzergah")
