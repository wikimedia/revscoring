import pickle

from pytest import mark

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve

from .util import compare_extraction

try:
    from revscoring.languages import bosnian
except ImportError:
    # Can't install the enchant dictionary, skip
    pytestmark = mark.nottravis

BAD = [
    "balija",
    "debil",
    "debili",
    "debilu",
    "drolja",
    "drolje",
    "droljetine",
    "droljo",
    "fašisti",
    "fuck",
    "govna",
    "govno",
    "iliriski",
    "jebanje",
    "jebe",
    "jebem",
    "jebem",
    "jebi",
    "jebiga",
    "jebite",
    "jebo",
    "kreten",
    "kretenčina",
    "kretenčuga",
    "kreteni",
    "kretenu",
    "kučka",
    "kuja",
    "kuje",
    "kurac",
    "kurce",
    "kurcina",
    "kurčina",
    "kurva",
    "lezbac",
    "lezbać",
    "maloglavi",
    "materinu",
    "mrš",
    "peder",
    "pederi",
    "pederima",
    "pederski",
    "pederu",
    "picka",
    "pička",
    "picke",
    "pičke",
    "picko",
    "pičko",
    "pizda",
    "pizdo",
    "pizdu",
    "puškomet",
    "shit",
    "sranje",
    "šupak"
]

INFORMAL = [
    "boriću",
    "bubaj",
    "drzava",
    "glup",
    "haha",
    "hahaha",
    "hahahaha",
    "hahahahaha",
    "hihi",
    "hihihi",
    "istorija",
    "lmao",
    "lol",
    "nesto",
    "neznam",
    "nista",
    "opština",
    "opštini",
    "orgaizovanje",
    "pokusava",
    "pokušavajuci",
    "povijest",
    "povješničari",
    "pregledaču",
    "šireči",
    "takođerr",
    "ucvršćivanja",
    "vecina",
    "zivjeli",
    "zivjelo"
]

OTHER = [
    """
    On je sjajni, srebreno-sivi četverovalentni prelazni metal. U hemijskom
    smislu, dosta je sličan cirkoniju a može se naći i u mineralima
    cirkonija. Njegovo postojanje je predvidio Mendeljejev već 1869. godine,
    ali sve do 1923. nije identificiran kao element. Bio je pretposljednji
    element sa stabilnim izotopima koji je otkriven (renij je identificiran
    dvije godine kasnije).
    """
]

r_text = revision_oriented.revision.text


@mark.nottravis
def test_badwords():
    compare_extraction(bosnian.badwords.revision.datasources.matches,
                       BAD, OTHER)

    assert bosnian.badwords == pickle.loads(pickle.dumps(bosnian.badwords))


@mark.nottravis
def test_informals():
    compare_extraction(bosnian.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    assert bosnian.informals == pickle.loads(pickle.dumps(bosnian.informals))


@mark.nottravis
def test_dictionary():
    cache = {r_text: "postojanje sličan worngly."}
    assert (solve(bosnian.dictionary.revision.datasources.dict_words,
                  cache=cache) ==
            ["postojanje", "sličan"])
    assert (solve(bosnian.dictionary.revision.datasources.non_dict_words,
                  cache=cache) ==
            ["worngly"])

    assert bosnian.dictionary == pickle.loads(pickle.dumps(bosnian.dictionary))


@mark.nottravis
def test_stopwords():
    cache = {r_text: "hercegovine jakiel kroz postojanje."}
    assert (solve(bosnian.stopwords.revision.datasources.stopwords, cache=cache) ==
            ["hercegovine", "jakiel", "kroz"])
    assert (solve(bosnian.stopwords.revision.datasources.non_stopwords,
                  cache=cache) ==
            ["postojanje"])

    assert bosnian.stopwords == pickle.loads(pickle.dumps(bosnian.stopwords))
