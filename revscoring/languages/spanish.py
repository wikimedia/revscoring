from .features import Dictionary, RegexMatches, Stemmed, Stopwords

name = "spanish"

try:
    import enchant
    dictionary = enchant.Dict("es")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'es'.  " +
                      "Consider installing 'myspell-es'.")

dictionary = Dictionary(name + ".dictionary", dictionary.check)
"""
:class:`~revscoring.languages.features.Dictionary` features via
`enchant.Dict <https://github.com/rfk/pyenchant>`_ "es".  Provided by `myspell-es`
"""

try:
    from nltk.corpus import stopwords as nltk_stopwords
    stopwords = set(nltk_stopwords.words('spanish'))
except LookupError:
    raise ImportError("Could not load stopwords for {0}. ".format(__name__) +
                      "You may need to install the nltk 'stopwords' " +
                      "corpora.  See http://www.nltk.org/data.html")

stopwords = Stopwords(name + ".stopwords", stopwords)
"""
:class:`~revscoring.languages.features.Stopwords` features provided by
`nltk.corpus.stopwords <https://www.nltk.org/api/nltk.corpus.html>`_ "spanish"
"""

try:
    from nltk.stem.snowball import SnowballStemmer
    stemmer = SnowballStemmer("spanish")
except ValueError:
    raise ImportError("Could not load stemmer for {0}. ".format(__name__))

stemmed = Stemmed(name + ".stemmed", stemmer.stem)
"""
:class:`~revscoring.languages.features.Stemmed` word features via
:class:`nltk.stem.snowball.SnowballStemmer` "spanish"
"""

