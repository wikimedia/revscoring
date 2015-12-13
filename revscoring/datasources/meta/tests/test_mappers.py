from nose.tools import eq_

from ....dependencies import solve
from ...datasource import Datasource
from ..mappers import ItemMapper, LowerCase


def extract_first_char(token):
    return token[:1]

tokens = Datasource("tokens")

lower_case = LowerCase("lower_tokens", tokens)
first_char = ItemMapper("lower_tokens", tokens, extract_first_char)


def test_item_mapper():
    cache = {tokens: ["alpha", "bravo", "charlie", "delta"]}
    eq_(solve(first_char, cache=cache),
        ["a", "b", "c", "d"])


def test_lower_case():
    cache = {tokens: ["foo", "Bar", "FOO"]}
    eq_(solve(lower_case, cache=cache),
        ["foo", "bar", "foo"])
