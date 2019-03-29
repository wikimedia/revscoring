import pickle

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.languages import finnish

from .util import compare_extraction

BAD = [
    "homo", "homoja", "homot",
    "hintti",
    "homppeli",
    "huora",
    "idiootti",
    "jumalauta",
    "juntti",
    "kakka", "kakkaa",
    "kikkeli",
    "kyrpä",
    "kulli",
    "kusi", "kusipää",
    "läski",
    "mamu",
    "matu",
    "neekeri",
    "nussii",
    "narttu",
    "paska", "paskaa", "paskat", "paskin", "paskova",
    "pelle",
    "perse", "perseeseen", "perseessä", "perseestä", "perseenreikä",
    "perkele",
    "pillu", "pilluun",
    "pippeli",
    "pieru",
    "retardi",
    "runkkari",
    "saatana", "saatanan",
    "tyhmä",
    "vammane", "vammanen",
    "vittu",
    "vitun",
    "äpärä"
]

INFORMAL = [
    "haistakaa",
    "imekää",
    "lol",
    "ootte",
    "moi",
    "hei",
    "sinä",
    "sä",
    "minä",
    "mää",
    "ok",
    "joo",
    "okei"
]

OTHER = [
    """
    Gunnar Nordström (12. maaliskuuta 1881 Helsinki – 24. joulukuuta 1923
    Helsinki) oli suomalainen fyysikko ja avaruustähtitieteilijä. Hänet
    tunnetaan erityisesti painovoimateoriastaan, joka oli yleistä
    suhteellisuusteoriaa edeltävä kilpaileva teoria. Nordström on saanut
    melko paljon huomiota ulkomailla, mutta kotimaassaan hän on melko
    tuntematon henkilö.
    """
]

r_text = revision_oriented.revision.text


def test_badwords():
    compare_extraction(finnish.badwords.revision.datasources.matches,
                       BAD, OTHER)

    assert finnish.badwords == pickle.loads(pickle.dumps(finnish.badwords))


def test_informals():
    compare_extraction(finnish.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    assert finnish.informals == pickle.loads(pickle.dumps(finnish.informals))


def test_stopwords():
    cache = {revision_oriented.revision.text: "Nordström on ette melko " +
                                              "paljon huomiota"}
    assert (solve(finnish.stopwords.revision.datasources.stopwords,
            cache=cache) == ["on", "ette"])
    assert (solve(finnish.stopwords.revision.datasources.non_stopwords,
            cache=cache) == ['Nordström', 'melko', 'paljon', 'huomiota'])

    assert finnish.stopwords == pickle.loads(pickle.dumps(finnish.stopwords))
