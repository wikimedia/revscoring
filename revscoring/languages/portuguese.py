import sys

from .space_delimited import SpaceDelimited

try:
    import enchant
    dictionary = enchant.Dict("pt")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'pt'.  " +
                      "Consider installing 'myspell-pt'.")

try:
    from nltk.stem.snowball import SnowballStemmer
    stemmer = SnowballStemmer("portuguese")
except ValueError:
    raise ImportError("Could not load stemmer for {0}. ".format(__name__))

try:
    from nltk.corpus import stopwords as nltk_stopwords
    stopwords = set(nltk_stopwords.words('portuguese'))
except LookupError:
    raise ImportError("Could not load stopwords for {0}. ".format(__name__) +
                      "You may need to install the nltk 'stopwords' " +
                      "corpora.  See http://www.nltk.org/data.html")


badwords = [
    r"babaca",  # douchebag
    r"bixa",  # ???
    r"boiola", r"boiolas",  # gay man
    r"boquete",  # blowjob
    r"bosta",  # shit
    r"bucet(a|inha)s?",  # pussy (vagina)
    r"bund(a|inha)s?",  # ass
    r"burr[ao]s?",  # donkey/jackass
    r"cacete",  # bludgeon
    r"cag([ao]|ad[ao]|and[ao]|aneir[ao]|ar|ou)s?",  # shit
    r"cara(i|io|lho)s?",  # fuck
    r"chat[ao]",  # boring
    r"(ch|x)up[ao](r|va|u)?s?",  # blow me
    r"cocô",  # poo
    r"comi",  # eat ???
    r"cona(ssa)?s?",  # cunt
    r"cuz([aã]o|inho)",  # asshole
    r"doido",  # crazy
    r"fed(e|ido)",  # stinks/stinky
    r"feia",  # ugly
    r"fendi",  # ???
    r"foda[sr]?", r"fude[sr]?",  # fuck
    r"gostos[aã][os]?", r"gostoso",  # yummy ???
    r"idiotas?",  # idiot
    r"loka", r"loko",  # crazy
    r"maconheiro",  # bothead
    r"mafia",  # mafia
    r"maldizentes",  # slanderers
    r"mecos",  # cum ???
    r"mentir(a|os[oa])s?",  # lie/liar
    r"merdas?",  # shit
    r"noob",  # noob
    r"ot[áa]rios?",  # sucker
    r"pariu",  # to give birth ???
    r"pategos",  # hick / yokel
    r"peid(a|ar|o|ei)s?",  # fart
    r"pênis",  # penis
    r"pilas?",  # dick
    r"piroca",  # dick
    r"poha",  # ???
    r"porcaria", r"porno",  # filth/porn
    r"porra",  # cum
    r"pum",  # fart
    r"punhet(a|eiro)",  # jack off / masturbate
    r"put(o|a|aria|eiro|inha)s?",  # bitch/hooker
    r"safado",  # shameless
    r"tesão",  # turn-on / horny
    r"tran[sz]ar",  # sex
    r"tr(eta|oxa)",  # bullshit
    r"vadia",  # bitch
    r"viad(agem|ão|inho|o)s?",  # gay person ("fucker")
    r"xixi"  # pee
]

informals = [
    r"adoro",  # love
    r"aki",  # ???
    r"amo",  # master
    r"(b+l+a+h*)+",  # bla, blah, bbblllaaaahhhhhblah
    r"carambas?",  # OMG
    r"coco",  # coconut
    r"copie[im]",  # I copied
    r"delicia",  # delicious
    r"editei",  # edited
    r"enfiar?",  # to stick (up one's ass)
    r"entao",  # then
    r"estrag(ar|uem)",  # spoiled / ruined
    r"fixe",  # cool
    r"gajo",  # dude
    r"h[aiou](h[aeiou])*", r"h[e](h[aeiou])+",  # hi, ha, hehe, hohoho
    r"k+",  # k, kkkkkkkkkkkkkkk
    r"lindo",  # pretty
    r"l+([uo]+l+)+",  # lol, LOLOLOL, LLLLoOOoLLL
    r"mae",  # mom
    r"mto",  # very
    r"naum",  # no (slang)
    r"n[óo]is",  # it's us (slang)
    r"odeio",  # hate
    r"oi+",  # hi
    r"ol[aá]",  # hello
    r"ratas?",  # "rat" -- a snitch
    r"(rs)+",  # lol
    r"tava",  # was / were (slang)
    r"tbm",  # also (slang)
    r"vao",  # vain
    r"vcs", r"voce", r"voces",  # you
    r"xau"  # bye
]


sys.modules[__name__] = SpaceDelimited(
    __name__,
    doc="""
portuguese
==========

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
    informals=informals,
    dictionary=dictionary,
    stemmer=stemmer,
    stopwords=stopwords
)
"""
portuguese
"""
