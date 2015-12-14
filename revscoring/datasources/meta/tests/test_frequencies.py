import pickle

from nose.tools import eq_

from .. import frequencies
from ....dependencies import solve
from ...datasource import Datasource

old_tokens = Datasource("old_tokens")
new_tokens = Datasource("new_tokens")

old_ft = frequencies.table(old_tokens, name="old_ft")
new_ft = frequencies.table(new_tokens, name="new_ft")

delta = frequencies.delta(old_ft, new_ft, name="delta")

prop_delta = frequencies.prop_delta(old_ft, delta, name="prop_delta")


def test_token_frequency():
    cache = {new_tokens: ["a"] * 3 + ["b"] * 2 + ["c"] * 45}
    eq_(solve(new_ft, cache=cache),
        {'a': 3, 'b': 2, 'c': 45})

    eq_(pickle.loads(pickle.dumps(new_ft)),
        new_ft)


def test_token_frequency_diff():
    cache = {old_tokens: ["a"] * 3 + ["b"] * 2 + ["c"] * 45,
             new_tokens: ["a"] * 1 + ["b"] * 5 + ["d"] * 3}
    eq_(solve(delta, cache=cache),
        {'a': -2, 'b': 3, 'c': -45, 'd': 3})

    eq_(pickle.loads(pickle.dumps(delta)),
        delta)


def test_proportional_token_frequency_diff():
    cache = {old_tokens: ["a"] * 3 + ["b"] * 2 + ["c"] * 45,
             new_tokens: ["a"] * 1 + ["b"] * 5 + ["d"] * 3}
    eq_(solve(prop_delta, cache=cache),
        {'a': -2 / 3, 'b': 3 / 2, 'c': -1, 'd': 3})

    eq_(pickle.loads(pickle.dumps(prop_delta)),
        prop_delta)
