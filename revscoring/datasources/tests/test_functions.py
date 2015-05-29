from nose.tools import eq_

from ...features import Feature
from ..datasource import Datasource
from ..functions import dig


def test_dig():
    foo = Datasource("foo")
    bar = Datasource("bar")
    foobar = Feature("foobar", lambda foo, bar: len(foo+bar), returns=int,
                     depends_on=[foo, bar])

    eq_(set(dig(foobar + 1)), {foo, bar})
