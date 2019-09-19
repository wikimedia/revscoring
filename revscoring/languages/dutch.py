from .features import Dictionary, RegexMatches, Stemmed, Stopwords

name = "dutch"

try:
    import enchant
    dictionary = enchant.Dict("nl")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'nl'.  " +
                      "Consider installing 'myspell-nl'.")

dictionary = Dictionary(name + ".dictionary", dictionary.check)
"""
:class:`~revscoring.languages.features.Dictionary` features via
`enchant.Dict <https://github.com/rfk/pyenchant>`_ "nl".  Provided by `myspell-nl`
"""

try:
    from nltk.corpus import stopwords as nltk_stopwords
    stopwords = set(nltk_stopwords.words('dutch'))
except LookupError:
    raise ImportError("Could not load stopwords for {0}. ".format(__name__) +
                      "You may need to install the nltk 'stopwords' " +
                      "corpora.  See http://www.nltk.org/data.html")

stopwords = Stopwords(name + ".stopwords", stopwords)
"""
:class:`~revscoring.languages.features.Stopwords` features provided by
`nltk.corpus.stopwords <https://www.nltk.org/api/nltk.corpus.html>`_ "dutch"
"""

try:
    from nltk.stem.snowball import SnowballStemmer
    stemmer = SnowballStemmer("dutch")
except ValueError:
    raise ImportError("Could not load stemmer for {0}. ".format(__name__))

stemmed = Stemmed(name + ".stemmed", stemmer.stem)
"""
:class:`~revscoring.languages.features.Stemmed` word features via
:class:`nltk.stem.snowball.SnowballStemmer` "dutch"
"""

badword_regexes = [
    # Curses
    "aars",  # ass
    "anaal", "anus",  # anal, anus
    "balhaar",  # ball hair (testicular hair)
    "debiel",  # infirm
    "diaree", "diarree",  # diarrhea
    "drol", "drollen",  # turd
    "fack", "facking", "focking",  # misspelling of "fuck"
    "flikker", "flikkers",  # perjorative for gay person ("faggot")
    "geil", "geile",  # horny
    "gelul",  # bullshit
    "hoer", "hoere", "hoeren",  # whore
    "homo", "homos", "homo's",  # perjorative for gay person
    "kak", "kaka",  # poop
    "kakhoofd", "kakken",  # kakhoofd = poopy head; kakken = to poop (verb)
    "kanker", "kenker",  # cancer
    "klootzak", "klootzakken",  # "ball sack"
    "klote",  # lit.: balls; equivalent: "sucky"
    "kolere", "klere",  # Cholera
    "kont", "kontgat",  # butt, butthole
    "kontje",  # little butt
    "lekkerding", "lekker ding",  # means something like "hot piece"
    "likken",  # lick
    "pedo", "pedofiel",  # pedophile
    "penis", "penissen",  # penis, penises
    "peop", "poep",  # misspelling of poep (poop)
    "pijpen",  # to give a blowjob
    "pik",  # dick
    "pimel", "piemel", "piemels",  # colloquial for penis (Eng: dick)
    "pipi",  # somewhat archaic, somewhat childish word for penis
    "poep", "poepen", "poephoofd",  # poop / poopy head
    "poepie", "poepje", "poepjes", "poepsex",  # more poop words
    "poept", "poepte", "poepseks",  # more poop words
    "poepstamper", "poepstampen",  # perjorative for gay person
    "pokke", "pokken",  # Smallpx
    "porn", "porno",  # porn
    "neuk", "neuke", "neuken", "neukende", "neukt",  # "fuck" conjugations
    "neukte", "neukten", "geneukt",  # "fuck" conjugations continued
    "nicht", "nichten",  # "faggot" but also sometimes "cousin"
    "strond", "stront",  # shit
    "zuigt", "suckt",  # sucks
    "sukkel", "sukkels",  # sucker (idiot)
    "tering",  # colloquial word for tuberculosis, now a swear word;
    "tiet", "tetten", "tieten",  # tits
    "verekte", "verrekte",  # "damn" or "fucking" (adj)
    "verkracht", "verkrachten",  # rape/raped
    "dikzak",  # fat person
    "mogolen", "mogool", "mongool", "mongolen",  # perj. for down syndrome
    "mooiboy",  # man who puts a lot of effort into his appearance
    "sperma",  # sperm
    "kut", "kutje", "kutjes",  # vulgar word for vagina (Eng.: cunt)
    "stelletje",  # "bunch of", as part of a racial slur or perj.
    "lul",  # dick
    "lullen",  # talking out of one's ass
    "lulltje",  # weak person
    "reet",  # buttcrack, often used in an idiom that means "don't give a shit"
    "slet",  # slut
    "scheet", "scheten",  # fart
    "schijt",  # shit
    "tyfus",  # Typhoid
    "smeerlap",  # literally: "grease rag"
    "het zuigt",  # "It sucks"
    "sukkel",  # "Sucker"
    "sul",  # "wimp", "dork", or "schlemiel". Its etymology is unclear
    "vreten",  # rude form of the verb "to eat"
    "vuil", "vuile",  # "filth" or "filthy"
    "wijf", "kutwijf", "kankerhoer", "rothoer", "vishoer",  # perj for women

    # Racial slurs
    "bamivreter",  # "bami eater" an ethnic slur for Asian people
    "bosneger",  # literally: "bushnegro"
    "geitenneuker",  # literally: "goat fucker"
    "kakker",  # "crapper" -- higher social class idiot
    "koelie",  # "coolie" Indonesian laborer
    "lijp",  # slur for Jewish people and "slow", "dumb", "sluggish"
    "mocro",  # people of Moroccan descent
    "mof", "moffenhoer", "mofrica", "kraut",  # ethnic slur of German people
    "neger", "negers", "nikker",  # n-word
    "poepchinees",  # "poop Chinese"
    "roetmop",  # ethnic slur for black people.
    "spaghettivreter", "pastavreter",  # perj. for people of Italian descent
    "loempiavouwer",  # "spring roll folder" people of Vietnamese descent
    "spleetoog",  # "slit eye" term for people of Asian descent
    "tuig",  # "scum"
    "zandneger",  # "sand negro" an ethnic slur for Middle Eastern people

    # Religion
    "gadverdamme", "godverdomme", "gadver", "getverderrie",   # "god damn"
    "getver", "verdomme", "verdamme", "verdorie",  # "god damn" continued
    "godskolere",  # "god fury"
    "graftak",  # "grave branch" old, moody, and/or cranky person.
    "jezus christus", "tjezus", "jeetje", "jezus mina", "jezus",  # Jesus
    "jesses", "jasses", "harrejasses", "here jezus",  # Jesus continued
]

