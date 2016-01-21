import pickle

from nose.tools import eq_

from .. import french
from ...datasources import revision_oriented
from ...dependencies import solve
from .util import compare_extraction

BAD = [
    "anus",
    "baise", "baisé",
    "baiz",
    "batar", "batard",
    "bite", "bites", "bitte",
    "branler", "branlette", "branleur",
    "caca", "cacas",
    "caliss",
    "chiant", "chiante", "chiasse",
    "chie", "chié", "chienne", "chier", "chiote", "chiotte",
    "con", "conar", "conard", "connar", "connard", "connards", "connasse",
        "conne", "connerie", "conneries",
    "couille", "couilles", "couillon",
    "cul",
    "debile", "débile",
    "ducon",
    "emmerde",
    "encule", "enculer", "enculé", "enculés",
    "enmerde",
    "fesse", "fesses",
    "fion",
    "foutre",
    "homosexuel",
    "lesbien",
    "marde", "merde", "merdes", "merdique",
    "nike", "niker", "nique", "niquer",
    "pd",
    "pedophile", "pédophile", "pédé",
    "petasse",
    "pipi",
    "pisse",
    "poop",
    "pouri", "pourri",
    "prostitué", "prostituee",
    "prout", "proute",
    "pue", "pues",
    "puta", "putain", "pute", "putes", "putin",
    "pénis",
    "pétasse",
    "quequette",
    "queu", "queue",
    "salaud",
    "salo", "salop", "salope", "salopes",
    "sodomie", "sodomiser",
    "stupide",
    "suce", "sucer", "suceur", "suceuse",
    "sucé",
    "tapette",
    "teub",
    "vagin",
    "zboub",
    "zizi"
]

INFORMAL = [
    "ahah",
    "allez",
    "allo",
    "bisous",
    "bla", "blabla", "blablabla",
    "bonjour",
    "coucou",
    "etais",
    "etes",
    "haha",
    "hahaha", "hahahaha", "hahahahaha",
    "hihi", "hihihi",
    "insérez",
    "jadore",
    "jai",
    "kikoo",
    "lol", "lool",
    "mdr", "mdrr",
    "moche",
    "ouai",
    "ouais",
    "ptdr",
    "truc",
    "voila",
    "voulez"
]

OTHER = [
    "connection", "fitness", "le"
]

r_text = revision_oriented.revision.text


def test_badwords():
    compare_extraction(french.badwords.revision.datasources.matches,
                       BAD, OTHER)

    eq_(french.badwords, pickle.loads(pickle.dumps(french.badwords)))


def test_informals():
    compare_extraction(french.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    eq_(french.informals, pickle.loads(pickle.dumps(french.informals)))


def test_dictionary():
    cache = {r_text: "Est un projet principe du worngly. <td>"}
    eq_(solve(french.dictionary.revision.datasources.dict_words, cache=cache),
        ["Est", "un", "projet", "principe", "du"])
    eq_(solve(french.dictionary.revision.datasources.non_dict_words,
              cache=cache),
        ["worngly"])

    eq_(french.dictionary, pickle.loads(pickle.dumps(french.dictionary)))


def test_stopwords():
    cache = {r_text: "Est un projet principe du worngly. <td>"}
    eq_(solve(french.stopwords.revision.datasources.stopwords, cache=cache),
        ["Est", "un", "du"])
    eq_(solve(french.stopwords.revision.datasources.non_stopwords,
              cache=cache),
        ["projet", "principe", "worngly"])

    eq_(french.stopwords, pickle.loads(pickle.dumps(french.stopwords)))


def test_stemmed():
    cache = {r_text: "Est un projet principe du worngly. <td>"}
    eq_(solve(french.stemmed.revision.datasources.stems, cache=cache),
        ["est", "un", "projet", "princip", "du", "worngly"])

    eq_(french.stemmed, pickle.loads(pickle.dumps(french.stemmed)))
