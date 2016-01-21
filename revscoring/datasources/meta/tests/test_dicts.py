import pickle

from nose.tools import eq_

from .. import dicts
from ....dependencies import solve
from ...datasource import Datasource

my_dict = Datasource("my_dict")

my_keys = dicts.keys(my_dict)
my_values = dicts.values(my_dict)


def test_dict_keys():
    cache = {my_dict: {"foo": 1, "bar": 2}}
    eq_(set(solve(my_keys, cache=cache)), {"foo", "bar"})
    cache = {my_dict: None}
    eq_(set(solve(my_keys, cache=cache)), set())

    eq_(pickle.loads(pickle.dumps(my_keys)), my_keys)


def test_dict_values():
    cache = {my_dict: {"foo": 1, "bar": 2}}
    eq_(set(solve(my_values, cache=cache)), {1, 2})
    cache = {my_dict: None}
    eq_(set(solve(my_values, cache=cache)), set())

    eq_(pickle.loads(pickle.dumps(my_values)), my_values)
