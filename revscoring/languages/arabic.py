from .features import Dictionary, RegexMatches, Stopwords

name = "arabic"

try:
    import enchant
    dictionary = enchant.Dict("ar")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'ar'.  " +
                      "Consider installing 'aspell-ar'.")

dictionary = Dictionary(name + ".dictionary", dictionary.check)
"""
:class:`~revscoring.languages.features.Dictionary` features via
`enchant.Dict <https://github.com/rfk/pyenchant>`_ "ar".  Provided by `aspell-ar`
"""

try:
    from nltk.corpus import stopwords as nltk_stopwords
    stopwords = set(nltk_stopwords.words('arabic'))
except LookupError:
    raise ImportError("Could not load stopwords for {0}. ".format(__name__) +
                      "You may need to install the nltk 'stopwords' " +
                      "corpora.  See http://www.nltk.org/data.html")

stopwords = Stopwords(name + ".stopwords", stopwords)
"""
:class:`~revscoring.languages.features.Stopwords` features provided by
`nltk.corpus.stopwords <https://www.nltk.org/api/nltk.corpus.html>`_ "arabic"
"""


badword_regexes = [
    r"احا",
    r"عاهرا",
    r"زندقتهما",
    r"حمار",  # Donkey
    r"لعن",  # Damn
    r"يلعن",  # Damned
    r"لعنه",  # Damn him/her
    r"امك",  # Your mother
    r"لعنتهما",  # Damn you
    r"فلعنهما",  # So damn you
    r"اعزبوا",
    r"عزبوا",
    r"لدحي",
    r"زبي",
    r"كلب",  # Dog
    r"كافر",  # Kafir
    r"والله",  # Swear to god
    r"الحمار",  # The donkey
    r"الزنا",
    r"النيك",
    r"كلابي",
    r"الكلب",  # The dog
    r"منو",
    r"نجس",
    r"والعياذ",
    r"يتبرز",
    r"الكافر",  # The Kaffir
    r"تتزر",
    r"منكاحا",
    r"وينكح",
    r"منافق",  # Monafigh
    r"الشيطان",  # Satan
]

badwords = RegexMatches(name + ".badwords", badword_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
    r"كالامازوه",
    r"فغانيون",
    r"ومراف",
    r"زوه",
    r"رلا",
    r"بلوجاتي",
    r"كتمتمان",
    r"سراريه",
    r"اجك",
    r"الجيدي",
    r"مناخرهم",
    r"الجيرل",
    r"وخلاخيل",
    r"اكشفي",
    r"ومحاسنه",
    r"يبزقن",
    r"اجهن",
    r"اطهن",
    r"ستنفض",
    r"خطبهن",
    r"اخدون",
    r"غمزني",
    r"فطلقني",
    r"فحكه",
    r"خرق",
    r"وهل",
    r"اللي",
    r"تحرموا",
    r"الزن",
    r"بالنعلين",
    r"وغلامك",
    r"عليلك",
    r"فتحدثها",
    r"اتمن",
    r"الشنبا",
    r"وروراو",
    r"والفاج",
    r"صوردون",
    r"ورجلاي",
    r"وضاحا",
    r"مختار",
    r"نسب",
    r"شيخ",  # Shikh
]

informals = RegexMatches(name + ".informals", informal_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
