import pickle

from nose.tools import eq_

from .. import french
from ...datasources import revision
from ...dependencies import solve
from .util import compare_extraction

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


def test_pickling():

    eq_(french, pickle.loads(pickle.dumps(french)))
