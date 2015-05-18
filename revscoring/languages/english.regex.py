import re
import warnings

import enchant
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from .language import Language, LanguageUtility

STEMMER = SnowballStemmer("english")
STOPWORDS = set(stopwords.words('english'))
BAD_REGEXES = set([
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
        "spigotty", "spik", "spook", "squarehead", "st(u|oo+)pid", "suck", "syphil+is",
    "turd", "twat",
    "wank", "wetback", "whore", "wog", "wop",
    "yank", "yankee", "yid",
    "zipperhead"
])
BAD_REGEX = re.compile("|".join(BAD_REGEXES))
DICTIONARY = enchant.Dict("en")

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

english = Language("revscoring.languages.english",
                   [stem_word, is_badword, is_misspelled, is_stopword])
