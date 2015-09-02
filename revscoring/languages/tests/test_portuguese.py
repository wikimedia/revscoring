import pickle

from nose.tools import eq_

from .. import portuguese
from ...datasources import revision
from ...dependencies import solve

BAD = [
    "babaca",
    "bixa",
    "boiola", "boiolas",
    "boquete",
    "bosta",
    "buceta", "bucetas", "bucetinha",
    "bunda", "bundinha",
    "burra", "burro", "burros",
    "cacete",
    "caga", "cagada", "cagado", "cagando", "caganeira", "cagar", "cagou",
    "carai", "caraio", "caralho",
    "chata", "chato",
    "chupa", "chupar", "chupava", "chupo", "chupou", "xupa",
    "cocô",
    "comi",
    "cona",
    "cuzao", "cuzão", "cuzinho",
    "doido",
    "fede", "fedido",
    "feia",
    "fendi",
    "foda", "fodas", "fude", "fuder",
    "gostosa", "gostosão", "gostosas", "gostoso",
    "idiota", "idiotas",
    "loka", "loko",
    "maconheiro",
    "mafia",
    "maldizentes",
    "mecos",
    "mentira", "mentiroso", "mentirosa", "mentirosos", "mentirosas",
    "merda",   "merdas",
    "noob",
    "otario", "otário", "otarios",
    "pariu",
    "pategos",
    "peida", "peidar", "peidei",  "peido", "peidos",
    "pênis",
    "pila", "pilas",
    "piroca",
    "poha",
    "porcaria", "porno",
    "porra",
    "pum",
    "punheta", "punheteiro",
    "puta", "putaria", "putas", "puteiro", "putinha",
    "puto", "putos",
    "safado",
    "tesão",
    "transar", "tranzar",
    "treta", "troxa",
    "vadia",
    "viadagem", "viadão",  "viadinho", "viadinhos",
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


def compare_extraction(extractor, examples, counter_examples):

    for example in examples:
        eq_(extractor.process(example), [example])
        eq_(extractor.process("Sentence " + example + " sandwich."), [example])
        eq_(extractor.process("Sentence end " + example + "."), [example])
        eq_(extractor.process(example + " start of sentence."), [example])

    for example in counter_examples:
        eq_(extractor.process(example), [])
        eq_(extractor.process("Sentence " + example + " sandwich."), [])
        eq_(extractor.process("Sentence end " + example + "."), [])
        eq_(extractor.process(example + " start of sentence."), [])


def test_badwords():
    compare_extraction(portuguese.revision.badwords_list, BAD, OTHER)


def test_informals():
    compare_extraction(portuguese.revision.informals_list, INFORMAL, OTHER)


def test_revision():
    # Words
    cache = {revision.text: "A haver, rebeliões: e m80 da Normandia."}
    eq_(solve(portuguese.revision.words_list, cache=cache),
        ["A", "haver", "rebeliões", "e", "m80", "da", "Normandia"])

    # Misspellings
    cache = {revision.text: 'O número de vítimas é difícil worngly. <td>'}
    eq_(solve(portuguese.revision.misspellings_list, cache=cache), ["worngly"])

    # Infonoise
    cache = {revision.text: "Esta a o corrida!"}
    eq_(solve(portuguese.revision.infonoise, cache=cache), 4/13)


def test_presence():
    assert hasattr(portuguese.revision, "words")
    assert hasattr(portuguese.revision, "content_words")
    assert hasattr(portuguese.revision, "badwords")
    assert hasattr(portuguese.revision, "informals")
    assert hasattr(portuguese.revision, "misspellings")

    assert hasattr(portuguese.parent_revision, "words")
    assert hasattr(portuguese.parent_revision, "content_words")
    assert hasattr(portuguese.parent_revision, "badwords")
    assert hasattr(portuguese.parent_revision, "informals")
    assert hasattr(portuguese.parent_revision, "misspellings")

    assert hasattr(portuguese.diff, "words_added")
    assert hasattr(portuguese.diff, "badwords_added")
    assert hasattr(portuguese.diff, "informals_added")
    assert hasattr(portuguese.diff, "misspellings_added")
    assert hasattr(portuguese.diff, "words_removed")
    assert hasattr(portuguese.diff, "badwords_removed")
    assert hasattr(portuguese.diff, "informals_removed")
    assert hasattr(portuguese.diff, "misspellings_removed")


def test_pickling():

    eq_(portuguese, pickle.loads(pickle.dumps(portuguese)))
