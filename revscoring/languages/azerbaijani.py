from nltk.corpus import stopwords

from .language import Language, LanguageUtility

# Notice:
# It seems like Azerbaijani stemmer isn't in the nltk snowball library for some reason:
# http://www.nltk.org/_modules/nltk/stem/snowball.html
# STEMMER = SnowballStemmer("azerbaijani")

#STOPWORDS = set([])
BADWORDS = set([])

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


azerbaijani = Language("revscoring.languages.azerbaijani",
                   [])
