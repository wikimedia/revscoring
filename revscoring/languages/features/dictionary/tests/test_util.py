from nose.tools import eq_

from ..util import utf16_cleanup


def test_utf16_cleanup():
    eq_(utf16_cleanup("Foobar" + chr(2 ** 16)),
        "Foobar\uFFFD")
