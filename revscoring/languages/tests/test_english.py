import pickle

from nose.tools import eq_

from .. import english
from ...datasources import revision_oriented
from ...dependencies import solve
from .util import compare_extraction

BAD = [
    "ass", "arse", "ASS", "assface", "asses", "stupidass", "fatass", "lazyass",
    "assclown", "asshat", "stupidasshat", "stupidarsehat",
    "autofellate", "autofellation", "autofellatio",
    "bitch", "biotch", "BITCH", "bitchface", "bitches",
    "blowjob", "blowme",
    "bollocks",
    "booger", "boogers", "boogereater", "boooooger",
    "bootlip",
    "bugger",
    "butt", "buttfuck", "buttclown", "assbuttclown",
    "clunge",
    "cock", "cocks", "cocking", "cockface",
    "coon", "coooon",
    "cracker", "kracker",
    "crackhead",
    "crook",
    "cunt", "CUNT", "cuntface", "cunts", "stupidcunt", "cunthead",
    "dick", "dicks", "dicking", "dickface", "limpdick",
    "dildo",
    "dishonest",
    "defraud",
    "dothead",
    "dyke",
    "fag", "faggot", "phaggot", "faaaag", "fagface", "fags",
    "fart", "farteater", "farter", "farting",
    "fuck", "FUCK", "fuckface", "fucker", "stupidfuck", "fuckboy", "fuckboi",
    "gay", "gaaaay", "gays", "ghey", "gayfuck",
    "gyp", "gypie", "gippo", "gyppie",
    "gook", "goook",
    "hillbilly", "hill-billy",
    "hooker",
    "homosexual", "homo",
    "injun",
    "jap", "jappo",
    "kike", "kyke", "kiike",
    "kwashee", "kwashi",
    "lesbian", "lesbo",
    "liar",
    "meth", "methhead",
    "nazi", "nazzzi",
    # The decision was made that "niggardly" is almost never used in good faith
    "nigger", "nigga", "nig", "niglet", "nigra", "niggardlyi",
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
    "shit", "SHIT", "shitface", "shitting", "stupidshit", "shat", "shithead",
    "slut", "SLUT", "slutface", "slutty",
    "spik", "spick", "spig", "spic",
    "subnormal",
    "squarehead",
    "terrorist", "terrorising", "terrorised", "terrorized", "terrorists",
    "theif", "theives",
    "tits", "titties", "tities", "titty",
    "transexual", "tranny",
    "twat", "TWAT", "twatface", "twatting", "stupidtwat",
    "vagina", "vajaja", "vag", "vajayjay",
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
    "hi", "hihi", "ha", "haha", "hehe", "ho", "hoho", "hu", "huhu", "muhaha",
    "mwuhahaha",
    "hello", "helo", "hellloooo",
    "hey", "heeeey", "haay",
    "hm", "hmmmm", "hhhmmmm",
    "i", "I",
    "idiot", "idiooot",
    "lalala", "lalalala",
    "lol", "lololol", "LLLolLLLlOL",
    "loser",
    "love", "looove", "luv",
    "meow", "meeeoooow",
    "mom", "mommy", "momma",
    "moron",
    "munch",
    "nope",
    "nerd", "nerds",
    "noob", "noobs",
    "omg",
    "ok", "okay",
    "poop", "poooops"
    "pretty",
    "retard", "retarded", "tard",
    "rofl",
    "sexy", "sexxxy",
    "smelly",
    "soo", "soooooo",
    "sorry",
    "stupid", "stooopid", "stupidface",
    "stink", "stinky", "stinks",
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
    'association', 'shihtzhu', 'shih tzu', 'shih tzhu', 'Wafflehats',
    "he", "hay", "morass", "wood",
    "pecker", 'suction', 'vaginal', 'titillatingly', 'test', 'edit'
]

r_text = revision_oriented.revision.text


def test_badwords():
    compare_extraction(english.badwords.revision.datasources.matches,
                       BAD, OTHER)

    eq_(english.badwords, pickle.loads(pickle.dumps(english.badwords)))


def test_informals():
    compare_extraction(english.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    eq_(english.informals, pickle.loads(pickle.dumps(english.informals)))


def test_dictionary():
    cache = {r_text: 'This is spelled worngly. <td>'}
    eq_(solve(english.dictionary.revision.datasources.dict_words, cache=cache),
        ["This", "is", "spelled"])
    eq_(solve(english.dictionary.revision.datasources.non_dict_words,
              cache=cache),
        ["worngly"])

    eq_(english.dictionary, pickle.loads(pickle.dumps(english.dictionary)))


def test_stopwords():
    cache = {r_text: 'This is spelled worngly. <td>'}
    eq_(solve(english.stopwords.revision.datasources.stopwords, cache=cache),
        ["This", "is"])
    eq_(solve(english.stopwords.revision.datasources.non_stopwords,
        cache=cache),
        ["spelled", "worngly"])

    eq_(english.stopwords, pickle.loads(pickle.dumps(english.stopwords)))


def test_stemmmed():
    cache = {r_text: 'This is spelled worngly. <td>'}
    eq_(solve(english.stemmed.revision.datasources.stems, cache=cache),
        ["this", "is", "spell", "worng"])

    eq_(english.stemmed, pickle.loads(pickle.dumps(english.stemmed)))
