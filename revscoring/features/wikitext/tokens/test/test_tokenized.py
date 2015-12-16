import pickle

from nose.tools import eq_

from .....datasources import Datasource
from .....dependencies import solve
from ..tokenized import tokenized

a_text = Datasource("a_text")

a_tokens = tokenized(a_text)


def test_tokenized():
    eq_(solve(a_tokens, cache={a_text: "foo bar"}),
        ['foo', ' ', 'bar'])

    eq_(pickle.loads(pickle.dumps(a_tokens)), a_tokens)
