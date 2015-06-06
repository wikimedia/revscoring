from nltk.corpus import stopwords

from .language import Language, LanguageUtility

# Notice:
# It seems like Turkish stemmer isn't in the nltk snowball library for some reason:
# http://www.nltk.org/_modules/nltk/stem/snowball.html
# STEMMER = SnowballStemmer("turkish")

STOPWORDS = set(stopwords.words("turkish"))
BADWORDS = set([
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
])

def is_badword_process():
    def is_badword(word):
        return word.lower() in BADWORDS
    return is_badword
is_badword = LanguageUtility("is_badword", is_badword_process, depends_on=[])

def is_stopword_process():
    def is_stopword(word):
        return word.lower() in STOPWORDS
    return is_stopword
is_stopword = LanguageUtility("is_stopword", is_stopword_process, depends_on=[])


turkish = Language("revscoring.languages.turkish",
                   [is_badword, is_stopword])
"""
Implements :class:`~revscoring.languages.language.Language` for Turkish.
:data:`~revscoring.languages.language.is_badword` and
:data:`~revscoring.languages.language.is_stopword` are provided.
"""
