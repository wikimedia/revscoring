import pickle

from nose.tools import eq_

from .. import norwegian
from ...datasources import revision_oriented
from ...dependencies import solve
from .util import compare_extraction

BAD = [
    "b1tch",
    "bitch",
    "blabla",
    "boobs",
    "bullshit",
    "bæsj",
    "bæsje",
    "bæsjen",
    "bæsjer",
    "cool",
    "cunt",
    "drit",
    "dritt",
    "fack",
    "faen",
    "fitta",
    "fitte",
    "fuck",
    "fucka",
    "homo",
    "homoseksuell",
    "homse",
    "hore",
    "jævla",
    "jævlig",
    "knull",
    "knulle",
    "kuk",
    "kukk",
    "kåt",
    "kødd",
    "ludder",
    "mordi",
    "motherfucker",
    "niggah",
    "nigger",
    "p0rn",
    "p3nis",
    "p3n1s",
    "pen1s",
    "pikk",
    "porn",
    "pr0n",
    "pule",
    "pulte",
    "pupper",
    "pussy",
    "rompa",
    "rompe",
    "ræva",
    "stupid",
    "teit",
    "tissemann",
    "tits",
    "twat",
    "wanker",
    "weed",
    "whore"
]

INFORMAL = [
    "haha",
    "hallo",
    "hehe",
    "hei",
    "heisann",
    "hey",
    "heya",
    "hihi",
    "lmao",
    "lol",
    "omg",
    "rofl",
    "yea",
    "yeah"
]

OTHER = [
    """
    Moulana Jalalod-din Balkhi Mohammad Rumi (født 30. september 1207 i Balkh,
    død 17. desember 1273 i Konya i daværende Persia) var en dikter,
    jurist, mystiker og teolog av tyrkisk, tadsjikisk eller persisk
    opprinnelse. Hans tilhengere stiftet den sufistiske Mevlevi-ordenen,
    kjent som De dansende dervisjer. Han skrev også flere bøker, hvorav den
    mest kjente er Masnavi-ye ma'navi, en samling av lignelser i diktform,
    ofte omtalt som «Koranen på persisk tungemål» (qorân dar zabân-e pahlavi).
    """
]

r_text = revision_oriented.revision.text


def test_badwords():
    compare_extraction(norwegian.badwords.revision.datasources.matches,
                       BAD, OTHER)

    eq_(norwegian.badwords, pickle.loads(pickle.dumps(norwegian.badwords)))


def test_informals():
    compare_extraction(norwegian.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    eq_(norwegian.informals, pickle.loads(pickle.dumps(norwegian.informals)))


def test_dictionary():
    cache = {r_text: "Hans tilhengere stiftet den worngly."}
    eq_(solve(norwegian.dictionary.revision.datasources.dict_words,
              cache=cache),
        ["Hans", "tilhengere", "stiftet", "den"])
    eq_(solve(norwegian.dictionary.revision.datasources.non_dict_words,
        cache=cache),
        ["worngly"])

    eq_(norwegian.dictionary, pickle.loads(pickle.dumps(norwegian.dictionary)))


def test_stopwords():
    cache = {r_text: "samme senere nye anmeldere."}
    eq_(solve(norwegian.stopwords.revision.datasources.stopwords, cache=cache),
        ["samme", "senere", "nye"])
    eq_(solve(norwegian.stopwords.revision.datasources.non_stopwords,
              cache=cache),
        ["anmeldere"])

    eq_(norwegian.stopwords, pickle.loads(pickle.dumps(norwegian.stopwords)))
