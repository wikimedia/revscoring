import pickle

from nose.tools import eq_

from .. import gramming
from ....dependencies import solve
from ...datasource import Datasource

my_tokens = Datasource("my_tokens")
my_grams = gramming.gram(my_tokens, grams=[(0,), (0, 2)])


def test_gramming():
    eq_(solve(my_grams, cache={my_tokens: ["one", "two", "three", "four"]}),
        [("one",), ("one", "three"), ("two",), ("two", "four"), ("three",),
         ("four",)])

    eq_(pickle.loads(pickle.dumps(my_grams)),
        my_grams)
