from .features import Dictionary, RegexMatches, Stemmed, Stopwords
from .features.dictionary import utf16_cleanup

name = "english"

try:
    import enchant
    enchant_dict = enchant.Dict("en")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'en'.  " +
                      "Consider installing 'myspell-en-au', " +
                      "'myspell-en-gb', 'myspell-en-us' and/or " +
                      "'myspell-en-za'.")


def safe_dictionary_check(word):
    return enchant_dict.check(utf16_cleanup(word))

dictionary = Dictionary(name + ".dictionary", safe_dictionary_check)
"""
:class:`~revscoring.languages.features.Dictionary` features via
:class:`enchant.Dict` "en". Provided by `myspell-en-au`, `myspell-en-gb`,
`myspell-en-us`, and `myspell-en-za`.
"""

try:
    from nltk.corpus import stopwords as nltk_stopwords
    stopwords = set(nltk_stopwords.words('english'))
except LookupError:
    raise ImportError("Could not load stopwords for {0}. ".format(__name__) +
                      "You may need to install the nltk 'stopwords' " +
                      "corpora.  See http://www.nltk.org/data.html")

stopwords = Stopwords(name + ".stopwords", stopwords)
"""
:class:`~revscoring.languages.features.Stopwords` features provided by
:func:`nltk.corpus.stopwords` "english"
"""

try:
    from nltk.stem.snowball import SnowballStemmer
    stemmer = SnowballStemmer("english")
except ValueError:
    raise ImportError("Could not load stemmer for {0}. ".format(__name__))

stemmed = Stemmed(name + ".stemmed", stemmer.stem)
"""
:class:`~revscoring.languages.features.Stemmed` word features via
:class:`nltk.stem.snowball.SnowballStemmer` "english"
"""

badword_regexes = [
    r"a+[sr]+s+e*([-_ ]?butt|clown|face|hole|hat|e?s)?",
    r"(fat|stupid|lazy)a+[sr]+s+e*([-_ ]?butt|clown|face|hole|hat|e?s)?",
    r"autofel+at(e|io|ing|ion)s?",
    r"b+i+o?t+c+h+\w*",
    r"bootlip",
    r"blow(job|me)\w*",
    r"bollock\w*",
    r"boo+ger\w*",
    r"b+u+t+t+([-_ ]?clown|face|hole|hat|es)?",
    r"(ass|arse)b+u+t+t+([-_ ]?clown|face|hole|hat|es)?",
    r"bugg(er|ing)\w*",
    r"butthead", r"buttface", r"buttsex", r"buttf+u+c*k+\w*",
    r"chlamydia",
    r"cholo",
    r"chug",
    r"clunge\w*",
    r"cock\w*",
    r"coo+n\w*",
    r"[ck]racker\w*",
    r"c+?u+?n+?t\w*",
    r"crack[-_ ]?head\w*",
    r"crooks?",
    r"defraud",
    r"limpdick\w*",
    r"dick\w*",
    r"d+?i+?l+?d+?o+?\w*",
    r"dishonest\w*",
    r"dot[-_ ]?head\w*",
    r"dyk(e|ing)\w*",
    r"(f|ph)a+g+(ot)?\w*",
    r"fart\w*",
    r"fraud",
    r"f+u+c*k+\w*",
    r"gh?[ea]+y+\w*",
    r"g[yi]p+(o|y|ie?)?", r"gyppie",
    r"goo+k",
    r"gringo",
    r"he+rpe+s",
    r"hill-?billy",
    r"hom(a|o|er)(sexual)?\w*",
    r"hooker\w*",
    r"injun\w*",
    r"j+a+p+o?",
    r"k[iy]+ke",
    r"kwash(i|ee)",
    r"l+?e+?s+?b+?(o+?|i+?a+?n+?)\w*",
    r"liar",
    r"lick(er)?s?",
    r"meth",
    r"meth[-_ ]?head\w*",
    r"naz+i",
    r"nig", r"n+?i+?gg+?[aeious]+?\w*", r"niglet", r"nigor", r"nigr", r"nigra",
    r"nonc(e|ing)\w*",
    r"overdose[sd]",
    r"peckerwood\w*",
    r"p(a?e|æ)do((f|ph)[iy]le)?s?",
    r"peni(s)?\w*",
    r"piss\w*",
    r"prostitute\w*",
    r"pot[-_ ]?head\w*",
    r"q(w|u)ash(i|ee)",
    r"rag[-_ ]?head",
    r"red[-_ ]?(neck|skin)",
    r"round[-_ ]?eye",
    r"satan(ic|ism|ist)s?",
    r"scabies",
    r"s+h+[ia]+t+\w*",
    r"s+?l+?u+?t+?\w*",
    r"spi(g|c|k)+",
    r"spigotty",
    r"spik",
    r"spook",
    r"squarehead",
    r"stupid(s+h+[ia]+t+|c+u+n+t+|f+u+c*k+|t+w+a+t+|w+h+o+r+e+)\w*",
    r"subnormal",
    r"su+c*k+(er|iest|a)",
    r"syphil+is",
    r"terror(ist|ism|i[zs](e|ing|ed))s?",
    r"thei[fv](e?s)?",
    r"tran(ny|sexual)",
    r"t+?w+?a+?t+?\w*",
    r"ti+t+((s|ies|y)[\w]*)?",
    r"v+?a+?g+?(i+n+a+)?", r"vajay?jay?\w*",
    r"wank\w*", r"wetback\w*", r"w+h+o+r+(e+|ing)\w*", r"w+o+g+", r"w+o+p+",
    r"yank(e+)?", r"yid",
    r"zipperhead"
]

