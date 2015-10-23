import sys

from .space_delimited import SpaceDelimited

try:
    from nltk.stem.snowball import SnowballStemmer
    stemmer = SnowballStemmer("dutch")
except ValueError:
    raise ImportError("Could not load stemmer for {0}. ".format(__name__))

try:
    from nltk.corpus import stopwords as nltk_stopwords
    stopwords = set(nltk_stopwords.words('dutch') + ["a"])
except LookupError:
    raise ImportError("Could not load stopwords for {0}. ".format(__name__) +
                      "You may need to install the nltk 'stopwords' " +
                      "corpora.  See http://www.nltk.org/data.html")

try:
    import enchant
    dictionary = enchant.Dict("nl")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'nl'.  " +
                      "Consider installing 'myspell-nl'.")

badwords = [ 
    r"aars", r"anaal", r"anus", r"balhaar", r"drol", r"drollen", r"fack", r"facking",                             
    r"fuck", r"fucking", r"gay", r"geil", r"geile", r"gelul", r"geneukt", r"hoer",                             
    r"homos", r"kak", r"kaka", r"kakhoofd", r"kakken", r"kanker", r"kenker", r"klootzak",                             
    r"kontgat", r"kontje", r"pedo", r"penis", r"penissen", r"peop", r"piemel", r"piemels",                             
    r"pipi", r"poep", r"poepchinees", r"poepen", r"poephoofd", r"poepie", r"poepje", r"poepjes",                             
    r"porn", r"porno", r"neuk", r"neuke", r"neuken", r"neukende", r"neukt", r"neukte",                             
    r"suck", r"sucks", r"suckt", r"zuigt", r"sukkel", r"sukkels", r"tering", r"tetten",                             
    r"verkracht", r"dikzak", r"dildo", r"mogolen", r"mogool", r"mongool", r"mooiboy", r"neger",                             
    r"kut", r"kutje", r"kutjes", r"stelletje", r"loser", r"losers", r"lul", r"lullen",                             
    r"reet", r"scheet", r"scheten", r"schijt", r"diaree", r"slet", r"lekkerding", r"likken",   
    r"utme", r"utml", r"utmn", r"utmz", r"rdn", r"cest", r"cet", r"sophonpanich",
    r"boe", r"dombo", r"domme", r"godverdomme", r"izan", r"kots", r"kusjes", r"lekker", r"lekkere",
    r"lkkr", r"nerd", r"nerds", r"noob", r"noobs", r"sex", r"sexy", r"stink", r"stinken", r"stinkt",
    r"stoer", r"vies", r"vieze", r"vuile", r"xxx", r"zielig", r"zooi", r"swag", r"swek", r"yolo"
]
informals = [
    r"hoi", r"hey", r"hallo", r"doei", r"heej", r"heey", r"groetjes", r"halloo", r"hoihoi", r"hoii",
    r"hoiii", r"heb", r"zeg", r"vind", r"bent", r"snap", r"boeit", r"klopt", r"hou", r"houd",
    r"gwn", r"maarja", r"nou", r"ofzo", r"oke", r"yeah", r"hoor", r"hihi", r"eigelijk", r"heeel", r"jij",
    r"jou", r"jullie", r"sorry", r"vetgedrukte", r"deelonderwerp", r"cursieve", r"nowiki", r"bewerkingsveld",
    r"cursief", r"minecraft", r"hotmail", r"hyves", r"bieber", r"werkstuk", r"spreekbeurt", r"haha", r"hahah",
    r"hahaha",     r"hahahah", r"hahahaha", r"hahahahah", r"hahahahaha", r"hahahahahaha", r"lala", r"lalala",
    r"lalalala", r"lalalalala", r"bla", r"blabla", r"blablabla", r"cool", r"coole", r"coolste", r"dikke", r"dom",
    r"lelijk", r"lelijke", r"lelijkste", r"leuk", r"leuke", r"lief", r"onzin", r"raar", r"saai", r"gek", r"gekke",
    r"goeie", r"grappig", r"stom", r"stomme", r"filmfocus", r"filmliefde", r"wikipedianl", r"diakrieten", r"egt",
    r"jah", r"jaja", r"jwz", r"lol", r"lolz", r"omg", r"tog", r"wtf", r"zever"
]
sys.modules[__name__] = SpaceDelimited(
    __name__,
    doc="""
dutch
=======

revision
--------
.. autoattribute:: revision.words
.. autoattribute:: revision.content_words
.. autoattribute:: revision.badwords
.. autoattribute:: revision.misspellings
.. autoattribute:: revision.informals
.. autoattribute:: revision.infonoise

parent_revision
---------------
.. autoattribute:: parent_revision.words
.. autoattribute:: parent_revision.content_words
.. autoattribute:: parent_revision.badwords
.. autoattribute:: parent_revision.misspellings
.. autoattribute:: parent_revision.informals
.. autoattribute:: parent_revision.infonoise

diff
----
.. autoattribute:: diff.words_added
.. autoattribute:: diff.words_removed
.. autoattribute:: diff.badwords_added
.. autoattribute:: diff.badwords_removed
.. autoattribute:: diff.misspellings_added
.. autoattribute:: diff.misspellings_removed
.. autoattribute:: diff.informals_added
.. autoattribute:: diff.informals_removed
    """,
    badwords=badwords,
    dictionary=dictionary,
    informals=informals,
    stemmer=stemmer,
    stopwords=stopwords
)
