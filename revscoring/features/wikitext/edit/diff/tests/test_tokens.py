import pickle

from nose.tools import eq_

from .. import tokens
from ......datasources.revision_oriented import revision
from ......dependencies import solve


def test_tokens():
    cache = {revision.parent.text: "This is not a string.",
             revision.text: "This is too a string."}
    eq_(solve(tokens.tokens_added, cache=cache), 1)
    eq_(solve(tokens.tokens_removed, cache=cache), 1)
    eq_(solve(tokens.datasources.tokens_added, cache=cache), ['too'])
    eq_(solve(tokens.datasources.tokens_removed, cache=cache), ['not'])

    eq_(pickle.loads(pickle.dumps(tokens.tokens_added)),
        tokens.tokens_added)
    eq_(pickle.loads(pickle.dumps(tokens.tokens_removed)),
        tokens.tokens_removed)


def test_tokens_matching():
    cache = {revision.parent.text: "This is not 55 a sring.",
             revision.text: "This is too 56 a tring."}
    eq_(solve(tokens.datasources.tokens_added_matching("^t"), cache=cache),
        ['too', 'tring'])
    eq_(solve(tokens.datasources.tokens_removed_matching("^(5|s)"),
              cache=cache),
        ['55', 'sring'])


def test_tokens_in_types():
    cache = {revision.parent.text: "This is not 55 a string.",
             revision.text: "This is too 56 a string!"}
    eq_(solve(tokens.datasources.tokens_added_in_types({'word', 'number'}),
              cache=cache),
        ['too', '56'])
    eq_(solve(tokens.datasources.tokens_removed_in_types({'period'}),
              cache=cache),
        ['.'])


def test_numbers():
    cache = {revision.parent.text: "This is 55 not a string.",
             revision.text: "This is 56 57 too a string."}
    eq_(solve(tokens.numbers_added, cache=cache), 2)
    eq_(solve(tokens.numbers_removed, cache=cache), 1)
    eq_(solve(tokens.datasources.numbers_added, cache=cache), ['56', '57'])
    eq_(solve(tokens.datasources.numbers_removed, cache=cache), ['55'])

    eq_(pickle.loads(pickle.dumps(tokens.numbers_added)),
        tokens.numbers_added)
    eq_(pickle.loads(pickle.dumps(tokens.numbers_removed)),
        tokens.numbers_removed)


def test_whitespaces():
    cache = {revision.parent.text: "This is  \na string.",
             revision.text: "This \t is a string."}
    eq_(solve(tokens.whitespaces_added, cache=cache), 1)
    eq_(solve(tokens.whitespaces_removed, cache=cache), 2)
    eq_(solve(tokens.datasources.whitespaces_added, cache=cache), [' \t '])
    eq_(solve(tokens.datasources.whitespaces_removed, cache=cache),
        ['  ', '\n'])

    eq_(pickle.loads(pickle.dumps(tokens.whitespaces_added)),
        tokens.whitespaces_added)
    eq_(pickle.loads(pickle.dumps(tokens.whitespaces_removed)),
        tokens.whitespaces_removed)


def test_markup():
    cache = {revision.parent.text: "This is 55 {{not}} a string.",
             revision.text: "This is 56 [[too]] a string."}
    eq_(solve(tokens.markups_added, cache=cache), 2)
    eq_(solve(tokens.markups_removed, cache=cache), 2)
    eq_(solve(tokens.datasources.markups_added, cache=cache), ['[[', ']]'])
    eq_(solve(tokens.datasources.markups_removed, cache=cache), ['{{', '}}'])

    eq_(pickle.loads(pickle.dumps(tokens.markups_added)),
        tokens.markups_added)
    eq_(pickle.loads(pickle.dumps(tokens.markups_removed)),
        tokens.markups_removed)


def test_cjks():
    cache = {revision.parent.text: "This is 55 {{るは}} a string.",
             revision.text: "This is 56 [[壌のは]] a string."}
    eq_(solve(tokens.cjks_added, cache=cache), 2)
    eq_(solve(tokens.cjks_removed, cache=cache), 1)
    eq_(solve(tokens.datasources.cjks_added, cache=cache), ['壌', 'の'])
    eq_(solve(tokens.datasources.cjks_removed, cache=cache), ['る'])

    eq_(pickle.loads(pickle.dumps(tokens.cjks_added)), tokens.cjks_added)
    eq_(pickle.loads(pickle.dumps(tokens.cjks_removed)), tokens.cjks_removed)


