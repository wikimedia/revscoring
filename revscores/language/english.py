import warnings

from nltk.corpus import wordnet
from nltk.stem.snowball import SnowballStemmer

from .language import Language

STEMMER = SnowballStemmer("english")

BADWORDS = set(STEMMER.stem(w) for w in [
    "shit",
    "piss",
    "suck",
    "lick",
    "fuck",
    "cunt",
    "cocksuck",
    "motherfuck",
    "bitch",
    "fart",
    "turd",
    "twat",
    "butt",
    "ass",
    "dick",
    "penis",
    "anus",
    "fag",
    "faggot",
    "homosexu",
    "whore",
    "lesbian",
    "fat",
    "bootlip",
    "cholo",
    "chug",
    "coonass",
    "cracker",
    "dothead",
    "gook",
    "gringo",
    "gyppo",
    "gippo",
    "gypo",
    "gyppie",
    "gyppy",
    "gipp",
    "hillbilli",
    "hori",
    "injun",
    "jap",
    "kike",
    "kyke",
    "nigger",
    "niglet",
    "nig",
    "nigor",
    "nigra",
    "nigr",
    "nigar",
    "niggur",
    "nigga",
    "niggah",
    "niggar",
    "nigguh",
    "niggress",
    "nigette",
    "peckerwood",
    "quashi",
    "kwashi",
    "raghead",
    "roundeye",
    "redskin",
    "redneck",
    "spic",
    "spick",
    "spik",
    "spig",
    "spigotty",
    "spook",
    "squarehead",
    "wetback",
    "wog",
    "wop",
    "yank",
    "yankee",
    "zipperhead",
    "herpes",
    "syphilis",
    "chlamydia",
    "gonorrhea",
    "hiv",
    "scabies",
    "stupid",
    "idiot"
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
                
                if len(wordnet.synsets(word)) == 0:
                    yield word
