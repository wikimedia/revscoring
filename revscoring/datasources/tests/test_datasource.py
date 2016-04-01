import pickle

from nose.tools import eq_

from ...dependencies import solve
from ..datasource import Datasource


def test_datasource():

    d = Datasource("d")

    eq_(pickle.loads(pickle.dumps(d)), d)

    eq_(solve(d, cache={d: "foo"}), "foo")

    eq_(solve(d, cache={"datasource.d": "foo"}), "foo")

    eq_(str(d), "datasource.d")
    eq_(repr(d), "<datasource.d>")
