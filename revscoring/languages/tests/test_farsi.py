from nose.tools import eq_

from ..farsi import is_misspelled


def test_language():
    assert is_misspelled()("Notafarsiword")
    assert not is_misspelled()("مهم")
