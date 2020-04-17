from .features import Dictionary, RegexMatches, Stemmed, Stopwords
from .features.dictionary import MultiDictChecker, load_dict, utf16_cleanup

name = "portuguese"


multi_dict = MultiDictChecker(
    load_dict('pt_PT', 'myspell-pt-pt'),
    load_dict('pt_BR', 'myspell-pt-br'))


def safe_dictionary_check(word):
    return multi_dict.check(utf16_cleanup(word))


dictionary = Dictionary(name + ".dictionary", safe_dictionary_check)
"""
:class:`~revscoring.languages.features.Dictionary` features via
`enchant.Dict <https://github.com/rfk/pyenchant>`_ "pt". Provided by
`myspell-pt-pt` and `myspell-pt-br`.
"""

try:
    from nltk.corpus import stopwords as nltk_stopwords
    stopwords = set(nltk_stopwords.words('portuguese'))
except LookupError:
    raise ImportError("Could not load stopwords for {0}. ".format(__name__) +
                      "You may need to install the nltk 'stopwords' " +
                      "corpora.  See http://www.nltk.org/data.html")

stopwords = Stopwords(name + ".stopwords", stopwords)
"""
:class:`~revscoring.languages.features.Stopwords` features provided by
`nltk.corpus.stopwords <https://www.nltk.org/api/nltk.corpus.html>`_ "portuguese"
"""

try:
    from nltk.stem.snowball import SnowballStemmer
    stemmer = SnowballStemmer("portuguese")
except ValueError:
    raise ImportError("Could not load stemmer for {0}. ".format(__name__))

stemmed = Stemmed(name + ".stemmed", stemmer.stem)
"""
:class:`~revscoring.languages.features.Stemmed` word features via
:class:`nltk.stem.snowball.SnowballStemmer` "portuguese"
"""

badword_regexes = [
    r"baba[ckq](as?|ão|ões|u?i[cçs]s?e)",  # douchebag
    r"bi(ch|x)as?",  # gay man
    r"boio(l[ai](tico)?|l[aã]o|lo(go|[gj]i[sx]ta))s?",  # gay man
    r"bo(qu|k)etes?",  # blowjob
    r"bo[sx]t(ao?s?|alhao?)",  # shit
    r"b[uo]s?[cçs]s?et+(a[os]?|inha)?",  # pussy (vagina)
    r"bu[mn]d((inh)?as?|[ãa]o)",  # ass
    r"b[uo]rr[oaei](ce|[ius])?",  # donkey/jackass
    r"[ck]a[csç]s?ete?s?",  # bludgeon
    # shit
    r"[ck]ag(a(r|n?do|dao?|n?ei(r[ao])?|(lh)?a?o|nitas?|dela|lhoto)?|ou)",
    r"[ck]ara(l?hl?([ou]?s?|ao|inh[ou]s?)|i([ou]s?)?)",  # fuck
    r"(ch|x)at[ao]s?",  # boring
    r"(ch|x)up[aeiou]([dv]a|te|nha|ndo|r|u)?",  # blow me
    r"[ck]o[ck]ô",  # poo
    r"[ck]om(er?|i)",  # fucked
    r"[ck]onas?",  # cunt
    r"[ck]uz([aã]o|inho)",  # asshole
    r"doid(inh)?[ao]s?",  # crazy
    r"fed?(id?[ao]|e|orent[ao])s?",  # stinks/stinky
    r"fei[ao]s?",  # ugly
    r"fendi",  # ???
    r"f[ou]d(a[os]?|e[ru]?|idos?)",  # fuck
    r"go[sx]tos([ao]s?|ão|ões|onas?)",  # hot
    r"idiot(a|i[cçs]s?e)s?",  # idiot
    r"lo(k[oa]s?|u[ck]([oa]s?|ura|a(mente)?))",  # crazy
    r"maconheir[ao]s?",  # bothead
    r"m[áa]fia",  # mafia
    r"maldizentes",  # slanderers
    r"mecos",  # cum ???
    r"mentir(a|os[oa])s?",  # lie/liar
    r"merd(a|[ãa]o|oso|ica)s?",  # shit
    r"noob",  # noob
    r"ot[áa]ri[oa]s?",  # sucker
    r"pari[ou]",  # part of "puta que o pariu"
    r"pategos",  # hick / yokel
    r"pau",  # dick
    r"peid([ao]|[ãa]o|ei|ar(ia)?|ando|aç[oa])s?",  # fart
    r"p[êe]nis+",  # penis
    r"pilas?",  # dick
    r"piroca",  # dick
    r"porcaria", r"porn[ôo]?",  # filth/porn
    r"po(rr|h)a",  # cum
    r"pum",  # fart
    r"punhet(a|eir[oa])s?",  # jack off / masturbate
    r"put([ao]|[ao]na|aria|eiro|inha)s?",  # bitch/hooker
    r"safad([ao]|ona)s?",  # shameless
    r"te[sz]ão", r"te[sz]ud[oa]s?",  # turn-on / horny
    r"tran[sz]([aá](r(am)?|n?do)?|ou)",  # sex
    r"tretas?",  # bullshit
    r"trou?(ch|x)as?",
    r"vadi([ao]s?|agem)",  # bitch
    r"viad(agem?|[aã]?o|inh[ou])s?",  # gay person ("fucker")
    r"xixi"  # pee
]