badword_regexes = [
    r"awe(onao|vo)",  # idiot
    r"babosa",  # slug
    r"bastardo",  # bastard
    r"bollo",  # drunk (to the extreme)
    r"boludo",  # asshole
    r"bugarr[óo]n",  # gay/bi man
    r"buseta",  # ???
    r"caca", r"cag(a|o|ar(ro)?)(n(es)?)?\w*",  # shit / shits / dirty
    r"caquita",  # shit
    r"cabr[óo]n(es)?",  # bastards
    r"cagad[ao]",  # funny / absurd
    r"capullo",  # end of a penis
    r"carajo", r"chinga(r|da)?", r"chingu?en",  # fuck
    r"chichornia",  # ???
    r"chiguero",  # ???
    r"chima(r|da|s)?",  # fuck
    r"chingad(o|azo|erita)s?",  # fuck
    r"chingo(n[cs]i[cs]imo|ner[íi]a|nes|rrón)s?",  # fuck
    r"chino(n[cs]i[cs]imo)?",  # chinese
    r"chosto",  # ???
    r"choch[oa]",  # cunt
    r"cholo",  # mixed race person
    r"chucha",  # fuck
    r"chupa(n|r|mea?|mel[ao]|medias|pollas|ban?)?s?\w*",
    r"chupen(la|me|mela)", r"chupo",  # variants of suck / blow me
    r"cipote",  # child (slang)
    r"cochetumadre",  # car of your mother ???
    r"co[gj]er",  # have sex / fuck
    r"cojio",  # wedgie
    r"cojones?",  # balls
    r"comeme",  # "eat me"
    r"comian",  # ???
    r"conch(a|etumadre)",  # vagina (of your mother)
    r"conejo",  # rabbit ???
    r"consolador",  # dildo
    r"co[ñn]o",  # dammit
    r"cupan",  # Misspelling of "chupan" ???
    r"cuca",  # vagina
    r"cule(ar|ros?)",  # fuck
    r"cul(o|ito|iaos?)",  # ass
    r"cundango",  # gay / homosexual
    r"desmadr([ae]r?|ado|arse)?",  # chaotic ???
    r"dlaversh",  # ???
    r"droga(ta)?s?",  # drugs
    r"emput(e|ar|ado)s?",  # pissed off
    r"enc", r"encabron(ar|ado|adas|arse)s?",  # pissed off
    r"encronada",  # ???
    r"enputado",  # bitch / complain
    r"fach(a|ero|era)",  # superficial appearance
    r"foll(o|ar|aban?)?",  # fuck
    r"fornicar",  # sex
    r"freg[oó]n",  # wet blanket -- no fun ???
    r"furcia",  # whore
    r"gabacho",  # frenchy (disrespectful)
    r"gamberro",  # thug
    r"gilipoll[ao]s?",  # asshole
    r"gitan[ao]s?",  # gypsy
    r"gord[ao]s?",  # fat
    r"gringo",  # US national (historically derogatory)
    r"guev(o|on(es)?)",  # cock / idiot
    r"g[uü]ey",  # bitch ???
    r"guiri",  # foreigner / tourist (derogatory)
    r"güila",  # ???
    r"golfa",  # slut
    r"huevos",  # balls
    r"huev[óo]n(es)?", r"huevospateados?",  # lazy ass
    r"hifueputa",  # ???
    r"hijode?putas?", r"hijoduta",  # motherfucker
    r"hijueputas?",  # son of a bitch
    r"holocuento",  # the Hollocaust
    r"idiotas?", r"jidiotas?",  # idiot
    r"imb[ée][cs]il(es)?",  # imbecile
    r"japo",  # japanese (derogatory)
    r"jetear",  # sleep (slang)
    r"jili(puerta|polla)s?",  # cock sucker ???
    r"joder",  # fuck
    r"jot(a|o|eria)s?",  # faggot
    r"jod(er|ido)",  # fucked
    r"komekaka",  # misspelling of 'come caca' -- "eat shit"
    r"lesbiana",  # lesbian
    r"lamadre",  # 'your mother' explitive
    r"mach(orra|etorra)",  # lesbian (offensive)
    r"madrea(do|r)",  # to beat someone up
    r"maldito",  # dammit
    r"malparid[oa]s?",  # miscarried
    r"mama(da|guevo)s?",  # blowjob
    r"mam[óo]+n(es)?",  # insolent little douchebag
    r"manola",  # the (female) hand one masturbates with
    r"mari[ck](a|[óo]ne?)s?",  # gay man
    r"marimach[ao]",  # tomboy
    r"maripos[óo]n",  # fag
    r"marrano",  # pig
    r"meachupan", r"meapelan",  # suck my cock
    r"me[- ]?castra[- ]?la[- ]?madre",  # 'I <something> your mother' ???
    r"me[- ]?la[- ]?pelan?s?",  # I don't give a f***
    r"mi?er[dg]a+s?\w*",  # shit
    r"mimsn",  # ???
    r"ming[ao]",  # ugly person
    r"mocos",  # boogers / mucus
    r"mojon",  # shit
    r"monda",  # man part / penis
    r"mongolo",  # idiot (slang)
    r"moro",  # moor / muslim (derogatory)
    r"nacio",  # ???
    r"nazi",  # nazi
    r"negrat[oa]",  # nigger
    r"n[oe]m[ea]mes",  # ???
    r"ojetes?", "ogts?",  # asshole / stingy
    r"paj(a|aro|ero)s?",  # wank / wanker
    r"paki",  # ???
    r"pamearlo",  # ???
    r"pario",  # ???
    r"pattaya",  # ???
    r"pedos?",  # pedofile
    r"pel(ado|an)",  # boy (derogatory)
    r"pelot(a|udo)s?",  # balls
    r"pendej(o|a|ada)s?",  # stupid people
    r"penes?",  # penis
    r"peos?",  # fart
    r"perras?",  # bitch
    r"petard[oa]s?",  # slow / retarded
    r"pich(a|ula)",  # cock
    r"pijas?",  # cock
    r"piko",  # cock
    r"pinches?",  # kitchen boy / insignificant
    r"pinga",  # dick
    r"pipi",  # small penis
    r"pirobos",  # fag
    r"pit(o|ito|ote)s?",  # penis
    r"pollas?",  # cock
    r"poronga",  # cock
    r"polvo",  # sexual intercourse
    r"poto",  # ass
    r"prostituta",  # prostitute
    r"put([ao]+|isim[oa]|iza)(s|n)?\w*",  # bitch/whore
    r"puñal",  # fag ???
    r"rabo",  # ass
    r"ramera",  # easy woman
    r"sida",  # AIDS
    r"sorete",  # piece of shit
    r"sudaca",  # greaser
    r"subnormal",  # retarded
    r"s[íi]filis",  # syphilis
    r"tajodido",  # ???
    r"tetas?",  # tits
    r"tont[ao]s?",  # fool / low intelligence
    r"torta",  # fat woman
    r"tortillera",  # lesbian
    r"tranca",  # bar ???
    r"travesti",  # transvestite
    r"travolo",  # transgender
    r"trol(o|a)",  # faggot
    r"uta", r"utama", r"utamadre",  # short for 'puta'
    r"verg(a|uero|ud[ao])s?\w*", r"versh",  # cock
    r"vibrador",  # vibrator
    r"viol(o|a|e|ar)",  # rape
    r"vulva",  # vulva
    r"watdafuq",  # "what the fuck"
    r"wea",  # shit
    r"webon(ada|e)?s?",  # Chileans (derogatory)
    r"zapatona",  # shoe ???
    r"zorr(a|ear)"  # bitch
]

