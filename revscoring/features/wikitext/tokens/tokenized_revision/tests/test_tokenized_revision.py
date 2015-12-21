import pickle

from nose.tools import eq_

from ......datasources import Datasource
from ......dependencies import solve
from ...tokenized import tokenized
from ..tokenized_revision import TokenizedRevision

my_text = Datasource("my_text")

my_tokens = tokenized(my_text)

text = """
This is an m80.  It has 50 grams of TNT. Here's some japanese:
修造のための勧進を担った組織の総称。[//google.com?foo=bar hats]
I can use &middot; and &nbsp;.  But [[can]] I {{foo}} a {{bar}}?

I guess we'll never know.
"""


def test_tokens():

    tokens = TokenizedRevision("test_tokenized_revision",
                               my_tokens)

    eq_(solve(tokens.tokens, cache={my_text: text}), 97)
    eq_(pickle.loads(pickle.dumps(tokens.tokens)), tokens.tokens)

    eq_(solve(tokens.datasources.numbers, cache={my_text: text}), ['50'])
    eq_(pickle.loads(pickle.dumps(tokens.numbers)), tokens.numbers)

    eq_(solve(tokens.whitespaces, cache={my_text: text}), 32)
    eq_(pickle.loads(pickle.dumps(tokens.whitespaces)), tokens.whitespaces)

    eq_(solve(tokens.datasources.markups, cache={my_text: text}),
        ['[', ']', '[[', ']]', '{{', '}}', '{{', '}}'])
    eq_(pickle.loads(pickle.dumps(tokens.markups)), tokens.markups)

    eq_(solve(tokens.datasources.cjks, cache={my_text: text}),
        list("修造のための勧進を担った組織の総称"))
    eq_(pickle.loads(pickle.dumps(tokens.cjks)), tokens.cjks)

    eq_(solve(tokens.datasources.entities, cache={my_text: text}),
        ['&middot;', '&nbsp;'])
    eq_(pickle.loads(pickle.dumps(tokens.entities)), tokens.entities)

    eq_(solve(tokens.datasources.urls, cache={my_text: text}),
        ['//google.com?foo=bar'])
    eq_(pickle.loads(pickle.dumps(tokens.urls)), tokens.urls)

    eq_(solve(tokens.datasources.words, cache={my_text: text}),
        ['This', 'is', 'an', 'm80', 'It', 'has', 'grams', 'of', 'TNT',
         'Here\'s', 'some', 'japanese', 'hats', 'I', 'can', 'use', 'and',
         'But', 'can', 'I', 'foo', 'a', 'bar', 'I', 'guess', 'we\'ll', 'never',
         'know'])
    eq_(pickle.loads(pickle.dumps(tokens.words)), tokens.words)
    eq_(solve(tokens.datasources.word_frequency, cache={my_text: text}),
        {'an': 1, 'never': 1, 'can': 2, 'hats': 1, 'foo': 1, 'but': 1,
         'some': 1, 'of': 1, 'this': 1, 'i': 3, 'a': 1, 'it': 1, 'bar': 1,
         'and': 1, "we'll": 1, 'guess': 1, 'grams': 1, 'know': 1, "here's": 1,
         'tnt': 1, 'is': 1, 'has': 1, 'm80': 1, 'japanese': 1, 'use': 1})

    eq_(solve(tokens.datasources.uppercase_words, cache={my_text: text}),
         ['TNT'])
    eq_(pickle.loads(pickle.dumps(tokens.uppercase_words)),
         tokens.uppercase_words)
    eq_(solve(tokens.datasources.uppercase_word_frequency,
        cache={my_text: text}),
         {'TNT': 1})

    eq_(solve(tokens.datasources.punctuations, cache={my_text: text}),
        ['.', '.', ':', '。', '.', '?', '.'])
    eq_(pickle.loads(pickle.dumps(tokens.punctuations)), tokens.punctuations)
    eq_(solve(tokens.datasources.punctuation_frequency, cache={my_text: text}),
        {'.': 4, ':': 1, '?': 1, '。': 1})