def test_entities():
    cache = {revision.parent.text: "This is &nsbp; not a string.",
             revision.text: "This is &middot; too a string."}
    eq_(solve(tokens.entities_added, cache=cache), 1)
    eq_(solve(tokens.entities_removed, cache=cache), 1)
    eq_(solve(tokens.datasources.entities_added, cache=cache), ['&middot;'])
    eq_(solve(tokens.datasources.entities_removed, cache=cache), ['&nsbp;'])

    eq_(pickle.loads(pickle.dumps(tokens.entities_added)),
        tokens.entities_added)
    eq_(pickle.loads(pickle.dumps(tokens.entities_removed)),
        tokens.entities_removed)


def test_urls():
    cache = {revision.parent.text: "This is https://google.com not a string.",
             revision.text: "This //google.com mailto:aaron@bar.com string."}
    eq_(solve(tokens.urls_added, cache=cache), 2)
    eq_(solve(tokens.urls_removed, cache=cache), 1)
    eq_(solve(tokens.datasources.urls_added, cache=cache),
        ['//google.com', 'mailto:aaron@bar.com'])
    eq_(solve(tokens.datasources.urls_removed, cache=cache),
        ['https://google.com'])

    eq_(pickle.loads(pickle.dumps(tokens.urls_added)), tokens.urls_added)
    eq_(pickle.loads(pickle.dumps(tokens.urls_removed)), tokens.urls_removed)


def test_words():
    cache = {revision.parent.text: "This is 55 not string.",
             revision.text: "This is 56 too a string."}
    eq_(solve(tokens.words_added, cache=cache), 2)
    eq_(solve(tokens.words_removed, cache=cache), 1)
    eq_(solve(tokens.datasources.words_added, cache=cache), ['too', 'a'])
    eq_(solve(tokens.datasources.words_removed, cache=cache), ['not'])

    eq_(pickle.loads(pickle.dumps(tokens.words_added)), tokens.words_added)
    eq_(pickle.loads(pickle.dumps(tokens.words_removed)), tokens.words_removed)


def test_uppercase_words():
    cache = {revision.parent.text: "This is 55 NOT string.",
             revision.text: "This is 56 TOO AS string."}
    eq_(solve(tokens.uppercase_words_added, cache=cache), 2)
    eq_(solve(tokens.uppercase_words_removed, cache=cache), 1)
    eq_(solve(tokens.datasources.uppercase_words_added, cache=cache),
        ['TOO', 'AS'])
    eq_(solve(tokens.datasources.uppercase_words_removed, cache=cache),
        ['NOT'])

    eq_(pickle.loads(pickle.dumps(tokens.uppercase_words_added)),
        tokens.uppercase_words_added)
    eq_(pickle.loads(pickle.dumps(tokens.uppercase_words_removed)),
        tokens.uppercase_words_removed)


def test_punctuations():
    cache = {revision.parent.text: "This is 55 not a, string.",
             revision.text: "This is 56 too a string?"}
    eq_(solve(tokens.punctuations_added, cache=cache), 1)
    eq_(solve(tokens.punctuations_removed, cache=cache), 2)
    eq_(solve(tokens.datasources.punctuations_added, cache=cache), ['?'])
    eq_(solve(tokens.datasources.punctuations_removed, cache=cache),
        [',', '.'])

    eq_(pickle.loads(pickle.dumps(tokens.punctuations_added)),
        tokens.punctuations_added)
    eq_(pickle.loads(pickle.dumps(tokens.punctuations_removed)),
        tokens.punctuations_removed)


def test_breaks():
    cache = {revision.parent.text: "This is \n\n not a string.",
             revision.text: "This is 56 too a \n\n string.\n\n"}
    eq_(solve(tokens.breaks_added, cache=cache), 2)
    eq_(solve(tokens.breaks_removed, cache=cache), 1)
    eq_(solve(tokens.datasources.breaks_added, cache=cache), ['\n\n', '\n\n'])
    eq_(solve(tokens.datasources.breaks_removed, cache=cache), ['\n\n'])

    eq_(pickle.loads(pickle.dumps(tokens.breaks_added)),
        tokens.breaks_added)
    eq_(pickle.loads(pickle.dumps(tokens.breaks_removed)),
        tokens.breaks_removed)
