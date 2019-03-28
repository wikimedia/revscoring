import pickle

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.languages import arabic

from .util import compare_extraction

BAD = [
    "احا",
    "عاهرا",
    "زندقتهما",
    "حمار",
    "لعن",
    "يلعن",
    "لعنه",
    "امك",
    "لعنتهما",
    "فلعنهما",
    "اعزبوا",
    "عزبوا",
    "لدحي",
    "زبي",
    "كلب",
    "كافر",
    "والله",
    "الحمار",
    "الزنا",
    "النيك",
    "كلابي",
    "الكلب",
    "منو",
    "نجس",
    "والعياذ",
    "يتبرز",
    "الكافر",
    "تتزر",
    "منكاحا",
    "وينكح",
    "منافق",
    "الشيطان",
]

INFORMAL = [
    "كالامازوه",
    "فغانيون",
    "ومراف",
    "زوه",
    "رلا",
    "بلوجاتي",
    "كتمتمان",
    "سراريه",
    "اجك",
    "الجيدي",
    "مناخرهم",
    "الجيرل",
    "وخلاخيل",
    "اكشفي",
    "ومحاسنه",
    "يبزقن",
    "اجهن",
    "اطهن",
    "ستنفض",
    "خطبهن",
    "اخدون",
    "غمزني",
    "فطلقني",
    "فحكه",
    "خرق",
    "وهل",
    "اللي",
    "تحرموا",
    "الزن",
    "بالنعلين",
    "وغلامك",
    "عليلك",
    "فتحدثها",
    "اتمن",
    "الشنبا",
    "وروراو",
    "والفاج",
    "صوردون",
    "ورجلاي",
    "وضاحا",
    "مختار",
    "نسب",
    "شيخ",
]

OTHER = [
    """يقوم تاريخ علم الأحياء بدراسة الأحياء من الزمن القديم إلى المعاصر.
    مع أن مفهوم علم الأحياء كمجال واحد متماسك ظهر في القرن التاسع عشر،
    فإن علوم الأحياء ظهرت من تقاليد الطب والتاريخ الطبيعي المأخوذة من
    أيورفيدا، الطب المصري القديم وكتابات أرسطو وجالينوس في العصور اليونانية
    والرومانية القديمة. تم تطوير هذا العمل القديم خلال القرون الوسطى من قبل
    الأطباء والعلماء المسلمين مثل ابن سينا. خلال عصر النهضة الأوروبية وبداية
    العصر الحديث، تم تحديث الفكر في علم الأحياء في أوروبا بسبب الاهتمام المتجدد
    بالفلسفة التجريبية واكتشاف العديد من الكائنات الحية التي لم تكن معروفة
    """
]


def test_badwords():
    compare_extraction(arabic.badwords.revision.datasources.matches, BAD,
                       OTHER)

    assert arabic.badwords == pickle.loads(pickle.dumps(arabic.badwords))


def test_informals():
    compare_extraction(arabic.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    assert arabic.informals == pickle.loads(pickle.dumps(arabic.informals))


def test_dictionary():
    cache = {revision_oriented.revision.text: 'التي لم تكن معروفة  worngly.'}
    assert (solve(arabic.dictionary.revision.datasources.dict_words, cache=cache) ==
            ["التي", "لم", "تكن", "معروفة"])
    assert (solve(arabic.dictionary.revision.datasources.non_dict_words,
                  cache=cache) ==
            ["worngly"])

    assert arabic.dictionary == pickle.loads(pickle.dumps(arabic.dictionary))


def test_stopwords():
    cache = {revision_oriented.revision.text: 'التي لم تكن معروفة'}
    assert (solve(arabic.stopwords.revision.datasources.stopwords,
            cache=cache) == ['التي', 'لم'])
    assert (solve(arabic.stopwords.revision.datasources.non_stopwords,
                  cache=cache) ==
            ['تكن', 'معروفة'])

    assert arabic.stopwords == pickle.loads(pickle.dumps(arabic.stopwords))
