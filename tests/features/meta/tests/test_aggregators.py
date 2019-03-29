import pickle

from revscoring.datasources import Datasource
from revscoring.dependencies import solve
from revscoring.features.meta import aggregators


def test_sum():
    my_list = Datasource("my_list")
    my_sum = aggregators.sum(my_list)
    cache = {my_list: [1, 2, 3, 4]}
    assert solve(my_sum, cache=cache) == 10
    cache = {my_list: []}
    assert solve(my_sum, cache=cache) == 0
    cache = {my_list: None}
    assert solve(my_sum, cache=cache) == 0
    assert str(my_sum) == "feature.sum(<datasource.my_list>)"

    assert pickle.loads(pickle.dumps(my_sum)) == my_sum


def test_sum_vectors():
    my_list = Datasource("my_list")
    my_sum = aggregators.sum(my_list, vector=True)
    cache = {my_list: [[1, 2, 3], [4, 5, 6]]}
    assert all(a == b for a, b in
               zip(solve(my_sum, cache=cache), [5, 7, 9]))
    cache = {my_list: [[]]}
    assert solve(my_sum, cache=cache) == [0]
    cache = {my_list: [None]}
    assert solve(my_sum, cache=cache) == [0]
    assert str(my_sum) == "feature_vector.sum(<datasource.my_list>)"

    assert pickle.loads(pickle.dumps(my_sum)) == my_sum


def test_min():
    my_list = Datasource("my_list")
    my_min = aggregators.min(my_list)
    cache = {my_list: [1, 2, 3, 4]}
    assert solve(my_min, cache=cache) == 1
    cache = {my_list: []}
    assert solve(my_min, cache=cache) == 0
    cache = {my_list: None}
    assert solve(my_min, cache=cache) == 0

    assert pickle.loads(pickle.dumps(my_min)) == my_min


def test_min_vectors():
    my_list = Datasource("my_list")
    my_min = aggregators.min(my_list, vector=True)
    cache = {my_list: [[1, 2, 3], [4, 5, 6]]}
    assert all(a == b for a, b in
               zip(solve(my_min, cache=cache), [1, 2, 3]))
    cache = {my_list: [[]]}
    assert solve(my_min, cache=cache) == [0]
    cache = {my_list: [None]}
    assert solve(my_min, cache=cache) == [0]

    assert pickle.loads(pickle.dumps(my_min)) == my_min


def test_max():
    my_list = Datasource("my_list")
    my_max = aggregators.max(my_list)
    cache = {my_list: [1, 2, 3, 4]}
    assert solve(my_max, cache=cache) == 4
    cache = {my_list: []}
    assert solve(my_max, cache=cache) == 0
    cache = {my_list: None}
    assert solve(my_max, cache=cache) == 0

    assert pickle.loads(pickle.dumps(my_max)) == my_max


def test_max_vectors():
    my_list = Datasource("my_list")
    my_max = aggregators.max(my_list, vector=True)
    cache = {my_list: [[1, 2, 3], [4, 5, 6]]}
    assert all(a == b for a, b in
               zip(solve(my_max, cache=cache), [4, 5, 6]))
    cache = {my_list: [[]]}
    assert solve(my_max, cache=cache) == [0]
    cache = {my_list: [None]}
    assert solve(my_max, cache=cache) == [0]

    assert pickle.loads(pickle.dumps(my_max)) == my_max


def test_len():
    my_list = Datasource("my_list")
    my_len = aggregators.len(my_list)
    cache = {my_list: [1, 2, 3, 4]}
    assert solve(my_len, cache=cache) == 4
    cache = {my_list: []}
    assert solve(my_len, cache=cache) == 0
    cache = {my_list: None}
    assert solve(my_len, cache=cache) == 0

    assert pickle.loads(pickle.dumps(my_len)) == my_len


def test_len_vectors():
    my_list = Datasource("my_list")
    my_len = aggregators.len(my_list, vector=True)
    cache = {my_list: [[1, 2, 3], [4, 5, 6]]}
    assert all(a == b for a, b in
               zip(solve(my_len, cache=cache), [2, 2, 2]))
    cache = {my_list: [[]]}
    assert solve(my_len, cache=cache) == [0]
    cache = {my_list: [None]}
    assert solve(my_len, cache=cache) == [0]

    assert pickle.loads(pickle.dumps(my_len)) == my_len


def test_mean_vectors():
    my_list = Datasource("my_list")
    my_mean = aggregators.mean(my_list, vector=True)
    cache = {my_list: [[1, 2, 3], [4, 5, 6]]}
    assert all(a == b for a, b in
               zip(solve(my_mean, cache=cache), [2.5, 3.5, 4.5]))
    cache = {my_list: [[]]}
    assert solve(my_mean, cache=cache) == [0]
    cache = {my_list: [None]}
    assert solve(my_mean, cache=cache) == [0]

    assert pickle.loads(pickle.dumps(my_mean)) == my_mean
