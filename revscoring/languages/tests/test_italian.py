import pickle

from nose.tools import eq_

from .. import italian
from ...datasources import revision
from ...dependencies import solve

BAD = [
    "anale",
    "ano",
    "bastardi", "bastardo",
    "buttana",
    "caca", "cacare", "cacata",
    "cacca", "cacche", "caccola", "caccole",
    "caga", "cagare", "cagata", "cagate", "cagato",
    "cavolata", "cavolate",
    "cazz", "cazzata", "cazzate", "cazzi", "cazzo", "cazzone", "cazzoni",
    "cesso",
    "ciccione",
    "ciuccia",
    "coglione", "coglioni",
    "cojone",
    "cretini", "cretino",
    "culo",
    "deficente", "deficenti",
    "fancazzista",
    "fanculo",
    "fica", "figa", "fighe", "figo",
    "fotte", "fottiti", "fottuto",
    "fregna",
    "froci", "frocio", "frocione",
    "gnocca",
    "idiota",
    "inculare", "inculato", "inculo",
    "kazzo",
    "maiala",
    "merd", "merda", "merdaccia", "merde", "merdosa", "merdoso",
    "mignotta",
    "minchia", "minkia",
    "pene", "peni",
    "pipi", "pippa", "pippe",
    "pirla",
    "piscio",
    "pisellino", "pisello", "pisellone",
    "pompini", "pompino",
    "porca", "porco",
    "porno",
    "pupu",
    "puttana", "puttane", "puttanella", "puttaniere",
    "puzza", "puzzano", "puzzate", "puzzava", "puzzi", "puzzolente", "puzzone",
    "ricchione",
    "sborra", "sburro",
    "scema", "scemi", "scemo",
    "schifo", "schifosa", "schifoso",
    "scopare", "scopata", "scopate", "scopato", "scopava",
    "scoreggia", "scorregge", "scorreggia",
    "seghe",
    "sfigati", "sfigato",
    "siffredi",
    "skifo",
    "sperma",
    "stocazzo",
    "stronza", "stronzata", "stronzate",
    "stronzi", "stronzo",
    "stupido",
    "suca",
    "succhia",
    "suka",
    "tette",
    "troia",
    "troie",
    "trombare",
    "vafanculo", "vaffanculo",
    "znccnk", "znccnl",
    "zoccola"
]

INFORMAL = [
    "ahah", "ahahah", "ahahaha", "ahahahah",
    "amo",
    "avete",
    "banana",
    "bla",
    "brutti", "brutto",
    "cavolo",
    "chiamo",
    "ciao", "ciaoo", "ciaooo", "ciaoooo",
    "cmq",
    "consigliamo",
    "corsivo",
    "dovete",
    "fermatevi",
    "frega",
    "grassetto",
    "hahaha", "hahahaha",
    "inserisci",
    "intestazione",
    "leggete",
    "lol",
    "mamma",
    "nascondi",
    "perche",
    "potete",
    "raga",
    "sapete",
    "scrivete",
    "scusate",
    "siete",
    "sto",
    "tua",
    "volete"
]

OTHER = [
    """
    Le locomotive del gruppo 851 erano un gruppo di locomotive a vapore delle
    Ferrovie dello Stato.

    Furono progettate e fatte costruire dalla Rete Adriatica (RA) quali
    macchine per il servizio di linea. Nel 1905, insieme alle locomotive dei
    gruppi poi FS 290, 600 e 870 anch'esse ex RA, vennero inserite tra quelle
    che le FS reputarono meritevoli di ulteriori commesse nell'attesa del
    completamento del progetto dei nuovi gruppi idonei a fronteggiare lo
    sviluppo del traffico conseguente alla statalizzazione.
    """
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
    compare_extraction(italian.revision.badwords_list, BAD, OTHER)


def test_informals():
    compare_extraction(italian.revision.informals_list, INFORMAL, OTHER)


def test_presence():
    assert hasattr(italian.revision, "words")
    assert hasattr(italian.revision, "content_words")
    assert hasattr(italian.revision, "badwords")
    assert hasattr(italian.revision, "informals")
    assert hasattr(italian.revision, "misspellings")

    assert hasattr(italian.parent_revision, "words")
    assert hasattr(italian.parent_revision, "content_words")
    assert hasattr(italian.parent_revision, "badwords")
    assert hasattr(italian.parent_revision, "informals")
    assert hasattr(italian.parent_revision, "misspellings")

    assert hasattr(italian.diff, "words_added")
    assert hasattr(italian.diff, "badwords_added")
    assert hasattr(italian.diff, "informals_added")
    assert hasattr(italian.diff, "misspellings_added")
    assert hasattr(italian.diff, "words_removed")
    assert hasattr(italian.diff, "badwords_removed")
    assert hasattr(italian.diff, "informals_removed")
    assert hasattr(italian.diff, "misspellings_removed")


def test_revision():
    # Words
    cache = {revision.text: "Furono progettate e m80 costruire dalla."}
    eq_(solve(italian.revision.words_list, cache=cache),
        ["Furono", "progettate", "e", "m80", "costruire", "dalla"])

    # Misspellings
    cache = {revision.text: 'Furono progettate e dalla worngly. <td>'}
    eq_(solve(italian.revision.misspellings_list, cache=cache), ["worngly"])

    # Infonoise
    cache = {revision.text: "Furono progettate e dalla!"}
    eq_(solve(italian.revision.infonoise, cache=cache), 7/22)


def test_pickling():

    eq_(italian, pickle.loads(pickle.dumps(italian)))
