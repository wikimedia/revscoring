import pickle

from nose.tools import eq_

from .. import russian
from ...datasources import revision_oriented
from ...dependencies import solve
from .util import compare_extraction

BAD = [
    "анал",
    "бля", "блядь", "блять",
    "бомжеград",
    "выкипидар", "выкипидары", "выкипидор", "выкипидоры",
    "гандон",
    "говна", "говно",
    "гондон",
    "дебил", "дебилы",
    "дерьмо",
    "дибил", "дибилы",
    "дырочка",
    "ебал", "ебали", "ебать",
    "жид", "жиды",
    "жопа", "жопе", "жопо", "жопу", "жопы",
    "ибаццо",
    "клизмофил", "клизмофилия",
    "лохом",
    "мрази", "мразь",
    "мудак",
    "нах", "нахуй",
    "нерусь",
    "нехуй",
    "отъеби", "отъебись", "отъебли",
    "педераст", "педерасты",
    "пидар", "пидарас", "пидарасы", "пидарок", "пидары",
    "пидор", "пидорас", "пидорасы", "пидорок", "пидоры",
    "пизда", "пиздец", "пиздой", "пизды",
    "писька",
    "писюн",
    "попку",
    "сосал",
    "сосать",
    "сосет", "сосёт",
    "соси", "сосите",
    "сосут",
    "сука", "суки",
    "сученок", "сучёнок",
    "твари",
    "трахал", "трахала", "трахали", "трахалась",
    "ублюдочные", "ублюдочный",
    "урод", "уроды",
    "фекальные",
    "херней", "херня",
    "хуев", "хуевы", "хуевый",
    "хуета",
    "хуи", "хуй",
    "хуя", "хуями",
    "хуйней", "хуйнёй", "хуйню", "хуйня",
    "чмо",
    "чурки",
    "шлюха",
    "щачло"
]

INFORMAL = [
    "lol",
    "арёл",
    "безопасносте",
    "блин",
    "быдло",
    "голактеко",
    "доблестне",
    "кароч", "кароче", "короче",
    "лол",
    "ляля", "ляляля",
    "онотоле",
    "отстой",
    "поганые",
    "превед",
    "пук",
    "сиськи",
    "статейки",
    "упячка",
    "ха", "хаха", "хахаха",
    "чувак",
    "чувиха",
    "чушь",
    "ыыы", "ыыыы", "ыыыыы"
]

OTHER = [
    """
    многочисленными войнами, приведшими к захвату обширных территорий
    в западном Средиземноморье, утраченных Римской империей в V веке.
    В качестве христианского императора Юстиниан считал своим долгом
    восстановить прежние границы государства. На востоке он продолжил
    войну с Персией, начатую в правление его предшественника Юстина I,
    и конфликты на этом направлении продолжались с перерывами до 562
    года. На западе Юстиниан вёл успешные войны с возникшими на
    территории Западной Римской империи варварскими королевствами.
    В результате войны 533—534 годов было завоёвано королевство
    вандалов и аланов в Северной Африке, а война с остготами в 535—554
    годах принесла Византии власть над Италией. Менее успешные войны с
    королевством вестготов привели к расширению византийских владений
    в Испании.
    """,
]

r_text = revision_oriented.revision.text


def test_badwords():
    compare_extraction(russian.badwords.revision.datasources.matches,
                       BAD, OTHER)

    eq_(russian.badwords, pickle.loads(pickle.dumps(russian.badwords)))


def test_informals():
    compare_extraction(russian.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    eq_(russian.informals, pickle.loads(pickle.dumps(russian.informals)))


def test_dictionary():
    cache = {r_text: 'прежние границы государства worngly. <td>'}
    eq_(solve(russian.dictionary.revision.datasources.dict_words, cache=cache),
        ['прежние', 'границы', 'государства'])
    eq_(solve(russian.dictionary.revision.datasources.non_dict_words,
              cache=cache),
        ["worngly"])

    eq_(russian.dictionary, pickle.loads(pickle.dumps(russian.dictionary)))


def test_stopwords():
    cache = {r_text: "начатую в правление его предшественника I"}
    eq_(solve(russian.stopwords.revision.datasources.stopwords, cache=cache),
        ['в', 'его'])
    eq_(solve(russian.stopwords.revision.datasources.non_stopwords,
        cache=cache),
        ['начатую', 'правление', 'предшественника', 'I'])

    eq_(russian.stopwords, pickle.loads(pickle.dumps(russian.stopwords)))


def test_stemmmed():
    cache = {r_text: "На востоке он продолжил войну с Персией"}
    eq_(solve(russian.stemmed.revision.datasources.stems, cache=cache),
        ['на', 'восток', 'он', 'продолж', 'войн', 'с', 'перс'])

    eq_(russian.stemmed, pickle.loads(pickle.dumps(russian.stemmed)))
