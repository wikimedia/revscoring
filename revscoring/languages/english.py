import sys

from .space_delimited import SpaceDelimited

try:
    from nltk.stem.snowball import SnowballStemmer
    stemmer = SnowballStemmer("english")
except ValueError:
    raise ImportError("Could not load stemmer for {0}. ".format(__name__))

try:
    from nltk.corpus import stopwords as nltk_stopwords
    stopwords = set(nltk_stopwords.words('english'))
except LookupError:
    raise ImportError("Could not load stopwords for {0}. ".format(__name__) +
                      "You may need to install the nltk 'stopwords' " +
                      "corpora.  See http://www.nltk.org/data.html")

try:
    import enchant
    dictionary = enchant.Dict("en")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'en'.  " +
                      "Consider installing 'myspell-en-au', " +
                      "'myspell-en-gb', 'myspell-en-us' and/or " +
                      "'myspell-en-za'.")

badwords = [
    r"(fat|stupid|lazy)?a+[sr]+s+e*([-_ ]?butt|clown|face|hole|hat|e?s)?",
    r"autofel+at(e|io|ing|ion)s?",
    r"\w*b+i+o?t+c+h+\w*", r"bootlip",
    r"\w*blow(job|me)\w*",
    r"bollock\w*",
    r"\w*boo+ger\w*",
    r"(ass|arse)?b+u+t+t+([-_ ]?clown|face|hole|hat|es)?",
    r"bugg(er|ing)\w*",
    r"chlamydia",
    r"cholo",
    r"chug",
    r"clunge\w*",
    r"cock\w*",
    r"coo+n\w*",
    r"[ck]racker\w*",
    r"\w*c+u+n+t\w*",
    r"crack[-_ ]?head\w*",
    r"crooks?",
    r"defraud",
    r"\w*dick\w*",
    r"\w*d+i+l+d+o+\w*",
    r"\w*dishonest\w*",
    r"dot[-_ ]?head\w*",
    r"\w*dyk(e|ing)\w*",
    r"(f|ph)a+g+(ot)?\w*",
    r"\w*fart\w*",
    r"fraud",
    r"\w*f+u+c*k+\w*",
    r"\w*gh?[ea]+y+\w*",
    r"g[yi]p+(o|y|ie?)?", r"gyppie",
    r"goo+k",
    r"gringo",
    r"he+rpe+s",
    r"hill-?billy",
    r"hom(a|o|er)(sexual)?\w*",
    r"\w*hooker\w*",
    r"\w*injun\w*",
    r"j+a+p+o?",
    r"k[iy]+ke",
    r"kwash(i|ee)",
    r"\w*l+e+s+b+i+a+n+\w*",
    r"liar",
    r"lick(er)?s?",
    r"meth",
    r"meth[-_ ]?head\w*",
    r"naz+i",
    r"nig", r"\w*n+i+gg+[aeious]+\w*", r"niglet", r"nigor", r"nigr", r"nigra",
    r"nonc(e|ing)\w*",
    r"overdose[sd]",
    r"peckerwood\w*",
    r"p(a?e|æ)do((f|ph)[iy]le)?s?",
    r"\w*peni(s)?\w*",
    r"piss\w*",
    r"\w*prostitute\w*",
    r"pot[-_ ]?head\w*",
    r"q(w|u)ash(i|ee)",
    r"rag[-_ ]?head",
    r"red[-_ ]?(neck|skin)",
    r"round[-_ ]?eye",
    r"satan(ic|ism|ist)s?",
    r"scabies",
    r"\w*s+h+[ia]+t+\w*",
    r"s+l+u+t+\w*",
    r"spi(g|c|k)+",
    r"spigotty",
    r"spik",
    r"spook",
    r"squarehead",
    r"subnormal",
    r"su+c*k+(er|iest|a)",
    r"syphil+is",
    r"terror(ist|ism|i[zs](e|ing|ed))s?",
    r"thei[fv](e?s)?",
    r"tran(ny|sexual)",
    r"\w*t+w+a+t+\w*",
    r"ti+t+((s|ies|y)[\w]*)?",
    r"v+a+g+(i+n+a+)?", r"vajaja\w*",
    r"wank\w*", r"wetback\w*", r"\w*w+h+o+r+(e+|ing)\w*", r"w+o+g+", r"w+o+p+",
    r"yank(e+)?", r"yid",
    r"zipperhead"
]
informals = [
    r"ain'?t", "a+we?some?(r|st)?",
    r"(b+l+a+h*)+",
    r"b+o+n+e+r+",
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
    r"d+u+d+e+\w*",
    r"good[-_]?bye",
    r"h+[aiou]+(h+[aeiou]*)*", r"h+[e]+(h+[aeiou]*)+",
    r"hel+o+", r"h(aa+|e+)y+",
    r"h+m+",
    r"i", r"i+d+i+o+t+",
    r"(l+[uo]+l+)([uo]+l+)*",
    r"l[ou]+ve?",
    r"m+e+o+w+",
    r"munch\w*",
    r"mom+(y|a)?",
    r"moron",
    r"no+pe",
    r"o+k+(a+y+)?",
    r"\w*o+m+g+\w*",
    r"poo+p\w*",
    r"\w*retard\w*", r"tard",
    r"shove",
    r"smelly",
    r"soo+",
    r"stinky",
    r"\w*s+t+[uo]+p+i+d+\w*",
    r"suck(s|ing|er)?", r"sux",
    r"shouldn'?t",
    r"test +edit", r"t+u+r+d+s?\w*",
    r"wasn'?t",
    r"w+[oua]+t+", r"\w*wtf\w*", r"wh?[ua]+t?[sz]+[ua]+p",
    r"wu+z+",
    r"won'?t",
    r"w+o+o+f+",
    r"ya'?ll", r"y+a+y+", r"y+e+a+h?", r"you('?(ve|re|ll))?",
    r"y+o+l+o+"
]


sys.modules[__name__] = SpaceDelimited(
    __name__,
    doc="""
english
=======

revision
--------
.. autoattribute:: revision.words
.. autoattribute:: revision.content_words
.. autoattribute:: revision.badwords
.. autoattribute:: revision.misspellings
.. autoattribute:: revision.informals
.. autoattribute:: revision.infonoise

parent_revision
---------------
.. autoattribute:: parent_revision.words
.. autoattribute:: parent_revision.content_words
.. autoattribute:: parent_revision.badwords
.. autoattribute:: parent_revision.misspellings
.. autoattribute:: parent_revision.informals
.. autoattribute:: parent_revision.infonoise

diff
----
.. autoattribute:: diff.words_added
.. autoattribute:: diff.words_removed
.. autoattribute:: diff.badwords_added
.. autoattribute:: diff.badwords_removed
.. autoattribute:: diff.misspellings_added
.. autoattribute:: diff.misspellings_removed
.. autoattribute:: diff.informals_added
.. autoattribute:: diff.informals_removed
    """,
    badwords=badwords,
    dictionary=dictionary,
    informals=informals,
    stemmer=stemmer,
    stopwords=stopwords
)
