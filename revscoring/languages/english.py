import re
import sys

import enchant
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from .language import RegexLanguage

stemmer = SnowballStemmer("english")
stopwords = set(stopwords.words('english'))
badwords = [
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
informals = [
    "ain'?t", 'awe?some(r|st)?',
    'bla', 'blah', 'boner', 'boobs', 'bullshit',
    "can'?t", "[ck](oo+|ew)l(er|est)?", 'crap',
    "don'?t", "dumb", "dumbass",
    "goodbye",
    "ha(ha)+", "hello", "hey", "hi"
    "i"
    "lol", "l(oo+|u)ve",
    "meow",
    'shove', 'smelly', 'soo+', 'stinky', 'suck(ing|er)?', 'sux', "shouldn\'t"
    "tits",
    "wasn'?t", "wuz", "won'?t", "woof",
    "ya'?ll", 'yay', 'yea', 'yolo'
]
try:
    dictionary = enchant.Dict("en")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'en'.  " +
                      "Consider installing 'myspell-en-au', 'myspell-en-gb', " +
                      "'myspell-en-us' and/or 'myspell-en-za'.")

sys.modules[__name__] = RegexLanguage(
    __name__,
    badwords=badwords,
    informals=informals,
    dictionary=dictionary,
    stemmer=stemmer,
    stopwords=stopwords
)
"""
Implements :class:`~revscoring.languages.language.RegexLanguage` for all
variants of English (e.g. US & British).  Comes complete with all language
utilities.
"""
