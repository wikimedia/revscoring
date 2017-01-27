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
:class:`enchant.Dict` "ru".  Provided by `aspell-ro`
"""

stopwords = Stopwords(name + ".stopwords", set([
    "a", "accessdate", "aceasta", "această", "acest", "acesta",
        "adresă", "ai", "al", "ale", "ales", "alt", "alte", "altitudine",
        "and", "ani", "anul", "apoi", "aprilie", "are", "asemenea", "astfel",
        "au", "august", "avea", "avut", "așezare",
    "b", "bibliografie", "bibliotecare", "bucurești",
    "c", "care", "categorie", "cea", "cei", "cel", "cele", "center", "ciot",
        "cod", "codpoștal", "com", "comuna", "comună", "coordonate",
        "cum", "când", "că", "către",
    "d", "dar", "data", "date", "dată", "decembrie", "defaultsort",
        "densitate", "descriere", "despre", "din", "dintre", "doar", "două",
        "după",
    "e", "ei", "era", "este", "externe",
    "f", "face", "februarie", "fiind", "file", "fişier", "fișier", "foarte",
        "fost", "fără",
    "harta", "hartă", "htm", "html", "http",
    "i", "ianuarie", "iar", "ii", "image", "imagine", "in", "index", "infobox",
        "infocaseta", "informații", "iulie", "iunie",
    "jpg", "județ", "județul", "județului",
    "l", "latd", "latm", "latns", "lats", "le", "lea", "left", "legături",
        "limba", "limbă", "lista", "listănote", "loc", "localități", "locul",
        "longd", "longev", "longm", "longs", "lor", "lui", "lumii",
    "m", "map", "mare", "martie", "mult", "multe",
    "n", "name", "nașteri", "național", "nbsp", "noiembrie", "note",
        "nu", "nume", "numele",
    "o", "oameni", "octombrie", "of", "old", "oraș", "orașe", "orașul",
        "orașului", "org",
    "p", "parte", "partea", "pe", "pentru", "peste", "php", "png", "poate",
        "populaţie", "populație", "prima", "primar", "primul", "prin",
        "printre", "publisher", "px", "până",
    "recensământ", "redirecteaza",
        "ref", "references", "referințe", "reflist", "right", "românia",
        "româniei", "română",
    "s", "sale", "sau", "secolul", "septembrie", "sit", "spre", "stat",
        "stemă", "style", "sub", "sunt", "suprafaţă", "suprafață", "svg",
        "să", "său",
    "the", "thumb", "timp", "timpul", "tip", "title", "titlu", "toate", "trei",
    "ul", "ului", "un", "unde", "unei", "unui", "unul", "url",
    "v", "va", "vezi", "viață",
    "web", "website", "www",
    "x",
    "în", "început", "într", "între",
    "şi",
    "ţară",
    "și",
    "țară", "țările"
]))

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
