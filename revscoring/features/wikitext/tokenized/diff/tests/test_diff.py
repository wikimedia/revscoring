import pickle

from nose.tools import eq_

from .. import diff
from ......datasources.revision_oriented import revision
from ......dependencies import solve

r_text = revision.text
p_text = revision.parent.text


def test_pickling():
    eq_(pickle.loads(pickle.dumps(diff.token_delta_sum)),
        diff.token_delta_sum)
    eq_(pickle.loads(pickle.dumps(diff.token_delta_increase)),
        diff.token_delta_increase)
    eq_(pickle.loads(pickle.dumps(diff.token_delta_decrease)),
        diff.token_delta_decrease)

    eq_(pickle.loads(pickle.dumps(diff.token_prop_delta_sum)),
        diff.token_prop_delta_sum)
    eq_(pickle.loads(pickle.dumps(diff.token_prop_delta_increase)),
        diff.token_prop_delta_increase)
    eq_(pickle.loads(pickle.dumps(diff.token_prop_delta_decrease)),
        diff.token_prop_delta_decrease)

    eq_(pickle.loads(pickle.dumps(diff.number_delta_sum)),
        diff.number_delta_sum)
    eq_(pickle.loads(pickle.dumps(diff.number_delta_increase)),
        diff.number_delta_increase)
    eq_(pickle.loads(pickle.dumps(diff.number_delta_decrease)),
        diff.number_delta_decrease)

    eq_(pickle.loads(pickle.dumps(diff.number_prop_delta_sum)),
        diff.number_prop_delta_sum)
    eq_(pickle.loads(pickle.dumps(diff.number_prop_delta_increase)),
        diff.number_prop_delta_increase)
    eq_(pickle.loads(pickle.dumps(diff.number_prop_delta_decrease)),
        diff.number_prop_delta_decrease)


def test_diff():
    cache = {p_text: "This is some tokens text with TOKENS.",
             r_text: "This is some TOKENS text tokens tokens!"}

    eq_(solve(diff.datasources.token_delta, cache=cache),
        {'tokens': 1, 'with': -1, '.': -1, '!': 1})
    eq_(solve(diff.datasources.token_prop_delta, cache=cache),
        {'tokens': 1 / 2, 'with': -1, '.': -1, '!': 1})
    eq_(round(solve(diff.token_prop_delta_sum, cache=cache), 2), -0.5)
    eq_(round(solve(diff.token_prop_delta_increase, cache=cache), 2), 1.5)
    eq_(round(solve(diff.token_prop_delta_decrease, cache=cache), 2), -2.0)

    eq_(solve(diff.datasources.word_delta, cache=cache),
        {'tokens': 1, 'with': -1})
    eq_(solve(diff.datasources.word_prop_delta, cache=cache),
        {'tokens': 1 / 3, 'with': -1})
    eq_(round(solve(diff.word_prop_delta_sum, cache=cache), 2), -0.67)
    eq_(round(solve(diff.word_prop_delta_increase, cache=cache), 2), 0.33)
    eq_(round(solve(diff.word_prop_delta_decrease, cache=cache), 2), -1.0)

    cache = {p_text: "This is 45 72 tokens 23 72.",
             r_text: "This is 45 72 hats pants 85 72 72."}
    eq_(solve(diff.datasources.number_delta, cache=cache),
        {'72': 1, '23': -1, '85': 1})
    eq_(solve(diff.datasources.number_prop_delta, cache=cache),
        {'72': 1 / 3, '23': -1, '85': 1})
    eq_(round(solve(diff.number_prop_delta_sum, cache=cache), 2), 0.33)
    eq_(round(solve(diff.number_prop_delta_increase, cache=cache), 2), 1.33)
    eq_(round(solve(diff.number_prop_delta_decrease, cache=cache), 2), -1.0)
