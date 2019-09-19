from .features import Dictionary, RegexMatches, Stopwords

name = "bosnian"

try:
    import enchant
    dictionary = enchant.Dict("bs")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'bs'.  " +
                      "Consider installing 'hunspell-bs'.")

dictionary = Dictionary(name + ".dictionary", dictionary.check)
"""
:class:`~revscoring.languages.features.Dictionary` features via
`enchant.Dict <https://github.com/rfk/pyenchant>`_ "bs". Provided by `hunspell-bs`
"""

stopwords = [
    "ali", "astronomija", "bazirano", "bez", "bih", "bila", "bili",
    "bilješke", "bilo", "bio", "biografije", "biti", "bosna", "bosne",
    "bosni", "broj", "buta", "clusters", "corwin", "dan", "danas", "datoteka",
    "datum", "deset", "desno", "digital", "dio", "dok", "druge", "drugi",
    "drugo", "država", "države", "dužina", "dva", "dvije", "editor", "edu",
    "eliptična", "euklidska", "euklidsku", "flag", "galaxies", "gdje",
    "general", "gif", "glavni", "godina", "godine", "gov", "grad", "grada",
    "grb", "gustoća", "hercegovina", "hercegovine", "hercegovini",
    "historija", "how", "ili", "ima", "ime", "infokutija", "isbn", "između",
    "izvor", "izvori", "jakiel", "jedan", "jedna", "jer", "jezik", "još",
    "kada", "kako", "kao", "karta", "kasnije", "kategorija", "kod", "koja",
    "koje", "koji", "koju", "kroz", "linkovi", "literatura", "lokacija",
    "mini", "minuta", "mjesta", "mjesto", "može", "najbliži", "najbližih",
    "nakon", "nalazi", "name", "naslov", "naziv", "nebulae", "nedostaju",
    "nekoliko", "new", "nije", "nisu", "note", "novi", "observe", "odewahn",
    "oko", "old", "opis", "općina", "ova", "ovaj", "pod", "pogledajte",
    "položaj", "površina", "preko", "prema", "preusmjeri", "prečkasta",
    "prije", "proširiti", "prvi", "publisher", "publishing", "put", "rat",
    "ref", "reference", "refspisak", "rezultati", "richard", "right",
    "rođeni", "rođenja", "sad", "sadrži", "samo", "sbb", "sbbc", "sbc",
    "sdss", "sekciju", "sib", "simboli", "sinnott", "slika", "slike",
    "sljedeći", "sloan", "službeni", "smrt", "smrti", "sortable", "spiralna",
    "spisak", "springer", "strane", "stranica", "sve", "svoje", "tako",
    "također", "tačka", "them", "toga", "tokom", "tri", "uglovnih", "ukupno",
    "umrli", "vanjski", "vaucouleurs", "veliki", "veličina", "već", "vijek",
    "visina", "više", "vrijeme", "vrsta", "zastava", "zbog", "zvanična",
    "čvor", "širina", "što"
]
"""
:class:`~revscoring.languages.features.Stopwords` features copied from
"common words" in https://meta.wikimedia.org/wiki/?oldid=17177571
"""

stopwords = Stopwords(name + ".stopwords", stopwords)

badword_regexes = [
    r"balija",
    r"debil",
    r"debili",
    r"debilu",
    r"drolja",
    r"drolje",
    r"droljetine",
    r"droljo",
    r"fašisti",
    r"fuck",
    r"govna",
    r"govno",
    r"iliriski",
    r"jebanje",
    r"jebe",
    r"jebem",
    r"jebem",
    r"jebi",
    r"jebiga",
    r"jebite",
    r"jebo",
    r"kreten",
    r"kretenčina",
    r"kretenčuga",
    r"kreteni",
    r"kretenu",
    r"kučka",
    r"kuja",
    r"kuje",
    r"kurac",
    r"kurce",
    r"kurcina",
    r"kurčina",
    r"kurva",
    r"lezbac",
    r"lezbać",
    r"maloglavi",
    r"materinu",
    r"mrš",
    r"peder",
    r"pederi",
    r"pederima",
    r"pederski",
    r"pederu",
    r"picka",
    r"pička",
    r"picke",
    r"pičke",
    r"picko",
    r"pičko",
    r"pizda",
    r"pizdo",
    r"pizdu",
    r"puškomet",
    r"shit",
    r"sranje",
    r"šupak"
]

badwords = RegexMatches(name + ".badwords", badword_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
    r"boriću",
    r"bubaj",
    r"drzava",
    r"glup",
    r"haha",
    r"hahaha",
    r"hahahaha",
    r"hahahahaha",
    r"hihi",
    r"hihihi",
    r"istorija",
    r"lmao",
    r"lol",
    r"nesto",
    r"neznam",
    r"nista",
    r"opština",
    r"opštini",
    r"orgaizovanje",
    r"pokusava",
    r"pokušavajuci",
    r"povijest",
    r"povješničari",
    r"pregledaču",
    r"šireči",
    r"takođerr",
    r"ucvršćivanja",
    r"vecina",
    r"zivjeli",
    r"zivjelo"
]

informals = RegexMatches(name + ".informals", informal_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
