from .features import Dictionary, RegexMatches, Stemmed, Stopwords

name = "russian"

try:
    import enchant
    dictionary = enchant.Dict("ru")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'ru'.  " +
                      "Consider installing 'myspell-ru'.")

dictionary = Dictionary(name + ".dictionary", dictionary.check)
"""
:class:`~revscoring.languages.features.Dictionary` features via
`enchant.Dict <https://github.com/rfk/pyenchant>`_ "ru".  Provided by `myspell-ru`
"""

try:
    from nltk.corpus import stopwords as nltk_stopwords
    stopwords = set(nltk_stopwords.words('russian'))
except LookupError:
    raise ImportError("Could not load stopwords for {0}. ".format(__name__) +
                      "You may need to install the nltk 'stopwords' " +
                      "corpora.  See http://www.nltk.org/data.html")

stopwords = Stopwords(name + ".stopwords", stopwords)
"""
:class:`~revscoring.languages.features.Stopwords` features provided by
`nltk.corpus.stopwords <https://www.nltk.org/api/nltk.corpus.html>`_ "russian"
"""

try:
    from nltk.stem.snowball import SnowballStemmer
    stemmer = SnowballStemmer("russian")
except ValueError:
    raise ImportError("Could not load stemmer for {0}. ".format(__name__))

stemmed = Stemmed(name + ".stemmed", stemmer.stem)
"""
:class:`~revscoring.languages.features.Stemmed` word features via
:class:`nltk.stem.snowball.SnowballStemmer` "russian"
"""

badword_regexes = [
    r"анал",
    r"бля", r"блядь", r"блять",
    r"бомжеград",
    r"выкипидар", r"выкипидары", r"выкипидор", r"выкипидоры",
    r"гандон",
    r"говна", r"говно",
    r"гондон",
    r"дебил", r"дебилы",
    r"дерьмо",
    r"дибил", r"дибилы",
    r"дырочка",
    r"ебал", r"ебали", r"ебать",
    r"жид", r"жиды",
    r"жопа", r"жопе", r"жопо", r"жопу", r"жопы",
    r"ибаццо",
    r"клизмофил", r"клизмофилия",
    r"лохом",
    r"мрази", r"мразь",
    r"мудак",
    r"нах", r"нахуй",
    r"нерусь",
    r"нехуй",
    r"отъеби", r"отъебись", r"отъебли",
    r"педераст", r"педерасты",
    r"пидар", r"пидарас", r"пидарасы", r"пидарок", r"пидары",
    r"пидор", r"пидорас", r"пидорасы", r"пидорок", r"пидоры",
    r"пизда", r"пиздец", r"пиздой", r"пизды",
    r"писька",
    r"писюн",
    r"попку",
    r"сосал", r"сосать",
    r"сосет", r"сосёт",
    r"соси", r"сосите",
    r"сосут",
    r"сука", r"суки",
    r"сученок", r"сучёнок",
    r"твари",
    r"трахал", r"трахала", r"трахали", r"трахалась",
    r"ублюдочные", r"ублюдочный",
    r"урод", r"уроды",
    r"фекальные",
    r"хер(ней|ня)",
    r"хуе(в(ый?)?|та)",
    r"ху[ий]",
    r"хуя(ми)?", r"хуями",
    r"хуйн([её]й|ю|я)",
    r"чмо",
    r"чурки",
    r"шлюха",
    r"щачло"
]

badwords = RegexMatches(name + ".badwords", badword_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
    r"lol",
    r"арёл",
    r"безопасносте",
    r"блин",
    r"быдло",
    r"голактеко",
    r"доблестне",
    r"к[ао]роче?",
    r"лол",
    r"ля(ля)+",
    r"онотоле",
    r"отстой",
    r"поганые",
    r"превед",
    r"пук",
    r"сиськи",
    r"статейки",
    r"упячка",
    r"(ха)+",
    r"чув(ак|иха)",
    r"чушь",
    r"ыы(ы)+"
]

informals = RegexMatches(name + ".informals", informal_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
