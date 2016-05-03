from .features import Dictionary, RegexMatches, Stemmed, Stopwords

name = "german"

try:
    import enchant
    dictionary = enchant.Dict("de")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'de'.  " +
                      "Consider installing 'myspell-de-de', " +
                      "'myspell-de-at', and/or 'myspell-de-ch'.")

dictionary = Dictionary(name + ".dictionary", dictionary.check)
"""
:class:`~revscoring.languages.features.Dictionary` features via
:class:`enchant.Dict` "de". Provided by `myspell-de-de`, `myspell-de-at`,
and `myspell-de-ch`.
"""

try:
    from nltk.corpus import stopwords as nltk_stopwords
    stopwords = set(nltk_stopwords.words('german'))
except LookupError:
    raise ImportError("Could not load stopwords for {0}. ".format(__name__) +
                      "You may need to install the nltk 'stopwords' " +
                      "corpora.  See http://www.nltk.org/data.html")

stopwords = Stopwords(name + ".stopwords", stopwords)
"""
:class:`~revscoring.languages.features.Stopwords` features provided by
:func:`nltk.corpus.stopwords` "german"
"""

try:
    from nltk.stem.snowball import SnowballStemmer
    stemmer = SnowballStemmer("german")
except ValueError:
    raise ImportError("Could not load stemmer for {0}. ".format(__name__))

stemmed = Stemmed(name + ".stemmed", stemmer.stem)
"""
:class:`~revscoring.languages.features.Stemmed` word features via
:class:`nltk.stem.snowball.SnowballStemmer` "german"
"""


badword_regexes = [
    r"[äa]rsch\w*",
    r"assi",
    r"bescheuert",
    r"deppen",
    r"dumm",
    r"fettsack",
    r"ficker",
    r"fotzen?",
    r"gefickte",
    r"homofürst",
    r"hur+e(n(s[oö]hne?)?)?",
    r"idioten",
    r"kack([ae]|wurst)",
    r"kanacken",
    r"lutscher",
    r"mis[st]geburt",
    r"muschis",
    r"nutte",
    r"pen+is+(kopf|e[ns]?)?", r"penis+e(n|s)?",
    r"sau",
    r"schei(s+|ß)(en?)?",
    r"schlampe",
    r"schwanzlutscher",
    r"schwu(chteln?|l+(er)?)",
    r"schw[äa]nze",
    r"spas+t(en)?",
    r"verarscht",
    r"verfickte",
    r"vollidiot",
    r"wichser",
    r"wix+e[rn]?"
]

badwords = RegexMatches(name + ".badwords", badword_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
    r"auserdem",
    r"bins",
    r"(?:bla)+",
    r"blub+",
    r"blöd(er)?",
    r"bodewell",
    r"bumsen",
    r"coo+?l(e|er|ste)?",
    r"deine",
    r"digga",
    r"dildos?",
    r"doof",
    r"dumm+?(e(n|r|s)?)?",
    r"döner",
    r"euch",
    r"fetter",
    r"fick(e|en|t|te|ten)?",
    r"fresse",
    r"f[uü]rt?z(en|e)?", r"f[uü]rn",
    r"gefickt",
    r"gehts",
    r"geil(e[nr]?|sten?)?",
    r"gez",
    r"gr[uü]ße",
    r"hab",
    r"(?:ha)+h?",
    r"hall+?o",
    r"halts",
    r"(?:hu)+",
    r"hässlich",
    r"(ja)+",
    r"jannik",
    r"juhu",
    r"kac?k([ae]n?|t)?",
    r"klo",
    r"kneipenschlägerein",
    r"kotzen?",
    r"kursiver",
    r"könnt",
    r"labert",
    r"(?:la)+",
    r"langhaardackel",
    r"langweilig",
    r"leck(er|t)?",
    r"lonni",
    r"looser",
    r"lutsch(en|t)",
    r"mama",
    r"mfg",
    r"moin",
    r"mudd(a|er)",
    r"mu(ha)+",
    r"mumu",
    r"muschie?",
    r"möse",
    r"naja",
    r"ni(ch|x)",
    r"nutten",
    r"oma",
    r"opfa",
    r"penner",
    r"pimmel",
    r"pipi",
    r"pisse",
    r"pop(el|o)",
    r"pornos?",
    r"puffs?",
    r"pups(en)?",
    r"scheis?",
    r"schlampen",
    r"schniedel",
    r"schwachsinn",
    r"schwule",
    r"seid",
    r"spasti",
    r"stin(gt|k(e[rn]?|s?t)?)",
    r"swag",
    r"titten?",
    r"tobi",
    r"toll",
    r"unformatierten",
    r"vaginas",
    r"wisst",
    r"xd+?",
    r"xnxx"
]

informals = RegexMatches(name + ".informals", informal_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
