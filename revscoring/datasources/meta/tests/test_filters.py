import pickle
import re

from nose.tools import eq_

from ....dependencies import solve
from ...datasource import Datasource
from ..filters import negative, positive, regex_matching

tokens = Datasource("tokens")

foo_tokens = regex_matching("foo", tokens, name="foo_tokens")
foo_case_tokens = regex_matching(re.compile("foo"), tokens,
                                 name="foo_case_tokens")

my_ints = Datasource("my_ints")

positive_ints = positive(my_ints)
negative_ints = negative(my_ints)


def test_regex_matching():
    cache = {tokens: ["foo", "bar", "FOO"]}
    eq_(solve(foo_tokens, cache=cache),
        ["foo", "FOO"])

    eq_(solve(foo_case_tokens, cache=cache),
        ["foo"])

    eq_(pickle.loads(pickle.dumps(foo_tokens)), foo_tokens)
    eq_(pickle.loads(pickle.dumps(foo_case_tokens)), foo_case_tokens)

"""
def test_positive():
    cache = {my_ints: [1, 0, -1]}
    eq_(solve(positive_ints, cache=cache),
        [1])
    eq_(pickle.loads(pickle.dumps(positive_ints)), positive_ints)


def test_negative():
    cache = {my_ints: [1, 0, -1]}
    eq_(solve(negative_ints, cache=cache),
        [-1])
    eq_(pickle.loads(pickle.dumps(negative_ints)), negative_ints)
"""
