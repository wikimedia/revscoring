import pickle

from revscoring.datasources.datasource import Datasource
from revscoring.datasources.meta import gramming
from revscoring.dependencies import solve

my_tokens = Datasource("my_tokens")
my_grams = gramming.gram(my_tokens, grams=[(0,), (0, 2)])


def test_gramming():
    assert (solve(my_grams, cache={my_tokens: ["one", "two", "three", "four"]}) ==
            [("one",), ("one", "three"), ("two",), ("two", "four"), ("three",),
             ("four",)])

    assert (pickle.loads(pickle.dumps(my_grams)) ==
            my_grams)