badwords = RegexMatches(name + ".badwords", badword_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
    r"agan",  # ???
    r"agregenme",  # ???
    r"aguante",  # stamina
    r"aki",  # ???
    r"amaona",  # ???
    r"amigui",  # best (girl) friend
    r"amo+",  # love
    r"apesta",  # stinks
    r"asco",  # disgust
    r"asi",  # so
    r"atte?",  # short for atentamente
    r"(?:b+l+a+h*)+",
    r"bobada",  # ???
    r"bobos?",  # stupid / simple / fool
    r"bubis",  # ???
    r"chafa",  # low quality
    r"chale",  # no way!
    r"chido",  # cool
    r"chí",  # ???
    r"chil[ei]ar",  # ???
    r"comi[ao]",  # ???
    r"copien",  # copy
    r"cursiva",  # italics
    r"esq",  # abbrev. of 'esquina' meaning "corner" -- used in addresses
    r"est[uú]pid[aeo]+[rs]?",  # stupid
    r"fulan[ao]",  # pronoun for person
    r"fe[ao]s?",  # ugly
    r"gra(x|sias)",  # thank you
    r"guapo",  # beautiful
    r"h?o+la+",  # hello
    r"ho+lis?",  # ???
    r"ijos",  # ???
    r"inserta",  # inserts
    r"j+[eaiou]+(j[aeiou]*)*",  # jaja jeje jojojo
    r"ke",  # short for 'que'
    r"kie(n|ro)",  # I want
    r"komo",  # ???
    r"lean",  # ???
    r"lees",  # ???
    r"lo[ck]os?",  # crazy
    r"l+[uo][uol]*l",  # lol lollloololol lulllololul
    r"madrazo",  # a crash (slang)
    r"malparida",  # miscaried
    r"mcfinnigan",  # ???
    r"mensos?",  # stupid / annoying person
    r"meti[oa]",  # ???
    r"metroflog",  # ???
    r"migu?is",  # ???
    r"muxo",  # ???
    r"negrit[ao]",  # black person (non-offensive)
    r"nocheto",  # ???
    r"noo+",  # noooo
    r"nop",  # nope
    r"ojala",  # hopefully
    r"o+l[ia]",
    r"osea",  # "that is"
    r"pollid",  # ???
    r"popo",  # ???
    r"pipi",  # small penis
    r"plis",  # ???
    r"por[- ]?favor",  # please
    r"por[- ]?[kq]ue?", r"porke", r"porqe?",  # why!?
    r"porquer[ií]as?",  # low quality
    r"profe",  # slang for teacher
    r"pupu",  # ???
    r"qiero",  # ???
    r"salud(o?s)?",  # cheers!
    r"sierto",  # ???
    r"shí",  # ???
    r"sii+",  # "yessss"
    r"soi",  # I am
    r"sophonpanich",  # ???
    r"ta?mbn", r"tkm",  # also (slang)
    r"tanga",  # thong
    r"te[- ]?quiero[- ]?mucho", r"tqm",  # I care for you a lot
    r"umaxnet",  # ???
    r"vallanse",  # move out
    r"vayanse",  # go away
    r"wen[ao]",  # Hello
    r"weon(es)?",  # dude / thing
    r"wey",  # buddy
    r"xd+",  # XD (smiley face squiting)
    r"xfarm",  # ???
    r"yolo",  # You Only Live Once
    r"zorpia"  # ???
]

informals = RegexMatches(name + ".informals", informal_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
