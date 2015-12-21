import pickle

from deltas import Delete, Equal, Insert
from nose.tools import eq_

from ......datasources import parent_revision, revision
from ......dependencies import solve
from ..tokens import (breaks_added, breaks_removed, cjks_added, cjks_removed,
                      entities_added, entities_removed, markups_added,
                      markups_removed, numbers_added, numbers_removed,
                      punctuations_added, punctuations_removed, tokens_added,
                      tokens_added_in_types, tokens_added_matching,
                      tokens_removed, tokens_removed_in_types,
                      tokens_removed_matching, uppercase_words_added,
                      uppercase_words_removed, urls_added, urls_removed,
                      whitespaces_added, whitespaces_removed, words_added,
                      words_removed)


def test_tokens():
    cache = {parent_revision.text: "This is not a string.",
             revision.text: "This is too a string."}
    eq_(solve(tokens_added, cache=cache),
        ['too'])
    eq_(solve(tokens_removed, cache=cache),
        ['not'])

    eq_(pickle.loads(pickle.dumps(tokens_added)), tokens_added)
    eq_(pickle.loads(pickle.dumps(tokens_removed)), tokens_removed)


def test_tokens_matching():
    cache = {parent_revision.text: "This is not 55 a sring.",
             revision.text: "This is too 56 a tring."}
    eq_(solve(tokens_added_matching("^t"), cache=cache),
        ['too', 'tring'])
    eq_(solve(tokens_removed_matching("^(5|s)"), cache=cache),
        ['55', 'sring'])


def test_tokens_in_types():
    cache = {parent_revision.text: "This is not 55 a string.",
             revision.text: "This is too 56 a string!"}
    eq_(solve(tokens_added_in_types({'word', 'number'}), cache=cache),
        ['too', '56'])
    eq_(solve(tokens_removed_in_types({'period'}), cache=cache),
        ['.'])


def test_numbers():
    cache = {parent_revision.text: "This is 55 not a string.",
             revision.text: "This is 56 too a string."}
    eq_(solve(numbers_added, cache=cache),
        ['56'])
    eq_(solve(numbers_removed, cache=cache),
        ['55'])

    eq_(pickle.loads(pickle.dumps(numbers_added)), numbers_added)
    eq_(pickle.loads(pickle.dumps(numbers_removed)), numbers_removed)


def test_whitespaces():
    cache = {parent_revision.text: "This is  \na string.",
             revision.text: "This \t is a string."}
    eq_(solve(whitespaces_added, cache=cache),
        [' \t '])
    eq_(solve(whitespaces_removed, cache=cache),
        ['  ', '\n'])

    eq_(pickle.loads(pickle.dumps(whitespaces_added)), whitespaces_added)
    eq_(pickle.loads(pickle.dumps(whitespaces_removed)), whitespaces_removed)


def test_markup():
    cache = {parent_revision.text: "This is 55 {{not}} a string.",
             revision.text: "This is 56 [[too]] a string."}
    eq_(solve(markups_added, cache=cache),
        ['[[', ']]'])
    eq_(solve(markups_removed, cache=cache),
        ['{{', '}}'])

    eq_(pickle.loads(pickle.dumps(markups_added)), markups_added)
    eq_(pickle.loads(pickle.dumps(markups_removed)), markups_removed)


def test_cjks():
    cache = {parent_revision.text: "This is 55 {{るいは}} a string.",
             revision.text: "This is 56 [[壌のは]] a string."}
    eq_(solve(cjks_added, cache=cache),
        ['壌', 'の'])
    eq_(solve(cjks_removed, cache=cache),
        ['る', 'い'])

    eq_(pickle.loads(pickle.dumps(cjks_added)), cjks_added)
    eq_(pickle.loads(pickle.dumps(cjks_removed)), cjks_removed)


def test_entities():
    cache = {parent_revision.text: "This is &nsbp; not a string.",
             revision.text: "This is &middot; too a string."}
    eq_(solve(entities_added, cache=cache),
        ['&middot;'])
    eq_(solve(entities_removed, cache=cache),
        ['&nsbp;'])

    eq_(pickle.loads(pickle.dumps(entities_added)), entities_added)
    eq_(pickle.loads(pickle.dumps(entities_removed)), entities_removed)


def test_urls():
    cache = {parent_revision.text: "This is https://google.com not a string.",
             revision.text: "This is //google.com too a string."}
    eq_(solve(urls_added, cache=cache),
        ['//google.com'])
    eq_(solve(urls_removed, cache=cache),
        ['https://google.com'])

    eq_(pickle.loads(pickle.dumps(urls_added)), urls_added)
    eq_(pickle.loads(pickle.dumps(urls_removed)), urls_removed)


def test_words():
    cache = {parent_revision.text: "This is 55 not a string.",
             revision.text: "This is 56 too a string."}
    eq_(solve(words_added, cache=cache),
        ['too'])
    eq_(solve(words_removed, cache=cache),
        ['not'])

    eq_(pickle.loads(pickle.dumps(words_added)), words_added)
    eq_(pickle.loads(pickle.dumps(words_removed)), words_removed)


def test_uppercase_words():
    cache = {parent_revision.text: "This is 55 NOT a string.",
             revision.text: "This is 56 TOO a string."}
    eq_(solve(uppercase_words_added, cache=cache),
        ['TOO'])
    eq_(solve(uppercase_words_removed, cache=cache),
        ['NOT'])

    eq_(pickle.loads(pickle.dumps(uppercase_words_added)),
        uppercase_words_added)
    eq_(pickle.loads(pickle.dumps(uppercase_words_removed)),
        uppercase_words_removed)


def test_punctuations():
    cache = {parent_revision.text: "This is 55 not a string.",
             revision.text: "This is 56 too a string?"}
    eq_(solve(punctuations_added, cache=cache),
        ['?'])
    eq_(solve(punctuations_removed, cache=cache),
        ['.'])

    eq_(pickle.loads(pickle.dumps(punctuations_added)), punctuations_added)
    eq_(pickle.loads(pickle.dumps(punctuations_removed)), punctuations_removed)


def test_breaks():
    cache = {parent_revision.text: "This is \n\n not a string.",
             revision.text: "This is 56 too a \n\n string."}
    eq_(solve(breaks_added, cache=cache),
        ['\n\n'])
    eq_(solve(breaks_removed, cache=cache),
        ['\n\n'])

    eq_(pickle.loads(pickle.dumps(breaks_added)), breaks_added)
    eq_(pickle.loads(pickle.dumps(breaks_removed)), breaks_removed)
