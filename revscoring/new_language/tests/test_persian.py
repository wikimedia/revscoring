import pickle

from nose.tools import eq_

from .. import persian
from ...datasources import diff, parent_revision, revision
from ...dependencies import solve

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
