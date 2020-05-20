import pickle

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.languages import galician

from .util import compare_extraction

BAD = [
    'tetas',
    'pis',
    'pedo',
    'zorra',
    'cabron',
    'cabrón',
    'caca',
    'caga',
    'carallo',
    'coño',
    'follar',
    'fuck',
    'maricon',
    'maricón',
    'merda',
    'mierda',
    'pendejo',
    'polla',
    'pollas',
    'puta',
    'putas',
    'puto',
    'putos',
    'stupid',
    'tonto',
    'verga',
    'porno',
    'estupido',
    'estupidos',
    'estupida',
    'estupidas',
    'estúpido',
    'estúpidos',
    'estúpida',
    'estúpidas',
    'chúpame',
    'cerdo',
    'cerdos',
    'cerda',
    'cerdas',
    'imbecil',
    'imbécil',
    'cagada',
    'mamada',
    'concha',
    'gilipollas',
]

INFORMAL = [
    'jajaja',
    'jajajaja',
    'ola',
    'adeus'
]

OTHER = [
    """
    A táboa periódica dos elementos é unha disposición en formato de táboa dos
    elementos químicos, ordenados polo seu número atómico, configuración
    electrónica e propiedades químicas recorrentes. Esta ordenación presenta
    unhas tendencias periódicas, como por exemplo a presenza de elementos
    semellantes na mesma columna. Presenta tamén catro bloques con propiedades
    químicas semellantes. As filas da táboa denomínanse períodos, mentres
    que as columnas chámanse grupos. Seis destes grupos teñen nomes xeralmente
    aceptados ademais de números. A táboa periódica pode utilizarse para
    derivar relacións entre as propiedades dos elementos e predicir as
    propiedades de novos elementos aínda non descubertos ou obtidos de
    maneira sintética.
    """
]


def test_badwords():
    compare_extraction(galician.badwords.revision.datasources.matches, BAD,
                       OTHER)

    assert galician.badwords == pickle.loads(pickle.dumps(galician.badwords))


def test_informals():
    compare_extraction(galician.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    assert galician.informals == pickle.loads(pickle.dumps(galician.informals))


def test_dictionary():
    cache = {revision_oriented.revision.text: 'táboa períodos worngly.'}
    assert (solve(galician.dictionary.revision.datasources.dict_words,
                  cache=cache) ==
            ['táboa', 'períodos'])
    assert (solve(galician.dictionary.revision.datasources.non_dict_words,
                  cache=cache) ==
            ["worngly"])

    assert galician.dictionary == pickle.loads(pickle.dumps(galician.dictionary))


def test_stopwords():
    cache = {
        revision_oriented.revision.text: 'Aínda que non se sabe moito'}
    assert (solve(galician.stopwords.revision.datasources.stopwords,
            cache=cache) == ['que', 'non'])
    assert (solve(galician.stopwords.revision.datasources.non_stopwords,
                  cache=cache) ==
            ['Aínda', 'se', 'sabe', 'moito'])

    assert galician.stopwords == pickle.loads(pickle.dumps(galician.stopwords))
