import pickle

from nose.tools import eq_

from .. import revision
from ....datasources import revision_oriented
from ....dependencies import solve

r_text = revision_oriented.revision.text
p_text = revision_oriented.revision.parent.text

text = """
This is an m80.  It has 50 grams of TNT. Here's some japanese:
修造のための勧進を担った組織の総称。[//google.com?foo=bar hats]
I can use &middot; and &nbsp;.  But [[can]] I {{foo}} a {{bar}}?

I guess we'll never know.
"""


def test_tokens():
    eq_(solve(revision.tokens, cache={r_text: text}), 97)
    eq_(pickle.loads(pickle.dumps(revision.tokens)), revision.tokens)


def test_tokens_in_types():
    my_words = revision.datasources.tokens_in_types({"word"})
    eq_(solve(my_words, cache={r_text: text}),
        ['This', 'is', 'an', 'm80', 'It', 'has', 'grams', 'of', 'TNT',
         "Here's", 'some', 'japanese', 'hats', 'I', 'can', 'use', 'and',
         'But', 'can', 'I', 'foo', 'a', 'bar', 'I', 'guess', "we'll", 'never',
         'know'])
    eq_(pickle.loads(pickle.dumps(my_words)), my_words)


def test_tokens_matching():
    my_s_words = revision.datasources.tokens_matching(r"^s")
    eq_(solve(my_s_words, cache={r_text: text}),
        ['some'])
    eq_(pickle.loads(pickle.dumps(my_s_words)), my_s_words)


def test_numbers():
    eq_(solve(revision.datasources.numbers, cache={r_text: text}), ['50'])
    eq_(pickle.loads(pickle.dumps(revision.numbers)), revision.numbers)


def test_whitespaces():
    eq_(solve(revision.whitespaces, cache={r_text: text}), 32)
    eq_(pickle.loads(pickle.dumps(revision.whitespaces)),
        revision.whitespaces)


def test_markups():
    eq_(solve(revision.datasources.markups, cache={r_text: text}),
        ['[', ']', '[[', ']]', '{{', '}}', '{{', '}}'])
    eq_(pickle.loads(pickle.dumps(revision.markups)), revision.markups)


def test_cjks():
    eq_(solve(revision.datasources.cjks, cache={r_text: text}),
        list("修造のための勧進を担った組織の総称"))
    eq_(pickle.loads(pickle.dumps(revision.cjks)), revision.cjks)


def test_entities():
    eq_(solve(revision.datasources.entities, cache={r_text: text}),
        ['&middot;', '&nbsp;'])
    eq_(pickle.loads(pickle.dumps(revision.entities)),
        revision.entities)


def test_urls():
    eq_(solve(revision.datasources.urls, cache={r_text: text}),
        ['//google.com?foo=bar'])
    eq_(pickle.loads(pickle.dumps(revision.urls)), revision.urls)


def test_words():
    eq_(solve(revision.datasources.words, cache={r_text: text}),
        ['This', 'is', 'an', 'm80', 'It', 'has', 'grams', 'of', 'TNT',
         'Here\'s', 'some', 'japanese', 'hats', 'I', 'can', 'use', 'and',
         'But', 'can', 'I', 'foo', 'a', 'bar', 'I', 'guess', 'we\'ll', 'never',
         'know'])
    eq_(pickle.loads(pickle.dumps(revision.words)), revision.words)
    eq_(solve(revision.datasources.word_frequency, cache={r_text: text}),
        {'an': 1, 'never': 1, 'can': 2, 'hats': 1, 'foo': 1, 'but': 1,
         'some': 1, 'of': 1, 'this': 1, 'i': 3, 'a': 1, 'it': 1, 'bar': 1,
         'and': 1, "we'll": 1, 'guess': 1, 'grams': 1, 'know': 1, "here's": 1,
         'tnt': 1, 'is': 1, 'has': 1, 'm80': 1, 'japanese': 1, 'use': 1})


def test_uppercase_words():
    eq_(solve(revision.datasources.uppercase_words, cache={r_text: text}),
         ['TNT'])
    eq_(pickle.loads(pickle.dumps(revision.uppercase_words)),
         revision.uppercase_words)
    eq_(solve(revision.datasources.uppercase_word_frequency,
        cache={r_text: text}),
         {'TNT': 1})


def test_punctuations():
    eq_(solve(revision.datasources.punctuations, cache={r_text: text}),
        ['.', '.', ':', '。', '.', '?', '.'])
    eq_(pickle.loads(pickle.dumps(revision.punctuations)),
        revision.punctuations)
    eq_(solve(revision.datasources.punctuation_frequency,
              cache={r_text: text}),
        {'.': 4, ':': 1, '?': 1, '。': 1})


def test_longest_token():
   eq_(solve(revision.longest_token, cache={r_text: text}), 20)

   eq_(pickle.loads(pickle.dumps(revision.longest_token)),
       revision.longest_token)


def test_longest_word():
    eq_(solve(revision.longest_word, cache={r_text: text}), 8)

    eq_(pickle.loads(pickle.dumps(revision.longest_word)),
        revision.longest_word)


def test_diff():
    diff = revision.diff

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

    eq_(solve(diff.datasources.uppercase_word_delta, cache=cache),
        {})
    eq_(solve(diff.datasources.uppercase_word_prop_delta, cache=cache),
        {})
    eq_(round(solve(diff.uppercase_word_prop_delta_sum, cache=cache), 2), 0)
    eq_(round(solve(diff.uppercase_word_prop_delta_increase, cache=cache), 2),
        0)
    eq_(round(solve(diff.uppercase_word_prop_delta_decrease, cache=cache), 2),
        0)

    cache = {p_text: "This is 45 72 tokens 23 72.",
             r_text: "This is 45 72 hats pants 85 72 72."}
    eq_(solve(diff.datasources.number_delta, cache=cache),
        {'72': 1, '23': -1, '85': 1})
    eq_(solve(diff.datasources.number_prop_delta, cache=cache),
        {'72': 1 / 3, '23': -1, '85': 1})
    eq_(round(solve(diff.number_prop_delta_sum, cache=cache), 2), 0.33)
    eq_(round(solve(diff.number_prop_delta_increase, cache=cache), 2), 1.33)
    eq_(round(solve(diff.number_prop_delta_decrease, cache=cache), 2), -1.0)

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
