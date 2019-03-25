
from revscoring.languages.features.dictionary.util import utf16_cleanup


def test_utf16_cleanup():
    assert (utf16_cleanup("Foobar" + chr(2 ** 16)) ==
            "Foobar\uFFFD")
