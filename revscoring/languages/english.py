import re
import sys

import enchant
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from .language import Language, LanguageUtility

STEMMER = SnowballStemmer("english")
STOPWORDS = set(stopwords.words('english'))
BAD_REGEXES = [
    "a+nus+", "ass+",
    "bitch", "bootlip", "butt+",
    "chlamydia", "cholo", "chug", "cocksuck", "coonass", "cracker", "cunt",
    "dick", "dothead",
    "(f|ph)ag+(ot)?", "fart", "fat", "fuck",
    "gipp", "gippo", "gonorrhea", "gook", "gringo", "gypo", "gyppie", "gyppo",
        "gyppy",
    "herpes", "hillbilly", "hiv", "homosexual", "hori",
    "idiot", "injun",
    "jap",
    "kike", "kwashi", "kyke",
    "lesbian", "lick",
    "motherfuck",
    "nig", "nig+(a|e|u)+(r|h)+", "niggress"
        "niglet", "nigor", "nigr", "nigra",
    "pecker(wood)?", "peni(s)?", "piss",
    "quashi",
    "raghead", "redneck", "redskin", "roundeye",
    "scabies", "shi+t+", "slut", "spi(g|c|k)+",
        "spigotty", "spik", "spook", "squarehead", "st(u|oo+)pid", "suck",
        "syphil+is",
    "turd", "twat",
    "wank", "wetback", "whore", "wog", "wop",
    "yank", "yankee", "yid",
    "zipperhead"
]
INFORMAL_REGEXES = [
    "ain'?t", 'awe?some(r|st)?',
    'bla', 'blah', 'boner', 'boobs', 'bullshit',
    "can'?t", "[ck](oo|ew)l(er|est)?", 'crap',
    "don'?t", "dumb", "dumbass",
    "goodbye",
    "haha", "hello", "hey",
    "i"
    "lol", "l(oo+|u)ve",
    "meow",
    'shove', 'smelly', 'soo+', 'stinky', 'suck(ing|er)?', 'sux', "shouldn\'t"
    "tits",
    "wasn'?t", "wuz", "won'?t", "woof",
    "ya'?ll", 'yay', 'yea', 'yolo'
]
BAD_REGEX = re.compile("|".join(BAD_REGEXES))
INFORMAL_REGEX = re.compile("|".join(INFORMAL_REGEXES))
try:
    DICTIONARY = enchant.Dict("en")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'en'.  " +
                      "Consider installing 'myspell-en-au', 'myspell-en-gb', " +
                      "'myspell-en-us' and/or 'myspell-en-za'.")

def stem_word_process():
    def stem_word(word):
        return STEMMER.stem(word).lower()
    return stem_word
stem_word = LanguageUtility("stem_word", stem_word_process)


def is_badword_process():
    def is_badword(word):
        return bool(BAD_REGEX.match(word.lower()))
    return is_badword
is_badword = LanguageUtility("is_badword", is_badword_process)


def is_informal_word_process():
    def is_informal_word(word):
        return bool(INFORMAL_REGEX.match(word.lower()))
    return is_informal_word
is_informal_word = LanguageUtility("is_informal_word",
    is_informal_word_process)


def is_misspelled_process():
    def is_misspelled(word):
        return not DICTIONARY.check(word)
    return is_misspelled

is_misspelled = LanguageUtility("is_misspelled", is_misspelled_process)

def is_stopword_process():
    def is_stopword(word):
        return word.lower() in STOPWORDS
    return is_stopword
is_stopword = LanguageUtility("is_stopword", is_stopword_process)

sys.modules[__name__] = Language(
    __name__,
    [stem_word, is_badword, is_misspelled, is_stopword, is_informal_word]
)
"""
Implements :class:`~revscoring.languages.language.Language` for all variants of
English (e.g. US & British).  Comes complete with all language utilities.
"""
