import sys

from .space_delimited import SpaceDelimited

try:
    from nltk.stem.snowball import SnowballStemmer
    stemmer = SnowballStemmer("dutch")
except ValueError:
    raise ImportError("Could not load stemmer for {0}. ".format(__name__))

try:
    from nltk.corpus import stopwords as nltk_stopwords
    stopwords = set(nltk_stopwords.words('dutch'))
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
    r"aars",
    r"an(aal|us)\w*",
    r"balhaar",
    r"drol(len)?",
    r"fack(en|ing|s)?", "facking",
    r"flikkers?",
    r"focking",
    r"ge(ile?|lul)",
    r"geneukt",
    r"hoer(en?)?",
    r"homos?",
    r"kaka?",
    r"kak(hoofd|ken)",
    r"k[ae]nker",
    r"klootzak(ken)?",
    r"klote",
    r"kont(gat|je)?",
    r"pedo",
    r"penis(sen)?",
    r"peop",
    r"piemels?",
    r"pijpen",
    r"pik",
    r"pimel",
    r"pipi",
    r"poep(chinees?|en|hoofd)?",
    r"poep(ie|je|sex|te?)s?",
    r"porno?",
    r"neuke?",
    r"neuken(de)?",
    r"neukt(en?)?",
    r"stron(d|t)",
    r"suck(s|t)?",
    r"zuigt",
    r"sukkels?",
    r"ter(ing|ten)", "tetten",
    r"tieten",
    r"vagina",
    r"verekte",
    r"verkracht",
    r"dikzak",
    r"dildo",
    r"mon?g(olen|ool)?", "mooiboy",
    r"negers?",
    r"shit",
    r"sperma",
    r"kut(jes?)?",
    r"stelletje",
    r"losers?",
    r"lul(len)?",
    r"reet",
    r"scheet", "scheten", r"schijt",
    r"diaree",
    r"slet",
    r"lekkerding",
    r"likken"
]

informals = [
    r"aap(jes)?",
    r"banaan",
    r"bent",
    r"boe(it)?",
    r"doei"
    r"dombo",
    r"domme",
    r"eigelijk",
    r"godverdomme",
    r"groetjes",
    r"gwn",
    r"hoi",
    r"hal+o+",
    r"heb",
    r"hee+[jyl]", r"heee+l",
    r"houd?",
    r"(hoi+)+",
    r"hoor",
    r"izan",
    r"jij",
    r"jou",
    r"jullie",
    r"kaas",
    r"klopt",
    r"kots",
    r"kusjes",
    r"le?kke?re?",
    r"maarja",
    r"mama",
    r"nou",
    r"oma",
    r"ofzo",
    r"oke",
    r"sexy?",
    r"snap",
    r"stink(en|t)",
    r"stoer",
    r"swag",
    r"swek",
    r"vies", "vieze",
    r"vind",
    r"vuile",
    r"xxx",
    r"yeah",
    r"zielig",
    r"zooi",
    r"yolo",
    r"zeg"
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
