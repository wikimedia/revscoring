import sys

import enchant
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from .language import RegexLanguage

stemmer = SnowballStemmer("french")
stopwords = set(stopwords.words('french') + ['a'])
badwords = [
    'anu+s+',
    'con', 'c(u|oo)l',
    'fesse', 'foutre',
    'gay',
    'herpes', 'hiv', 'homosexu(e|a)l',
    'idio+t',
    'lesbi(e|a)n',
    'merde+', 'merdique',
    'peni(s|5)', 'prostituee?', 'putain', 'putes',
    'salop', 'stupide',
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
