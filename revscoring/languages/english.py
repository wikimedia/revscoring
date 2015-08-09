import re
import sys

import enchant
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from .language import RegexLanguage

stemmer = SnowballStemmer("english")
try:
    stopwords = set(stopwords.words('english'))
except LookupError:
    raise ImportError("Could not load stopwords for {0}. ".format(__name__) +
                      "You may need to install the nltk 'stopwords' corpora. " +
                      "See http://www.nltk.org/data.html")
badwords = [
    r"a+nus+", r"ass+(face.*|hole.*|hat.*)?",
    r"b+i+o?t+c+h+.*", r"bootlip", r"butt+(fuck.*)?",
    r"chlamydia", r"cholo", r"chug", r"cock.*", r"coon.*", r"cracker",
        r"cunt.*",
    r"dick.*", r"dothead.*",
    r"(f|ph)ag+(ot)?", r".*fart.*", r"fat.*", r".*f+u+c*k.*",
    r"g[yi]p+(o|y|ie?)?", r"gonorrhea", r"goo+k", r"gringo", r"gyppie",
    r"he+rpe+s", r"hill-?billy", r"hom(a|o|er)sexual.*",
    r".*injun.*",
    r"j+a+p+",
    r"k[iy]ke", r"kwash(i|ee)",
    r".*lesbian.*", r"lick",
    r"nig", r"nig+(a|e|u)+(r|h)+", r"niggress"
        r"niglet", r"nigor", r"nigr", r"nigra",
    r"pecker(wood)?.*", r".*peni(s)?.*", r"piss.*",
    r"quashi",
    r"raghead", r"red(neck|skin)", r"roundeye",
    r"scabies", r".*shi+t+.*", r"slu+t+", r"spi(g|c|k)+",
        r"spigotty", r"spik", r"spook", r"squarehead", r"st(u|oo+)pid",
        r"su+c*k+(er|iest|a)", r"syphil+is",
    r"tu+rds?", r"twat",
    r"wank.*", r"wetback", r"w?hor(e|i|y).*", r"wog", r"wop",
    r"yank(e+)?", r"yid",
    r"zipperhead"
]
informals = [
    r"ain'?t", "awe?some(r|st)?",
    "bla", "blah", "boner", "boobs", "bullshit",
    r"can'?t", r"[ck](oo+|ew)l(er|est)?", "crap",
    r"don'?t", r"dumb", r"dumbass",
    r"goodbye",
    r"h[aiou](h[aeiou])*", r"h[e](h[aeiou])+", r"hell+o+", r"h[ae]+y+",
         r"hm+",
    r"i+", r"idiot",
    r"lol", r"l(oo+|u)ve",
    r"meow",
    r"shove", r"smelly", r"soo+", r"stinky", r"suck(ing|er)?", r"sux",
        r"shouldn\'t"
    r"tits",
    r"wasn'?t", r"w[ua]+[sz]+[ua]+p", r"wuz", r"won'?t", r"woof",
    r"ya'?ll", r"y+a+y+", r"yeah?", r"yolo",
]
try:
    dictionary = enchant.Dict("en")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'en'.  " +
                      "Consider installing 'myspell-en-au', 'myspell-en-gb', " +
                      "'myspell-en-us' and/or 'myspell-en-za'.")

sys.modules[__name__] = RegexLanguage(
    __name__,
    badwords=badwords,
    informals=informals,
    dictionary=dictionary,
    stemmer=stemmer,
    stopwords=stopwords
)
"""
Implements :class:`~revscoring.languages.language.RegexLanguage` for all
variants of English (e.g. US & British).  Comes complete with all language
utilities.
"""
