from .features import Dictionary, RegexMatches, Stopwords

name = "norwegian"

try:
    import enchant
    dictionary = enchant.Dict("nb")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'nb'.  " +
                      "Consider installing 'myspell-nb'.")

dictionary = Dictionary(name + ".dictionary", dictionary.check)
"""
:class:`~revscoring.languages.features.Dictionary` features via
`enchant.Dict <https://github.com/rfk/pyenchant>`_ "nb".  Provided by `myspell-nb`
"""

try:
    from nltk.corpus import stopwords as nltk_stopwords
    stopwords = set(nltk_stopwords.words('norwegian'))
except LookupError:
    raise ImportError("Could not load stopwords for {0}. ".format(__name__) +
                      "You may need to install the nltk 'stopwords' " +
                      "corpora.  See http://www.nltk.org/data.html")

stopwords = Stopwords(name + ".stopwords", stopwords)
"""
:class:`~revscoring.languages.features.Stopwords` features provided by
`nltk.corpus.stopwords <https://www.nltk.org/api/nltk.corpus.html>`_ "norwegian"
"""


badword_regexes = [
    r"b1tch",
    r"bitch",
    r"blabla",
    r"boobs",
    r"bullshit",
    r"bæsj",
    r"bæsje",
    r"bæsjen",
    r"bæsjer",
    r"cool",
    r"cunt",
    r"drit",
    r"dritt",
    r"fack",
    r"faen",
    r"fitta",
    r"fitte",
    r"fuck",
    r"fucka",
    r"homo",
    r"homoseksuell",
    r"homse",
    r"hore",
    r"jævla",
    r"jævlig",
    r"knull",
    r"knulle",
    r"kuk",
    r"kukk",
    r"kåt",
    r"kødd",
    r"ludder",
    r"mordi",
    r"motherfucker",
    r"niggah",
    r"nigger",
    r"p0rn",
    r"p3nis",
    r"p3n1s",
    r"pen1s",
    r"pikk",
    r"porn",
    r"pr0n",
    r"pule",
    r"pulte",
    r"pupper",
    r"pussy",
    r"rompa",
    r"rompe",
    r"ræva",
    r"stupid",
    r"teit",
    r"tissemann",
    r"tits",
    r"twat",
    r"wanker",
    r"weed",
    r"whore"
]

badwords = RegexMatches(name + ".badwords", badword_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
    r"haha",
    r"hallo",
    r"hehe",
    r"hei",
    r"heisann",
    r"hey",
    r"heya",
    r"hihi",
    r"lmao",
    r"lol",
    r"omg",
    r"rofl",
    r"yea",
    r"yeah"
]

informals = RegexMatches(name + ".informals", informal_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
