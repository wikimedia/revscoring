import warnings

from nltk.corpus import wordnet
from nltk.stem.snowball import SnowballStemmer

from .language import Language

STEMMER = SnowballStemmer("portuguese")

BADWORDS = set(STEMMER.stem(w) for w in [
    "",
])

class English(Language):
    
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
