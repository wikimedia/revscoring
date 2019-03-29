import pickle

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.languages import romanian

from .util import compare_extraction

BAD = [
    "bou",
    "caca", "cacat",
    "cur", "curu", "curva", "curve",
    "dracu",
    "fraier", "fraieri", "fraierilor",
    "fut", "fute", "futut",
    "kkt",
    "laba",
    "mata",
    "muie", "muist",
    "pidar",
    "pizda",
    "plm",
    "porcarie",
    "pula", "pule", "puli", "pulii",
    "suge", "sugeti", "sugi",
    "supt"
]

INFORMAL = [
    "aia", "asa",
    "asta", "astea",
    "ati", "aveti",
    "bag", "bagat",
    "bla",
    "naspa",
    "prost", "prosti", "prostie", "prostii", "prostilor",
    "rahat",
    "smecher",
    "tigani"
]

OTHER = [
    """
    Perioada Dinastiei Song (în chineză 宋朝, Sòng Cháo; sʊŋ tʂʰɑʊ̯)
    reprezintă denumirea unei epoci istorice din istoria Chinei,
    care a a început în anul 960 și a durat până în anul 1279. Ea a a
    fost precedată de „Perioada Celor Cinci Dinastii și a Celor Zece Regate”
    și a fost urmată de „Perioada Dinastiei Yuan”. În timpul acestei perioade
    au fost emiși primii bani adevărați de hârtie din istoria lumii - bancnote
    - de către un guvern național. Tot în această perioadă a fost înființată
    prima flotă maritimă militară permanentă a Chinei, s-a folosit pentru prima
    dată praful de pușcă și s-a determinat, tot pentru prima dată, nordului
    geografic cu ajutorul busolei.
    """,
]

r_text = revision_oriented.revision.text


def test_badwords():
    compare_extraction(romanian.badwords.revision.datasources.matches,
                       BAD, OTHER)

    assert romanian.badwords == pickle.loads(pickle.dumps(romanian.badwords))


def test_informals():
    compare_extraction(romanian.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    assert romanian.informals == pickle.loads(pickle.dumps(romanian.informals))


def test_dictionary():
    cache = {r_text: 'În timpul acestei perioade worngly. <td>'}
    assert (solve(romanian.dictionary.revision.datasources.dict_words,
                  cache=cache) ==
            ['În', 'timpul', 'acestei', 'perioade'])
    assert (solve(romanian.dictionary.revision.datasources.non_dict_words,
                  cache=cache) ==
            ["worngly"])

    assert romanian.dictionary == pickle.loads(
        pickle.dumps(romanian.dictionary))


def test_stopwords():
    cache = {r_text: "În timpul acestei perioade"}
    assert (solve(romanian.stopwords.revision.datasources.stopwords, cache=cache) ==
            ['În', 'acestei'])
    assert (solve(romanian.stopwords.revision.datasources.non_stopwords,
                  cache=cache) ==
            ['timpul', 'perioade'])

    assert romanian.stopwords == pickle.loads(pickle.dumps(romanian.stopwords))


def test_stemmmed():
    cache = {r_text: "În timpul acestei perioade"}
    assert (solve(romanian.stemmed.revision.datasources.stems, cache=cache) ==
            ['în', 'timp', 'aceste', 'perioad'])

    assert romanian.stemmed == pickle.loads(pickle.dumps(romanian.stemmed))
