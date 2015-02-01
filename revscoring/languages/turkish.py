import warnings

from nltk.corpus import wordnet
from nltk.stem.snowball import SnowballStemmer

from .language import Language

STEMMER = SnowballStemmer("turkish") #It seems like Turkish stemmer isn't in the nltk snowball library for some reason: http://www.nltk.org/_modules/nltk/stem/snowball.html

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

class Turkish(Language):
    
    def badwords(self, words):
        
        for word in words:
            
            if STEMMER.stem(word).lower() in BADWORDS:
                yield word
                    
    def misspellings(self, words):
        
        for word in words:
            
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                
                if len(wordnet.synsets(word, lang="tur")) == 0:
                    yield word
