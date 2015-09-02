import pickle

from nose.tools import eq_

from .. import english
from ...datasources import revision
from ...dependencies import solve

BAD = [
    "ass", "arse", "ASS", "assface", "asses", "stupidass", "fatass", "lazyass",
    "assclown", "asshat", "stupidasshat", "stupidarsehat",
    "autofellate", "autofellation", "autofellatio",
    "bitch", "biotch", "BITCH", "bitchface", "bitches", "supidbitch",
    "asdasdbitchasdlnasla",
    "blowjob", "blowme",
    "bollocks",
    "booger", "boogers", "boogereater", "boooooger"
    "bootlip",
    "bugger",
    "butt", "buttfuck", "buttclown", "assbuttclown",
    "clunge",
    "cock", "cocks", "cocking", "cockface",
    "coon", "coooon",
    "cracker", "kracker",
    "crackhead",
    "crook",
    "cunt", "CUNT", "cuntface", "cunts", "stupidcunt",
    "dick", "dicks", "dicking", "dickface", "limpdick",
    "dildo",
    "dishonest",
    "defraud",
    "dothead",
    "dyke",
    "fag", "faggot", "phaggot", "faaaag", "fagface", "fags",
    "fart", "farteater", "farter", "farting",
    "fuck", "FUCK", "fuckface", "fucker", "stupidfuck", "whatthefuck",
    "gay", "gaaaay", "gays", "ghey",
    "gyp", "gypie", "gippo", "gyppie",
    "gook", "goook",
    "hillbilly", "hill-billy",
    "hooker",
    "homosexual", "homo",
    "injun",
    "jap", "jappo",
    "kike", "kyke", "kiike",
    "kwashee", "kwashi",
    "lesbian",
    "liar",
    "meth", "methhead",
    "nazi", "nazzzi",
    "nigger", "nigga", "nig", "niglet", "nigra",
    "nonce", "noncer", "noncing",
    "overdosed",
    "peckerwood",
    "penis", "peni", "penises",
    "pedo", "pedophile", "paedophyles", "pedofile",
    "piss", "pissface", "pisser",
    "pothead",
    "prostitute", "prostituteface"
    "qwashi", "qwashee",
    "raghead", "rag-head",
    "redneck", "red-neck",
    "redskin", "red-skin",
    "roundeye", "round-eye",
    "satanic", "satanists",
    "shit", "SHIT", "shitface", "shitting", "stupidshit", "shite", "shat",
    "slut", "SLUT", "slutface", "slutty",
    "spik", "spick", "spig", "spic",
    "subnormal",
    "squarehead",
    "terrorist", "terrorising", "terrorised", "terrorized", "terrorists",
    "theif", "theives",
    "tits", "titties", "tities", "titty",
    "transexual", "tranny",
    "twat", "TWAT", "twatface", "twatting", "stupidtwat",
    "vagina", "vajaja", "vag",
    "wank", "wanker", "wanka", "wankface",
    "wetback", "wetbacker",
    "whore", "WHORE", "whoreface", "whoring", "stupidwhore",
    "wog", "woggg",
    "wop", "woppp",
    "yid",
    "zipperhead"
]

INFORMAL = [
    "ain't", "aint",
    "awesome", "AWESOME", "aaawsome", "awesom",
    "bla", "blah", "blaaahhh", "blahblahblahblaaaaa",
    "bro",
    "bye", "byebye",
    "boner", "booner",
    "can't", "cant",
    "cool", "kewl", "cooler", "coolest", "coolass",
    "chug",
    "crap", "crappp", "crappiest", "crappier",
    "don't", "dont",
    "dude", "duuuuude",
    "dumb", "dummy", "dumbest", "dummies",
    "dad", "daddy", "dada",
    "goodbye", "good-bye",
    "hi", "hihi", "ha", "haha", "hehe", "ho", "hoho", "hu", "huhu",
    "hello", "helo", "hellloooo",
    "hey", "heeeey", "haay",
    "hm", "hmmmm", "hhhmmmm",
    "i", "I",
    "idiot", "idiooot",
    "lol", "lololol", "LLLolLLLlOL",
    "love", "looove", "luv",
    "meow", "meeeoooow",
    "mom", "mommy", "momma",
    "moron",
    "munch",
    "nope",
    "omg",
    "ok", "okay",
    "poop", "poooops"
    "pretty",
    "retard", "retarded", "tard",
    "smelly",
    "soo", "soooooo",
    "stupid", "stooopid", "stupidface", "brainstupid"
    "suck", "sucker", "sucking", "sux",
    "shouldn't", "shouldnt",
    "test edit",
    "turd", "turds",
    "wasn't", "wasnt",
    "whatsup", "wuzzzap", "wussup",
    "wuz",
    "won't", "wont",
    "woof",
    "wtf", "omgwtfbbq",
    "ya'll", "yall",
    "yay", "yyyaaaayyyy",
    "yeah", "yea", "yeaaaa",
    "you", "you've", "you're", "you'll",
    "yolo", "yooolloo"
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
    compare_extraction(english.revision.badwords_list, BAD, OTHER)


def test_informals():
    compare_extraction(english.revision.informals_list, INFORMAL, OTHER)


def test_presence():
    assert hasattr(english.revision, "words")
    assert hasattr(english.revision, "content_words")
    assert hasattr(english.revision, "badwords")
    assert hasattr(english.revision, "informals")
    assert hasattr(english.revision, "misspellings")

    assert hasattr(english.parent_revision, "words")
    assert hasattr(english.parent_revision, "content_words")
    assert hasattr(english.parent_revision, "badwords")
    assert hasattr(english.parent_revision, "informals")
    assert hasattr(english.parent_revision, "misspellings")

    assert hasattr(english.diff, "words_added")
    assert hasattr(english.diff, "badwords_added")
    assert hasattr(english.diff, "informals_added")
    assert hasattr(english.diff, "misspellings_added")
    assert hasattr(english.diff, "words_removed")
    assert hasattr(english.diff, "badwords_removed")
    assert hasattr(english.diff, "informals_removed")
    assert hasattr(english.diff, "misspellings_removed")


def test_revision():
    # Words
    cache = {revision.text: "I have an m80; and a shovel."}
    eq_(solve(english.revision.words_list, cache=cache),
        ["I", "have", "an", "m80", "and", "a", "shovel"])

    # Misspellings
    cache = {revision.text: 'This is spelled worngly. <td>'}
    eq_(solve(english.revision.misspellings_list, cache=cache), ["worngly"])

    # Infonoise
    cache = {revision.text: "This is running!"}
    eq_(solve(english.revision.infonoise, cache=cache), 3/13)


def test_pickling():

    eq_(english, pickle.loads(pickle.dumps(english)))
