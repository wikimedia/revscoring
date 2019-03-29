import pickle

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.languages import persian

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

r_text = revision_oriented.revision.text


def test_badwords():
    compare_extraction(persian.badwords.revision.datasources.matches,
                       BAD, OTHER)

    assert persian.badwords == pickle.loads(pickle.dumps(persian.badwords))


def test_informals():
    compare_extraction(persian.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    assert persian.informals == pickle.loads(pickle.dumps(persian.informals))


def test_dictionary():
    cache = {r_text: "خشندهٔ اعتصامی معروف به پروین اعتصامی (زاده ۲"}
    assert (solve(persian.dictionary.revision.datasources.dict_words,
                  cache=cache) ==
            ['معروف', 'به', 'پروین', 'زاده'])
    assert (solve(persian.dictionary.revision.datasources.non_dict_words,
                  cache=cache) ==
            ['خشندهٔ', 'اعتصامی', 'اعتصامی'])

    assert (persian.dictionary ==
            pickle.loads(pickle.dumps(persian.dictionary)))


def test_stopwords():
    cache = {r_text: "خشندهٔ اعتصامی معروف به پروین اعتصامی (زاده ۲"}
    assert (solve(persian.stopwords.revision.datasources.stopwords, cache=cache) ==
            ['معروف'])
    assert (solve(persian.stopwords.revision.datasources.non_stopwords,
                  cache=cache) ==
            ['خشندهٔ', 'اعتصامی', 'به', 'پروین', 'اعتصامی', 'زاده'])

    assert persian.stopwords == pickle.loads(pickle.dumps(persian.stopwords))
