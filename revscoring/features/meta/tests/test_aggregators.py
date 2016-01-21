import pickle

from nose.tools import eq_

from .. import aggregators
from ....datasources import Datasource
from ....dependencies import solve


def test_sum():
    my_list = Datasource("my_list")
    my_sum = aggregators.sum(my_list)
    cache = {my_list: [1, 2, 3, 4]}
    eq_(solve(my_sum, cache=cache), 10)
    cache = {my_list: []}
    eq_(solve(my_sum, cache=cache), 0)
    cache = {my_list: None}
    eq_(solve(my_sum, cache=cache), 0)

    eq_(pickle.loads(pickle.dumps(my_sum)), my_sum)


def test_min():
    my_list = Datasource("my_list")
    my_min = aggregators.min(my_list)
    cache = {my_list: [1, 2, 3, 4]}
    eq_(solve(my_min, cache=cache), 1)
    cache = {my_list: []}
    eq_(solve(my_min, cache=cache), 0)
    cache = {my_list: None}
    eq_(solve(my_min, cache=cache), 0)

    eq_(pickle.loads(pickle.dumps(my_min)), my_min)


def test_max():
    my_list = Datasource("my_list")
    my_max = aggregators.max(my_list)
    cache = {my_list: [1, 2, 3, 4]}
    eq_(solve(my_max, cache=cache), 4)
    cache = {my_list: []}
    eq_(solve(my_max, cache=cache), 0)
    cache = {my_list: None}
    eq_(solve(my_max, cache=cache), 0)

    eq_(pickle.loads(pickle.dumps(my_max)), my_max)


def test_len():
    my_list = Datasource("my_list")
    my_len = aggregators.len(my_list)
    cache = {my_list: [1, 2, 3, 4]}
    eq_(solve(my_len, cache=cache), 4)
    cache = {my_list: []}
    eq_(solve(my_len, cache=cache), 0)
    cache = {my_list: None}
    eq_(solve(my_len, cache=cache), 0)

    eq_(pickle.loads(pickle.dumps(my_len)), my_len)
