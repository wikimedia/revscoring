from .features import Dictionary, RegexMatches, Stopwords

name = "estonian"

try:
    import enchant
    dictionary = enchant.Dict("et")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'et'.  " +
                      "Consider installing 'myspell-et'.")

dictionary = Dictionary(name + ".dictionary", dictionary.check)
"""
:class:`~revscoring.languages.features.Dictionary` features via
:class:`enchant.Dict` "et". Provided by `myspell-et`
"""

# No stemmer

# Copied from https://meta.wikimedia.org/wiki/?oldid=13987775
stopwords = [
    "aasta", "aastal", "aastani", "aastast", "aastat", "aastatel", "aeg",
    "aga", "ainult", "ajal", "ajalugu", "alates", "all", "alla", "allikad",
    "ameerika", "and", "aprill", "artikkel", "artiklit", "asub", "august",
    "autor", "category", "class", "com", "commons", "coordinate",
    "detsember", "di", "eest", "eesti", "eestis", "ega", "ehk", "ei", "elu",
    "enam", "enne", "esimene", "esimese", "est", "euroopa", "ew", "file",
    "hiljem", "htm", "html", "http", "ide", "iga", "ii", "il", "ile", "image",
    "in", "index", "inglise", "inimesed", "ist", "jaanuar", "jpg", "juba",
    "juuli", "juuni", "juures", "jäi", "järgi", "järjesta", "kaks", "kas",
    "kategooria", "keel", "keeles", "keeletoimeta", "kes", "kirjandus",
    "koduleht", "kogu", "kohta", "kokku", "kolm", "koos", "korda", "kui",
    "kuid", "kuna", "kuni", "kus", "kuu", "kõige", "kõik", "le", "left",
    "liit", "link", "linna", "lisa", "lisaks", "lk", "läbi", "lõuna",
    "maailma", "maakonna", "mida", "mille", "mis", "mitte", "märts", "nad",
    "nagu", "name", "need", "neid", "neist", "nende", "news", "ng", "nii",
    "nime", "nimi", "ning", "november", "nr", "ns", "näiteks", "of",
    "oktoober", "old", "ole", "oli", "olid", "olla", "olnud", "oma", "on",
    "org", "osa", "palju", "pdf", "peale", "php", "pildi", "pilt", "pisi",
    "png", "pole", "poolt", "px", "pärast", "põhja", "ref", "region", "right",
    "riigi", "riik", "rohkem", "rootsi", "räägib", "saab", "saanud", "sai",
    "saksa", "saksamaa", "sama", "samal", "samuti", "seal", "seda", "see",
    "selle", "sellest", "seotud", "september", "sest", "siis", "siiski",
    "small", "sse", "surnud", "suur", "svg", "sündinud", "tagasi", "tallinn",
    "tallinna", "tartu", "teda", "teine", "teise", "teiste", "tema", "the",
    "thumb", "toimeta", "toimetaaeg", "tuntud", "type", "tõttu", "umbes",
    "usa", "uus", "vaata", "vahel", "vaid", "vald", "vana", "varem", "vastu",
    "veebruar", "veel", "vene", "venemaa", "viide", "viited", "von", "väga",
    "välislingid", "välja", "või", "võib", "www", "ära", "ühe", "üks", "üle",
    "ülikool",
]
"""
:class:`~revscoring.languages.features.Stopwords` features copied from
"common words" in https://meta.wikimedia.org/wiki/?oldid=13987775
"""

stopwords = Stopwords(name + ".stopwords", stopwords)

badword_regexes = [
    r"pede",
    r"loll(akas|id)?",
    r"t(s|š)mir",
    r"pers+e(s)?",
    r"munn(i|id)?",
    r"kaka(junn)?",
    r"noku",
    r"pede(d|kas)?",
    r"vitt(u)?",
    r"pask",
    r"homo(d)?",
    r"puts(i)?",
    r"pederast(id)?",
    r"sitt(a)?",
    r"lits(id)?",
    r"pihku",
    r"türa",
    r"jobu",
    r"sita(ne|junn)?",
    r"vitupea",
    r"neeger",
    r"nigga",
    r"junn(i)?",
    r"kepp(is|i|ida)?",
    r"tuss"
]

badwords = RegexMatches(name + ".badwords", badword_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
    r"lol(l)?"
    r"yolo",
    r"jou",
    r"raisk",
    r"tere",
    r"suht",
    r"haha",
    r"tsau",
    r"tegelt",
    r"sakib",
    r"noob",
    r"hahaha",
    r"räme",
    r"ilge",
    r"lahe",
    r"hmm"
]

informals = RegexMatches(name + ".informals", informal_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
