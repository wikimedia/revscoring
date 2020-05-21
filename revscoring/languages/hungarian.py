from .features import Dictionary, RegexMatches, Stopwords

name = "hungarian"

try:
    import enchant
    dictionary = enchant.Dict("hu")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'hu'.  " +
                      "Consider installing 'aspell-hu'.")

dictionary = Dictionary(name + ".dictionary", dictionary.check)
"""
:class:`~revscoring.languages.features.Dictionary` features via
`enchant.Dict <https://github.com/rfk/pyenchant>`_ "hungarian".  Provided by
`aspell-hu`
"""

try:
    from nltk.corpus import stopwords as nltk_stopwords
    stopwords = set(nltk_stopwords.words('hungarian'))
except LookupError:
    raise ImportError("Could not load stopwords for {0}. ".format(__name__) +
                      "You may need to install the nltk 'stopwords' " +
                      "corpora.  See http://www.nltk.org/data.html")

stopwords = Stopwords(name + ".stopwords", stopwords)
"""
:class:`~revscoring.languages.features.Stopwords` features provided by
`nltk.corpus.stopwords <https://www.nltk.org/api/nltk.corpus.html>`_ "hungarian"
"""

badword_regexes = [
    r"anyad",
    r"anyád",
    r"anyádat",
    r"anyátok",
    r"anyátokat",
    r"apád",
    r"asd",
    r"balfasz",
    r"baszni",
    r"baszott",
    r"bazd",
    r"bazdmeg",
    r"bazmeg",
    r"béna",
    r"birkanépet",
    r"birkanépünk",
    r"büdös",
    r"buktája",
    r"buzi",
    r"buzik",
    r"csicska",
    r"csá",
    r"fasszopó",
    r"fasz",
    r"fasza",
    r"faszfej",
    r"faszkalap",
    r"faszok",
    r"faszom",
    r"faszomat",
    r"faszság",
    r"faszt",
    r"faszát",
    r"fing",
    r"fos",
    r"fuck",
    r"geci",
    r"gecik",
    r"gecis",
    r"gecit",
    r"hulye",
    r"hülye",
    r"hülyék",
    r"kabbe",
    r"kaka",
    r"kaki",
    r"kibaszott",
    r"kocsog",
    r"kuki",
    r"kurva",
    r"kurvák",
    r"kurvára",
    r"kurvát",
    r"köcsög",
    r"köcsögök",
    r"lófasz",
    r"megbaszta",
    r"mocskos",
    r"málejku",
    r"mizu",
    r"naon",
    r"picsa",
    r"picsája",
    r"pina",
    r"punci",
    r"putri",
    r"pöcs",
    r"retkes",
    r"ribanc",
    r"rohadt",
    r"sissitek",
    r"szar",
    r"szarok",
    r"szaros",
    r"szart",
    r"szopd",
    r"sále",
    r"elmenyekvolgye",
    r"immoviva",
    r"infosarok",
    r"kirandulastervezo",
    r"kirándulástervező",
    r"magyarvendeglatas",
    r"magyarvendéglátás",
    r"magyarvirtus",
    r"matraonline",
    r"mátraonline",
    r"nosztalgiautazasok",
    r"pestmost",
    r"tapioregio",
    r"turist",
    r"utazasi",
    r"vandorhorgasz",
    r"vándorhorgász",
    r"ellopásával",
    r"eszünkbe",
    r"felelőtlen",
    r"gergényi",
    r"gyurcsány",
    r"hatalmakat",
    r"hazaáruló",
    r"hazudnak",
    r"hazugság",
    r"hazugságra",
    r"hazánknak",
    r"honfitársaim",
    r"hunyadiné",
    r"kicsinyes",
    r"kluboldala",
    r"laci",
    r"lejárató",
    r"lenéznek",
    r"lopásra",
    r"megalázni",
    r"megdézsmálásának",
    r"megvetnek",
    r"megválasztó",
    r"megérdemel",
    r"nemzsidókra",
    r"panamai",
    r"rovástáblás",
    r"szavazófülke",
    r"szex",
    r"talmudjukban",
    r"tiszaeszlár",
    r"toaffot",
    r"tehetetlenül",
    r"torolják",
    r"érdekeik",
    r"érdekeiknek",
]

badwords = RegexMatches(name + ".badwords", badword_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
    r"baromság",
    r"dencey",
    r"haha",
    r"hahaha",
    r"hehe",
    r"hello",
    r"hihi",
    r"hülyeség",
    r"képviselőink",
    r"képviselőinket",
    r"képünkbe",
    r"lol",
    r"megválasszuk",
    r"mészárosaim",
    r"országunk",
    r"special",
    r"soknevű",
    r"szavazatunkat",
    r"szeretem",
    r"szeretlek",
    r"szerintem",
    r"szia",
    r"sziasztok",
    r"tex",
    r"xdd",
    r"xddd",
    r"tudjátok",
    r"tönkretesszük",
    r"ugye",
    r"unokáink",
    r"user",
    r"utálom",
    r"vagyok",
    r"vagytok",
]

informals = RegexMatches(name + ".informals", informal_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
