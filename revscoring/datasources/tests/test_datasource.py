import pickle

from nose.tools import eq_

from ..datasource import Datasource


def test_datasource():

    d = Datasource("d")

    eq_(pickle.loads(pickle.dumps(d)), d)
