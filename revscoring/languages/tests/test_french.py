import pickle

from nose.tools import eq_

from .. import french
from ...datasources import revision
from ...dependencies import solve

BAD = [
    "con",
    "fesse",
    "foutre",
    "merde", "merdee",
    "merdique",
    "prostituee", "prostitue",
    "putain", "putes",
    "salop",
    "stupide"
]

OTHER = [
    "connection", "fitness", "le"
]


def compare_extraction(extractor, examples, counter_examples):

    for example in examples:
        eq_(extractor.process(example), [example])
        eq_(extractor.process("Sentence " + example + " sandwich."), [example])
        eq_(extractor.process("Sentence end " + example + "."), [example])
        eq_(extractor.process(example + " start of sentence."), [example])

    for example in counter_examples:
        eq_(extractor.process(example), [])
        eq_(extractor.process("Sentence " + example + " sandwich."), [])
        eq_(extractor.process("Sentence end " + example + "."), [])
        eq_(extractor.process(example + " start of sentence."), [])


def test_badwords():
    compare_extraction(french.revision.badwords_list, BAD, OTHER)


def test_revision():
    # Words
    cache = {revision.text: "Wikipédia est un projet d’encyclopédie."}
    eq_(solve(french.revision.words_list, cache=cache),
        ["Wikipédia", "est", "un", "projet", "d’encyclopédie"])

    # Misspellings
    cache = {revision.text: 'Est un projet principe du worngly. <td>'}
    eq_(solve(french.revision.misspellings_list, cache=cache), ["worngly"])

    # Infonoise
    cache = {revision.text: "Est un projet principe."}
    eq_(solve(french.revision.infonoise, cache=cache), 13/19)


def test_presence():
    assert hasattr(french.revision, "words")
    assert hasattr(french.revision, "content_words")
    assert hasattr(french.revision, "badwords")
    assert hasattr(french.revision, "misspellings")

    assert hasattr(french.parent_revision, "words")
    assert hasattr(french.parent_revision, "content_words")
    assert hasattr(french.parent_revision, "badwords")
    assert hasattr(french.parent_revision, "misspellings")

    assert hasattr(french.diff, "words_added")
    assert hasattr(french.diff, "badwords_added")
    assert hasattr(french.diff, "misspellings_added")
    assert hasattr(french.diff, "words_removed")
    assert hasattr(french.diff, "badwords_removed")
    assert hasattr(french.diff, "misspellings_removed")


def test_pickling():

    eq_(french, pickle.loads(pickle.dumps(french)))
