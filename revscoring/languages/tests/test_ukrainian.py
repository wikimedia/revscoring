import pickle

from nose.tools import eq_

from .. import ukrainian
from ...datasources import revision_oriented
from ...dependencies import solve
from .util import compare_extraction

BAD = [
    "довбойоб", "сучий", "ебать", "пісяти", "серун", "бздюха", "бздюх",
    "матюгальники", "їбе", "вйоб", "дристало", "серуха", "мудак",
    "дристун", "задниці", "матюкайтеся", "гімно", "залупа", "блять",
    "бля", "дибіли", "їбати", "хуя", "срака", "сраку", "говно", "пізда",
    "пісяють", "пизда", "какають", "хуйня", "підарешт", "гавно", "хуй"
]

INFORMAL = [
    "здох", "фігня", "лол", "лох", "лохи"
]

OTHER = [
    """
    потовщена, ущільнена і міцна передня пара крил у комах низки рядів.
    Виконують переважно захисну функцію. Утворення твердих і міцних
    надкрил стало ключовим моментом в еволюції комах і дозволило низці
    груп опанувати такі різні середовища як повітря, деревина, ґрунт і
    вода, заселити найрізноманітніші екологічні ніші. Надкрила деяких
    видів комах застосовують у декоративно-ужитковому мистецтві.
    Вивчення будови та механічних властивостей надкрил може стати у
    нагоді для конструкторів аерокосмічної техніки та композитних
    матеріалів.
    """,
]

r_text = revision_oriented.revision.text


def test_badwords():
    compare_extraction(ukrainian.badwords.revision.datasources.matches,
                       BAD, OTHER)

    eq_(ukrainian.badwords, pickle.loads(pickle.dumps(ukrainian.badwords)))


def test_informals():
    compare_extraction(ukrainian.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    eq_(ukrainian.informals, pickle.loads(pickle.dumps(ukrainian.informals)))


def test_dictionary():
    cache = {r_text: 'потовщена, ущільнена і, worngly. <td>'}
    eq_(solve(ukrainian.dictionary.revision.datasources.dict_words,
              cache=cache),
        ['потовщена', 'ущільнена', 'і'])
    eq_(solve(ukrainian.dictionary.revision.datasources.non_dict_words,
              cache=cache),
        ["worngly"])

    eq_(ukrainian.dictionary, pickle.loads(pickle.dumps(ukrainian.dictionary)))


def test_stopwords():
    cache = {r_text: "ущільнена і міцна передня як крил у комах."}
    eq_(solve(ukrainian.stopwords.revision.datasources.stopwords, cache=cache),
        ["як"])
    eq_(solve(ukrainian.stopwords.revision.datasources.non_stopwords,
        cache=cache),
        ['ущільнена', 'і', 'міцна', 'передня', 'крил', 'у', 'комах'])

    eq_(ukrainian.stopwords, pickle.loads(pickle.dumps(ukrainian.stopwords)))
