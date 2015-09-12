import pickle

from nose.tools import eq_

from .. import german
from ...datasources import revision
from ...dependencies import solve

BAD = [
    "arsch", "arschfick", "arschficken", "arschgesicht", "arschloch", "arschlöcher", "assi",
    "bescheuert", "bitch", "bitches", "deppen", "dumm", "fettsack", "ficker", "fotze", "fotzen",
    "fucker", "fucking", "gaylord", "gefickte", "homofürst", "hure", "huren", "hurensohn",
    "hurensöhne", "hurre", "hurrensohn", "idiot", "idioten", "kacka", "kacke", "kackwurst",
    "kanacken", "lutscher", "missgeburt", "mistgeburt", "motherfucker", "muschis", "nigga",
    "nigger", "noobs", "nutte", "peniskopf", "penisse", "pennis", "pisser", "sau", "scheise",
    "scheiss", "scheisse", "scheiß", "scheiße", "scheißen", "schlampe", "schwanzlutscher", "schwuchtel",
    "schwuchteln", "schwul", "schwuler", "schwull", "schwänze", "spasst", "spast", "spasten",
    "verarscht", "verfickte", "vollidiot", "wichser", "wixer", "wixxe", "wixxen", "wixxer"
]

INFORMAL = [
    "anal", "auserdem", "autorenportal", "bins", "bla", "blabla", "blablabla", "blub", "blubb",
    "blöd", "blöder", "bodewell", "bumsen", "cool", "coole", "cooler", "coolste", "coool", "deine",
    "digga", "dildo", "dildos", "doof", "dumme", "dummen", "dummer", "dummes", "dummm", "döner",
    "euch", "fetter", "fick", "ficke", "ficken", "fickt", "fickte", "fickten", "fresse", "fuck",
    "furtz", "furz", "furzen", "fürn", "fürze", "gay", "gefickt", "gehts", "geil", "geile", "geilen",
    "geiler", "geilste", "geilsten", "gez", "grüße", "hab", "haha", "hahah", "hahaha", "hahahah",
    "hahahaha", "hahahahaha", "hahahahahaha", "hahahahahahaha", "halllo", "hallo", "halts", "hehe",
    "hey", "hihi", "hihihi", "homos", "huhu", "hässlich", "jaja", "jannik", "juhu", "kack", "kacken",
    "kackt", "kaka", "kake", "kaken", "klo", "kneipenschlägerein", "kotze", "kotzen", "kursiver",
    "könnt", "labert", "lalala", "lalalala", "langhaardackel", "langweilig", "leck", "lecker", "leckt",
    "lol", "lonni", "looser", "lutschen", "lutscht", "mama", "mfg", "minecraft", "moin", "mudda",
    "mudder", "muhaha", "muhahaha", "mumu", "muschi", "muschie", "möse", "naja", "nich", "nix",
    "noob", "nutten", "oma", "omg", "opfa", "penis", "penise", "penisen", "penises", "penner",
    "pimmel", "pipi", "pisse", "popel", "popo", "porno", "pornos", "puff", "puffs", "pups", "pupsen",
    "rofl", "schei", "scheis", "schlampen", "schniedel", "schwachsinn", "schwule", "seid", "sex", "sexy",
    "shit", "soo", "sooo", "soooo", "sooooo", "spasti", "spezial", "stingt", "stink", "stinke", "stinken",
    "stinker", "stinkst", "stinkt", "sucks", "swag", "titte", "titten", "tobi", "toll", "unformatierten",
    "vaginas", "wisst", "xdd", "xddd", "xdddd", "xnxx", "yeah", "yolo", "youporn", "ärsche"
]

OTHER = [
    """
    The Smyth Report is the common name of an administrative history written
    by physicist Henry DeWolf Smyth about the Manhattan Project, the Allied
    effort to develop atomic bombs during World War II. It was released to the
    public on August 12, 1945, just days after the atomic bombings of Hiroshima
    and Nagasaki. Smyth was commissioned to write the report by Major General
    Leslie Groves, the director of the Manhattan Project. The Smyth Report was
    the first official account of the development of the atomic bombs and the
    basic physical processes behind them. Since anything in the declassified
    Smyth Report could be discussed openly, it focused heavily on basic nuclear
    physics and other information which was either already widely known in the
    scientific community or easily deducible by a competent scientist. It
    omitted details about chemistry, metallurgy, and ordnance, ultimately
    giving a false impression that the Manhattan Project was all about physics.
    """,
    'association', 'shihtzhu', 'Wafflehats', "he", "hay", "morass", "wood",
    "pecker", 'suction', 'vaginal', 'titillatingly', 'test', 'edit'
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
    cache = {revision.text: "I have an m80; and a shovel."}
    eq_(solve(german.revision.words_list, cache=cache),
        ["I", "have", "an", "m80", "and", "a", "shovel"])

    # Misspellings
    cache = {revision.text: 'This is spelled worngly. <td>'}
    eq_(solve(german.revision.misspellings_list, cache=cache), ["worngly"])

    # Infonoise
    cache = {revision.text: "This is running!"}
    eq_(solve(german.revision.infonoise, cache=cache), 3/13)


def test_pickling():

    eq_(german, pickle.loads(pickle.dumps(german)))
