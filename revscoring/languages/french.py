import sys

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
                      "You may need to install the nltk 'stopwords' " +
                      "corpora.  See http://www.nltk.org/data.html")

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
    doc="""
french
======

revision
--------
.. autoattribute:: revision.words
.. autoattribute:: revision.content_words
.. autoattribute:: revision.badwords
.. autoattribute:: revision.misspellings
.. autoattribute:: revision.infonoise

parent_revision
---------------
.. autoattribute:: parent_revision.words
.. autoattribute:: parent_revision.content_words
.. autoattribute:: parent_revision.badwords
.. autoattribute:: parent_revision.misspellings
.. autoattribute:: parent_revision.infonoise

diff
----
.. autoattribute:: diff.words_added
.. autoattribute:: diff.words_removed
.. autoattribute:: diff.badwords_added
.. autoattribute:: diff.badwords_removed
.. autoattribute:: diff.misspellings_added
.. autoattribute:: diff.misspellings_removed
    """,
    badwords=badwords,
    dictionary=dictionary,
    stemmer=stemmer,
    stopwords=stopwords
)
