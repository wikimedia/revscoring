from .features import Dictionary, RegexMatches, Stemmed, Stopwords

name = "french"

try:
    import enchant
    dictionary = enchant.Dict("fr")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'fr'.  " +
                      "Consider installing 'myspell-fr'.")

dictionary = Dictionary(name + ".dictionary", dictionary.check)
"""
:class:`~revscoring.languages.features.Dictionary` features via
`enchant.Dict <https://github.com/rfk/pyenchant>`_ "fr".  Provided by `myspell-fr`
"""

try:
    from nltk.corpus import stopwords as nltk_stopwords
    stopwords = set(nltk_stopwords.words('french') + ["a"])
except LookupError:
    raise ImportError("Could not load stopwords for {0}. ".format(__name__) +
                      "You may need to install the nltk 'stopwords' " +
                      "corpora.  See http://www.nltk.org/data.html")

stopwords = Stopwords(name + ".stopwords", stopwords)
"""
:class:`~revscoring.languages.features.Stopwords` features provided by
`nltk.corpus.stopwords <https://www.nltk.org/api/nltk.corpus.html>`_ "french"
"""

try:
    from nltk.stem.snowball import SnowballStemmer
    stemmer = SnowballStemmer("french")
except ValueError:
    raise ImportError("Could not load stemmer for {0}. ".format(__name__))

stemmed = Stemmed(name + ".stemmed", stemmer.stem)
"""
:class:`~revscoring.languages.features.Stemmed` word features via
:class:`nltk.stem.snowball.SnowballStemmer` "french"
"""

badword_regexes = [
    r"anus",
    r"bais[eé]",
    r"baiz",
    r"batard?",
    r"bit+?es?",
    r"branle(r|tte|ur)",
    r"cacas?",
    r"caliss",
    r"chiante?",
    r"chiasse",
    r"chi[eé](nne|r)?", r"chiot+e",
    r"con(ard?|nard?)?s?", r"conn(asse|e|erie)s?",
    r"couill(es?|on)",
    r"cul",
    r"d[ée]bile",
    r"ducon",
    r"encul[eé][rs]?",
    r"fesses?",
    r"fion",
    r"foutre",
    r"homosexuel",
    r"lesbien",
    r"m[ae]rd(es?|ique)",
    r"e[mn]m[ae]rd(es?|ique)",
    r"ni(ke|gue)r?", "niker", "nique", "niquer",
    "pd", "p[eé]dophile", "p[eé]d[eé]",
    "petasse",
    "pipi",
    "piss+e",
    "poop",
    "pour+i",
    "prostitu[eé]+",
    "proute?",
    "pues?",
    "put(a|ain|e|in)s?",
    "pénis",
    "pétasse",
    "quequette",  # pecker
    "queu", "queue",  # tail
    "salaud",
    "salo(p|pe?|pes?)?",
    "sodom(ie|iser)",
    "stupide",
    "suc[eé](u?r|use)?",
    "tapette",
    "teub",
    "vagin",
    "zboub",
    "zizi"
]

badwords = RegexMatches(name + ".badwords", badword_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
    r"ahah",
    r"allez",
    r"allo",
    r"bisous",
    r"(?:bla)+",
    r"bonjour",
    r"coucou",
    r"etais",
    r"etes",
    r"ha(ha)+",
    r"hi(hi)+",
    r"insérez",
    r"jadore",
    r"jai",
    r"kikoo",
    r"lo+?l",
    r"mdr+",
    r"moche",
    r"ouais?",
    r"ptdr",
    r"truc",
    r"voila",
    r"voulez"
]

informals = RegexMatches(name + ".informals", informal_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