badwords = RegexMatches(name + ".badwords", badword_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
    r"adoro",  # love
    r"aki",  # here
    r"amo",  # master
    r"(?:b+?l+?a+?h*)+",  # bla, blah, bbblllaaaahhhhhblah
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
    r"k+?",  # k, kkkkkkkkkkkkkkk
    r"lindo",  # pretty
    r"l+[uo][uol]*l",   # lol, LOLOLOL, LLLLoOOoLLL
    r"mae",  # mom
    r"mto",  # very
    r"naum",  # no (slang)
    r"n[óo]is",  # it's us (slang)
    r"odeio",  # hate
    r"oi+",  # hi
    r"ol[aá]",  # hello
    r"ratas?",  # "rat" -- a snitch
    r"(?:rs)+",  # lol
    r"tava",  # was / were (slang)
    r"tbm",  # also (slang)
    r"vao",  # vain
    r"vcs", r"voce", r"voces",  # you
    r"xau"  # bye
]

informals = RegexMatches(name + ".informals", informal_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""

words_to_watch_regexes = [
    # Puffery
    r'lendári[ao]s?', r'grandes?', r'eminentes?', r'visionári[ao]s?',
    r'notáve(?:l|is)', r'líder(?:es)?', r'célebres?', r'de última linha',
    r'extraordinári[ao]s?', r'brilhantes?', r'famos[ao]s?', r'renomad[ao]s?',
    r'prestigios[ao]s?', r'de nível mundial', r'respeitad[ao]s?',
    r'excepciona(?:l|is)', r'excelentes?', r'virtuos[ao]s?',
    r'de grande estima',
    # Contentious labels (-gate removed)
    r'cult[ao]s?', r'racistas?', r'pervers[ao]s?', r'seitas?',
    r'fundamentalistas?', r'hereges?', r'extremistas?', r'negacionistas?',
    r'terroristas?', r'libertador(?:as?|es)?', r'neo[- ]?nazis(?:ta|mo)?',
    r'pseudo-?(ciência|científic[oa]s?|intelectua(?:l|is))',
    r'controvers[ao]s?',
    # Unsupported attributions
    r'algu(?:n|ma)s dizem', r'acredita-se', r'muit[ao]s têm a opinião',
    r'a maioria sente', r'especialistas afirmam', r'frequentemente se relata',
    r'é a opinião corrente', r'estudos mostram', r'a ciência diz',
    r'provou-se que',
    # Expressions of doubt
    r'supost[ao]s?', r'alegad[ao]s?', r'pretens[ao]s?', r'acusad[ao]s?',
    r'chamad[ao]s?',
    # Editorializing
    r'notavelmente', r'interessantemente', r'deve-se ter em mente',
    r'claramente', r'certamente', r'sem dúvida', r'é claro', r'afortunadamente',
    r'(?:in)?felizmente', r'tragicamente', r'precocemente',
    # Synonyms for "said"
    r'revel(?:ou|aram)', r'indic(?:ou|aram)', r'expôs', r'explic(?:ou|aram)',
    r'encontr(?:ou|aram)', r'not(?:ou|aram)', r'observ(?:ou|aram)',
    r'insist(?:iu|iram)', r'especul(?:ou|aram)', r'conjetur(?:ou|aram)',
    r'aleg(?:ou|aram)', r'afirm(?:ou|aram)', r'admit(?:iu|iram)',
    r'confess(?:ou|aram)', r'neg(?:ou|aram)',
    # Lack of precision
    r'falec(?:eu|eram)', r'fo(?:i|ram) desta para a melhor', r'deu sua vida',
    r'deram suas vidas', r'local de descanso', r'fazer amor', r'uma questão com',
    r'danos colaterais', r'limpeza étnica', r'convivendo com o câncer',
    r'sem visão', r'pessoas com cegueira',
]

words_to_watch = RegexMatches(name + ".words_to_watch", words_to_watch_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
problematic words and phrases for use in reference text
"""
