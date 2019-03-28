import pickle

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.languages import croatian

from .util import compare_extraction

BAD = [
    "fuck",
    "jebi",
    "jebite",
    "jebanje",
    "kučka",
    "kurva",
    "kuja",
    "kuje",
    "prokleta",
    "proklet",
    "proklete",
    "prokleto",
    "drolja",
    "drolje",
    "droljetine",
    "droljo",
    "kreten",
    "kretenčuga",
    "kretenčina",
    "kreteni",
    "kretenu",
    "krebil",
    "krebulu",
    "krebili",
    "idiot",
    "idijot",
    "idijoti",
    "idioti",
    "glupan",
    "glupani",
    "glupav",
    "glupavi",
    "glupavo",
    "glupson",
    "glupsoni",
    "glupača",
    "glupaća",
    "glupačo",
    "glupaćo",
    "glupo",
    "glup",
    "glupi",
    "debil",
    "debilu",
    "debili",
    "debel",
    "debelo",
    "debela",
    "debeli",
    "shit",
    "sranje",
    "sranja",
    "govno",
    "govna",
    "govana",
    "kurac",
    "kurca",
    "pička",
    "pičku",
    "pizda",
    "pizdu",
    "ukurac",
    "mrš",
    "marš",
    "peder",
    "pederu",
    "pederi",
    "gay",
    "dragy",
    "glupa",
    "glupost",
    "gluposti",
    "jebanja",
    "jebač",
    "jebe",
    "jebem",
    "jebiga",
    "jebo",
    "defnyddiwr",
    "ententini",
    "kurce",
    "materina",
    "pederski",
    "fijufić",
    "pederčina",
    "picka",
    "picku",
    "pičke",
    "šupak",
    "šipac",
    "pig",
    "lebac",
    "nazi",
    "nazy",
    "morons",
    "budala",
    "smrdi",
    "budale",
    "bljuvač",
    "suljić",
    "suljo",
    "zločinac",
    "maloglavi",
]

INFORMAL = [
    "adeo",
    "pozdrav",
    "bok",
    "lol",
    "hej",
    "haha",
    "hahaha",
    "nezna",
    "neznam",
    "hahahah",
    "hahahaha",
    "okej",
    "jeste",
    "ok",
    "vidimo se",
    "hvala",
    "zahvaljujem",
    "inace",
    "inače",
    "šta",
    "vas",
    "moze",
    "mozete",
    "gde",
    "reci",
    "niste",
    "unesi",
    "unesite",
    "suradnik",
    "suradnicko",
    "suradničko",
    "suradnica",
    "suradnice",
    "suradnici",
    "vam",
    "čak",
    "ste",
    "sta",
]

OTHER = [
    """
    Iako je često vezan i uz egzistencijalizam, Camus je odbijao tu
    povezanost. No, u drugu ruku, Camus u svom eseju Pobunjeni čovjek
    piše da se cijeli svoj život borio protiv filozofije nihilizma.
    Njegova religioznost također je bila čestom temom, a sam je u
    jednoj od svojih knjiga napisao: Ne vjerujem u boga "i" nisam
    ateist.
    """
]

r_text = revision_oriented.revision.text


def test_badwords():
    compare_extraction(croatian.badwords.revision.datasources.matches,
                       BAD, OTHER)

    assert croatian.badwords == pickle.loads(pickle.dumps(croatian.badwords))


def test_informals():
    compare_extraction(croatian.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    assert croatian.informals == pickle.loads(pickle.dumps(croatian.informals))


def test_dictionary():
    cache = {r_text: "svom eseju worngly."}
    assert (solve(croatian.dictionary.revision.datasources.dict_words,
                  cache=cache) ==
            ["svom", "eseju"])
    assert (solve(croatian.dictionary.revision.datasources.non_dict_words,
                  cache=cache) ==
            ["worngly"])

    assert croatian.dictionary == pickle.loads(
        pickle.dumps(croatian.dictionary))


def test_stopwords():
    cache = {r_text: "može mrva primatelj nagrade."}
    assert (solve(croatian.stopwords.revision.datasources.stopwords, cache=cache) ==
            ["može", "mrva", "nagrade"])
    assert (solve(croatian.stopwords.revision.datasources.non_stopwords,
                  cache=cache) ==
            ["primatelj"])

    assert croatian.stopwords == pickle.loads(pickle.dumps(croatian.stopwords))