badwords = RegexMatches(name + ".badwords", badword_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
    r"aap(jes)?",
    r"banaan",
    r"bent",
    r"boe(it)?",
    r"doei"
    r"dombo",
    r"domme",
    r"eigelijk",
    r"fransoos",  # Fransoos is a lightly derogatory term for French people.
    r"godverdomme",
    r"groetjes",
    r"gwn",
    r"hoi",
    r"hal+o+",
    r"hangjongere",  # meaning "a youngster hanging around"
    r"heb",
    r"hee+[jyl]", r"heee+?l",
    r"houd?",
    r"(?:hoi+)+",
    r"hoor",
    r"indo",  # dutch-indonesian descent
    r"izan",
    r"jij",
    r"jou",
    r"jullie",
    r"kaas", r"kaaskop",  # "cheese head" a term for dutch people
    r"klopt",
    r"kots",
    r"kusjes",
    r"le?kke?re?",
    r"maarja",
    r"mama",
    r"medelander",  # Foreigner in Netherlands (only used ironically)
    r"nou",
    r"oma",
    r"ofzo",
    r"oke",
    r"pauper",  # Low social standing
    r"plebejer",  # low social standing
    r"pinda",  # "peanut" slur used against people of Indonesian descent.
    r"proleet",  # "proletarius" someone who is very rude and uncultured
    r"rapalje", r"rapaille",  # Low social class
    r"snap",
    r"stink(en|t)",
    r"stoer",
    r"swek",
    r"tatta",  # neutral term used by Antilleans and Surinamese people
    r"tokkie",  # lower-class, anti-social people
    r"vies", "vieze",
    r"vind",
    r"vuile",
    r"xxx",
    r"zielig",
    r"zooi",
    r"zeg"
]

informals = RegexMatches(name + ".informals", informal_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
