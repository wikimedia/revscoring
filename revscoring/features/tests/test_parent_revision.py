from collections import namedtuple

from mw import Timestamp
from nose.tools import eq_

from ... import languages
from ...datasources import parent_revision, revision
from ...dependencies import solve
from ..parent_revision import (badwords, bytes, chars, markup_chars,
                               misspellings, numeric_chars, seconds_since,
                               symbolic_chars, uppercase_chars, was_same_user,
                               words)


def test_was_same_user():
    FakeRevisionMetadata = namedtuple("FakeRevisionMetadata",
                                      ['user_id', 'user_text'])

    cache = {
        revision.metadata: FakeRevisionMetadata(10, "Foobar"),
        parent_revision.metadata: FakeRevisionMetadata(10, "Foobar")
    }
    eq_(solve(was_same_user, cache=cache), True)

    cache = {
        revision.metadata: FakeRevisionMetadata(10, "Foobar"),
        parent_revision.metadata: FakeRevisionMetadata(10, "Fleebar")
    }
    eq_(solve(was_same_user, cache=cache), True)

    cache = {
        revision.metadata: FakeRevisionMetadata(None, "127.4.5.6"),
        parent_revision.metadata: FakeRevisionMetadata(None, "127.4.5.6")
    }
    eq_(solve(was_same_user, cache=cache), True)

def test_seconds_since():
    FakeRevisionMetadata = namedtuple("FakeRevisionMetadata",
                                      ['timestamp'])

    cache = {
        revision.metadata: FakeRevisionMetadata(Timestamp(10)),
        parent_revision.metadata: FakeRevisionMetadata(Timestamp(1))
    }
    eq_(solve(seconds_since, cache=cache), 9)

def test_bytes():
    FakeRevisionMetadata = namedtuple("FakeRevisionMetadata",
                                      ['bytes'])

    cache = {
        parent_revision.metadata: FakeRevisionMetadata(25)
    }
    eq_(solve(bytes, cache=cache), 25)

def test_chars():
    cache = {
        parent_revision.text: "Twelve chars"
    }
    eq_(solve(chars, cache=cache), 12)

def test_markup_chars():
    cache = {
        parent_revision.text: "Twelve {{chars}}"
    }
    eq_(solve(markup_chars, cache=cache), 4)

    cache = {
        parent_revision.text: None
    }
    eq_(solve(markup_chars, cache=cache), 0)

def test_numeric_chars():
    cache = {
        parent_revision.text: "Twelve hats pants 95 bananas!"
    }
    eq_(solve(numeric_chars, cache=cache), 2)

    cache = {
        parent_revision.text: None
    }
    eq_(solve(numeric_chars, cache=cache), 0)

def test_symbolic_chars():
    cache = {
        parent_revision.text: "Twelve hats?  Pants, #95 bananas!"
    }
    eq_(solve(symbolic_chars, cache=cache), 4)

    cache = {
        parent_revision.text: None
    }
    eq_(solve(symbolic_chars, cache=cache), 0)

def test_uppercase_chars():
    cache = {
        parent_revision.text: "Twelve hats?  Pants, #95 bananas!"
    }
    eq_(solve(uppercase_chars, cache=cache), 2)

    cache = {
        parent_revision.text: None
    }
    eq_(solve(uppercase_chars, cache=cache), 0)

def test_words():
    cache = {
        parent_revision.words: ["I", "am", "four", "words"]
    }
    eq_(solve(words, cache=cache), 4)

def test_badwords():
    def is_badword(w): return w == "badword"
    cache = {
        languages.is_badword: is_badword,
        parent_revision.words: ["I", "am", "badword", "badword"]
    }
    eq_(solve(badwords, cache=cache), 2)

def test_misspellings():
    def is_misspelled(w): return w == "misspelled"
    cache = {
        languages.is_misspelled: is_misspelled,
        parent_revision.words: ["I", "am", "misspelled", "badword"]
    }
    eq_(solve(misspellings, cache=cache), 1)
