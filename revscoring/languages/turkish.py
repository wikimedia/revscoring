import sys

from nltk.corpus import stopwords

from .language import RegexLanguage

# Notice:
# It seems like Turkish stemmer isn't in the nltk snowball library:
# http://www.nltk.org/_modules/nltk/stem/snowball.html

stopwords = set(stopwords.words("turkish"))
badwords = [
    "ağzına sıçayım", "ahlaksız", "ahmak", "am", "amcık", "amın oğlu",
        "amına koyayım", "amına koyyim", "amk", "aptal",
    "beyinsiz", "bok", "boktan",
    "çük",
    "dedeler",
    "embesil",
    "gerizekalı", "gerzek", "göt", "göt oğlanı", "götlek", "götoğlanı",
        "götveren",
    "haysiyetsiz",
    "ibne", "inci", "it", "it oğlu it",
    "kıç",
    "mal", "meme",
    "nobrain",
    "oğlan", "oğlancı", "orospu", "orospu çocuğu", "orospunun evladı",
    "pezevengin evladı", "pezevenk", "piç", "puşt",
    "salak", "şerefsiz", "sik", "siktir",
    "yarrak"
]


sys.modules[__name__] = RegexLanguage(
    __name__,
    badwords=badwords,
    stopwords=stopwords
)
"""
Implements :class:`~revscoring.languages.language.RegexLanguage` for Turkish.
:data:`~revscoring.languages.language.is_badword` and
:data:`~revscoring.languages.language.is_stopword` are provided.
"""
