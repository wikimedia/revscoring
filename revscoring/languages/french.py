import warnings

import enchant
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from .language import Language, LanguageUtility

STEMMER = SnowballStemmer("french")
STOPWORDS = set(stopwords.words('french') + ['a'])
BADWORDS = set([
    'anus',
    'con', 'cul',
    'fesse', 'Foutre',
    'gay',
    'herpes', 'hiv', 'homosexuel',
    'idiot',
    'lesbien',
    'merde', 'merdique',
    'penis', 'prostituee', 'Putain', 'putes',
    'Salop', 'stupide',
])

STEMMED_BADWORDS = set(STEMMER.stem(w) for w in BADWORDS)
DICTIONARY = enchant.Dict("fr")

def stem_word_process():
    def stem_word(word):
        return STEMMER.stem(word.lower())
    return stem_word
stem_word = LanguageUtility("stem_word", stem_word_process, depends_on=[])

def is_badword_process(stem_word):
    def is_badword(word):
        return stem_word(word) in STEMMED_BADWORDS
    return is_badword
is_badword = LanguageUtility("is_badword", is_badword_process,
                             depends_on=[stem_word])


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

french = Language("revscoring.languages.french",
                      [stem_word, is_badword, is_misspelled, is_stopword])
"""
Implements :class:`~revscoring.languages.language.Language` for French.  Comes
complete with all language utilities. 
"""
