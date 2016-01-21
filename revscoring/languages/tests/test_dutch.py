import pickle

from nose.tools import eq_

from .. import dutch
from ...datasources import revision_oriented
from ...dependencies import solve
from .util import compare_extraction

BAD = [
    "aars",
    "anaal", "anus",
    "balhaar",
    "drol", "drollen",
    "fack", "facking",
    "flikker", "flikkers",
    "focking",
    "geil", "geile", "gelul",
    "geneukt",
    "hoer", "hoere", "hoeren",
    "homo", "homos",
    "kak", "kaka",
    "kakhoofd", "kakken",
    "kanker", "kenker",
    "klootzak", "klootzakken",
    "klote",
    "kont", "kontgat",
    "kontje",
    "pedo",
    "penis", "penissen",
    "peop",
    "piemel", "piemels",
    "pijpen",
    "pik",
    "pimel",
    "pipi",
    "poep", "poepchinees", "poepen", "poephoofd",
    "poepie", "poepje", "poepjes", "poepsex", "poept", "poepte",
    "porn", "porno",
    "neuk", "neuke",
    "neuken", "neukende",
    "neukt", "neukte", "neukten",
    "strond", "stront",
    "suck", "sucks", "suckt",
    "zuigt",
    "sukkel", "sukkels",
    "tering", "tetten", "tieten",
    "vagina",
    "verekte", "verkracht",
    "dikzak",
    "dildo",
    "mogolen", "mogool", "mongool", "mooiboy",
    "neger", "negers",
    "shit",
    "sperma",
    "kut", "kutje", "kutjes",
    "stelletje",
    "loser", "losers",
    "lul", "lullen",
    "reet",
    "scheet", "scheten",
    "schijt",
    "diaree",
    "slet",
    "lekkerding",
    "likken"
]

INFORMAL = [
    "aap", "aapjes",
    "banaan",
    "bent",
    "boe", "boeit",
    "doei"
    "dombo", "domme",
    "eigelijk",
    "godverdomme",
    "groetjes",
    "gwn",
    "hoi",
    "hallo", "halloo",
    "heb",
    "heej", "heey", "heeel",
    "hou", "houd",
    "hoihoi", "hoii", "hoiii",
    "hoor",
    "izan",
    "jij",
    "jou",
    "jullie",
    "kaas",
    "klopt",
    "kots",
    "kusjes",
    "lekker", "lekkere", "lkkr",
    "maarja",
    "mama",
    "nou",
    "oma",
    "ofzo",
    "oke",
    "sex", "sexy",
    "snap",
    "stinken", "stinkt",
    "stoer",
    "swag",
    "swek",
    "vies", "vieze",
    "vind",
    "vuile",
    "xxx",
    "zielig",
    "zooi",
    "yolo",
    "zeg"
]

OTHER = [
    """
    De stemtoonhoogte is de toonhoogte van de kamertoon. Door middel van een
    stemvork is deze kamertoon beschikbaar voor het stemmen van een
    muziekinstrument.

    Internationaal is deze toonhoogte in het midden van de 20e eeuw vastgesteld
    op een frequentie van 440 Hz. De stemtoon lag echter niet altijd vast. Soms
    leest men ergens dat de stemtoon door de eeuwen heen steeds hoger is komen
    te liggen, maar dat is slechts de helft van het verhaal. Er waren orgels
    die een hogere stemtoon hadden, en later lager gestemd werden. Kerkorgels
    verschilden enorm van stemtoon. In de loop van de tijd is die variatie
    steeds kleiner geworden. Naarmate mensen steeds mobieler werden, ontstond
    ook de behoefte aan meer compatibiliteit van instrumenten.
    """
]


def test_badwords():
    compare_extraction(dutch.badwords.revision.datasources.matches, BAD, OTHER)

    eq_(dutch.badwords, pickle.loads(pickle.dumps(dutch.badwords)))


def test_informals():
    compare_extraction(dutch.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    eq_(dutch.informals, pickle.loads(pickle.dumps(dutch.informals)))


def test_dictionary():
    cache = {revision_oriented.revision.text: 'Door middel van een worngly.'}
    eq_(solve(dutch.dictionary.revision.datasources.dict_words, cache=cache),
        ["Door", "middel", "van", "een"])
    eq_(solve(dutch.dictionary.revision.datasources.non_dict_words,
              cache=cache),
        ["worngly"])

    eq_(dutch.dictionary, pickle.loads(pickle.dumps(dutch.dictionary)))


def test_stopwords():
    cache = {revision_oriented.revision.text: 'Door middel van een!'}
    eq_(solve(dutch.stopwords.revision.datasources.stopwords, cache=cache),
        ["Door", "van", "een"])
    eq_(solve(dutch.stopwords.revision.datasources.non_stopwords,
        cache=cache),
        ["middel"])

    eq_(dutch.stopwords, pickle.loads(pickle.dumps(dutch.stopwords)))


def test_stemmed():
    cache = {revision_oriented.revision.text: 'Door middel van een!'}
    eq_(solve(dutch.stemmed.revision.datasources.stems, cache=cache),
        ["dor", "middel", "van", "een"])

    eq_(dutch.stemmed, pickle.loads(pickle.dumps(dutch.stemmed)))
