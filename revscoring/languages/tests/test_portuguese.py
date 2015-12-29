import pickle

from nose.tools import eq_

from .. import portuguese
from ...datasources import revision_oriented
from ...dependencies import solve
from .util import compare_extraction

BAD = [
    "babaca", "babacas", "babacão", "babacões", "babaquice",
    "bixa", "bixas", "bicha", "bichas",
    "boiola", "boiolas", "boiolão",
    "boquete", "boquetes", "bokete", "boketes",
    "bosta", "bostas", "bostao", "bostalhao",
    "buceta", "bucetas", "bucetao", "bucetinha", "boceta", "busseta", "buçeta",
    "bunda", "bundinha", "bundas", "bundinhas", "bundão", "bundao", "bumda",
    "burra", "burras", "burro", "burros", "burrice",
    "cacete", "cacetes", "kacete", "kacetes", "caçete", "cacet", "caçetes",
    "caga", "cagada", "cagado", "cagando", "caganeira", "cagar", "cagou",
    "kaga", "kagada", "cagalhao", "caganita", "cagadela", "cagalhoto", "kagou",
    "carai", "caraio", "caralho", "caralhos", "caralhao", "caralhinho",
    "karai", "karaio", "karalho", "caralhinhu", "caraios", "caraius",
    "chata", "chato", "chatas", "chatos", "xata", "xato", "xatas", "xatos",
    "chupa", "chupar", "chupava", "chupo", "chupou", "xupa", "chupada",
    "chupete", "xupar", "chupe",
    "cocô", "cokô", "kocô", "kokô",
    "comi", "come", "comer", "komi", "kome", "komer",
    "cona", "conas", "kona", "konas",
    "cuzao", "cuzão", "cuzinho", "kuzao", "kuzão", "kuzinho",
    "doido", "doida", "doidinho", "doidinha", "doidos", "doidas", "doidinhas",
    "fede", "fedido", "fedida", "fedorento", "fedorenta", "fedia", "fedidos",
    "fedidas", "fedorentos", "fedorentas",
    "feia", "feio", "feias", "feios",
    "fendi",
    "foda", "fodas", "fude", "fuder", "fodao", "fudido", "fodido", "fodidos",
    "gostosa", "gostosão", "gostosas", "gostoso", "goxtosa", "gostosona",
    "idiota", "idiotas", "idiotice", "idiotices", "idiotiçe", "idiotisses",
    "louca", "louco", "loka", "loko", "loucura", "loukura", "loucamente",
    "maconheira", "maconheiro", "maconheiras", "maconheiros",
    "mafia", "máfia",
    "maldizentes",
    "mecos",
    "mentira", "mentiroso", "mentirosa", "mentiras", "mentirosos",
    "merda", "merdas", "merdão", "merdao", "merdoso", "merdica",
    "noob",
    "otario", "otário", "otarios", "otaria", "otária", "otarias",
    "pariu", "pario",
    "pategos",
    "pau",
    "peida", "peido", "peidão", "peidao", "peidei", "peidar", "peidaria",
    "peidando", "peidaço", "peideis", "peidos",
    "pênis", "penis",
    "pila", "pilas",
    "piroca",
    "porcaria", "pornô", "porno", "porn",
    "porra", "poha",
    "pum",
    "punheta", "punhetas", "punheteiro", "punheteira", "punheteiros",
    "puta", "putona", "putaria", "putas", "puteiro", "putinha", "putos",
    "puto", "putos",
    "safado", "safada", "safadona", "safadonas", "safados", "safadas",
    "tesão", "tezão", "tesudo", "tesuda", "tesudos", "tesudas", "tezudas",
    "transa", "transar", "transaram", "transando", "tranzáram", "transou",
    "treta", "tretas",
    "troxa", "trouxa", "troxas", "trouxas", "trocha", "troucha", "trochas",
    "vadia", "vadio", "vadias", "vadios", "vadiagem",
    "viadage", "viadagem", "viadão", "viadao", "viado", "viadinho",
    "viadinhos", "viadinhu", "viadinhus",
    "viado", "viados",
    "xixi",
]

INFORMAL = [
    "adoro",
    "aki",
    "amo",
    "bla", "blablabla", "bbblllaaaahhhhhblah",
    "coco",
    "copiei", "copiem",
    "delicia",
    "editei",
    "enfia", "enfiar",
    "entao",
    "estraguem",
    "fixe",
    "gajo",
    "haha", "hahaha", "hehe", "hehehe",
    "kkk", "kkkk", "kkkkk", "kkkkkk", "kkkkkkk",
    "lindo",
    "lol",
    "mae",
    "mto",
    "naum",
    "nois",
    "odeio",
    "oi", "oiiiiiiiiii",
    "ola", "olá",
    "rata", "ratas",
    "rs", "rsrsrs",
    "tava",
    "tbm",
    "vao",
    "vcs", "voce", "voces",
    "xau"
]

OTHER = [
    """
    A batalha de Hastings foi travada em 14 de outubro de 1066 entre o exército
    franco-normando do duque Guilherme II da Normandia (r. 1035–1087) e um
    exército inglês sob o rei anglo-saxão Haroldo II (r. 1066), durante a
    conquista normanda da Inglaterra. Ocorreu cerca de 11 quilômetros a
    noroeste de Hastings, perto da atual cidade de Battle, em Sussex Oriental,
    e teve como resultado uma decisiva vitória normanda.
    """,
    "arvere"
]

r_text = revision_oriented.revision.text


def test_badwords():
    compare_extraction(portuguese.badwords.revision.datasources.matches,
                       BAD, OTHER)

    eq_(portuguese.badwords, pickle.loads(pickle.dumps(portuguese.badwords)))


def test_informals():
    compare_extraction(portuguese.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    eq_(portuguese.informals, pickle.loads(pickle.dumps(portuguese.informals)))


def test_dictionary():
    cache = {r_text: "A haver, rebeliões: e m80 da Normandia."}
    eq_(solve(portuguese.dictionary.revision.datasources.dict_words,
              cache=cache),
        ["A", "haver", "rebeliões", "e", "da", "Normandia"])
    eq_(solve(portuguese.dictionary.revision.datasources.non_dict_words,
              cache=cache),
        ["m80"])

    eq_(portuguese.dictionary,
        pickle.loads(pickle.dumps(portuguese.dictionary)))


def test_stopwords():
    cache = {r_text: "Esta a o corrida!"}
    eq_(solve(portuguese.stopwords.revision.datasources.stopwords,
        cache=cache),
        ["Esta", "a", "o"])
    eq_(solve(portuguese.stopwords.revision.datasources.non_stopwords,
        cache=cache),
        ["corrida"])

    eq_(portuguese.stopwords, pickle.loads(pickle.dumps(portuguese.stopwords)))


def test_stemmmed():
    cache = {r_text: "A haver, rebeliões: e m80 da Normandia."}
    eq_(solve(portuguese.stemmed.revision.datasources.stems, cache=cache),
        ["a", "hav", "rebeliõ", "e", "m80", "da", "normand"])

    eq_(portuguese.stemmed, pickle.loads(pickle.dumps(portuguese.stemmed)))
