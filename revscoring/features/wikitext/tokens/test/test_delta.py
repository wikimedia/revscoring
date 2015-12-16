import pickle

from nose.tools import eq_

from .....datasources import Datasource
from .....dependencies import solve
from ..delta import Delta
from ..tokens import Tokens

a_text = Datasource("a_text")
b_text = Datasource("b_text")

a_tokens = Tokens("a_tokens", text_datasource=a_text)
b_tokens = Tokens("b_tokens", text_datasource=b_text)

my_delta = Delta("my_delta", a_tokens, b_tokens)


def test_pickling():
    eq_(pickle.loads(pickle.dumps(my_delta.token_delta_sum)),
        my_delta.token_delta_sum)
    eq_(pickle.loads(pickle.dumps(my_delta.token_delta_increase)),
        my_delta.token_delta_increase)
    eq_(pickle.loads(pickle.dumps(my_delta.token_delta_decrease)),
        my_delta.token_delta_decrease)

    eq_(pickle.loads(pickle.dumps(my_delta.token_prop_delta_sum)),
        my_delta.token_prop_delta_sum)
    eq_(pickle.loads(pickle.dumps(my_delta.token_prop_delta_increase)),
        my_delta.token_prop_delta_increase)
    eq_(pickle.loads(pickle.dumps(my_delta.token_prop_delta_decrease)),
        my_delta.token_prop_delta_decrease)

    eq_(pickle.loads(pickle.dumps(my_delta.number_delta_sum)),
        my_delta.number_delta_sum)
    eq_(pickle.loads(pickle.dumps(my_delta.number_delta_increase)),
        my_delta.number_delta_increase)
    eq_(pickle.loads(pickle.dumps(my_delta.number_delta_decrease)),
        my_delta.number_delta_decrease)

    eq_(pickle.loads(pickle.dumps(my_delta.number_prop_delta_sum)),
        my_delta.number_prop_delta_sum)
    eq_(pickle.loads(pickle.dumps(my_delta.number_prop_delta_increase)),
        my_delta.number_prop_delta_increase)
    eq_(pickle.loads(pickle.dumps(my_delta.number_prop_delta_decrease)),
        my_delta.number_prop_delta_decrease)


def test_diff():
    cache = {a_text: "This is some tokens text with TOKENS.",
             b_text: "This is some TOKENS text tokens tokens!"}

    eq_(solve(my_delta.datasources.token_delta, cache=cache),
        {'tokens': 1, 'with': -1, '.': -1, '!': 1})
    eq_(solve(my_delta.datasources.token_prop_delta, cache=cache),
        {'tokens': 1 / 2, 'with': -1, '.': -1, '!': 1})
    eq_(round(solve(my_delta.token_prop_delta_sum, cache=cache), 2), -0.5)
    eq_(round(solve(my_delta.token_prop_delta_increase, cache=cache), 2), 1.5)
    eq_(round(solve(my_delta.token_prop_delta_decrease, cache=cache), 2), -2.0)

    eq_(solve(my_delta.datasources.word_delta, cache=cache),
        {'tokens': 1, 'with': -1})
    eq_(solve(my_delta.datasources.word_prop_delta, cache=cache),
        {'tokens': 1 / 3, 'with': -1})
    eq_(round(solve(my_delta.word_prop_delta_sum, cache=cache), 2), -0.67)
    eq_(round(solve(my_delta.word_prop_delta_increase, cache=cache), 2), 0.33)
    eq_(round(solve(my_delta.word_prop_delta_decrease, cache=cache), 2), -1.0)

    cache = {a_text: "This is 45 72 tokens 23 72.",
             b_text: "This is 45 72 hats pants 85 72 72."}
    eq_(solve(my_delta.datasources.number_delta, cache=cache),
        {'72': 1, '23': -1, '85': 1})
    eq_(solve(my_delta.datasources.number_prop_delta, cache=cache),
        {'72': 1 / 3, '23': -1, '85': 1})
    eq_(round(solve(my_delta.number_prop_delta_sum, cache=cache), 2), 0.33)
    eq_(round(solve(my_delta.number_prop_delta_increase, cache=cache), 2), 1.33)
    eq_(round(solve(my_delta.number_prop_delta_decrease, cache=cache), 2), -1.0)
