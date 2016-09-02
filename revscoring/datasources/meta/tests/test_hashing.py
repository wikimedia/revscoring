import pickle

from nose.tools import eq_

from .. import hashing
from ....dependencies import solve
from ...datasource import Datasource

my_tokens = Datasource("my_tokens")
my_hashes = hashing.hash(my_tokens, n=10)


def test_hashing():
    hashes = solve(
        my_hashes, cache={my_tokens: [("one", "two"), "two", "three", "four"]})

    eq_(len(hashes), 4)
    assert max(hashes) <= 10, str(max(hashes))

    hashes_again = solve(
        my_hashes, cache={my_tokens: [("one", "two"), "two", "three", "four"]})

    eq_(hashes, hashes_again)

    eq_(pickle.loads(pickle.dumps(my_hashes)),
        my_hashes)
