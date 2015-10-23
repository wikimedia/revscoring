import sys

from .space_delimited import SpaceDelimited

try:
    from nltk.stem.snowball import SnowballStemmer
    stemmer = SnowballStemmer("german")
except ValueError:
    raise ImportError("Could not load stemmer for {0}. ".format(__name__))

try:
    from nltk.corpus import stopwords as nltk_stopwords
    stopwords = set(nltk_stopwords.words('german') + ["a"])
except LookupError:
    raise ImportError("Could not load stopwords for {0}. ".format(__name__) +
                      "You may need to install the nltk 'stopwords' " +
                      "corpora.  See http://www.nltk.org/data.html")

try:
    import enchant
    dictionary = enchant.Dict("de")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'de'.  " +
                      "Consider installing 'myspell-de'.")

badwords = [
    r"arsch", r"arschfick", r"arschficken", r"arschgesicht", r"arschloch", r"arschlöcher", r"assi",
    r"bescheuert", r"bitch", r"bitches", r"deppen", r"dumm", r"fettsack", r"ficker", r"fotze", r"fotzen",
    r"fucker", r"fucking", r"gaylord", r"gefickte", r"homofürst", r"hure", r"huren", r"hurensohn",
    r"hurensöhne", r"hurre", r"hurrensohn", r"idiot", r"idioten", r"kacka", r"kacke", r"kackwurst",
    r"kanacken", r"lutscher", r"missgeburt", r"mistgeburt", r"motherfucker", r"muschis", r"nigga",
    r"nigger", r"noobs", r"nutte", r"peniskopf", r"penisse", r"pennis", r"pisser", r"sau", r"scheise",
    r"scheiss", r"scheisse", r"scheiß", r"scheiße", r"scheißen", r"schlampe", r"schwanzlutscher", r"schwuchtel",
    r"schwuchteln", r"schwul", r"schwuler", r"schwull", r"schwänze", r"spasst", r"spast", r"spasten",
    r"verarscht", r"verfickte", r"vollidiot", r"wichser", r"wixer", r"wixxe", r"wixxen", r"wixxer"
]
informals = [
    r"anal", r"auserdem", r"autorenportal", r"bins", r"bla", r"blabla", r"blablabla", r"blub", r"blubb",
    r"blöd", r"blöder", r"bodewell", r"bumsen", r"cool", r"coole", r"cooler", r"coolste", r"coool", r"deine",
    r"digga", r"dildo", r"dildos", r"doof", r"dumme", r"dummen", r"dummer", r"dummes", r"dummm", r"döner",
    r"euch", r"fetter", r"fick", r"ficke", r"ficken", r"fickt", r"fickte", r"fickten", r"fresse", r"fuck",
    r"furtz", r"furz", r"furzen", r"fürn", r"fürze", r"gay", r"gefickt", r"gehts", r"geil", r"geile", r"geilen",
    r"geiler", r"geilste", r"geilsten", r"gez", r"grüße", r"hab", r"haha", r"hahah", r"hahaha", r"hahahah",
    r"hahahaha", r"hahahahaha", r"hahahahahaha", r"hahahahahahaha", r"halllo", r"hallo", r"halts", r"hehe",
    r"hey", r"hihi", r"hihihi", r"homos", r"huhu", r"hässlich", r"jaja", r"jannik", r"juhu", r"kack", r"kacken",
    r"kackt", r"kaka", r"kake", r"kaken", r"klo", r"kneipenschlägerein", r"kotze", r"kotzen", r"kursiver",
    r"könnt", r"labert", r"lalala", r"lalalala", r"langhaardackel", r"langweilig", r"leck", r"lecker", r"leckt",
    r"lol", r"lonni", r"looser", r"lutschen", r"lutscht", r"mama", r"mfg", r"minecraft", r"moin", r"mudda",
    r"mudder", r"muhaha", r"muhahaha", r"mumu", r"muschi", r"muschie", r"möse", r"naja", r"nich", r"nix",
    r"noob", r"nutten", r"oma", r"omg", r"opfa", r"penis", r"penise", r"penisen", r"penises", r"penner",
    r"pimmel", r"pipi", r"pisse", r"popel", r"popo", r"porno", r"pornos", r"puff", r"puffs", r"pups", r"pupsen",
    r"rofl", r"schei", r"scheis", r"schlampen", r"schniedel", r"schwachsinn", r"schwule", r"seid", r"sex", r"sexy",
    r"shit", r"soo", r"sooo", r"soooo", r"sooooo", r"spasti", r"spezial", r"stingt", r"stink", r"stinke", r"stinken",
    r"stinker", r"stinkst", r"stinkt", r"sucks", r"swag", r"titte", r"titten", r"tobi", r"toll", r"unformatierten",
    r"vaginas", r"wisst", r"xdd", r"xddd", r"xdddd", r"xnxx", r"yeah", r"yolo", r"youporn", r"ärsche"
]
sys.modules[__name__] = SpaceDelimited(
    __name__,
    doc="""
german
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
