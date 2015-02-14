import warnings

from nltk.corpus import wordnet
#from nltk.stem.snowball import SnowballStemmer

from .language import Language

# It seems like Turkish stemmer isn't in the nltk snowball library for some reason:
# http://www.nltk.org/_modules/nltk/stem/snowball.html
# STEMMER = SnowballStemmer("turkish")
class STEMMER:
    """
    Dummy stemmer for turkish
    """

    def stem(word):
        """
        Do not change the word
        """
        return word

BADWORDS = set(STEMMER.stem(w) for w in [
    "ağzına sıçayım",
    "ahlaksız",
    "ahmak",
    "am",
    "amcık",
    "amın oğlu",
    "amına koyayım",
    "amına koyyim",
    "amk",
    "aptal",
    "beyinsiz",
    "bok",
    "boktan",
    "çük",
    "dedeler",
    "embesil",
    "gerizekalı",
    "gerzek",
    "göt",
    "göt oğlanı",
    "götlek",
    "götoğlanı",
    "götveren",
    "haysiyetsiz",
    "ibne",
    "inci",
    "it",
    "it oğlu it",
    "kıç",
    "mal",
    "meme",
    "nobrain",
    "oğlan",
    "oğlancı",
    "orospu",
    "orospu çocuğu",
    "orospunun evladı",
    "pezevengin evladı",
    "pezevenk",
    "piç",
    "puşt",
    "salak",
    "şerefsiz",
    "sik",
    "siktir",
    "yarrak"
])

def is_badword(word):
    return STEMMER.stem(word).lower() in BADWORDS

def is_misspelled(word):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        # It seems we don't have a wordnet for Turkish in the Open Multilingual Wordnet (omw) data provided by NLTK
        # return len(wordnet.synsets(word, lang="tur")) == 0
        return False

turkish = Language(
    is_badword,
    is_misspelled
)
turkish.STEMMER = STEMMER
turkish.BADWORDS = BADWORDS
