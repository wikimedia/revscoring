from nose.tools import eq_

from ..turkish import is_badword, is_stopword


def test_language():
    assert is_badword()("Mal")
    assert is_badword()("orospu çocuğu")
    assert not is_badword()("Resim")
    
    assert is_stopword()("bazı")
    assert is_stopword()("O")
    assert not is_stopword()("Güzergah")
