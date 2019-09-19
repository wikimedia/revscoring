from .features import Dictionary, RegexMatches, Stopwords

name = "icelandic"

try:
    import enchant
    dictionary = enchant.Dict("is")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'is'.  " +
                      "Consider installing 'aspell-is'.")

dictionary = Dictionary(name + ".dictionary", dictionary.check)
"""
:class:`~revscoring.languages.features.Dictionary` features via
`enchant.Dict <https://github.com/rfk/pyenchant>`_ "is".  Provided by `aspell-is`
"""

stopwords = [
    "aftur", "alignbars", "and", "annars", "auk", "aðeins", "bæði", "eftir",
    "einnig", "eins", "enn", "eru", "eða", "flokkur", "fram", "frá", "hafa",
    "hafi", "hafði", "hana", "hann", "hans", "hefur", "heldur", "helstu",
    "hennar", "hins", "hjá", "honum", "hvað", "höfðu", "hún",
    "landafræðistubbur", "linedata", "líka", "með", "mánuðurskoðað", "orðið",
    "plotarea", "seinna", "sem", "sig", "sinn", "sinni", "sitt", "sjá",
    "stubbur", "svo", "sér", "sína", "sínum", "síðan", "síðar", "talið",
    "tengill", "til", "tillpos", "timeaxis", "varð", "vegna", "vera", "verið",
    "verður", "við", "voru", "væri", "wpheimild", "árið", "árskoðað", "ásamt",
    "þann", "þannig", "þar", "þau", "það", "þegar", "þeim", "þeir", "þeirra",
    "þess", "þessi", "þessum", "þetta", "því", "þær"
]

stopwords = Stopwords(name + ".stopwords", stopwords)
"""
:class:`~revscoring.languages.features.Stopwords` features copied from
"common words" in https://meta.wikimedia.org/wiki/?oldid=17380335
"""

badword_regexes = [
    r"adc",
    r"böllinn",
    r"böllur",
    r"hommi",
    r"idiot",
    r"typpi",
    r"typpið",
    r"andskotans",
    r"andskotinn",
    r"djöfulsins",
    r"djöfullinn",
    r"helvítis",
    r"helvíti",
    r"hóra",
    r"freta",
    r"fretaði",
    r"kúkar",
    r"kúkaði",
    r"faggi",
    r"fábjáni",
    r"fitabolla",
    r"grenjuskjóða",
    r"suckar",
    r"suck",
    r"sjúgðu",
    r"saug",
    r"væluskjóða",
    r"fæðingarhálviti",
    r"mannfjandi",
    r"drulludeli",
    r"drullukunta",
    r"raggeit",
    r"brundþró",
    r"trunta",
    r"prumpa",
    r"prumpaði",
    r"píka",
    r"píku",
    r"hálfviti",
    r"hommadjöfull",
    r"drullusokkur",
    r"fáviti",
    r"aumingi",
    r"mannfýla",
    r"negri",
    r"negrar",
    r"hlandbrenndu",
    r"náriðill",
    r"vesalingur",
    r"ónytjungur",
    r"fitubelgur",
    r"lúði",
    r"lúðablesi",
    r"kvikindi",
    r"kvikindið",
    r"klikkhaus",
    r"mella",
    r"skítseiði",
    r"kill",
    r"drepa",
    r"fjandinn",
    r"fjandans",
    r"fokka",
    r"fokkaði",
    r"nauðga",
    r"nauðgaði"
]

badwords = RegexMatches(name + ".badwords", badword_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
    r"awesome",
    r"del",
    r"face",
    r"mockbuster",
    r"sick",
    r"stupid",
    r"bla+",
    r"bæ",
    r"bless",
    r"hæ",
    r"halló",
    r"haha+",
    r"bull",
    r"kveðja",
    r"pampered",
    r"lol",
    r"auli",
    r"aulast",
    r"aulablesi",
    r"fífl",
    r"skúrkur",
    r"flón",
    r"skoffín",
    r"garmur",
    r"jullur",
    r"mellufær",
    r"dræsur",
    r"brjóst"
]

informals = RegexMatches(name + ".informals", informal_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
