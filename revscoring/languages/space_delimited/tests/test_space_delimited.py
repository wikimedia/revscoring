import pickle
from collections import namedtuple

from nose.tools import eq_

from ....datasources import diff, parent_revision, revision
from ....dependencies import solve
from ..space_delimited import SpaceDelimited


def test_no_params():
    SpaceDelimited("fake") # Should not error

def test_badwords():
    sd = SpaceDelimited("fake", badwords=[r"bad(words)?"])

    cache = {revision.text: "Foobar bad badwords hat."}
    eq_(solve(sd.revision.badwords_list, cache=cache), ["bad", "badwords"])

    assert hasattr(sd.revision, "badwords")
    assert hasattr(sd.parent_revision, "badwords")
    assert hasattr(sd.diff, "badwords_added")
    assert hasattr(sd.diff, "badwords_removed")

def test_informals():
    sd = SpaceDelimited("fake", informals=[r"inform(als)?"])

    cache = {revision.text: "Foobar inform informals als hat."}
    eq_(solve(sd.revision.informals_list, cache=cache), ["inform", "informals"])

    assert hasattr(sd.revision, "informals")
    assert hasattr(sd.parent_revision, "informals")
    assert hasattr(sd.diff, "informals_added")
    assert hasattr(sd.diff, "informals_removed")

def test_infonoise():
    Stemmer = namedtuple("Stemmer", ["stem"])
    stemmer = Stemmer(lambda w:w[0]) # First char
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
    dictionary = Dictionary(lambda w: w != "misspelled") # First char

    sd = SpaceDelimited("fake", dictionary=dictionary)

    cache = {revision.text: "Foobar misspelled als hat."}
    eq_(solve(sd.revision.misspellings_list, cache=cache), ["misspelled"])

    assert hasattr(sd.revision, "misspellings")
    assert hasattr(sd.parent_revision, "misspellings")
    assert hasattr(sd.diff, "misspellings_added")
    assert hasattr(sd.diff, "misspellings_removed")

def test_pickle():
    badwords = [r"bad(words)?"]
    Dictionary = namedtuple("Dictionary", ["check"])
    dictionary = Dictionary(lambda w: w != "misspelled") # First char
    informals = [r"inform(als)?"]
    Stemmer = namedtuple("Stemmer", ["stem"])
    stemmer = Stemmer(lambda w:w[0]) # First char
    stopwords = set(["stop", "word"])

    sd = SpaceDelimited("fake", badwords=badwords, dictionary=dictionary,
                        informals=informals, stemmer=stemmer,
                        stopwords=stopwords)

    eq_(pickle.loads(pickle.dumps(sd)), sd)
