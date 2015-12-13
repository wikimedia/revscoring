import pickle
from collections import namedtuple

import enchant
from nose.tools import eq_

from ....datasources import parent_revision, revision
from ....dependencies import solve
from ..space_delimited import SpaceDelimited


def test_no_params():
    SpaceDelimited("fake")  # Should not error


def test_words():
    sd = SpaceDelimited("fake")

    cache = {revision.text: "Foobar bad badwords hat 75 m80, <td> {{foo}}"}
    eq_(solve(sd.revision.words_list, cache=cache),
        ["Foobar", "bad", "badwords", "hat", "m80", "foo"])
    eq_(solve(sd.revision.content_words_list, cache=cache),
        ["Foobar", "bad", "badwords", "hat", "m80"])

    cache = {parent_revision.text: None}
    eq_(solve(sd.parent_revision.words_list, cache=cache), [])
    eq_(solve(sd.parent_revision.content_words_list, cache=cache), [])


def test_badwords():
    sd = SpaceDelimited("fake", badwords=[r"bad(words)?"])

    cache = {revision.text: "Foobar bad badwords hat."}
    eq_(solve(sd.revision.badwords_list, cache=cache), ["bad", "badwords"])

    assert hasattr(sd.revision, "badwords")
    assert hasattr(sd.parent_revision, "badwords")
    assert hasattr(sd.diff, "badwords_added")
    assert hasattr(sd.diff, "badwords_removed")

    cache = {parent_revision.text: None}
    eq_(solve(sd.parent_revision.badwords_list, cache=cache), [])


def test_informals():
    sd = SpaceDelimited("fake", informals=[r"inform(als)?"])

    cache = {revision.text: "Foobar inform informals als hat."}
    eq_(solve(sd.revision.informals_list, cache=cache),
        ["inform", "informals"])

    assert hasattr(sd.revision, "informals")
    assert hasattr(sd.parent_revision, "informals")
    assert hasattr(sd.diff, "informals_added")
    assert hasattr(sd.diff, "informals_removed")

    cache = {parent_revision.text: None}
    eq_(solve(sd.parent_revision.informals_list, cache=cache), [])


def test_infonoise():
    Stemmer = namedtuple("Stemmer", ["stem"])
    stemmer = Stemmer(lambda w: w[0])  # First char
    stopwords = set(["stop", "word"])
    sd = SpaceDelimited("fake", stemmer=stemmer, stopwords=stopwords)

    cache = {revision.text: "Waffle stop word"}
    eq_(solve(sd.revision.infonoise, cache=cache), 1/len("Wafflestopword"))

    cache = {parent_revision.text: "Waffle stop word"}
    eq_(solve(sd.parent_revision.infonoise, cache=cache),
        1/len("Wafflestopword"))

    assert hasattr(sd.revision, "infonoise")
    assert hasattr(sd.parent_revision, "infonoise")


def test_misspellings():
    Dictionary = namedtuple("Dictionary", ["check"])
    dictionary = Dictionary(lambda w: w != "misspelled")

    sd = SpaceDelimited("fake", dictionary=dictionary)

    cache = {revision.text: "Foobar misspelled als hat."}
    eq_(solve(sd.revision.misspellings_list, cache=cache), ["misspelled"])

    assert hasattr(sd.revision, "misspellings")
    assert hasattr(sd.parent_revision, "misspellings")
    assert hasattr(sd.diff, "misspellings_added")
    assert hasattr(sd.diff, "misspellings_removed")

    cache = {parent_revision.text: None}
    eq_(solve(sd.parent_revision.misspellings_list, cache=cache), [])


def test_utf16_issue():
    dictionary = enchant.Dict('en')

    sd = SpaceDelimited("fake", dictionary=dictionary)

    cache = {revision.text: "𐎤𐎢𐎽𐎢𐏁"}
    eq_(solve(sd.revision.misspellings_list, cache=cache), ["𐎤𐎢𐎽𐎢𐏁"])


BADWORDS = [r"bad(words)?"]
Dictionary = namedtuple("Dictionary", ["check"])


def check(word):
    return word != "misspelled"

DICTIONARY = Dictionary(check)
INFORMALS = [r"inform(als)?"]
Stemmer = namedtuple("Stemmer", ["stem"])


def stem(word):
    return word[0]  # First char

STEMMER = Stemmer(stem)
STOPWORDS = set(["stop", "word"])


def test_pickle():
    sd = SpaceDelimited("fake", badwords=BADWORDS, dictionary=DICTIONARY,
                        informals=INFORMALS, stemmer=STEMMER,
                        stopwords=STOPWORDS)

    pickled_sd = pickle.dumps(sd)
    print(pickled_sd)
    unpickled_sd = pickle.loads(pickled_sd)
    eq_(unpickled_sd, sd)
