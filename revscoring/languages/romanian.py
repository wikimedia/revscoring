from .features import Dictionary, RegexMatches, Stemmed, Stopwords

name = "romanian"

try:
    import enchant
    dictionary = enchant.Dict("ro")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'ro'.  " +
                      "Consider installing 'aspell-ro'.")

dictionary = Dictionary(name + ".dictionary", dictionary.check)
"""
:class:`~revscoring.languages.features.Dictionary` features via
`enchant.Dict <https://github.com/rfk/pyenchant>`_ "ru".  Provided by `aspell-ro`
"""

try:
    from nltk.corpus import stopwords as nltk_stopwords
    stopwords = set(nltk_stopwords.words('romanian'))
except LookupError:
    raise ImportError("Could not load stopwords for {0}. ".format(__name__) +
                      "You may need to install the nltk 'stopwords' " +
                      "corpora.  See http://www.nltk.org/data.html")

stopwords = Stopwords(name + ".stopwords", stopwords)
"""
:class:`~revscoring.languages.features.Stopwords` features provided by
`nltk.corpus.stopwords <https://www.nltk.org/api/nltk.corpus.html>`_ "romanian"
"""

try:
    from nltk.stem.snowball import SnowballStemmer
    stemmer = SnowballStemmer("romanian")
except ValueError:
    raise ImportError("Could not load stemmer for {0}. ".format(__name__))

stemmed = Stemmed(name + ".stemmed", stemmer.stem)
"""
:class:`~revscoring.languages.features.Stemmed` word features via
:class:`nltk.stem.snowball.SnowballStemmer` "romanian"
"""

badword_regexes = [
    r"bou",
    r"cacat?",
    r"cur(u|v[ae])?",
    r"dracu",
    r"fraier(i(lor)?)?",
    r"fut(e|ut)?",
    r"kkt",
    r"laba",
    r"mata",
    r"mui(e|st)",
    r"pidar",
    r"pizda",
    r"plm",
    r"porcarie",
    r"pul[aei]+",
    r"sug(e(ti)?|i)",
    r"supt"
]

badwords = RegexMatches(name + ".badwords", badword_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
    "aia", "asa",
    "aste?a",
    "a(ve)?ti", "aveti",
    "bag(at)?", "bagat",
    "bla+",
    "naspa",
    "prost(i[ei]?|ilor)?", "prosti", "prostie", "prostii", "prostilor",
    "rahat",
    "smecher",
    "tigani"
]

informals = RegexMatches(name + ".informals", informal_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
