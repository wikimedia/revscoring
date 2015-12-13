import re

from nose.tools import eq_

from ....dependencies import solve
from ...datasource import Datasource
from ..filters import TokensMatching

tokens = Datasource("tokens")

foo_tokens = TokensMatching("foo_tokens", tokens, "foo")
foo_case_tokens = TokensMatching("foo_case_tokens", tokens, re.compile("foo"))


def test_tokens_matching():
    cache = {tokens: ["foo", "bar", "FOO"]}
    eq_(solve(foo_tokens, cache=cache),
        ["foo", "FOO"])

    eq_(solve(foo_case_tokens, cache=cache),
        ["foo"])
