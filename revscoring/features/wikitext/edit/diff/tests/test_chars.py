import pickle

from deltas import Delete, Equal, Insert
from nose.tools import eq_

from .. import chars
from ......datasources.revision_oriented import revision
from ......dependencies import solve


def test_chars():
    cache = {revision.parent.text: "This is some nice text.",
             revision.text: "This is some more text."}

    eq_(solve(chars.chars_added, cache=cache), 4)
    eq_(solve(chars.chars_removed, cache=cache), 4)

    eq_(pickle.loads(pickle.dumps(chars.chars_added)),
        chars.chars_added)
    eq_(pickle.loads(pickle.dumps(chars.chars_removed)),
        chars.chars_removed)


def test_numeric_chars():
    cache = {revision.parent.text: "This is some 45 nice text.",
             revision.text: "This is some more 5000 text."}

    eq_(solve(chars.numeric_chars_added, cache=cache), 4)
    eq_(solve(chars.numeric_chars_removed, cache=cache), 2)

    eq_(pickle.loads(pickle.dumps(chars.numeric_chars_added)),
        chars.numeric_chars_added)
    eq_(pickle.loads(pickle.dumps(chars.numeric_chars_removed)),
        chars.numeric_chars_removed)


def test_whitespace_chars():
    cache = {revision.parent.text: "This is some\tnice text.",
             revision.text: "This is some\nmore\ntext."}

    eq_(solve(chars.whitespace_chars_added, cache=cache), 2)
    eq_(solve(chars.whitespace_chars_removed, cache=cache), 2)

    eq_(pickle.loads(pickle.dumps(chars.whitespace_chars_added)),
        chars.whitespace_chars_added)
    eq_(pickle.loads(pickle.dumps(chars.whitespace_chars_removed)),
        chars.whitespace_chars_removed)


def test_markup_chars():
    cache = {revision.parent.text: "This is some {{nice}} text.",
             revision.text: "This is [[some|more]] text."}

    eq_(solve(chars.markup_chars_added, cache=cache), 4)
    eq_(solve(chars.markup_chars_removed, cache=cache), 4)

    eq_(pickle.loads(pickle.dumps(chars.markup_chars_added)),
        chars.markup_chars_added)
    eq_(pickle.loads(pickle.dumps(chars.markup_chars_removed)),
        chars.markup_chars_removed)


def test_cjk_chars():
    cache = {revision.parent.text: "This is 55 {{るは}} a string.",
             revision.text: "This is 56 [[壌のは]] a string."}

    eq_(solve(chars.cjk_chars_added, cache=cache), 2)
    eq_(solve(chars.cjk_chars_removed, cache=cache), 1)

    eq_(pickle.loads(pickle.dumps(chars.cjk_chars_added)),
        chars.cjk_chars_added)
    eq_(pickle.loads(pickle.dumps(chars.cjk_chars_removed)),
        chars.cjk_chars_removed)


def test_cjk_chars():
    cache = {revision.parent.text: "This is 55 {{るは}} a string.",
             revision.text: "This is 56 [[壌のは]] a string."}

    eq_(solve(chars.cjk_chars_added, cache=cache), 2)
    eq_(solve(chars.cjk_chars_removed, cache=cache), 1)

    eq_(pickle.loads(pickle.dumps(chars.cjk_chars_added)),
        chars.cjk_chars_added)
    eq_(pickle.loads(pickle.dumps(chars.cjk_chars_removed)),
        chars.cjk_chars_removed)


def test_entity_chars():
    cache = {revision.parent.text: "This is &nsbp; not a string.",
             revision.text: "This is &middot; too a string."}

    eq_(solve(chars.entity_chars_added, cache=cache), 8)
    eq_(solve(chars.entity_chars_removed, cache=cache), 6)

    eq_(pickle.loads(pickle.dumps(chars.entity_chars_added)),
        chars.entity_chars_added)
    eq_(pickle.loads(pickle.dumps(chars.entity_chars_removed)),
        chars.entity_chars_removed)


def test_url_chars():
    cache = {revision.parent.text: "This is https://google.com not a string.",
             revision.text: "This //google.com mailto:aaron@bar.com string."}

    eq_(solve(chars.url_chars_added, cache=cache), 32)
    eq_(solve(chars.url_chars_removed, cache=cache), 18)

    eq_(pickle.loads(pickle.dumps(chars.url_chars_added)),
        chars.url_chars_added)
    eq_(pickle.loads(pickle.dumps(chars.url_chars_removed)),
        chars.url_chars_removed)


def test_word_chars():
    cache = {revision.parent.text: "This is 55 not string.",
             revision.text: "This is 56 too a string."}

    eq_(solve(chars.word_chars_added, cache=cache), 4)
    eq_(solve(chars.word_chars_removed, cache=cache), 3)

    eq_(pickle.loads(pickle.dumps(chars.word_chars_added)),
        chars.word_chars_added)
    eq_(pickle.loads(pickle.dumps(chars.word_chars_removed)),
        chars.word_chars_removed)


def test_uppercase_word_chars():
    cache = {revision.parent.text: "This is 55 NOT string.",
             revision.text: "This IS 56 TOO a string."}

    eq_(solve(chars.uppercase_word_chars_added, cache=cache), 5)
    eq_(solve(chars.uppercase_word_chars_removed, cache=cache), 3)

    eq_(pickle.loads(pickle.dumps(chars.uppercase_word_chars_added)),
        chars.uppercase_word_chars_added)
    eq_(pickle.loads(pickle.dumps(chars.uppercase_word_chars_removed)),
        chars.uppercase_word_chars_removed)


def test_punctuation_chars():
    cache = {revision.parent.text: "This is, 55 NOT string.",
             revision.text: "This IS 56 TOO a string."}

    eq_(solve(chars.punctuation_chars_added, cache=cache), 0)
    eq_(solve(chars.punctuation_chars_removed, cache=cache), 1)

    eq_(pickle.loads(pickle.dumps(chars.punctuation_chars_added)),
        chars.punctuation_chars_added)
    eq_(pickle.loads(pickle.dumps(chars.punctuation_chars_removed)),
        chars.punctuation_chars_removed)


def test_break_chars():
    cache = {revision.parent.text: "This is, 55\n\nNOT\n\nstring.",
             revision.text: "This IS 56 TOO\n\na string."}

    eq_(solve(chars.break_chars_added, cache=cache), 0)
    eq_(solve(chars.break_chars_removed, cache=cache), 2)

    eq_(pickle.loads(pickle.dumps(chars.break_chars_added)),
        chars.break_chars_added)
    eq_(pickle.loads(pickle.dumps(chars.break_chars_removed)),
        chars.break_chars_removed)


def test_longest_repeated_char_added():
    cache = {revision.parent.text: "This is words.",
             revision.text: "This is aaaa words. kkkkkkkkkkkk"}

    eq_(solve(chars.longest_repeated_char_added, cache=cache), 12)

    eq_(pickle.loads(pickle.dumps(chars.longest_repeated_char_added)),
        chars.longest_repeated_char_added)
