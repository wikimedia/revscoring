from nose.tools import eq_

from .. import language, persian


def test_language():

    is_misspelled = persian.solve(language.is_misspelled)

    assert is_misspelled("Notafarsiword")
    assert not is_misspelled("مهم")

    is_badword = persian.solve(language.is_badword)

    assert is_badword("کیرم")
    assert not is_badword("hat")
