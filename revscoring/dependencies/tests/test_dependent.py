from nose.tools import eq_

from ..dependent import Dependent


def test_dependent():

    foobar1 = Dependent("foobar", lambda: "foobar1")
    foobar2 = Dependent("foobar", lambda: "foobar2")

    eq_(foobar1, foobar2)

    eq_(hash(foobar1), hash(foobar2))

    assert foobar1 in {foobar2}
