import sys

from nltk.corpus import stopwords

from .language import RegexLanguage

# Notice:
# It seems like Turkish stemmer isn't in the nltk snowball library:
# http://www.nltk.org/_modules/nltk/stem/snowball.html

stopwords = set(stopwords.words("turkish"))
badwords = [
    r"ağzına sıçayım", r"ahlaksız", r"ahmak", r"am", r"amcık", r"amın oğlu",
        r"amına koyayım", r"amına koyyim", r"amk", r"aptal",
    r"beyinsiz", r"bok", r"boktan",
    r"çük",
    r"dedeler",
    r"embesil",
    r"gerizekalı", r"gerzek", r"göt", r"göt oğlanı", r"götlek", r"götoğlanı",
        r"götveren",
    r"haysiyetsiz",
    r"ibne", r"inci", r"it", r"it oğlu it",
    r"kıç",
    r"mal", r"meme",
    r"nobrain",
    r"oğlan", r"oğlancı", r"orospu", r"orospu çocuğu", r"orospunun evladı",
    r"pezevengin evladı", r"pezevenk", r"piç", r"puşt",
    r"salak", r"şerefsiz", r"sik", r"siktir",
    r"yarrak"
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
