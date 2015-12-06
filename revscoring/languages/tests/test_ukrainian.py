import pickle

from nose.tools import eq_

from .. import ukrainian
from ...datasources import revision
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


def test_badwords():
    compare_extraction(ukrainian.revision.badwords_list, BAD, OTHER)


def test_informals():
    compare_extraction(ukrainian.revision.informals_list, INFORMAL, OTHER)


def test_revision():
    # Words
    cache = {revision.text: "потовщена, ущільнена і m80, передня пара."}
    eq_(solve(ukrainian.revision.words_list, cache=cache),
        ["потовщена", "ущільнена", "і", "m80", "передня", "пара"])

    # Misspellings
    cache = {revision.text: 'потовщена, ущільнена і, worngly. <td>'}
    eq_(solve(ukrainian.revision.misspellings_list, cache=cache), ["worngly"])


def test_pickling():

    eq_(ukrainian, pickle.loads(pickle.dumps(ukrainian)))
