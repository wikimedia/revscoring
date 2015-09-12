import pickle

from nose.tools import eq_

from .. import dutch
from ...datasources import revision
from ...dependencies import solve

BAD = [
    "aars", "anaal", "anus", "balhaar", "drol", "drollen", "fack", "facking",                             
    "fuck", "fucking", "gay", "geil", "geile", "gelul", "geneukt", "hoer",                             
    "homos", "kak", "kaka", "kakhoofd", "kakken", "kanker", "kenker", "klootzak",                             
    "kontgat", "kontje", "pedo", "penis", "penissen", "peop", "piemel", "piemels",                             
    "pipi", "poep", "poepchinees", "poepen", "poephoofd", "poepie", "poepje", "poepjes",                             
    "porn", "porno", "neuk", "neuke", "neuken", "neukende", "neukt", "neukte",                             
    "suck", "sucks", "suckt", "zuigt", "sukkel", "sukkels", "tering", "tetten",                             
    "verkracht", "dikzak", "dildo", "mogolen", "mogool", "mongool", "mooiboy", "neger",                             
    "kut", "kutje", "kutjes", "stelletje", "loser", "losers", "lul", "lullen",                             
    "reet", "scheet", "scheten", "schijt", "diaree", "slet", "lekkerding", "likken",   
    "utme", "utml", "utmn", "utmz", "rdn", "cest", "cet", "sophonpanich",
    "boe", "dombo", "domme", "godverdomme", "izan", "kots", "kusjes", "lekker", "lekkere",
    "lkkr", "nerd", "nerds", "noob", "noobs", "sex", "sexy", "stink", "stinken", "stinkt",
    "stoer", "vies", "vieze", "vuile", "xxx", "zielig", "zooi", "swag", "swek", "yolo"
]

INFORMAL = [
    "hoi", "hey", "hallo", "doei", "heej", "heey", "groetjes", "halloo", "hoihoi", "hoii",
    "hoiii", "heb", "zeg", "vind", "bent", "snap", "boeit", "klopt", "hou", "houd",
    "gwn", "maarja", "nou", "ofzo", "oke", "yeah", "hoor", "hihi", "eigelijk", "heeel", "jij",
    "jou", "jullie", "sorry", "vetgedrukte", "deelonderwerp", "cursieve", "nowiki", "bewerkingsveld",
    "cursief", "minecraft", "hotmail", "hyves", "bieber", "werkstuk", "spreekbeurt", "haha", "hahah",
    "hahaha",     "hahahah", "hahahaha", "hahahahah", "hahahahaha", "hahahahahaha", "lala", "lalala",
    "lalalala", "lalalalala", "bla", "blabla", "blablabla", "cool", "coole", "coolste", "dikke", "dom",
    "lelijk", "lelijke", "lelijkste", "leuk", "leuke", "lief", "onzin", "raar", "saai", "gek", "gekke",
    "goeie", "grappig", "stom", "stomme", "filmfocus", "filmliefde", "wikipedianl", "diakrieten", "egt",
    "jah", "jaja", "jwz", "lol", "lolz", "omg", "tog", "wtf", "zever"
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
    compare_extraction(dutch.revision.badwords_list, BAD, OTHER)


def test_informals():
    compare_extraction(dutch.revision.informals_list, INFORMAL, OTHER)


def test_presence():
    assert hasattr(dutch.revision, "words")
    assert hasattr(dutch.revision, "content_words")
    assert hasattr(dutch.revision, "badwords")
    assert hasattr(dutch.revision, "informals")
    assert hasattr(dutch.revision, "misspellings")

    assert hasattr(dutch.parent_revision, "words")
    assert hasattr(dutch.parent_revision, "content_words")
    assert hasattr(dutch.parent_revision, "badwords")
    assert hasattr(dutch.parent_revision, "informals")
    assert hasattr(dutch.parent_revision, "misspellings")

    assert hasattr(dutch.diff, "words_added")
    assert hasattr(dutch.diff, "badwords_added")
    assert hasattr(dutch.diff, "informals_added")
    assert hasattr(dutch.diff, "misspellings_added")
    assert hasattr(dutch.diff, "words_removed")
    assert hasattr(dutch.diff, "badwords_removed")
    assert hasattr(dutch.diff, "informals_removed")
    assert hasattr(dutch.diff, "misspellings_removed")


def test_revision():
    # Words
    cache = {revision.text: "I have an m80; and a shovel."}
    eq_(solve(dutch.revision.words_list, cache=cache),
        ["I", "have", "an", "m80", "and", "a", "shovel"])

    # Misspellings
    cache = {revision.text: 'This is spelled worngly. <td>'}
    eq_(solve(dutch.revision.misspellings_list, cache=cache), ["worngly"])

    # Infonoise
    cache = {revision.text: "This is running!"}
    eq_(solve(dutch.revision.infonoise, cache=cache), 3/13)


def test_pickling():

    eq_(dutch, pickle.loads(pickle.dumps(dutch)))
