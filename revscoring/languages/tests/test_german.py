import pickle

from nose.tools import eq_

from .. import german
from ...datasources import revision_oriented
from ...dependencies import solve
from .util import compare_extraction

BAD = [
    "ärsche", "arsch", "arschfick", "arschficken", "arschgesicht", "arschloch",
    "arschlöcher",
    "assi",
    "bescheuert",
    "deppen",
    "dumm",
    "du hurensohn",
    "fettsack",
    "ficker",
    "fotze", "fotzen",
    "gefickte",
    "homofürst",
    "hure", "huren", "hurensohn", "hurensöhne", "hurre", "hurrensohn",
    "idioten",
    "kacka", "kacke", "kackwurst",
    "kanacken",
    "lutscher",
    "missgeburt", "mistgeburt",
    "muschis",
    "nutte",
    "peniskopf", "penisse", "pennis", "penise", "penisen", "penises",
    "sau",
    "scheise", "scheiss", "scheisse", "scheiß", "scheiße", "scheißen",
    "schlampe",
    "schwanzlutscher",
    "schwuchtel", "schwuchteln", "schwul", "schwuler", "schwull",
    "schwänze",
    "spasst", "spast", "spasten",
    "verarscht",
    "verfickte",
    "vollidiot",
    "wichser",
    "wixer", "wixxe", "wixxen", "wixxer"
]

INFORMAL = [
    "auserdem",
    "bins",
    "bla", "blabla", "blablabla",
    "blub", "blubb",
    "blöd", "blöder",
    "bodewell",
    "bumsen",
    "cool", "coole", "cooler", "coolste", "coool",
    "deine",
    "digga",
    "dildo", "dildos",
    "doof",
    "dumme", "dummen", "dummer", "dummes", "dummm",
    "döner",
    "euch",
    "fetter",
    "fick", "ficke", "ficken", "fickt", "fickte", "fickten",
    "fresse",
    "furtz", "furz", "furzen", "fürn", "fürze",
    "gefickt",
    "gehts",
    "geil", "geile", "geilen", "geiler", "geilste", "geilsten",
    "gez",
    "grüße",
    "hab",
    "haha", "hahah", "hahaha", "hahahah", "hahahaha",
    "halllo", "hallo",
    "halts",
    "huhu",
    "hässlich",
    "jaja",
    "jannik",
    "juhu",
    "kack", "kacken", "kackt", "kaka", "kake", "kaken",
    "klo",
    "kneipenschlägerein",
    "kotze", "kotzen",
    "kursiver",
    "könnt",
    "labert",
    "lalala", "lalalala",
    "langhaardackel",
    "langweilig",
    "leck", "lecker", "leckt",
    "lonni",
    "looser",
    "lutschen", "lutscht",
    "mama",
    "mfg",
    "moin",
    "mudda", "mudder",
    "muhaha", "muhahaha",
    "mumu",
    "muschi", "muschie",
    "möse",
    "naja",
    "nich", "nix",
    "nutten",
    "oma",
    "opfa",
    "penner",
    "pimmel",
    "pipi",
    "pisse",
    "popel", "popo",
    "porno", "pornos",
    "puff", "puffs",
    "pups", "pupsen",
    "schei", "scheis",
    "schlampen",
    "schniedel",
    "schwachsinn",
    "schwule",
    "seid",
    "spasti",
    "stingt", "stink", "stinke", "stinken", "stinker", "stinkst", "stinkt",
    "swag",
    "titte", "titten",
    "tobi",
    "toll",
    "unformatierten",
    "vaginas",
    "wisst",
    "xdd", "xddd", "xdddd",
    "xnxx"
]

OTHER = [
    """
    Das Kürzel Gulag (russisch Гулаг) bezeich­net das Netz von Arbeits­lagern
    in der Sowjet­union; im weiteren Sinn steht es für die Gesamt­heit des
    sowje­tischen Zwangs­arbeits­systems, das auch Spezial­gefäng­nisse,
    Zwangs­arbeits­pflichten ohne Haft sowie einige psychia­trische Kliniken
    als Haft­verbüßungs­orte umfasste. Von 1930 bis 1953 waren in den Lagern
    mindes­tens 18 Millionen Menschen inhaf­tiert. Mehr als 2,7 Millionen
    starben im Lager oder in der Verbannung. In den letzten Lebens­jahren
    Stalins erreichte der Gulag mit rund 2,5 Millionen Insassen seine größte
    quantitative Aus­dehnung.
    """
]

r_text = revision_oriented.revision.text


def test_badwords():
    compare_extraction(german.badwords.revision.datasources.matches,
                       BAD, OTHER)

    eq_(german.badwords, pickle.loads(pickle.dumps(german.badwords)))


def test_informals():
    compare_extraction(german.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    eq_(german.informals, pickle.loads(pickle.dumps(german.informals)))


def test_dictionary():
    cache = {r_text: "Hinzu kamen rund sechs m80 Personen."}
    eq_(solve(german.dictionary.revision.datasources.dict_words, cache=cache),
        ["Hinzu", "kamen", "rund", "sechs", "Personen"])
    eq_(solve(german.dictionary.revision.datasources.non_dict_words,
        cache=cache),
        ["m80"])

    eq_(german.dictionary, pickle.loads(pickle.dumps(german.dictionary)))


def test_stopwords():
    cache = {r_text: "im Lager oder in der Verbannung."}
    eq_(solve(german.stopwords.revision.datasources.stopwords, cache=cache),
        ["im", "oder", "in", "der"])
    eq_(solve(german.stopwords.revision.datasources.non_stopwords,
              cache=cache),
        ["Lager", "Verbannung"])

    eq_(german.stopwords, pickle.loads(pickle.dumps(german.stopwords)))


def test_stemmed():
    cache = {r_text: "Hinzu kamen rund sechs m80 Personen."}
    eq_(solve(german.stemmed.revision.datasources.stems, cache=cache),
        ["hinzu", "kam", "rund", "sech", "m80", "person"])

    eq_(german.stemmed, pickle.loads(pickle.dumps(german.stemmed)))
