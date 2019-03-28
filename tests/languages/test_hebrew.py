import pickle

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.languages import hebrew

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

    assert hebrew.badwords == pickle.loads(pickle.dumps(hebrew.badwords))


def test_informals():
    compare_extraction(hebrew.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    assert hebrew.informals == pickle.loads(pickle.dumps(hebrew.informals))


def test_dictionary():
    cache = {r_text: "סוויפט גדלה בוויומיסינג, לנאשוויל"}
    assert (solve(hebrew.dictionary.revision.datasources.dict_words, cache=cache) ==
            ['גדלה'])
    assert (solve(hebrew.dictionary.revision.datasources.non_dict_words,
                  cache=cache) ==
            ['סוויפט', 'בוויומיסינג', 'לנאשוויל'])

    assert hebrew.dictionary == pickle.loads(pickle.dumps(hebrew.dictionary))


""" TODO:
def test_stopwords():
    cache = {r_text: "סוויפט גדלה בוויומיסינג, פנסילבניה, לנאשוויל"}
    assert_equal(solve(hebrew.stopwords.revision.datasources.stopwprds, cache=cache),
        ["סוויפט", "גדלה", "בוויומיסינג", "פנסילבניה", "לנאשוויל"])
    assert_equal(solve(hebrew.stopwords.revision.datasources.non_stopwords,
              cache=cache),
        ["סוויפט", "גדלה", "בוויומיסינג", "פנסילבניה", "לנאשוויל"])

    assert_equal(hebrew.stopwords, pickle.loads(pickle.dumps(hebrew.stopwords)))


def test_stemmed():
    cache = {r_text: "סוויפט גדלה בוויומיסינג, פנסילבניה, לנאשוויל"}
    assert_equal(solve(hebrew.stemmed.revision.datasources.stems, cache=cache),
        ["סוויפט", "גדלה", "בוויומיסינג", "פנסילבניה", "לנאשוויל"])

    assert_equal(hebrew.stemmed, pickle.loads(pickle.dumps(hebrew.stemmed)))
"""