badwords = RegexMatches(name + ".badwords", badword_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
    r"ain'?t", "a+we?some?(r|st)?",
    r"(b+l+a+h*)+",
    r"b+?o+?n+?e+?r+?",
    r"boobs?",
    r"bullshit",
    r"bro",
    r"(bye)+",
    r"can'?t",
    r"[ck](oo+|e+w+)l+\w*",
    r"[ck]+r+a+p+(s|ier|iest)?",
    r"chu+g+",
    r"dad+(y|a)?",
    r"don'?t", r"dum+b*(y|ies|er|est)?(ass)?",
    r"d+?u+?d+?e+?\w*",
    r"good[-_]?bye",
    r"h+[aiou]+(h+[aeiou]*)*",
    r"mw?[au]+h+[aiou]+(h+[aeiou]*)*",
    r"h+[e]+(h+[aeiou]*)+",
    r"hel+?o+", r"h(aa+?|e+?)y+?",
    r"h+?m+?",
    r"i", r"i+?d+?i+?o+?t+?",
    r"(la)+",
    r"loser",
    r"(l+[uo]+l+)([uo]+l+)*",
    r"l+?m+?a+?o+?",
    r"l[ou]+?ve?",
    r"m+?e+?o+?w+?",
    r"munch\w*",
    r"mom+(y|a)?",
    r"moron",
    r"nerds?",
    r"noo+b(y|ie|s)?\w*",
    r"no+?pe",
    r"o+?k+?(a+?y+?)?",
    r"o+?m+?g+?\w*",
    r"poo+?p\w*",
    r"retard\w*", r"tard",
    r"r+?o+?f+?l+?(mao)?",
    r"s+?e+?x+?y+?",
    r"so+?rry",
    r"shove",
    r"smelly",
    r"soo+?",
    r"stink(s|y)?",
    r"s+?t+?[uo]+?p+?i+?d+?\w*",
    r"suck(s|ing|er)?", r"sux",
    r"shouldn'?t",
    r"test +edit", r"t+?u+?r+?d+?s?\w*",
    r"wasn'?t",
    r"w+[oua]+t+", r"wtf\w*", r"wh?[ua]+?t?[sz]+[ua]+p", "s+?u+?p+?",
    r"wu+?z+?",
    r"won'?t",
    r"w+?o+?o+?f+?",
    r"ya'?ll", r"y+?a+?y+?", r"y+?e+?a+?h?", r"you('?(ve|re|ll))?",
    r"y+?o+?l+?o+?"
]

informals = RegexMatches(name + ".informals", informal_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
