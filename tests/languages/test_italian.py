import pickle

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.languages import italian

from .util import compare_extraction

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
    """, "ha"
]

r_text = revision_oriented.revision.text


def test_badwords():
    compare_extraction(italian.badwords.revision.datasources.matches,
                       BAD, OTHER)

    assert italian.badwords == pickle.loads(pickle.dumps(italian.badwords))


def test_informals():
    compare_extraction(italian.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    assert italian.informals == pickle.loads(pickle.dumps(italian.informals))


def test_dictionary():
    cache = {r_text: "Furono progettate e m80 costruire dalla."}
    assert (solve(italian.dictionary.revision.datasources.dict_words,
                  cache=cache) ==
            ['Furono', 'progettate', 'e', 'costruire', 'dalla'])
    assert (solve(italian.dictionary.revision.datasources.non_dict_words,
                  cache=cache) ==
            ['m80'])

    assert (italian.dictionary ==
            pickle.loads(pickle.dumps(italian.dictionary)))


def test_stopwords():
    cache = {r_text: "Furono progettate e m80 costruire dalla."}
    assert (solve(italian.stopwords.revision.datasources.stopwords, cache=cache) ==
            ['Furono', 'e', 'dalla'])
    assert (solve(italian.stopwords.revision.datasources.non_stopwords,
                  cache=cache) ==
            ['progettate', 'm80', 'costruire'])

    assert italian.stopwords == pickle.loads(pickle.dumps(italian.stopwords))


def test_stemmmed():
    cache = {r_text: "Furono progettate e m80 costruire dalla."}
    assert (solve(italian.stemmed.revision.datasources.stems, cache=cache) ==
            ['fur', 'progett', 'e', 'm80', 'costru', 'dall'])

    assert italian.stemmed == pickle.loads(pickle.dumps(italian.stemmed))
