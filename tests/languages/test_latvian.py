import pickle

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.languages import latvian

from .util import compare_extraction

BAD = [
    "bla",
    "ble",
    "bomzis",
    "bļa",
    "bļe",
    "bļeģ",
    "daunis",
    "dauņi",
    "dick",
    "dildo",
    "dirsa",
    "dirsas",
    "dirst",
    "dirsu",
    "dirsā",
    "diseni",
    "fuck",
    "fucking",
    "gay",
    "homītis",
    "huiņa",
    "idioti",
    "idiots",
    "izpisa",
    "jebal",
    "jobans",
    "kaka",
    "kakas",
    "kaku",
    "kroplis",
    "kuce",
    "kuces",
    "loh",
    "lohi",
    "lohs",
    "lohu",
    "lose",
    "losene",
    "losis",
    "lox",
    "loxi",
    "loxs",
    "mauka",
    "maukas",
    "mauku",
    "nahuj",
    "nais",
    "nepiš",
    "niga",
    "nigga",
    "pauti",
    "pediņi",
    "pediņš",
    "peža",
    "pidaras",
    "pidarasi",
    "pidari",
    "pidars",
    "pidaru",
    "pimpi",
    "pimpis",
    "pimpja",
    "pimpji",
    "pipele",
    "pirdiens",
    "piš",
    "pizda",
    "pīzda",
    "pohuj",
    "porno",
    "seks",
    "sex",
    "shit",
    "smird",
    "smirdi",
    "stulba",
    "stulbs",
    "stūlbs",
    "suck",
    "suds",
    "sukaja",
    "suukaa",
    "sūda",
    "sūdi",
    "sūdiem",
    "sūds",
    "sūdu",
    "sūkā",
    "sūkāja",
    "sūkāt"
]

INFORMAL = [
    "arii",
    "boldā",
    "cau",
    "caw",
    "chau",
    "dibens",
    "diseni",
    "ejat",
    "ejiet",
    "fail",
    "garso",
    "garšo",
    "haha",
    "hello",
    "jaa",
    "kko",
    "kruts",
    "lol",
    "nais",
    "naw",
    "mēsls",
    "paldies",
    "rullē",
    "stulbi",
    "sveiki",
    "swag",
    "taa",
    "urlas",
    "urlu",
    "vinjam",
    "vinji",
    "vinju",
    "vinsh",
    "wtf",
    "yolo",
    "čalis",
    "čau"
]

OTHER = [
    """
    gada laikapstākļi Latvijā temperatūras ziņā bija tuvu normai gada vidējā
    gaisa temperatūra bija kas ir grādu virs normas, tādējādi ierindojoties
    siltāko gadu vietā. Vislielākā temperatūras novirze no normas bija decembrī
    aptuveni Aukstāks par normu bija tikai februāris, tā vidējā gaisa
    temperatūra valstī kopumā bija grādu zem klimatiskās normas. Pārējo mēnešu
    vidējās gaisa temperatūras novirze no ilggadējiem vidējiem rādītājiem bija
    no grādiem maijā līdz grādam jūlijā. Nokrišņu daudzums gadā bija tuvs
    """
]


def test_badwords():
    compare_extraction(latvian.badwords.revision.datasources.matches, BAD,
                       OTHER)

    assert latvian.badwords == pickle.loads(pickle.dumps(latvian.badwords))


def test_informals():
    compare_extraction(latvian.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    assert latvian.informals == pickle.loads(pickle.dumps(latvian.informals))


def test_dictionary():
    cache = {revision_oriented.revision.text:
             'novirze no ilggadējiem vidējiem  worngly.'}
    assert (solve(latvian.dictionary.revision.datasources.dict_words, cache=cache) ==
            ["novirze", "no", "ilggadējiem", "vidējiem"])
    assert (solve(latvian.dictionary.revision.datasources.non_dict_words,
                  cache=cache) ==
            ["worngly"])

    assert latvian.dictionary == pickle.loads(pickle.dumps(latvian.dictionary))


def test_stopwords():
    cache = {revision_oriented.revision.text: 'novirze būt vidējiem'}
    assert (solve(latvian.stopwords.revision.datasources.stopwords, cache=cache) ==
            ['būt'])
    assert (solve(latvian.stopwords.revision.datasources.non_stopwords,
                  cache=cache) ==
            ['novirze', 'vidējiem'])

    assert latvian.stopwords == pickle.loads(pickle.dumps(latvian.stopwords))
