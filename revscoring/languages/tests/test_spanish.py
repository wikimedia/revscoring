import pickle

from nose.tools import eq_

from .. import spanish
from ...datasources import revision
from ...dependencies import solve

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
    "meachupan",
    "meapelan",
    "mecagoenlaleche",
    "mecastralamadre",
    "melachupan", "melapelan",
    "merda", "merga",
    "mevalemergas", "mevalevergas",
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
    "yjodeputa",
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
    compare_extraction(spanish.revision.badwords_list, BAD, OTHER)


def test_informals():
    compare_extraction(spanish.revision.informals_list, INFORMAL, OTHER)


def test_revision():
    # Words
    cache = {revision.text: "Su cuerpo es largo y estilizado, está áreas."}
    eq_(solve(spanish.revision.words_list, cache=cache),
        ["Su", "cuerpo", "es", "largo", "y", "estilizado", "está", "áreas"])

    # Misspellings
    cache = {revision.text: 'Su cuerpo es largo y worngly. <td>'}
    eq_(solve(spanish.revision.misspellings_list, cache=cache), ["worngly"])

    # Infonoise
    cache = {revision.text: "Su cuerpo es largo!"}
    eq_(solve(spanish.revision.infonoise, cache=cache), 9/15)


def test_presence():
    assert hasattr(spanish.revision, "words")
    assert hasattr(spanish.revision, "content_words")
    assert hasattr(spanish.revision, "badwords")
    assert hasattr(spanish.revision, "informals")
    assert hasattr(spanish.revision, "misspellings")

    assert hasattr(spanish.parent_revision, "words")
    assert hasattr(spanish.parent_revision, "content_words")
    assert hasattr(spanish.parent_revision, "badwords")
    assert hasattr(spanish.parent_revision, "informals")
    assert hasattr(spanish.parent_revision, "misspellings")

    assert hasattr(spanish.diff, "words_added")
    assert hasattr(spanish.diff, "badwords_added")
    assert hasattr(spanish.diff, "informals_added")
    assert hasattr(spanish.diff, "misspellings_added")
    assert hasattr(spanish.diff, "words_removed")
    assert hasattr(spanish.diff, "badwords_removed")
    assert hasattr(spanish.diff, "informals_removed")
    assert hasattr(spanish.diff, "misspellings_removed")


def test_pickling():

    eq_(spanish, pickle.loads(pickle.dumps(spanish)))
