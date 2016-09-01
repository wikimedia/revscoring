import pickle

from nose.tools import eq_

from .. import vectorizers
from ....datasources import Datasource
from ....dependencies import solve

my_dict = Datasource("my_dict")


class KeysDict(Datasource):

    def __init__(self, name, keys):
        super().__init__(name)
        self._keys = keys

    def keys(self):
        return self._keys

my_keys_dict = KeysDict("my_keys_dict", ["a", "b", "c"])


def test_vectorize():
    my_vector = vectorizers.vectorize(
        my_dict, ["a", "b", "c"], returns=int)

    eq_(solve(my_vector, cache={my_dict: {"a": 5}}),
        [5, 0, 0])
    eq_(solve(my_vector, cache={my_dict: {"d": 5}}),
        [0, 0, 0])
    eq_(solve(my_vector, cache={my_dict: {"a": 1, "b": 2, "c": 3}}),
        [1, 2, 3])

    eq_(pickle.loads(pickle.dumps(my_vector)), my_vector)

    my_keys_vector = vectorizers.vectorize(my_keys_dict, returns=int)

    eq_(solve(my_keys_vector, cache={my_keys_dict: {"a": 1, "b": 2, "c": 3}}),
        [1, 2, 3])
