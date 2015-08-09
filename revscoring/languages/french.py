import sys

import enchant
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from .language import RegexLanguage

stemmer = SnowballStemmer("french")
stopwords = set(stopwords.words("french") + ["a"])
badwords = [
    r"con",
    r"fesse", r"foutre",
    r"herpes",
    r"merde+", r"merdique",
    r"peni(s|5)", r"prostituee?", r"putain", r"putes",
    r"salop", r"stupide",
]
try:
    dictionary = enchant.Dict("fr")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'fr'.  " +
                      "Consider installing 'myspell-fr'.")

sys.modules[__name__] = RegexLanguage(
    __name__,
    badwords=badwords,
    dictionary=dictionary,
    stopwords=stopwords,
    stemmer=stemmer
)
"""
Implements :class:`~revscoring.languages.language.RegexLanguage` for French.
Comes complete with all language utilities.
"""
