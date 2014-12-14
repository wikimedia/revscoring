import warnings

from nltk.corpus import wordnet
from nltk.stem.snowball import SnowballStemmer

from .language import Language

STEMMER = SnowballStemmer("english")

BADWORDS = set(STEMMER.stem(w) for w in [
    "anus",
    "ass",
    "bitch",
    "bootlip",
    "butt",
    "chlamydia",
    "cholo",
    "chug",
    "cocksuck",
    "coonass",
    "cracker",
    "cunt",
    "dick",
    "dothead",
    "fag",
    "faggot",
    "fart",
    "fat",
    "fuck",
    "gipp",
    "gippo",
    "gonorrhea",
    "gook",
    "gringo",
    "gypo",
    "gyppie",
    "gyppo",
    "gyppy",
    "herpes",
    "hillbilly",
    "hiv",
    "homosexual",
    "hori",
    "idiot",
    "injun",
    "jap",
    "kike",
    "kwashi",
    "kyke",
    "lesbian",
    "lick",
    "motherfuck",
    "nig",
    "nigar",
    "nigette",
    "nigga",
    "niggah",
    "niggar",
    "nigger",
    "niggress",
    "nigguh",
    "niggur",
    "niglet",
    "nigor",
    "nigr",
    "nigra",
    "peckerwood",
    "penis",
    "piss",
    "quashi",
    "raghead",
    "redneck",
    "redskin",
    "roundeye",
    "scabies",
    "shit",
    "spic",
    "spick",
    "spig",
    "spigotty",
    "spik",
    "spook",
    "squarehead",
    "stupid",
    "suck",
    "syphilis",
    "turd",
    "twat",
    "wank",
    "wetback",
    "whore",
    "wog",
    "wop",
    "yank",
    "yankee",
    "yid",
    "zipperhead"
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
