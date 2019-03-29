import pickle

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.languages import swedish

from .util import compare_extraction

BAD = [
    "anal",
    "analen",
    "anus",
    "arslet",
    "bajs",
    "bajsa",
    "bajsade",
    "bajsar",
    "bajsat",
    "bajset",
    "bajskorv",
    "bajskorvar",
    "bajskorven",
    "balle",
    "ballen",
    "blabla",
    "blattar",
    "bög",
    "bögar",
    "bögarna",
    "bögarnas",
    "bögen",
    "bögig",
    "bögiga",
    "bögigaste",
    "bögigt",
    "bögjävel",
    "bööög",
    "dase",
    "dildo",
    "dildos",
    "dum",
    "dumma",
    "efterbliven",
    "faan",
    "fan",
    "fetto",
    "fis",
    "fitt",
    "fitta",
    "fittan",
    "fittor",
    "fjortisar",
    "fuck",
    "fuckers",
    "fucking",
    "gay",
    "gubbe",
    "hacked",
    "homosexuel",
    "hora",
    "horan",
    "horor",
    "hororna",
    "horungar",
    "horunge",
    "idiot",
    "idioter",
    "heil",
    "jävel",
    "jävla",
    "jävlar",
    "jävligt",
    "knull",
    "knulla",
    "knullad",
    "knullade",
    "knullar",
    "knullare",
    "knullat",
    "kuk",
    "kukar",
    "kukarna",
    "kuken",
    "kukens",
    "kuksugar",
    "kuksugare",
    "kåt",
    "kåta",
    "körv",
    "meatspin",
    "mongo",
    "penis",
    "penisar",
    "penisen",
    "piss",
    "poop",
    "pornhub",
    "porr",
    "porrstjärna",
    "prutt",
    "pung",
    "pungkula",
    "pungkulor",
    "puss",
    "pussy",
    "redtube",
    "tjockis",
    "tuttar",
    "snopp",
    "snoppar",
    "snoppen",
    "snubbe",
    "sucks",
    "sug",
    "suga",
    "sugare",
    "suger",
    "swag",
    "sög",
    "rumpa",
    "rumpan",
    "rumpor",
    "runk",
    "runka",
    "runkade",
    "runkar",
    "röv",
    "röven",
    "rövhål",
    "rövhålet",
    "rövslickare",
    "sexig",
    "mamma",
    "korv",
    "kossa",
    "kossor",
    "luktade",
    "luktar",
    "mammas",
    "mammor",
    "apa",
    "apor",
    "fet",
    "feta",
    "fett",
    "hårig",
    "håriga",
    "knark",
    "tönt",
    "töntar",
    "vafan",
    "morsa",
    "mycke",
    "najs",
    "neger",
    "negrar",
    "negrarna",
    "nigga",
    "noob",
    "noobs",
    "nörd",
    "nötaland",
    "ollon",
    "omg",
    "oxå",
    "pedofil",
    "sebbe",
    "sjukt",
    "sket",
    "skit",
    "skiten",
    "skiter",
    "yolo",
    "äcklig",
    "äckliga",
    "äckligt",
    "älskar",
    "våldtagen",
    "våldtog",
    "sämst",
    "slicka",
    "snygging",
    "sperma",
    "svejsan",
    "särbarn",
    "snygg",
    "snygga",
    "snyggast",
]

INFORMAL = [
    "adda",
    "asså",
    "awesome",
    "btw",
    "cool",
    "coola",
    "coolaste",
    "coolt",
    "din",
    "ftw",
    "ful",
    "fula",
    "fulaste",
    "fult",
    "gillade",
    "gillar",
    "gött",
    "haha",
    "hahaha",
    "hata",
    "hatar",
    "heej",
    "hehe",
    "hehehe",
    "hej",
    "hejdå",
    "hejhej",
    "hejsan",
    "here",
    "hihi",
    "jätte",
    "killar",
    "kille",
    "kolla",
    "lol",
    "mkt",
    "wow",
    "yeah",
    "kul",
    "kompis",
    "mvh",
    "suck",
    "tja",
    "tjej",
    "tjejer",
    "tjena",
    "snälla",
]

OTHER = [
    """
    Stockholms trafiksignaler började tas i drift år 1925 och den första
    anläggningen stod i korsningen Kungsgatan/Vasagatan. Vid den tiden
    hade trafiksignalerna bara två huvudfärger och kretsloppet i
    signalväxlingen var indelat i endast två faser, rött och grönt.
    År 1932 introducerades ”Stockholmsmetoden” som innebar att man visade
    rött/gult respektive grönt/gult i mellanfaserna. Även den första
    anläggningen med fyrskensväxling installerades 1932 i korsningen
    Kungsgatan/Vasagatan, som var en sorts experimenterplats för nya
    trafiksignaler. År 1937 blev Stockholmsmetoden officiell svensk
    standard och ändrades först år 1999 till dagens, europaanpassade
    signalväxling utan grön/gult i mellanfasen.
    """
]

r_text = revision_oriented.revision.text


def test_badwords():
    compare_extraction(swedish.badwords.revision.datasources.matches,
                       BAD, OTHER)

    assert swedish.badwords == pickle.loads(pickle.dumps(swedish.badwords))


def test_informals():
    compare_extraction(swedish.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    assert swedish.informals == pickle.loads(pickle.dumps(swedish.informals))


def test_dictionary():
    cache = {r_text: "skötts övervakning av worngly."}
    assert (solve(swedish.dictionary.revision.datasources.dict_words, cache=cache) ==
            ["skötts", "övervakning", "av"])
    assert (solve(swedish.dictionary.revision.datasources.non_dict_words,
                  cache=cache) ==
            ["worngly"])

    assert swedish.dictionary == pickle.loads(pickle.dumps(swedish.dictionary))


def test_stopwords():
    cache = {r_text: "även omkring introducerades när."}
    assert (solve(swedish.stopwords.revision.datasources.stopwords,
            cache=cache) == ["när"])
    assert (solve(swedish.stopwords.revision.datasources.non_stopwords,
                  cache=cache) ==
            ["även", "omkring", "introducerades"])

    assert swedish.stopwords == pickle.loads(pickle.dumps(swedish.stopwords))
