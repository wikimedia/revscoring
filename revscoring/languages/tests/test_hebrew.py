import pickle

from nose.tools import eq_

from .. import hebrew
from ...datasources import revision_oriented
from ...dependencies import solve
from .util import compare_extraction

BAD = [
    "שרמוטה"
]

INFORMAL = [
    "בגללך"  # Because of you
]

OTHER = [
    "בגלל", "חתול"
]

r_text = revision_oriented.revision.text


def test_badwords():
    compare_extraction(hebrew.badwords.revision.datasources.matches,
                       BAD, OTHER)

    eq_(hebrew.badwords, pickle.loads(pickle.dumps(hebrew.badwords)))


def test_informals():
    compare_extraction(hebrew.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    eq_(hebrew.informals, pickle.loads(pickle.dumps(hebrew.informals)))


def test_dictionary():
    cache = {r_text: "סוויפט גדלה בוויומיסינג, לנאשוויל"}
    eq_(solve(hebrew.dictionary.revision.datasources.dict_words, cache=cache),
        ['גדלה'])
    eq_(solve(hebrew.dictionary.revision.datasources.non_dict_words,
              cache=cache),
        ['סוויפט', 'בוויומיסינג', 'לנאשוויל'])

    eq_(hebrew.dictionary, pickle.loads(pickle.dumps(hebrew.dictionary)))


""" TODO:
def test_stopwords():
    cache = {r_text: "סוויפט גדלה בוויומיסינג, פנסילבניה, לנאשוויל"}
    eq_(solve(hebrew.stopwords.revision.datasources.stopwprds, cache=cache),
        ["סוויפט", "גדלה", "בוויומיסינג", "פנסילבניה", "לנאשוויל"])
    eq_(solve(hebrew.stopwords.revision.datasources.non_stopwords,
              cache=cache),
        ["סוויפט", "גדלה", "בוויומיסינג", "פנסילבניה", "לנאשוויל"])

    eq_(hebrew.stopwords, pickle.loads(pickle.dumps(hebrew.stopwords)))


def test_stemmed():
    cache = {r_text: "סוויפט גדלה בוויומיסינג, פנסילבניה, לנאשוויל"}
    eq_(solve(hebrew.stemmed.revision.datasources.stems, cache=cache),
        ["סוויפט", "גדלה", "בוויומיסינג", "פנסילבניה", "לנאשוויל"])

    eq_(hebrew.stemmed, pickle.loads(pickle.dumps(hebrew.stemmed)))
"""
