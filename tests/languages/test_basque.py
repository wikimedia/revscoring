import pickle

from revscoring.languages import basque
from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve

# from .util import compare_extraction

BAD = [
]

INFORMAL = [
]

OTHER = [
]

r_text = revision_oriented.revision.text


'''
@mark.nottravis
def test_badwords():
    compare_extraction(basque.badwords.revision.datasources.matches,
                       BAD, OTHER)

    assert basque.badwords == pickle.loads(pickle.dumps(basque.badwords))


@mark.nottravis
def test_informals():
    compare_extraction(basque.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    assert basque.informals == pickle.loads(pickle.dumps(basque.informals))
'''


def test_dictionary():
    cache = {r_text: "gizonezko dominadun worngly."}
    assert solve(basque.dictionary.revision.datasources.dict_words,
                 cache=cache) == ['gizonezko']
    assert solve(basque.dictionary.revision.datasources.non_dict_words,
                 cache=cache) == ['dominadun', "worngly"]

    assert basque.dictionary == pickle.loads(pickle.dumps(basque.dictionary))


'''
@mark.nottravis
def test_stopwords():
    cache = {r_text: "আন চলচ্চিত্র."}
    assert (solve(basque.stopwords.revision.datasources.stopwords, cache=cache) ==
            ["আন"])
    assert (solve(basque.stopwords.revision.datasources.non_stopwords,
                  cache=cache) ==
            ['চলচ্চিত্র'])

    assert basque.stopwords == pickle.loads(pickle.dumps(basque.stopwords))
'''
