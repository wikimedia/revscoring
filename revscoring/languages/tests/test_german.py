import pickle

from nose.tools import eq_

from .. import german
from ...datasources import revision
from ...dependencies import solve

BAD = [
    "ärsche", "arsch", "arschfick", "arschficken", "arschgesicht", "arschloch",
    "arschlöcher",
    "assi",
    "bescheuert",
    "deppen",
    "dumm",
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
    "autorenportal",
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
    Das Kürzel Gulag (russisch Гулаг) bezeich­net das Netz von Arbeits­lagern in
    der Sowjet­union; im weiteren Sinn steht es für die Gesamt­heit des
    sowje­tischen Zwangs­arbeits­systems, das auch Spezial­gefäng­nisse,
    Zwangs­arbeits­pflichten ohne Haft sowie einige psychia­trische Kliniken als
    Haft­verbüßungs­orte umfasste. Von 1930 bis 1953 waren in den Lagern
    mindes­tens 18 Millionen Menschen inhaf­tiert. Mehr als 2,7 Millionen starben
    im Lager oder in der Verbannung. In den letzten Lebens­jahren Stalins
    erreichte der Gulag mit rund 2,5 Millionen Insassen seine größte
    quantitative Aus­dehnung.
    """
]


def compare_extraction(extractor, examples, counter_examples):

    for example in examples:
        eq_(extractor.process(example), [example])
        eq_(extractor.process("Sentence " + example + " sandwich."), [example])
        eq_(extractor.process("Sentence end " + example + "."), [example])
        eq_(extractor.process(example + " start of sentence."), [example])

    for example in counter_examples:
        eq_(extractor.process(example), [])
        eq_(extractor.process("Sentence " + example + " sandwich."), [])
        eq_(extractor.process("Sentence end " + example + "."), [])
        eq_(extractor.process(example + " start of sentence."), [])


def test_badwords():
    compare_extraction(german.revision.badwords_list, BAD, OTHER)


def test_informals():
    compare_extraction(german.revision.informals_list, INFORMAL, OTHER)


def test_presence():
    assert hasattr(german.revision, "words")
    assert hasattr(german.revision, "content_words")
    assert hasattr(german.revision, "badwords")
    assert hasattr(german.revision, "informals")
    assert hasattr(german.revision, "misspellings")

    assert hasattr(german.parent_revision, "words")
    assert hasattr(german.parent_revision, "content_words")
    assert hasattr(german.parent_revision, "badwords")
    assert hasattr(german.parent_revision, "informals")
    assert hasattr(german.parent_revision, "misspellings")

    assert hasattr(german.diff, "words_added")
    assert hasattr(german.diff, "badwords_added")
    assert hasattr(german.diff, "informals_added")
    assert hasattr(german.diff, "misspellings_added")
    assert hasattr(german.diff, "words_removed")
    assert hasattr(german.diff, "badwords_removed")
    assert hasattr(german.diff, "informals_removed")
    assert hasattr(german.diff, "misspellings_removed")


def test_revision():
    # Words
    cache = {revision.text: "Hinzu kamen rund sechs m80 Personen."}
    eq_(solve(german.revision.words_list, cache=cache),
        ["Hinzu", "kamen", "rund", "sechs", "m80", "Personen"])

    # Misspellings
    cache = {revision.text: 'Hinzu kamen rund worngly. <td>'}
    eq_(solve(german.revision.misspellings_list, cache=cache), ["worngly"])

    # Infonoise
    cache = {revision.text: "Hinzu kamen rund!"}
    eq_(solve(german.revision.infonoise, cache=cache), 12/14)


def test_pickling():

    eq_(german, pickle.loads(pickle.dumps(german)))
