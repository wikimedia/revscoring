import warnings

from nltk.corpus import wordnet
from nltk.stem.snowball import SnowballStemmer

from .language import Language

STEMMER = SnowballStemmer("portuguese")

BADWORDS = set(STEMMER.stem(w) for w in [
    "ânus",
    "baitola",
    "bicha",
    "boceta",
    "bosta",
    "buceta",
    "bunda",
    "burro",
    "cagar",
    "caipira",
    "chupador",
    "chupar",
    "clamídia",
    "cocô",
    "cu",
    "estúpido",
    "fezes",
    "foder",
    "gonorréia",
    "gordo",
    "gringo",
    "herpes",
    "hiv",
    "homosexual",
    "idiota",
    "imbecil",
    "japa",
    "jeca",
    "lamber",
    "lésbica",
    "merda",
    "mijar",
    "nego",
    "negro",
    "neguinho",
    "peidar",
    "pênis",
    "pinto",
    "preto",
    "punheta",
    "puta",
    "rabo",
    "sarna",
    "transar",
    "traseiro",
    "trepar",
    "vadia",
    "veado",
    "viado"
])

class Portuguese(Language):
    
    def badwords(self, words):
        
        for word in words:
            
            if STEMMER.stem(word).lower() in BADWORDS:
                yield word
                    
    def misspellings(self, words):
        
        for word in words:
            
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                
                if len(wordnet.synsets(word, lang="por")) == 0:
                    yield word
