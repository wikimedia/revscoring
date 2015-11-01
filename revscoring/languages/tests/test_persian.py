import pickle

from nose.tools import eq_

from .. import persian
from ...datasources import revision
from ...dependencies import solve
from .util import compare_extraction

BAD = [
    "جنده",
    "کاکاسیاه",
    "آشغال",
    "آله",
    "ایتالیک",
    "بخواب",
    "برووتو",
    "جمهورمحترم",
    "فرمود",
    "فرمودند",
    "فرموده",
    "لعنت",
    "مشنگ",
    "ننتو",
    "کون",
    "کونی",
    "کیر",
    "گائیدم",
    "گوزیده",
    "کیرم"
]

INFORMAL = [

]

OTHER = [
    """
    رخشندهٔ اعتصامی معروف به پروین اعتصامی (زاده ۲۵ اسفند ۱۲۸۵ در تبریز –
    درگذشته ۱۵ فروردین ۱۳۲۰ در تهران) شاعر ایرانی بود گه از وی به عنوان
    «مشهورترین شاعر زن ایران یاد شده است.» اعتصامی از کودکی فارسی، انگلیسی
    و عربی را نزد پدرش آموخت و از همان کودکی تحت نظر پدرش و استادانی
    چون دهخدا و ملک الشعرای بهار سرودن شعر را آغاز کرد. پدر وی یوسف اعتصامی،
    از شاعران و مترجمان معاصر ایرانی بود که در شکل‌گیری زندگی هنری پروین و کشف
    استعداد و گرایش وی به سرودن شعر نقش مهمی داشت.
    """
]


def test_badwords():
    compare_extraction(persian.revision.badwords_list, BAD, OTHER)


def test_informals():
    compare_extraction(persian.revision.informals_list, INFORMAL, OTHER)


def test_revision():
    # Words
    cache = {revision.text: "I have an m80; and a shovel."}
    eq_(solve(persian.revision.words_list, cache=cache),
        ["I", "have", "an", "m80", "and", "a", "shovel"])

    # Misspellings
    cache = {revision.text: 'رخشندهٔ  معروف به پروین  worngly. <td>'}
    eq_(solve(persian.revision.misspellings_list, cache=cache), ["worngly"])


def test_pickling():

    eq_(persian, pickle.loads(pickle.dumps(persian)))
