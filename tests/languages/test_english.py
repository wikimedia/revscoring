import pickle

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.languages import english

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
    "nazi", "nazzzi", "nazism",
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

# Borrowed from
# https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Words_to_watch
WORDS_TO_WATCH = [
    # Puffery
    "legendary", "best", "great", "acclaimed", "iconic",
    "visionary", "outstanding", "leading", "celebrated", "award-winning",
    "landmark", "cutting-edge", "innovative", "extraordinary", "brilliant",
    "hit", "famous", "renowned", "remarkable", "prestigious",
    "world-class", "respected", "notable", "virtuoso", "honorable",
    "awesome", "unique", "pioneering",
    # Contentious labels (-gate removed)
    "cult", "racist", "perverted", "sect", "fundamentalist", "heretic",
    "extremist", "denialist", "terrorist", "freedom fighter", "bigot",
    "myth", "neo-Nazi", "pseudoscientific", "controversial",
    # Unsupported attributions
    "people say", "scholars state", "it is believed", "it is regarded",
    "are of the opinion", "most feel", "many feel", "experts declare",
    "it is often reported", "it is sometimes said", "it is widely thought",
    "research has shown", "science says", "experts say", "scientists claim",
    # Expressions of doubt
    "supposed", "apparent", "purported", "alleged", "accused", "so-called",
    # Editorializing
    "notably", "it should be noted", "arguably", "interestingly",
    "essentially", "actually", "clearly", "of course", "without a doubt",
    "happily", "tragically", "aptly", "fortunately", "unfortunately",
    "untimely", "but", "despite", "however", "though", "although",
    "furthermore",
    # Synonyms for "said"
    "reveal", "point out", "clarify", "expose", "explain", "find", "note",
    "observe", "insist", "speculate", "surmise", "claim", "assert", "admit",
    "confess", "deny",
    # Lack of precision
    "passed away", "gave his life", "eternal rest", "make love",
    "an issue with", "collateral damage", "living with cancer",
    # Idioms
    "lion's share", "tip of the iceberg", "white elephant", "gild the lily",
    "take the plunge", "ace up the sleeve", "bird in the hand",
    "twist of fate", "at the end of the day",
    # Relative time reference
    "recently", "lately", "currently", "today", "presently", "to date",
    "15 years ago", "formerly", "in the past", "traditionally",
    "this fall", "this year", "last autumn", "next month",
    "yesterday", "tomorrow", "in the future", "now", "soon", "since",
    # Unspecified places or events
    "this country", "here", "there", "somewhere", "sometimes", "often",
    "occasionally", "somehow",
    # Survived by
    "is survived by", "was survived by",
    # Neologisms
    "pre-trumpism", "post-truth", "anti-choice", "trump-like"
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
    basic physical processes behind them. Anything in the declassified
    Smyth Report could be discussed openly, so it focused heavily on basic
    nuclear physics and other information which was either already widely known
    in the scientific community or easily deducible by a competent scientist.
    It omitted details about chemistry, metallurgy, and ordnance, ultimately
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

    assert english.badwords == pickle.loads(pickle.dumps(english.badwords))


def test_informals():
    compare_extraction(english.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    assert english.informals == pickle.loads(pickle.dumps(english.informals))


def test_words_to_watch():
    compare_extraction(english.words_to_watch.revision.datasources.matches,
                       WORDS_TO_WATCH, OTHER)

    assert english.words_to_watch == \
        pickle.loads(pickle.dumps(english.words_to_watch))


def test_dictionary():
    cache = {r_text: 'This color colour is spelled worngly. <td>'}
    assert (solve(english.dictionary.revision.datasources.dict_words,
                  cache=cache) ==
            ["This", "color", "colour", "is", "spelled"])
    assert (solve(english.dictionary.revision.datasources.non_dict_words,
                  cache=cache) ==
            ["worngly"])

    assert english.dictionary == pickle.loads(pickle.dumps(english.dictionary))


def test_stopwords():
    cache = {r_text: 'This is spelled worngly. <td>'}
    assert (solve(english.stopwords.revision.datasources.stopwords,
                  cache=cache) ==
            ["This", "is"])
    assert (solve(english.stopwords.revision.datasources.non_stopwords,
                  cache=cache) ==
            ["spelled", "worngly"])

    assert english.stopwords == pickle.loads(pickle.dumps(english.stopwords))


def test_stemmmed():
    cache = {r_text: 'This is spelled worngly. <td>'}
    assert (solve(english.stemmed.revision.datasources.stems, cache=cache) ==
            ["this", "is", "spell", "worng"])

    assert english.stemmed == pickle.loads(pickle.dumps(english.stemmed))


def test_idioms():
    cache = {
        r_text: "This is some text.  I don't want to beat around the bush."}
    assert (solve(english.idioms.revision.datasources.matches, cache=cache) ==
            ['beat around the bush'])

    assert english.idioms == pickle.loads(pickle.dumps(english.idioms))
