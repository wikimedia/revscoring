import json
from pkg_resources import resource_filename

from .features import Dictionary, SubstringMatches, Stemmed, Stopwords, \
    RegexMatches
from .features.dictionary import MultiDictChecker, load_dict, utf16_cleanup

name = "english"

multi_dict = MultiDictChecker(
    load_dict('en_US', 'hunspell-en-us'),
    load_dict('en_GB', 'hunspell-en-gb'),
    load_dict('en_AU', 'hunspell-en-au'))


def safe_dictionary_check(word):
    return multi_dict.check(utf16_cleanup(word))


dictionary = Dictionary(name + ".dictionary", safe_dictionary_check)
"""
:class:`~revscoring.languages.features.Dictionary` features via
`enchant.Dict <https://github.com/rfk/pyenchant>`_ "en". Provided by
`hunspell-en-au`, `hunspell-en-gb`, and `hunspell-en-us`.
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
`nltk.corpus.stopwords <https://www.nltk.org/api/nltk.corpus.html>`_ "english"
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
    r"naz+i(sm?)?",
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
    r"ain'?t", r"a+we?some?(r|st)?",
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
    r"h+[aiou]+(h[aeiou]*)*",
    r"mw?[au]+h+[aiou]+(h[aeiou]*)*",
    r"h+[e]+(h[aeiou]*)+",
    r"hel+?o+", r"h(aa+?|e+?)y+?",
    r"h+?m+?",
    r"i", r"i+?d+?i+?o+?t+?",
    r"(la)+",
    r"loser",
    r"l+[uo][uol]*l",
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
    r"w+[oua]+t+", r"wtf\w*", r"wh?[ua]+?t?[sz]+[ua]+p", r"s+?u+?p+?",
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

words_to_watch_regexes = [
    # Puffery
    r'legendary', r'best', r'great', r'acclaimed', r'iconic',
    r'visionary', r'outstanding', r'leading', r'celebrated',
    r'award[- ]?winning',
    r'landmark', r'cutting[- ]?edge', r'innovative', r'extraordinary',
    r'brilliant', r'hit', r'famous', r'renowned', r'remarkable',
    r'prestigious',
    r'world[- ]?class', r'respected', r'notable', r'virtuoso', r'honorable',
    r'awesome', r'unique', r'pioneering',
    # Contentious labels (-gate removed)
    r'cult', r'racist', r'perverted', r'sect', r'fundamentalist', r'heretic',
    r'extremist', r'denialist', r'terrorist', r'freedom[- ]?fighter', r'bigot',
    r'myth', r'neo[- ]?nazi', r'pseudo(scientific|intellectual)',
    r'controversial',
    # Unsupported attributions
    r'(most|many|some|people|scholars|scientists|science|experts) ' +
        '(say|state|believe|regard|report|claim|feel|declare)',
    r'it is ((often|sometimes|widely) )?' +
        '(believed|regarded|said|shown|reported|thought)',
    r'are of the opinion',
    r'(research|science) (has shown|says|claims)',
    # Expressions of doubt
    r'supposed', r'apparent', r'purported', r'alleged', r'accused',
    r'so[- ]called',
    # Editorializing
    r'notably', r'it should be noted', r'arguably', r'interestingly',
    r'essentially', r'actually', r'clearly', r'of course', r'without a doubt',
    r'happily', r'tragically', r'aptly', r'fortunately', r'unfortunately',
    r'untimely', r'but', r'despite', r'however', r'though', r'although',
    r'furthermore',
    # Synonyms for "said"
    r'reveal', r'point out', r'clarify', r'expose', r'explain', r'find',
    r'note', r'observe', r'insist', r'speculate', r'surmise', r'claim',
    r'assert', r'admit', r'confess', r'deny',
    # Lack of precision
    r'passed away', r'gave his life', r'eternal rest', r'make love',
    r'an issue with', r'collateral damage', r'living with cancer',
    # Idioms
    r'lion\'s share', r'tip of the iceberg', r'white elephant',
    r'gild the lily', r'take the plunge', r'ace up the sleeve',
    r'bird in the hand', r'twist of fate', r'at the end of the day',
    # Relative time reference
    r'recently', r'lately', r'currently', r'today', r'presently', r'to date',
    r'15 years ago', r'formerly', r'in the past', r'traditionally',
    r'(this|last|next) (year|month|winter|spring|summer|fall|autumn)',
    r'yesterday', r'tomorrow', r'in the future', r'now', r'soon', r'since',
    # Unspecified places or events
    r'this country', r'here', r'there', r'somewhere', r'sometimes', r'often',
    r'occasionally', r'somehow',
    # Survived by
    r'(is|was) survived by', r'was survived by',
    # Neologisms
    r'(pre|post|anti|non)-\w+', r'\w+-like'
]

words_to_watch = RegexMatches(name + ".words_to_watch", words_to_watch_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
problematic words and phrases for use in reference text
"""

filepath = resource_filename('revscoring', 'assets/enwiktionary_idioms.txt')
with open(filepath) as f:
    idioms_list = [json.loads(line) for line in f]

idioms = SubstringMatches(name + ".idioms", idioms_list)
"""
:class:`~revscoring.languages.features.SubstringMatches` features via a list of
idioms from the `~assets/enwiktionary_idioms.txt` file
"""
