from .features import Dictionary, RegexMatches, Stemmed, Stopwords

name = "dutch"

try:
    import enchant
    dictionary = enchant.Dict("nl")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'nl'.  " +
                      "Consider installing 'myspell-nl'.")

dictionary = Dictionary(name + ".dictionary", dictionary.check)
"""
:class:`~revscoring.languages.features.Dictionary` features via
:class:`enchant.Dict` "nl".  Provided by `myspell-nl`
"""

try:
    from nltk.corpus import stopwords as nltk_stopwords
    stopwords = set(nltk_stopwords.words('dutch'))
except LookupError:
    raise ImportError("Could not load stopwords for {0}. ".format(__name__) +
                      "You may need to install the nltk 'stopwords' " +
                      "corpora.  See http://www.nltk.org/data.html")

stopwords = Stopwords(name + ".stopwords", stopwords)
"""
:class:`~revscoring.languages.features.Stopwords` features provided by
:func:`nltk.corpus.stopwords` "dutch"
"""

try:
    from nltk.stem.snowball import SnowballStemmer
    stemmer = SnowballStemmer("dutch")
except ValueError:
    raise ImportError("Could not load stemmer for {0}. ".format(__name__))

stemmed = Stemmed(name + ".stemmed", stemmer.stem)
"""
:class:`~revscoring.languages.features.Stemmed` word features via
:class:`nltk.stem.snowball.SnowballStemmer` "dutch"
"""

badword_regexes = [
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

badwords = RegexMatches(name + ".badwords", badword_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
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
    r"hee+[jyl]", r"heee+?l",
    r"houd?",
    r"(?:hoi+)+",
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

informals = RegexMatches(name + ".informals", informal_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
