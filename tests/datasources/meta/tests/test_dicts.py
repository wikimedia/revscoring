import pickle

from revscoring.datasources.datasource import Datasource
from revscoring.datasources.meta import dicts
from revscoring.dependencies import solve

my_dict = Datasource("my_dict")

my_keys = dicts.keys(my_dict)
my_values = dicts.values(my_dict)


def test_dict_keys():
    cache = {my_dict: {"foo": 1, "bar": 2}}
    assert set(solve(my_keys, cache=cache)) == {"foo", "bar"}
    cache = {my_dict: None}
    assert set(solve(my_keys, cache=cache)) == set()

    assert pickle.loads(pickle.dumps(my_keys)) == my_keys


def test_dict_values():
    cache = {my_dict: {"foo": 1, "bar": 2}}
    assert set(solve(my_values, cache=cache)) == {1, 2}
    cache = {my_dict: None}
    assert set(solve(my_values, cache=cache)) == set()

    assert pickle.loads(pickle.dumps(my_values)) == my_values
