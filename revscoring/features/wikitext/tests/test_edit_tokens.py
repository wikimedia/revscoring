import pickle

from nose.tools import eq_

from .. import revision
from ....datasources import revision_oriented
from ....dependencies import solve

r_text = revision_oriented.revision.text
p_text = revision_oriented.revision.parent.text


def test_tokens():
    cache = {p_text: "This is not a string.",
             r_text: "This is too a string."}
    eq_(solve(revision.diff.tokens_added, cache=cache), 1)
    eq_(solve(revision.diff.tokens_removed, cache=cache), 1)
    eq_(solve(revision.diff.datasources.tokens_added, cache=cache), ['too'])
    eq_(solve(revision.diff.datasources.tokens_removed, cache=cache), ['not'])

    eq_(pickle.loads(pickle.dumps(revision.diff.tokens_added)),
        revision.diff.tokens_added)
    eq_(pickle.loads(pickle.dumps(revision.diff.tokens_removed)),
        revision.diff.tokens_removed)


def test_tokens_matching():
    cache = {p_text: "This is not 55 a sring.",
             r_text: "This is too 56 a tring."}
    eq_(solve(revision.diff.datasources.tokens_added_matching("^t"),
              cache=cache),
        ['too', 'tring'])
    eq_(solve(revision.diff.datasources.tokens_removed_matching("^(5|s)"),
              cache=cache),
        ['55', 'sring'])


def test_tokens_in_types():
    cache = {p_text: "This is not 55 a string.",
             r_text: "This is too 56 a string!"}
    eq_(solve(
        revision.diff.datasources.tokens_added_in_types({'word', 'number'}),
        cache=cache
    ), ['too', '56'])
    eq_(solve(revision.diff.datasources.tokens_removed_in_types({'period'}),
              cache=cache),
        ['.'])


def test_numbers():
    cache = {p_text: "This is 55 not a string.",
             r_text: "This is 56 57 too a string."}
    eq_(solve(revision.diff.numbers_added, cache=cache), 2)
    eq_(solve(revision.diff.numbers_removed, cache=cache), 1)
    eq_(solve(revision.diff.datasources.numbers_added, cache=cache),
        ['56', '57'])
    eq_(solve(revision.diff.datasources.numbers_removed, cache=cache), ['55'])

    eq_(pickle.loads(pickle.dumps(revision.diff.numbers_added)),
        revision.diff.numbers_added)
    eq_(pickle.loads(pickle.dumps(revision.diff.numbers_removed)),
        revision.diff.numbers_removed)


def test_whitespaces():
    cache = {p_text: "This is  \na string.",
             r_text: "This \t is a string."}
    eq_(solve(revision.diff.whitespaces_added, cache=cache), 1)
    eq_(solve(revision.diff.whitespaces_removed, cache=cache), 2)
    eq_(solve(revision.diff.datasources.whitespaces_added, cache=cache),
        [' \t '])
    eq_(solve(revision.diff.datasources.whitespaces_removed, cache=cache),
        ['  ', '\n'])

    eq_(pickle.loads(pickle.dumps(revision.diff.whitespaces_added)),
        revision.diff.whitespaces_added)
    eq_(pickle.loads(pickle.dumps(revision.diff.whitespaces_removed)),
        revision.diff.whitespaces_removed)


def test_markup():
    cache = {p_text: "This is 55 {{not}} a string.",
             r_text: "This is 56 [[too]] a string."}
    eq_(solve(revision.diff.markups_added, cache=cache), 2)
    eq_(solve(revision.diff.markups_removed, cache=cache), 2)
    eq_(solve(revision.diff.datasources.markups_added, cache=cache),
        ['[[', ']]'])
    eq_(solve(revision.diff.datasources.markups_removed, cache=cache),
        ['{{', '}}'])

    eq_(pickle.loads(pickle.dumps(revision.diff.markups_added)),
        revision.diff.markups_added)
    eq_(pickle.loads(pickle.dumps(revision.diff.markups_removed)),
        revision.diff.markups_removed)


def test_cjks():
    cache = {p_text: "This is 55 {{るは}} a string.",
             r_text: "This is 56 [[壌のは]] a string."}
    eq_(solve(revision.diff.cjks_added, cache=cache), 2)
    eq_(solve(revision.diff.cjks_removed, cache=cache), 1)
    eq_(solve(revision.diff.datasources.cjks_added, cache=cache), ['壌', 'の'])
    eq_(solve(revision.diff.datasources.cjks_removed, cache=cache), ['る'])

    eq_(pickle.loads(pickle.dumps(revision.diff.cjks_added)),
        revision.diff.cjks_added)
    eq_(pickle.loads(pickle.dumps(revision.diff.cjks_removed)),
        revision.diff.cjks_removed)


