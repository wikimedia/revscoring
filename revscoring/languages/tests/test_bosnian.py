import pickle

from nose.tools import eq_

from .. import bosnian
from ...datasources import revision_oriented
from ...dependencies import solve
from .util import compare_extraction

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


def test_badwords():
    compare_extraction(bosnian.badwords.revision.datasources.matches,
                       BAD, OTHER)

    eq_(bosnian.badwords, pickle.loads(pickle.dumps(bosnian.badwords)))


def test_informals():
    compare_extraction(bosnian.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    eq_(bosnian.informals, pickle.loads(pickle.dumps(bosnian.informals)))


def test_dictionary():
    cache = {r_text: "postojanje sličan worngly."}
    eq_(solve(bosnian.dictionary.revision.datasources.dict_words,
              cache=cache),
        ["postojanje", "sličan"])
    eq_(solve(bosnian.dictionary.revision.datasources.non_dict_words,
        cache=cache),
        ["worngly"])

    eq_(bosnian.dictionary, pickle.loads(pickle.dumps(bosnian.dictionary)))


def test_stopwords():
    cache = {r_text: "hercegovine jakiel kroz postojanje."}
    eq_(solve(bosnian.stopwords.revision.datasources.stopwords, cache=cache),
        ["hercegovine", "jakiel", "kroz"])
    eq_(solve(bosnian.stopwords.revision.datasources.non_stopwords,
              cache=cache),
        ["postojanje"])

    eq_(bosnian.stopwords, pickle.loads(pickle.dumps(bosnian.stopwords)))
