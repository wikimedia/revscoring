import pickle
import re

from revscoring.datasources.datasource import Datasource
from revscoring.datasources.meta import filters
from revscoring.dependencies import solve

tokens = Datasource("tokens")

foo_tokens = filters.regex_matching("foo", tokens, name="foo_tokens")
foo_case_tokens = filters.regex_matching(re.compile("foo"), tokens,
                                         name="foo_case_tokens")

my_ints = Datasource("my_ints")

positive_ints = filters.positive(my_ints)
negative_ints = filters.negative(my_ints)

not_none_tokens = filters.not_none(tokens, name="not_none_tokens")


def test_regex_matching():
    cache = {tokens: ["foo", "bar", "FOO"]}
    assert (solve(foo_tokens, cache=cache) ==
            ["foo", "FOO"])

    assert (solve(foo_case_tokens, cache=cache) ==
            ["foo"])

    assert pickle.loads(pickle.dumps(foo_tokens)) == foo_tokens
    assert pickle.loads(pickle.dumps(foo_case_tokens)) == foo_case_tokens

    assert foo_tokens != foo_case_tokens


def test_positive():
    cache = {my_ints: [1, 0, -1]}
    assert (solve(positive_ints, cache=cache) ==
            [1])
    assert pickle.loads(pickle.dumps(positive_ints)) == positive_ints

    assert positive_ints != negative_ints


def test_negative():
    cache = {my_ints: [1, 0, -1]}
    assert (solve(negative_ints, cache=cache) ==
            [-1])
    assert pickle.loads(pickle.dumps(negative_ints)) == negative_ints

    assert negative_ints != positive_ints


def test_not_none():
    cache = {tokens: ["foo", None, 1]}
    assert (solve(not_none_tokens, cache=cache) ==
            ["foo", 1])

    assert pickle.loads(pickle.dumps(not_none_tokens)) == not_none_tokens
