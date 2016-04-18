import pickle

from nose.tools import eq_

from .. import hungarian
from ...datasources import revision_oriented
from ...dependencies import solve
from .util import compare_extraction

BAD = [
    "anyad",
    "anyád",
    "anyádat",
    "anyátok",
    "anyátokat",
    "apád",
    "asd",
    "balfasz",
    "baszni",
    "baszott",
    "bazd",
    "bazdmeg",
    "bazmeg",
    "béna",
    "birkanépet",
    "birkanépünk",
    "büdös",
    "buktája",
    "buzi",
    "buzik",
    "csicska",
    "csá",
    "fasszopó",
    "fasz",
    "fasza",
    "faszfej",
    "faszkalap",
    "faszok",
    "faszom",
    "faszomat",
    "faszság",
    "faszt",
    "faszát",
    "fing",
    "fos",
    "fuck",
    "geci",
    "gecik",
    "gecis",
    "gecit",
    "hulye",
    "hülye",
    "hülyék",
    "kabbe",
    "kaka",
    "kaki",
    "kibaszott",
    "kocsog",
    "kuki",
    "kurva",
    "kurvák",
    "kurvára",
    "kurvát",
    "köcsög",
    "köcsögök",
    "lófasz",
    "megbaszta",
    "mocskos",
    "málejku",
    "mizu",
    "naon",
    "picsa",
    "picsája",
    "pina",
    "punci",
    "putri",
    "pöcs",
    "retkes",
    "ribanc",
    "rohadt",
    "sissitek",
    "szar",
    "szarok",
    "szaros",
    "szart",
    "szopd",
    "sále",
    "elmenyekvolgye",
    "immoviva",
    "infosarok",
]

INFORMAL = [
    "baromság",
    "dencey",
    "haha",
    "hahaha",
    "hehe",
    "hello",
    "hihi",
    "hülyeség",
    "képviselőink",
    "képviselőinket",
    "képünkbe",
    "lol",
    "megválasszuk",
    "mészárosaim",
    "országunk",
    "special",
    "soknevű",
    "szavazatunkat",
    "szeretem",
    "szeretlek",
    "szerintem",
    "szia",
    "sziasztok",
    "tex",
    "xdd",
    "xddd",
    "tudjátok",
    "tönkretesszük",
    "ugye",
    "unokáink",
    "user",
    "utálom",
    "vagyok",
    "vagytok",
]

OTHER = [
    """A Károlyi-kert közpark Budapest V. kerületében. A Belváros legrégibb
    kertje, valamint a kevés magyarországi palotakert között a legjobban
    dokumentált. A kertet északról a Ferenczy István utca, keletről a Magyar
    utca, délről a Henszlmann Imre utca, nyugatról a Károlyi-palota
    határolja. 1932 óta funkcionál közparkként, területe a 17. század
    vége óta változatlan: 7625 m², vagyis 0,76 hektár."""
]


def test_badwords():
    compare_extraction(hungarian.badwords.revision.datasources.matches, BAD,
                       OTHER)

    eq_(hungarian.badwords, pickle.loads(pickle.dumps(hungarian.badwords)))


def test_informals():
    compare_extraction(hungarian.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    eq_(hungarian.informals, pickle.loads(pickle.dumps(hungarian.informals)))


def test_dictionary():
    cache = {
        revision_oriented.revision.text:
            'nyugatról között  worngly.'
    }
    eq_(solve(
            hungarian.dictionary.revision.datasources.dict_words,
            cache=cache),
        ["nyugatról", "között"])
    eq_(solve(hungarian.dictionary.revision.datasources.non_dict_words,
              cache=cache),
        ["worngly"])

    eq_(hungarian.dictionary,
        pickle.loads(pickle.dumps(hungarian.dictionary)))


def test_stopwords():
    cache = {
        revision_oriented.revision.text:
            'játszótérnek adott helyett park'
    }
    eq_(solve(hungarian.stopwords.revision.datasources.stopwords, cache=cache),
        ['adott', ])
    eq_(solve(hungarian.stopwords.revision.datasources.non_stopwords,
        cache=cache),
        ['játszótérnek', 'helyett', 'park'])

    eq_(hungarian.stopwords, pickle.loads(pickle.dumps(hungarian.stopwords)))
