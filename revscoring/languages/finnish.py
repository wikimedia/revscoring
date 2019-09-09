from .features import RegexMatches, Stopwords

name = "finnish"

# No dictionary

# No stemmer

try:
    from nltk.corpus import stopwords as nltk_stopwords
    stopwords = set(nltk_stopwords.words('finnish'))
except LookupError:
    raise ImportError("Could not load stopwords for {0}. ".format(__name__) +
                      "You may need to install the nltk 'stopwords' " +
                      "corpora.  See http://www.nltk.org/data.html")

stopwords = Stopwords(name + ".stopwords", stopwords)
"""
:class:`~revscoring.languages.features.Stopwords` features provided by
`nltk.corpus.stopwords <https://www.nltk.org/api/nltk.corpus.html>`_ "finnish"
"""

badword_regexes = [
    r"homo",
    r"homoja",
    r"homot",
    r"hintti",
    r"homppeli",
    r"huora",
    r"idiootti",
    r"jumalauta",
    r"juntti",
    r"kakka",
    r"kakkaa",
    r"kikkeli",
    r"kyrpä",
    r"kulli",
    r"kusi",
    r"kusipää",
    r"läski",
    r"mamu",
    r"matu",
    r"neekeri",
    r"nussii",
    r"narttu",
    r"paska",
    r"paskaa",
    r"paskat",
    r"paskin",
    r"paskova",
    r"pelle",
    r"perse",
    r"perseeseen",
    r"perseessä",
    r"perseestä",
    r"perseenreikä",
    r"perkele",
    r"pillu",
    r"pilluun",
    r"pippeli",
    r"pieru",
    r"retardi",
    r"runkkari",
    r"saatana",
    r"saatanan",
    r"tyhmä",
    r"vammane",
    r"vammanen",
    r"vittu",
    r"vitun",
    r"äpärä"
]

badwords = RegexMatches(name + ".badwords", badword_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
    r"haistakaa",
    r"imekää",
    r"lol",
    r"ootte",
    r"moi",
    r"hei",
    r"sinä",
    r"sä",
    r"minä",
    r"mää",
    r"ok",
    r"joo",
    r"okei"
]

informals = RegexMatches(name + ".informals", informal_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
