import pickle

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.languages import spanish

from .util import compare_extraction

BAD = [
    "aweonao",
    "awevo",
    "babosa",
    "boludo",
    "buseta",
    "cabron", "cabrón", "cabrones", "cabrones",
    "caca",
    "caga", "cagada", "cagado",
    "cago", "cagon", "cagones",
    "caquita",
    "carajo",
    "chichornia",
    "chiguero",
    "chimar",
    "chinga", "chingada", "chingadazo", "chingaderita", "chingaderitas",
    "chingado", "chingados", "chingoncisimo", "chingonería",
    "chingones", "chingonsicimo", "chingonsisimo", "chingorrón", "chinguen",
    "chinoncicimo",
    "chosto",
    "chupame", "chupamea", "chupamela", "chupan", "chupar", "chupenmela",
    "cochetumadre",
    "cojio", "cojones",
    "coño",
    "culero", "culeros",
    "culiaos", "culito",
    "cupan",
    "desmadrado", "desmadrar", "desmadrarse", "desmadre",
    "dlaversh",
    "emputado",
    "enc", "encabronadas", "encabronado", "encabronar", "encabronarse",
    "encronada",
    "enputado",
    "follaban", "follar",
    "fregon", "fregón",
    "gamberro",
    "gilipollas",
    "golfa",
    "guevo", "guevon", "guevones",
    "guey", "güey",
    "güila",
    "hifueputa",
    "hijodeputa", "hijodeputas", "hijodputa", "hijodputas", "hijoduta",
    "huevon", "huevones", "huevospateados",
    "idiota", "idiotas",
    "imbecil", "imbécil", "imbeciles", "imbesil",
    "jetear",
    "jidiota",
    "jilipollas", "jilipuertas",
    "joder", "jodido",
    "jotas", "joterias",
    "joto", "jotos",
    "komekaka",
    "lamadre",
    "madreado", "madrear",
    "malparida", "malparidos",
    "mamada", "mamadas", "mamaguevo", "mamon", "mamon", "mamón", "mamones",
    "marica", "maricas", "maricon", "maricones", "marika",
    "marrano",
    "meapelan",
    "cagoenlaleche",
    "mecastralamadre",
    "chupan", "melapelan",
    "merda", "merga",
    "mergas", "vergas",
    "mierda", "mierdas",
    "mimsn",
    "mojon",
    "monda",
    "nemames", "nememes", "nomames",
    "ogt", "ogts",
    "ojete",
    "pamearlo",
    "pajaro",
    "pattaya",
    "pedos",
    "pelan",
    "pelotudo", "pelotudos",
    "pendejada", "pendejadas",
    "pendejo", "pendejos",
    "pene", "penes",
    "perras",
    "petardas", "petardo",
    "picha", "pichula",
    "pija", "pijas",
    "pinche", "pinches",
    "pirobos",
    "pitito", "pito", "pitos", "pitote",
    "polla", "pollas", "pollas",
    "poronga",
    "puta", "putamadre", "putas",
    "putisima", "putisimo", "putiza",
    "puto", "puton", "putos",
    "sorete",
    "tajodido",
    "tetas",
    "tontos", "tonta",
    "trolo",
    "uta", "utama", "utamadre",
    "verga", "vergas",
    "vergasos", "vergazos", "verguda", "vergudo",
    "versh",
    "violo",
    "watdafuq",
    "webon", "webonada", "webones",
    "puta",
    "zorra", "zorrear",
]

INFORMAL = [
    "aki",
    "amaona",
    "amigui",
    "amo", "amooo", "amoooo",
    "asi",
    "atte",
    "bla", "blablabla", "blah", "blahblahblah",
    "bobos",
    "bubis",
    "chafa",
    "chale",
    "chí",
    "chido",
    "chilear", "chiliar",
    "esq",
    "estupida", "estúpida", "estupidas", "estupides", "estupido", "estupido",
    "estupidos", "estúpidos",
    "grasias",
    "grax",
    "holaaaaa", "holi", "holis", "holis", "hoooola", "hooooli",
    "ijos",
    "inserta",
    "jaja", "jajaja", "jajajaja", "jeje", "jejejeje",
    "ke",
    "kiero",
    "komo",
    "loco", "loko", "lokos",
    "lol", "lolololololololololol", "looooooool",
    "madrazo",
    "mensos",
    "metia",
    "migis", "miguis",
    "muxo",
    "nocheto",
    "nooooo",
    "nop",
    "oooli", "oooola",
    "osea",
    "pipi",
    "plis",
    "popo",
    "porfavor", "por favor",
    "porque", "por que", "porke", "porq", "porqe",
    "porquería", "porquerías",
    "profe",
    "pupu",
    "qiero",
    "shí",
    "sierto",
    "siiii",
    "soi",
    "tambn", "tmbn",
    "tkm",
    "tqm",
    "vallanse",
    "wena", "weno",
    "wey",
    "XD", "xdd", "xddddd"
]

OTHER = [
    """
    Su cuerpo es largo y estilizado, de un color gris parduzco, menos en su
    parte inferior, que es blanquecina. Existen dos subespecies diferenciadas:
    el rorcual del norte, que tiene su hábitat en el Atlántico Norte, y el
    rorcual antártico, de mayor tamaño, que vive habitualmente en aguas del
    océano Antártico. Puede verse en los principales océanos del planeta,
    desde las aguas polares a las tropicales.
    """,
]

r_text = revision_oriented.revision.text


def test_badwords():
    compare_extraction(spanish.badwords.revision.datasources.matches,
                       BAD, OTHER)

    assert spanish.badwords == pickle.loads(pickle.dumps(spanish.badwords))


def test_informals():
    compare_extraction(spanish.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    assert spanish.informals == pickle.loads(pickle.dumps(spanish.informals))


def test_dictionary():
    cache = {r_text: 'Su cuerpo es largo y worngly. <td>'}
    assert (solve(spanish.dictionary.revision.datasources.dict_words, cache=cache) ==
            ['Su', 'cuerpo', 'es', 'largo', 'y'])
    assert (solve(spanish.dictionary.revision.datasources.non_dict_words,
                  cache=cache) ==
            ["worngly"])

    assert spanish.dictionary == pickle.loads(pickle.dumps(spanish.dictionary))


def test_stopwords():
    cache = {r_text: "Su cuerpo es largo y estilizado, está áreas."}
    assert (solve(spanish.stopwords.revision.datasources.stopwords, cache=cache) ==
            ['Su', 'es', 'y', 'está'])
    assert (solve(spanish.stopwords.revision.datasources.non_stopwords,
                  cache=cache) ==
            ['cuerpo', 'largo', 'estilizado', 'áreas'])

    assert spanish.stopwords == pickle.loads(pickle.dumps(spanish.stopwords))


def test_stemmmed():
    cache = {r_text: "Su cuerpo es largo y estilizado, está áreas."}
    assert (solve(spanish.stemmed.revision.datasources.stems, cache=cache) ==
            ['su', 'cuerp', 'es', 'larg', 'y', 'estiliz', 'esta', 'are'])

    assert spanish.stemmed == pickle.loads(pickle.dumps(spanish.stemmed))
