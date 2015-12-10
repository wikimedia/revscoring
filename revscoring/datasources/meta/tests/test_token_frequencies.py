import pickle

from nose.tools import eq_

from ....dependencies import solve
from ...datasource import Datasource
from ..token_frequencies import (ProportionalTokenFrequencyDiff,
                                 TokenFrequency, TokenFrequencyDiff)

old_tokens = Datasource("old_tokens")
new_tokens = Datasource("new_tokens")


def return_foo():
    return "foo"

old_tf = TokenFrequency("old_tf", old_tokens, if_none=return_foo)
new_tf = TokenFrequency("new_tf", new_tokens, if_none=return_foo)

tf_diff = TokenFrequencyDiff("tf_diff", old_tf, new_tf)

prop_tf_diff = ProportionalTokenFrequencyDiff("prop_tf_diff", old_tf, tf_diff)


def test_token_frequency():
    cache = {new_tokens: ["a"] * 3 + ["b"] * 2 + ["c"] * 45}
    eq_(solve(new_tf, cache=cache),
        {
            'a': 3,
            'b': 2,
            'c': 45
        })

    cache = {new_tokens: None}
    eq_(solve(new_tf, cache=cache),
        "foo")

    eq_(pickle.loads(pickle.dumps(new_tf)),
        new_tf)


def test_token_frequency_diff():
    cache = {old_tokens: ["a"] * 3 + ["b"] * 2 + ["c"] * 45,
             new_tokens: ["a"] * 1 + ["b"] * 5 + ["d"] * 3}
    eq_(solve(tf_diff, cache=cache),
        {
            'a': -2,
            'b': 3,
            'c': -45,
            'd': 3
        })

    eq_(pickle.loads(pickle.dumps(tf_diff)),
        tf_diff)


def test_proportional_token_frequency_diff():
    cache = {old_tokens: ["a"] * 3 + ["b"] * 2 + ["c"] * 45,
             new_tokens: ["a"] * 1 + ["b"] * 5 + ["d"] * 3}
    eq_(solve(prop_tf_diff, cache=cache),
        {
            'a': -2/3,
            'b': 3/2,
            'c': -1,
            'd': 3
        })

    eq_(pickle.loads(pickle.dumps(prop_tf_diff)),
        prop_tf_diff)
