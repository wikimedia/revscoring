import pickle

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.languages import dutch

from .util import compare_extraction

BAD = [
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
    "homo", "homos",  # add "homo's" ; perjorative for gay person
    "kak", "kaka",  # poop
    "kakhoofd", "kakken",  # kakhoofd = poopy head; kakken = to poop (verb)
    "kanker", "kenker",  # cancer
    "klootzak", "klootzakken",  # "ball sack"
    "klote",  # lit.: balls; equivalent: "sucky"
    "kolere", "klere",  # Chollera
    "kont", "kontgat",  # butt, butthole
    "kontje",  # little butt
    "lekkerding", "lekker ding",  # means something like "hot piece"
    "likken",  # lick (not totally sure why this is here)
    "pedo",  # add "pedofiel"; pedophile
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
    "verekte", "verkracht", "verrekte",  # "damn" or "fucking" (adj)
    "verkracht", "verkrachten",  # rape/raped
    "dikzak",  # fat person
    "mogolen", "mogool", "mongool", "mongolen",  # perj. for down syndrome
    "mooiboy",  # man who puts a lot of effort into his appearance
    "sperma",  # sperm
    "kut", "kutje", "kutjes",  # vulgar word for vagina (Eng.: cunt)
    "stelletje",  # "bunch of", as part of a racial slur or perj.
    "lul",  # dick
    "lullen",  # out of an ass
    "lulltje",  # weak person
    "reet",  # buttcrack, often used in an idiom that means "don't give a shit"
    "slet",  # slut
    "scheet", "scheten",  # fart
    "schijt",  # shit
    "tyfus",  # Typhoid
    "smeerlap",  # literally: "grease rag"
    "het zuigt",  # "It sucks"
    "sukkel",  # "Sucker"
    "sul",  # "wimp", "dork", or "schlemiel". Its etymology is unclear.
    "vreten",  # rude form of the verb "to eat"
    "vuil", "vuile",  # "filth" or "filthy"
    "wijf", "kutwijf", "kankerhoer", "rothoer", "vishoer",  # perj for women

    # Racial slurs
    "bamivreter",  # "bami eater" an ethnic slur used against people of Asian
    "bosneger",  # literally: "bushnegro"
    "geitenneuker",  # literally: "goat fucker"
    "kakker",  # "crapper" -- higher social class idiot
    "koelie",  # "coolie" Indonesian laborer
    "lijp",  # slur for Jewish people and "slow", "dumb", "sluggish"
    "mocro",  # people of Moroccan descent
    "mof", "moffenhoer", "mofrica",  # ethnic slur used for german people
    "neger", "negers", "nikker",  # n-word
    "poepchinees",  # "poop Chinese"
    "roetmop",  # ethnic slur for black people.
    "spaghettivreter", "pastavreter",  # perj. for people of Italian descent
    "loempiavouwer",  # "spring roll folder" people of Vietnamese descent
    "spleetoog",  # "slit eye" term for people of Asian descent
    "tuig",  # "scum"
    "zandneger",  # "sand negro" an ethnic slur for people of Middle Eastern

    # Religion
    "gadverdamme", "godverdomme", "gadver", "getverderrie",   # "god damn"
    "getver", "verdomme", "verdamme", "verdorie",  # "god damn" continued
    "godskolere",  # "god fury"
    "graftak",  # "grave branch" an old, moody, cranky person.
    "jezus christus", "jezus", "tjezus", "jeetje", "jezus mina",  # Jesus
    "jesses", "jasses", "harrejasses", "here jezus",  # Jesus continued
]

INFORMAL = [
    "aap", "aapjes",
    "banaan",
    "bent",
    "boe", "boeit",
    "doei"
    "dombo", "domme",
    "eigelijk",
    "godverdomme",
    "groetjes",
    "gwn",
    "hoi",
    "hallo", "halloo",
    "heb",
    "heej", "heey", "heeel",
    "hou", "houd",
    "hoihoi", "hoii", "hoiii",
    "hoor",
    "izan",
    "jij",
    "jou",
    "jullie",
    "kaas",
    "klopt",
    "kots",
    "kusjes",
    "lekker", "lekkere", "lkkr",
    "maarja",
    "mama",
    "nou",
    "oma",
    "ofzo",
    "oke",
    "snap",
    "stinken", "stinkt",
    "stoer",
    "swek",
    "vies", "vieze",
    "vind",
    "vuile",
    "zielig",
    "zooi",
    "zeg"
]

OTHER = [
    """
    De stemtoonhoogte is de toonhoogte van de kamertoon. Door middel van een
    stemvork is deze kamertoon beschikbaar voor het stemmen van een
    muziekinstrument.

    Internationaal is deze toonhoogte in het midden van de 20e eeuw vastgesteld
    op een frequentie van 440 Hz. De stemtoon lag echter niet altijd vast. Soms
    leest men ergens dat de stemtoon door de eeuwen heen steeds hoger is komen
    te liggen, maar dat is slechts de helft van het verhaal. Er waren orgels
    die een hogere stemtoon hadden, en later lager gestemd werden. Kerkorgels
    verschilden enorm van stemtoon. In de loop van de tijd is die variatie
    steeds kleiner geworden. Naarmate mensen steeds mobieler werden, ontstond
    ook de behoefte aan meer compatibiliteit van instrumenten.
    """
]


def test_badwords():
    compare_extraction(dutch.badwords.revision.datasources.matches, BAD, OTHER)

    assert dutch.badwords == pickle.loads(pickle.dumps(dutch.badwords))


def test_informals():
    compare_extraction(dutch.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    assert dutch.informals == pickle.loads(pickle.dumps(dutch.informals))


def test_dictionary():
    cache = {revision_oriented.revision.text: 'Door middel van een worngly.'}
    assert (solve(dutch.dictionary.revision.datasources.dict_words, cache=cache) ==
            ["Door", "middel", "van", "een"])
    assert (solve(dutch.dictionary.revision.datasources.non_dict_words,
                  cache=cache) ==
            ["worngly"])

    assert dutch.dictionary == pickle.loads(pickle.dumps(dutch.dictionary))


def test_stopwords():
    cache = {revision_oriented.revision.text: 'Door middel van een!'}
    assert (solve(dutch.stopwords.revision.datasources.stopwords, cache=cache) ==
            ["Door", "van", "een"])
    assert (solve(dutch.stopwords.revision.datasources.non_stopwords,
                  cache=cache) ==
            ["middel"])

    assert dutch.stopwords == pickle.loads(pickle.dumps(dutch.stopwords))


def test_stemmed():
    cache = {revision_oriented.revision.text: 'Door middel van een!'}
    assert (solve(dutch.stemmed.revision.datasources.stems, cache=cache) ==
            ["dor", "middel", "van", "een"])

    assert dutch.stemmed == pickle.loads(pickle.dumps(dutch.stemmed))
