import sys

import enchant

from .language import Language, LanguageUtility

try:
    DICTIONARY = enchant.Dict("fa")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'fa'.  " +
                      "Consider installing 'myspell-fa'.")

REVERENTWORDS = set([
    ur"آله", ur"فرموده?",ur"فرمودند",ur"السلام",ur"حضرت\b",ur"\([سعص]\)",ur"\(ره\)",ur"\(قس\)",
    ur"\(عج\)",ur"\bامام\b",ur"فرمودند",ur"روحی?‌? ?ا?ل?فدا",ur"شَ?هید\b",ur"آزادهٔ? سرا?فراز",
    ur"شادروان",ur"جهانخوار",ur"مستکبر", ur"ملحد",ur"ملعون", ur"عل[يی]ه‌? ?السلام",
    ur"(لعن[تة]|رحمت|صلی|صلوات|سلام)‌? ?اللہ",ur"دام‌? ?(ظلّ?ه|برکات)",ur"قدس‌? ?سره‌? ?شریف",
    ur"اسقف محترم",ur"خدا[یش]? بیامرز",ur"دار فانی",ur"به هلاکت",ur"سَقط شد",ur"ا?علیا?‌? ?حضرت",
    ur"خادم خادمان", ur"مقام معظّ?م",ur"(حرم|مرقد) مطهر",ur"\bمرحوم\b",ur"\bشهادت",ur"شاهنشاه\b",
    ur"علیها", ur"مد ?ظله"])

BADWORDS_FINGLISH = set([
    ur"(madar|nanae|zan|khahar)\s*?(ghahbeh|ghahveh|ghabe|jendeh?|be khata)",
    ur"khar madar",ur"khar kos deh",
    ur"([qkc]+o+s+|[qkc]+o+n+|[qkc]+i+r+|m+e+g+h+a+d)\s*?((va|o)\s*?[qkc]oon|lis|pareh?|k+h+a+r+|[qkc]esh|nane|nanat|babat|khah?a?r|abjit|mi ?dad|mi ?dah[iy]|[qkc]on|deh|khor|goshad|gondeh|[qkc]oloft|[qkc]esh|mashang|khol|baz|shenas|nag[uo]o?|maghz|sh[ae]r)",
    ur"\bmameh?",ur"sho+[mn]bo+l",ur"\brazl",ur"gaei?d[ia]m",ur"\bk+i+r+i+",ur"\bk+o+s+o+",ur"\bk+o+n+i+",
    ur"j+e+n+d+e+h?",ur"[qkc]iram",ur"(pedar|baba|naneh?|tokhme?) sag",ur"pedasag",ur"bi (sho+r|shour|sharaf|namo+s)",
    ur"madareto?",ur"\bamato?",ur"da[iy]o+s",ur"goh? ?nakhor",ur"\bashghal",ur"\bavazi"])


BADWORDS = set([
    ur"کیرم", ur"کونی", ur"برووتو", ur"لعنت", ur"کاکاسیاه", ur"آشغال", ur"گائیدم", ur"گوزیده", ur"مشنگ", ur"ننتو", ur"بخواب",
    ur"\b((ما\.?در|ننه|زن|خو?اه?ر) ?(خرابه|ق\.?[حه]\.?ب\.?ه|قحبه|قبه|ج\.?ن\.?د\.?ه|به خطا)",
    ur"خار مادر",ur"خوار کس ده",
    ur"\b([کك]+س+|[کك]+و+ن+|[کك]+[یي]+ر+|مقعد|عضو ?تحتانی|ما?تحت)\s*(و کون|لیسی?|پاره|خر|[کك]ش|نن[هت]\b|بابات|خو?اه?ر|آبجیت|هم ?شیره|می ?داد|می ?ده?ی|می ?کنی?|کن|خور)",
    ur"\b[کك]+(و+ن|س)\s*(خر|گشاد|گنده|کش|مشنگ|پاره|ننت|ننه\b|خل|باز|خور\b|شناس|نگو|مغز|ه؟ ؟شعر|و ?شعر|مادر|خو?اه?ر|آبجیت|هم ?شیره|داد)",
    ur"شو?مبول",ur"\bممه\b",
    ur"ر[زذ]ل\b",ur"[کك]+[یي]+ر+\s*م?(ی|خر|(ب|)خور|تو[ی ]|مو |دهن)",
    ur"گا[يئی]ید[میي]",ur"گاهييد[نه]",ur"بگامت\b",ur"(پدر|ننه|مادر|بابا|تخم)\s*سگ",
    ur"بی ?(شعور|شرف|ناموس)[یي]", ur"\پريودى\؟",ur"مادرت گا",
    ur"تنت میخاره", ur"به کیرم",ur"به گا ميدم",ur"\bبگای?د",
    ur"برای مادرت",ur"دیو[سث]\b",ur"\bننتو",ur"گوزید[نه]?",ur"\bگه نخور",ur"انگشت به كون",
    ur"\bچاکت\b",ur"\bجنده",ur"گه اضاف[يی] خورد[هیي]",ur"خاک تو سرت",
    ur"[کك][یي]رم\b",ur"ر[یي]د[همی]\b",ur"[کك]ون ?ده",ur"[کك]س ?ده",
    ur"گا[یي]ش",ur"ب[کك]ن ب[کك]ن",ur"([کك]+[یي]+ر+)ی+\b",
    ur"(به پشت|دمر|دمرو) بخواب",ur"خایه لیس",ur"حسن کلیدساز",ur"\bکره خر",
    ur"آشغال ع+و+ض+ی+",ur"پدسگ",ur"سا[کك] زد",ur"فاک (‌فنا|یو\b)",ur"برو (گ+م+ش+و\b|ب+م+ی+ر+\b)",
    ur"\bگوه خورد",ur"\bشاش اضافه",ur"آب [کك][یي]رو?\b",ur"[کك]و?س [کك]ردن?\b",ur"[کك][یي]ر [کك]لفت",
    ur"کیونده",ur"جر دادن?",ur"مردک\b")]

def is_misspelled_process():
    def is_misspelled(word):
        return not DICTIONARY.check(word)
    return is_misspelled


def is_badword_process():
    def is_badword(word):
        return word.lower() in BADWORDS
    return is_badword


is_badword = LanguageUtility("is_badword", is_badword_process, depends_on=[])
is_misspelled = LanguageUtility("is_misspelled", is_misspelled_process,
                                depends_on=[])

sys.modules[__name__] = Language(__name__, [is_badword, is_misspelled])
"""
Implements :class:`~revscoring.languages.language.Language` for Persian/Farsi.
:data:`~revscoring.languages.language.is_badword` and
:data:`~revscoring.languages.language.is_misspelled` are provided.
"""
