import warnings

import enchant
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from .language import Language, LanguageUtility

STEMMER = SnowballStemmer("english")
STOPWORDS = set(stopwords.words('english'))
BADWORDS = set([
    "anus", "ass",
    "bitch", "bootlip", "butt",
    "chlamydia", "cholo", "chug", "cocksuck", "coonass", "cracker", "cunt",
    "dick", "dothead",
    "fag", "faggot",
    "fart", "fat", "fuck", "fucker",
    "gipp", "gippo", "gonorrhea", "gook", "gringo", "gypo", "gyppie", "gyppo",
        "gyppy",
    "herpes", "hillbilly", "hiv", "homosexual", "hori",
    "idiot", "injun",
    "jap",
    "kike", "kwashi", "kyke",
    "lesbian", "lick",
    "motherfuck",
    "nig", "nigar", "nigette", "nigga", "niggah", "niggar", "nigger",
        "niggress", "nigguh", "niggur", "niglet", "nigor", "nigr", "nigra",
    "peckerwood", "penis", "piss",
    "quashi",
    "raghead", "redneck", "redskin", "roundeye",
    "scabies", "shit", "shitty", "slut", "slutty", "spic", "spick", "spig",
        "spigotty", "spik", "spook", "squarehead", "stupid", "suck", "syphilis",
    "turd", "twat",
    "wank", "wetback", "whore", "wog", "wop",
    "yank", "yankee", "yid",
    "zipperhead"
])
STEMMED_BADWORDS = set(STEMMER.stem(w) for w in BADWORDS)
DICTIONARY = enchant.Dict("en")

def stem_word_process():
    def stem_word(word):
        return STEMMER.stem(word).lower()
    return stem_word
stem_word = LanguageUtility("stem_word", stem_word_process, depends_on=[])

def is_badword_process(stem_word):
    def is_badword(word):
        return stem_word(word) in STEMMED_BADWORDS
    return is_badword
is_badword = LanguageUtility("is_badword", is_badword_process, depends_on=[stem_word])


def is_misspelled_process():
    def is_misspelled(word):
        return not DICTIONARY.check(word)
    return is_misspelled

is_misspelled = LanguageUtility("is_misspelled", is_misspelled_process,
                                depends_on=[])

def is_stopword_process():
    def is_stopword(word):
        return word.lower() in STOPWORDS
    return is_stopword
is_stopword = LanguageUtility("is_stopword", is_stopword_process, depends_on=[])

english = Language("revscoring.languages.english",
                   [stem_word, is_badword, is_misspelled, is_stopword])
"""
Implements :class:`~revscoring.languages.language.Language` for all variants of
English (e.g. US & British).  Comes complete with all language utilities.
"""
