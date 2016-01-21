import pickle

from nose.tools import eq_

from ..datasource import Datasource


def check_datasource(ds):
    assert isinstance(ds, Datasource)
    eq_(pickle.loads(pickle.dumps(ds)), ds)
