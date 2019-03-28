import pickle

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.languages import catalan

from .util import compare_extraction

BAD = [
    'cabron',
    'cabrones',
    'caca',
    'caga',
    'cagar',
    'cago',
    'capullo',
    'catalufo',
    'catalufos',
    'cojones',
    'cony',
    'coño',
    'chocho',
    'chuper',
    'chupame',
    'cul',
    'culito',
    'culo',
    'coi',
    'facha',
    'fatxa',
    'folla',
    'follar',
    'follen',
    'gay',
    'gilipollas',
    'gordo',
    'gorda',
    'guarra',
    'imbecil',
    'imbècil',
    'joder',
    'maricon',
    'marimacha',
    'mariposon',
    'meadas',
    'merda',
    'merdas',
    'merdes',
    'mierda',
    'mierdas',
    'minga',
    'mocos',
    'mojon',
    'moro',
    'negrata',
    'paja',
    'pajero',
    'paki',
    'pedo',
    'pene',
    'penes',
    'penis',
    'pipi',
    'polla',
    'pollas',
    'polles',
    'popo',
    'porno',
    'puta',
    'putas',
    'putes',
    'puticlub',
    'puto',
    'putos',
    'rabo',
    'ramera',
    'separata',
    'subnormal',
    'tonta',
    'tonto',
    'tontos',
    'trolo',
    'vergas',
    'vibrador',
    'xdd',
    'xddd',
    'zorra',
]

INFORMAL = [
    'asi',
    'bienvenido',
    'bienvenidos',
    'esto',
    'estúpid',
    'jaja',
    'jajaja',
    'jajajaja',
    'haha',
    'hehe',
    'hola',
    'holi',
    'hosti',
    'hostia',
    'hòstia',
    'ignorant',
    'llamo',
    'lol',
    'malparit',
    'muaha',
    'merci',
    'nadie',
    'osti',
    'quede',
    'quereis',
    'resto',
    'soy',
    'traga',
    'tranqui',
    'visca',
    'viva',
    'vuestros',
    'xd',
    'xupa',
    'wtf',
]

OTHER = [
    """Els cromatòfors són cèl·lules amb pigments a l'interior que reflecteixen
    la llum. Poden trobar-se en diversos éssers vius, com els amfibis, els
    peixos, certs crustacis i alguns cefalòpodes. Són els principals
    responsables del color de la pell, del color dels ulls en els animals
    ectoterms i de la formació de la cresta neural al llarg del desenvolupament
    embrionari."""
]

r_text = revision_oriented.revision.text


def test_badwords():
    compare_extraction(catalan.badwords.revision.datasources.matches,
                       BAD, OTHER)

    assert catalan.badwords == pickle.loads(pickle.dumps(catalan.badwords))


def test_informals():
    compare_extraction(catalan.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    assert catalan.informals == pickle.loads(pickle.dumps(catalan.informals))


def test_dictionary():
    cache = {r_text: "diferència dels animals worngly"}
    assert (solve(catalan.dictionary.revision.datasources.dict_words,
            cache=cache) == ['diferència', 'dels', 'animals'])
    assert (solve(catalan.dictionary.revision.datasources.non_dict_words,
                  cache=cache) ==
            ['worngly'])

    assert catalan.dictionary == pickle.loads(pickle.dumps(catalan.dictionary))
