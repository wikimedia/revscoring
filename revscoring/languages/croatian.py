from .features import Dictionary, RegexMatches, Stopwords

name = "croatian"

try:
    import enchant
    dictionary = enchant.Dict("hr")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'hr'.  " +
                      "Consider installing 'myspell-hr'.")

dictionary = Dictionary(name + ".dictionary", dictionary.check)
"""
:class:`~revscoring.languages.features.Dictionary` features via
`enchant.Dict <https://github.com/rfk/pyenchant>`_ "hr". Provided by `myspell-hr`
"""

stopwords = [
    "ako", "ali", "bez", "bila", "bili", "bilo", "bio", "biti", "broj", "dan",
    "dana", "danas", "datoteka", "datum", "defaultsort", "desno", "dio",
    "dobio", "dok", "dolazi", "druga", "druge", "drugi", "drugih", "država",
    "države", "dva", "dvije", "eng", "gdje", "glavni", "glavniraspored",
    "godina", "godine", "grad", "grada", "hrvatska", "hrvatske", "hrvatski",
    "hrvatskoj", "iako", "ili", "ima", "image", "imaju", "imao", "ime",
    "infookvir", "interwiki", "ipak", "ivan", "između", "izvor", "izvori",
    "jedan", "jedna", "jednom", "jer", "jezik", "još", "kad", "kada", "kako",
    "kao", "karta", "kasnije", "kategorija", "kod", "koja", "koje", "kojeg",
    "kojem", "koji", "kojih", "kojima", "kojoj", "koju", "kolovoza", "kraj",
    "kroz", "lijevo", "lipnja", "listopada", "ljudi", "među", "mini", "mjesta",
    "mjesto", "mjestu", "mogu", "može", "mrva", "nagrade", "nakon", "nalazi",
    "name", "naslov", "naziv", "način", "nego", "neke", "neki", "nekoliko",
    "nema", "net", "nije", "nisu", "njegov", "njegova", "njih", "novi",
    "odnosno", "oko", "old", "ona", "oni", "opis", "osim", "ostali", "ova",
    "ovaj", "ove", "ovo", "oznaka", "ožujka", "pod", "području", "popis",
    "poslije", "postaje", "postao", "postoji", "poveznice", "povijest",
    "povijesti", "pred", "preko", "prema", "preusmjeri", "pri", "prije",
    "prosinca", "protiv", "prva", "prvi", "puno", "put", "puta", "radi", "rat",
    "rata", "republike", "right", "rođenja", "rujna", "sad", "sam", "samo",
    "sastav", "siječnja", "slika", "slike", "smrti", "srpnja", "stoljeća",
    "stoljeće", "str", "strane", "stranica", "sve", "svi", "svibnja", "svih",
    "svjetski", "svoj", "svoje", "svojim", "svoju", "tada", "taj", "tako",
    "također", "tek", "the", "tijekom", "toga", "tom", "tome", "travnja",
    "tri", "uglavnom", "uvijek", "vanjske", "velika", "velike", "veliki",
    "veličina", "veljače", "već", "vidi", "više", "vremena", "vrijeme",
    "vrlo", "vrsta", "wprojekti", "zagreb", "zajedno", "zbog", "čak",
    "često", "četiri", "širina", "što", "život", "životopis", "životopisi",
]
"""
:class:`~revscoring.languages.features.Stopwords` features copied from
"common words" in https://meta.wikimedia.org/wiki/?oldid=17051164
"""

stopwords = Stopwords(name + ".stopwords", stopwords)

badword_regexes = [
    r"fuck",
    r"jebi",
    r"jebite",
    r"jebanje",
    r"kučka",
    r"kurva",
    r"kuja",
    r"kuje",
    r"prokleta",
    r"proklet",
    r"proklete",
    r"prokleto",
    r"drolja",
    r"drolje",
    r"droljetine",
    r"droljo",
    r"kreten",
    r"kretenčuga",
    r"kretenčina",
    r"kreteni",
    r"kretenu",
    r"krebil",
    r"krebulu",
    r"krebili",
    r"idiot",
    r"idijot",
    r"idijoti",
    r"idioti",
    r"glupan",
    r"glupani",
    r"glupav",
    r"glupavi",
    r"glupavo",
    r"glupson",
    r"glupsoni",
    r"glupača",
    r"glupaća",
    r"glupačo",
    r"glupaćo",
    r"glupo",
    r"glup",
    r"glupi",
    r"debil",
    r"debilu",
    r"debili",
    r"debel",
    r"debelo",
    r"debela",
    r"debeli",
    r"shit",
    r"sranje",
    r"sranja",
    r"govno",
    r"govna",
    r"govana",
    r"kurac",
    r"kurca",
    r"pička",
    r"pičku",
    r"pizda",
    r"pizdu",
    r"ukurac",
    r"mrš",
    r"marš",
    r"peder",
    r"pederu",
    r"pederi",
    r"gay",
    r"dragy",
    r"glupa",
    r"glupost",
    r"gluposti",
    r"jebanja",
    r"jebač",
    r"jebe",
    r"jebem",
    r"jebiga",
    r"jebo",
    r"defnyddiwr",
    r"ententini",
    r"kurce",
    r"materina",
    r"pederski",
    r"fijufić",
    r"pederčina",
    r"picka",
    r"picku",
    r"pičke",
    r"šupak",
    r"šipac",
    r"pig",
    r"lebac",
    r"nazi",
    r"nazy",
    r"morons",
    r"budala",
    r"smrdi",
    r"budale",
    r"bljuvač",
    r"suljić",
    r"suljo",
    r"zločinac",
    r"maloglavi",
]

badwords = RegexMatches(name + ".badwords", badword_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
    r"adeo",
    r"pozdrav",
    r"bok",
    r"lol",
    r"hej",
    r"haha",
    r"hahaha",
    r"nezna",
    r"neznam",
    r"hahahah",
    r"hahahaha",
    r"okej",
    r"jeste",
    r"ok",
    r"vidimo se",
    r"hvala",
    r"zahvaljujem",
    r"inace",
    r"inače",
    r"šta",
    r"vas",
    r"moze",
    r"mozete",
    r"gde",
    r"reci",
    r"niste",
    r"unesi",
    r"unesite",
    r"suradnik",
    r"suradnicko",
    r"suradničko",
    r"suradnica",
    r"suradnice",
    r"suradnici",
    r"vam",
    r"čak",
    r"ste",
    r"sta",
]

informals = RegexMatches(name + ".informals", informal_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
