import pickle

from revscoring.datasources.datasource import Datasource
from revscoring.datasources.meta import hashing
from revscoring.dependencies import solve

my_tokens = Datasource("my_tokens")
my_hashes = hashing.hash(my_tokens, n=10)


def test_hashing():
    hashes = solve(
        my_hashes, cache={my_tokens: [("one", "two"), "two", "three", "four"]})

    assert len(hashes) == 4
    assert max(hashes) <= 10, str(max(hashes))

    hashes_again = solve(
        my_hashes, cache={my_tokens: [("one", "two"), "two", "three", "four"]})

    assert hashes == hashes_again

    assert (pickle.loads(pickle.dumps(my_hashes)) ==
            my_hashes)
