import sys

import enchant

from .space_delimited import SpaceDelimited

try:
    from nltk.stem.snowball import SnowballStemmer
    stemmer = SnowballStemmer("french")
except ValueError:
    raise ImportError("Could not load stemmer for {0}. ".format(__name__))

try:
    from nltk.corpus import stopwords as nltk_stopwords
    stopwords = set(nltk_stopwords.words('french') + ["a"])
except LookupError:
    raise ImportError("Could not load stopwords for {0}. ".format(__name__) +
                      "You may need to install the nltk 'stopwords' corpora. " +
                      "See http://www.nltk.org/data.html")

try:
    import enchant
    dictionary = enchant.Dict("fr")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'fr'.  " +
                      "Consider installing 'myspell-fr'.")

badwords = [
    r"con",
    r"fesse", r"foutre",
    r"merde+", r"merdique",
    r"prostituee?", r"putain", r"putes",
    r"salop", r"stupide",
]

sys.modules[__name__] = SpaceDelimited(
    __name__,
    badwords=badwords,
    dictionary=dictionary,
    stemmer=stemmer,
    stopwords=stopwords
)
"""
french
"""
