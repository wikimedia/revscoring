import warnings

from nltk.corpus import wordnet
from nltk.stem.snowball import SnowballStemmer

from .language import Language

STEMMER = SnowballStemmer("turkish")

BADWORDS = set(STEMMER.stem(w) for w in [
    "abracao",
    "Ağzına sıçayım",
    "Ahlaksız",
    "Ahmak",
    "Am",
    "Amcık",
    "Amın oğlu",
    "Amına koyayım",
    "Amına koyyim",
    "Amk",
    "Aptal",
    "Beyinsiz",
    "Bok",
    "Boktan",
    "Çük",
    "Dedeler",
    "Embesil",
    "Gerizekalı",
    "Gerzek",
    "Göt",
    "Göt oğlanı",
    "Götlek",
    "Götoğlanı",
    "Götveren",
    "Haysiyetsiz",
    "İbne",
    "İnci",
    "İt oğlu it",
    "Kıç",
    "Mal",
    "Meme",
    "Nobrain",
    "Oğlan",
    "Oğlancı",
    "Orospu",
    "Orospu çocuğu",
    "Orospunun evladı",
    "Pezevengin evladı",
    "Pezevenk",
    "Piç",
    "Puşt",
    "Salak",
    "Şerefsiz",
    "Sik",
    "Siktir",
    "Yarrak"
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