def test_entities():
    cache = {p_text: "This is &nsbp; not a string.",
             r_text: "This is &middot; too a string."}
    eq_(solve(revision.diff.entities_added, cache=cache), 1)
    eq_(solve(revision.diff.entities_removed, cache=cache), 1)
    eq_(solve(revision.diff.datasources.entities_added, cache=cache),
        ['&middot;'])
    eq_(solve(revision.diff.datasources.entities_removed, cache=cache),
        ['&nsbp;'])

    eq_(pickle.loads(pickle.dumps(revision.diff.entities_added)),
        revision.diff.entities_added)
    eq_(pickle.loads(pickle.dumps(revision.diff.entities_removed)),
        revision.diff.entities_removed)


def test_urls():
    cache = {p_text: "This is https://google.com not a string.",
             r_text: "This //google.com mailto:aaron@bar.com string."}
    eq_(solve(revision.diff.urls_added, cache=cache), 2)
    eq_(solve(revision.diff.urls_removed, cache=cache), 1)
    eq_(solve(revision.diff.datasources.urls_added, cache=cache),
        ['//google.com', 'mailto:aaron@bar.com'])
    eq_(solve(revision.diff.datasources.urls_removed, cache=cache),
        ['https://google.com'])

    eq_(pickle.loads(pickle.dumps(revision.diff.urls_added)),
        revision.diff.urls_added)
    eq_(pickle.loads(pickle.dumps(revision.diff.urls_removed)),
        revision.diff.urls_removed)


def test_words():
    cache = {p_text: "This is 55 not string.",
             r_text: "This is 56 too a string."}
    eq_(solve(revision.diff.words_added, cache=cache), 2)
    eq_(solve(revision.diff.words_removed, cache=cache), 1)
    eq_(solve(revision.diff.datasources.words_added, cache=cache),
        ['too', 'a'])
    eq_(solve(revision.diff.datasources.words_removed, cache=cache),
        ['not'])

    eq_(pickle.loads(pickle.dumps(revision.diff.words_added)),
        revision.diff.words_added)
    eq_(pickle.loads(pickle.dumps(revision.diff.words_removed)),
        revision.diff.words_removed)


def test_uppercase_words():
    cache = {p_text: "This is 55 NOT string.",
             r_text: "This is 56 TOO AS string."}
    eq_(solve(revision.diff.uppercase_words_added, cache=cache), 2)
    eq_(solve(revision.diff.uppercase_words_removed, cache=cache), 1)
    eq_(solve(revision.diff.datasources.uppercase_words_added, cache=cache),
        ['TOO', 'AS'])
    eq_(solve(revision.diff.datasources.uppercase_words_removed, cache=cache),
        ['NOT'])

    eq_(pickle.loads(pickle.dumps(revision.diff.uppercase_words_added)),
        revision.diff.uppercase_words_added)
    eq_(pickle.loads(pickle.dumps(revision.diff.uppercase_words_removed)),
        revision.diff.uppercase_words_removed)


def test_punctuations():
    cache = {p_text: "This is 55 not a, string.",
             r_text: "This is 56 too a string?"}
    eq_(solve(revision.diff.punctuations_added, cache=cache), 1)
    eq_(solve(revision.diff.punctuations_removed, cache=cache), 2)
    eq_(solve(revision.diff.datasources.punctuations_added, cache=cache),
        ['?'])
    eq_(solve(revision.diff.datasources.punctuations_removed, cache=cache),
        [',', '.'])

    eq_(pickle.loads(pickle.dumps(revision.diff.punctuations_added)),
        revision.diff.punctuations_added)
    eq_(pickle.loads(pickle.dumps(revision.diff.punctuations_removed)),
        revision.diff.punctuations_removed)


def test_breaks():
    cache = {p_text: "This is \n\n not a string.",
             r_text: "This is 56 too a \n\n string.\n\n"}
    eq_(solve(revision.diff.breaks_added, cache=cache), 2)
    eq_(solve(revision.diff.breaks_removed, cache=cache), 1)
    eq_(solve(revision.diff.datasources.breaks_added, cache=cache),
        ['\n\n', '\n\n'])
    eq_(solve(revision.diff.datasources.breaks_removed, cache=cache),
        ['\n\n'])

    eq_(pickle.loads(pickle.dumps(revision.diff.breaks_added)),
        revision.diff.breaks_added)
    eq_(pickle.loads(pickle.dumps(revision.diff.breaks_removed)),
        revision.diff.breaks_removed)
