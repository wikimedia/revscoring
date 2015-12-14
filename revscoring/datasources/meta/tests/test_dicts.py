import pickle

from nose.tools import eq_

from ....dependencies import solve
from ...datasource import Datasource
from ..dicts import dict_keys, dict_values

my_dict = Datasource("my_dict")

my_keys = dict_keys(my_dict)
my_values = dict_values(my_dict)


def test_dict_keys():
    cache = {my_dict: {"foo": 1, "bar": 2}}
    eq_(set(solve(my_keys, cache=cache)), {"foo", "bar"})

    eq_(pickle.loads(pickle.dumps(my_keys)), my_keys)

def test_dict_values():
    cache = {my_dict: {"foo": 1, "bar": 2}}
    eq_(set(solve(my_values, cache=cache)), {1, 2})

    eq_(pickle.loads(pickle.dumps(my_values)), my_values)
