import pickle

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.languages import polish

from .util import compare_extraction

BAD = [
    "burdel",
    "burdelu",
    "chuj",
    "chuja",
    "chuje",
    "chujowy",
    "chuju",
    "chój",
    "ciota",
    "cioty",
    "cipa",
    "cipe",
    "cipie",
    "cipka",
    "cipki",
    "cipy",
    "cwel",
    "cwele",
    "cycki",
    "debil",
    "debile",
    "debili",
    "downa",
    "dupa",
    "dupe",
    "dupeczki",
    "dupek",
    "dupie",
    "dupsko",
    "dupy",
    "dupę",
    "dziwek",
    "dziwka",
    "dziwki",
    "elo",
    "fiut",
    "fiuta",
    "fuck",
    "gej",
    "gejem",
    "glupi",
    "glupia",
    "glupie",
    "gowno",
    "gunwo",
    "gupia",
    "guwno",
    "gówna",
    "gównem",
    "gówno",
    "huj",
    "huja",
    "huje",
    "hujem",
    "hujowa",
    "hujowy",
    "huju",
    "hwdp",
    "idiota",
    "idioto",
    "japierdole",
    "jebac",
    "jebana",
    "jebane",
    "jebany",
    "jebać",
    "jebał",
    "jebcie",
    "jebie",
    "joł",
    "kiblu",
    "koles",
    "kupa",
    "kupe",
    "kupy",
    "kupą",
    "kupę",
    "kurwa",
    "kurwy",
    "kutafon",
    "kutas",
    "kutasa",
    "kutasem",
    "kutasiarz",
    "kutasy",
    "lalala",
    "loda",
    "lol",
    "mać",
    "noob",
    "nooby",
    "pała",
    "pałe",
    "pały",
    "pałę",
    "pedal",
    "pedaly",
    "pedał",
    "pedałem",
    "pedały",
    "penis",
    "penisa",
    "penisy",
    "piedol",
    "pierdole",
    "pierdolone",
    "pierdolony",
    "pisior",
    "pizda",
    "pizdy",
    "piździe",
    "pojebane",
    "przygłup",
    "przygłupa",
    "przygłupów",
    "pupa",
    "redtube",
    "rucha",
    "ruchania",
    "ruchanie",
    "ruchaniu",
    "ryj",
    "skurwiel",
    "skurwysyn",
    "smierdzi",
    "spierdalaj",
    "sraczka",
    "sraka",
    "sraką",
    "sranie",
    "sraniu",
    "ssie",
    "ssij",
    "ssijcie",
    "syf",
    "szmata",
    "technotłuki",
    "wiocha",
    "wogule",
    "wpierdol",
    "wpierdoli",
    "wyruchany",
    "zadupie",
    "zajebista",
    "zajebisty",
    "zajebiście",
    "zapierdala",
    "ziom",
    "ziomki",
    "ziomy",
    "zjeb",
    "zjebany",
    "śmierdzi",
    "śmierdziele",
    "żul"
]

INFORMAL = [
    "elo",
    "fajna",
    "fajne",
    "fajnie",
    "fajny",
    "glupi",
    "glupia",
    "glupie",
    "haha",
    "hahah",
    "hahaha",
    "hahahaha",
    "hahahahaha",
    "heh",
    "hehe",
    "hehehe",
    "hej",
    "hihi",
    "pozdro",
    "siema",
    "siemka",
    "spoko"
]

OTHER = [
    """
    Najczęściej pojawia się na skórze niezmienionej, choć może powstać
    w obrębie znamion barwnikowych. Podejrzenie czerniaka budzi pojawienie
    się nowej zmiany przypominającej atypowe znamię lub zmiana wcześniej
    istniejącego znamienia barwnikowego. Do głównych objawów czerniaka należą:
    asymetryczne zabarwienie, kształt i powierzchnia zmiany, uniesienie się
    zmiany ponad otaczającą skórę, nieregularne ograniczenie zmiany, a także
    duży jej wymiar.
    """
]


def test_badwords():
    compare_extraction(polish.badwords.revision.datasources.matches, BAD,
                       OTHER)

    assert polish.badwords == pickle.loads(pickle.dumps(polish.badwords))


def test_informals():
    compare_extraction(polish.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    assert polish.informals == pickle.loads(pickle.dumps(polish.informals))


def test_dictionary():
    cache = {revision_oriented.revision.text:
             'obrębie znamion barwnikowych  worngly.'}
    assert (solve(polish.dictionary.revision.datasources.dict_words, cache=cache) ==
            ["obrębie", "znamion", "barwnikowych"])
    assert (solve(polish.dictionary.revision.datasources.non_dict_words,
                  cache=cache) ==
            ["worngly"])

    assert polish.dictionary == pickle.loads(pickle.dumps(polish.dictionary))


def test_stopwords():
    cache = {revision_oriented.revision.text: 'być barwnikowych pomocniczą'}
    assert (solve(polish.stopwords.revision.datasources.stopwords, cache=cache) ==
            ['być'])
    assert (solve(polish.stopwords.revision.datasources.non_stopwords,
                  cache=cache) ==
            ['barwnikowych', 'pomocniczą'])

    assert polish.stopwords == pickle.loads(pickle.dumps(polish.stopwords))
