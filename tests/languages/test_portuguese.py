import pickle

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.languages import portuguese

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

WORDS_TO_WATCH = [
    # Puffery
    "lendária", "lendárias", "lendário", "lendários", "grande", "grandes",
    "eminente", "eminentes", "visionária", "visionárias", "visionário",
    "visionários", "notável", "notáveis", "líder", "líderes", "célebre",
    "célebres", "de última linha", "extraordinária", "extraordinárias",
    "extraordinário", "extraordinários", "brilhantes", "brilhantes", "famosa",
    "famosas", "famoso", "famosos", "renomada", "renomadas", "renomado",
    "renomados", "prestigiosa", "prestigiosas", "prestigioso", "prestigiosos",
    "de nível mundial", "respeitada", "respeitadas", "respeitado",
    "respeitados", "excepcional", "excepcionais", "excelente", "excelentes",
    "virtuosa", "virtuosas", "virtuoso", "virtuosos", "de grande estima",
    # Contentious labels (-gate removed)
    "culta", "cultas", "culto", "cultos", "racista", "racistas", "perversa",
    "perversas", "perverso", "perversos", "seita", "seitas",
    "fundamentalista", "fundamentalistas", "herege", "hereges", "extremista",
    "extremistas", "negacionista", "negacionistas", "terrorista",
    "terroristas", "libertador", "libertadora", "libertadoras", "libertadores",
    "neonazis", "neo-nazis", "neo nazis", "neonazista", "neo-nazista",
    "neo nazista", "neonazismo", "neo-nazismo", "neo nazismo", "pseudociência",
    "pseudo-ciência", "pseudointelectual", "pseudo-intelectual",
    "pseudointelectuais", "pseudo-intelectuais", "pseudocientífico",
    "pseudocientífica", "pseudocientíficos", "pseudocientíficas",
    "pseudo-científico", "pseudo-científica", "pseudo-científicos",
    "pseudo-científicas", "controversa", "controversas", "controverso",
    "controversos",
    # Unsupported attributions
    "alguns dizem", "algumas dizem", "acredita-se", "muitos têm a opinião",
    "muitas têm a opinião", "a maioria sente", "especialistas afirmam",
    "frequentemente se relata", "é a opinião corrente", "estudos mostram",
    "a ciência diz", "provou-se que",
    # Expressions of doubt
    "suposta", "supostas", "suposto", "supostos", "alegada", "alegadas",
    "alegado", "alegados", "pretensa", "pretensas", "pretenso", "pretensos",
    "acusada", "acusadas", "acusado", "acusados", "chamada", "chamadas",
    "chamado", "chamados",
    # Editorializing
    "notavelmente", "interessantemente", "deve-se ter em mente",
    "claramente", "certamente", "sem dúvida", "é claro", "afortunadamente",
    "felizmente", "infelizmente", "tragicamente", "precocemente",
    # Synonyms for "said"
    "revelou", "revelaram", "indicou", "indicaram", "expôs", "explicou",
    "explicaram",
    "encontrou", "encontraram", "notou", "notaram", "observou", "observaram",
    "insistiu", "insistiram", "especulou", "especularam", "conjeturou",
    "conjeturaram",
    "alegou", "alegaram", "afirmou", "afirmaram", "admitiu", "admitiram",
    "confessou", "confessaram", "negou", "negaram",
    # Lack of precision
    "faleceu", "faleceram", "foi desta para a melhor",
    "foram desta para a melhor", "deu sua vida", "deram suas vidas",
    "local de descanso", "fazer amor", "uma questão com", "danos colaterais",
    "limpeza étnica", "convivendo com o câncer", "sem visão",
    "pessoas com cegueira",
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

    assert portuguese.badwords == pickle.loads(
        pickle.dumps(portuguese.badwords))


def test_informals():
    compare_extraction(portuguese.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    assert portuguese.informals == pickle.loads(
        pickle.dumps(portuguese.informals))


def test_words_to_watch():
    compare_extraction(portuguese.words_to_watch.revision.datasources.matches,
                       WORDS_TO_WATCH, OTHER)

    assert portuguese.words_to_watch == \
        pickle.loads(pickle.dumps(portuguese.words_to_watch))


def test_dictionary():
    cache = {r_text: "A haver, rebeliões: e m80 da Normandia."}
    assert (solve(portuguese.dictionary.revision.datasources.dict_words,
                  cache=cache) ==
            ["A", "haver", "rebeliões", "e", "da", "Normandia"])
    assert (solve(portuguese.dictionary.revision.datasources.non_dict_words,
                  cache=cache) ==
            ["m80"])

    assert (portuguese.dictionary ==
            pickle.loads(pickle.dumps(portuguese.dictionary)))


def test_stopwords():
    cache = {r_text: "Esta a o corrida!"}
    assert (solve(portuguese.stopwords.revision.datasources.stopwords,
                  cache=cache) ==
            ["Esta", "a", "o"])
    assert (solve(portuguese.stopwords.revision.datasources.non_stopwords,
                  cache=cache) ==
            ["corrida"])

    assert portuguese.stopwords == pickle.loads(
        pickle.dumps(portuguese.stopwords))


def test_stemmmed():
    cache = {r_text: "A haver, rebeliões: e m80 da Normandia."}
    assert (solve(portuguese.stemmed.revision.datasources.stems,
                  cache=cache) ==
            ["a", "hav", "rebeliõ", "e", "m80", "da", "normand"])

    assert portuguese.stemmed == pickle.loads(pickle.dumps(portuguese.stemmed))
