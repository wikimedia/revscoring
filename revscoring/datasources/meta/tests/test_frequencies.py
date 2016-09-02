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
pos_delta = frequencies.positive(delta, name="pos_delta")
neg_delta = frequencies.negative(delta, name="neg_delta")
neg_abs_delta = frequencies.negative(
    delta, absolute=True, name="neg_abs_delta")

prop_delta = frequencies.prop_delta(old_ft, delta, name="prop_delta")


def test_table():
    cache = {new_tokens: ["a"] * 3 + ["b"] * 2 + ["c"] * 45}
    eq_(solve(new_ft, cache=cache),
        {'a': 3, 'b': 2, 'c': 45})

    eq_(pickle.loads(pickle.dumps(new_ft)),
        new_ft)


def test_delta():
    cache = {old_tokens: ["a"] * 3 + ["b"] * 2 + ["c"] * 45,
             new_tokens: ["a"] * 1 + ["b"] * 5 + ["d"] * 3}
    eq_(solve(delta, cache=cache),
        {'a': -2, 'b': 3, 'c': -45, 'd': 3})

    eq_(pickle.loads(pickle.dumps(delta)),
        delta)


def test_prop_delta():
    cache = {old_tokens: ["a"] * 3 + ["b"] * 2 + ["c"] * 45 + ["e"] * 2,
             new_tokens: ["a"] * 1 + ["b"] * 5 + ["d"] * 3 + ["e"] * 3}

    pd = solve(prop_delta, cache=cache)
    eq_(pd.keys(), {'a', 'b', 'c', 'd', 'e'})
    eq_(round(pd['a'], 2), -0.67)
    eq_(round(pd['b'], 2), 1)
    eq_(round(pd['c'], 2), -1)
    eq_(round(pd['d'], 2), 3)
    eq_(round(pd['e'], 2), 0.33)

    eq_(pickle.loads(pickle.dumps(prop_delta)),
        prop_delta)


def test_positive():
    cache = {old_tokens: ["a"] * 3 + ["b"] * 2 + ["c"] * 45 + ["e"] * 2,
             new_tokens: ["a"] * 1 + ["b"] * 5 + ["d"] * 3 + ["e"] * 3}
    eq_(solve(pos_delta, cache=cache),
        {'b': 3, 'd': 3, 'e': 1})


def test_negative():
    cache = {old_tokens: ["a"] * 3 + ["b"] * 2 + ["c"] * 45 + ["e"] * 2,
             new_tokens: ["a"] * 1 + ["b"] * 5 + ["d"] * 3 + ["e"] * 3}
    eq_(solve(neg_delta, cache=cache),
        {'a': -2, 'c': -45})

    cache = {old_tokens: ["a"] * 3 + ["b"] * 2 + ["c"] * 45 + ["e"] * 2,
             new_tokens: ["a"] * 1 + ["b"] * 5 + ["d"] * 3 + ["e"] * 3}
    eq_(solve(neg_abs_delta, cache=cache),
        {'a': 2, 'c': 45})
