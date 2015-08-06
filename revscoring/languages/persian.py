import sys

import enchant

from .language import Language, LanguageUtility

try:
    DICTIONARY = enchant.Dict("fa")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'fa'.  " +
                      "Consider installing 'myspell-fa'.")

INFORMAL_REGEXES = set([
    #Partial words
    r"آله", r"فرموده?",r"فرمودند",r"السلام",r"حضرت\b",r"\([سعص]\)",r"\(ره\)",r"\(قس\)",
    r"\(عج\)",r"\bامام\b",r"فرمودند",r"روحی?‌? ?ا?ل?فدا",r"شَ?هید\b",r"آزادهٔ? سرا?فراز",
    r"شادروان",r"جهانخوار",r"مستکبر", r"ملحد",r"ملعون", r"عل[يی]ه‌? ?السلام",r"جناب",
    r"(لعن[تة]|رحمت|صلی|صلوات|سلام)‌? ?اللہ",r"دام‌? ?(ظلّ?ه|برکات)",r"قدس‌? ?سره‌? ?شریف",
    r"اسقف محترم",r"خدا[یش]? بیامرز",r"دار فانی",r"به هلاکت",r"سَقط شد",r"ا?علیا?‌? ?حضرت",
    r"خادم خادمان", r"مقام معظّ?م",r"(حرم|مرقد) مطهر",r"\bمرحوم\b",r"\bشهادت",r"شاهنشاه\b",
    r"علیها", r"مد ?ظله",r"ایشان",r"منظورشان",r"ماشالا",
    #Slangy verbs
    r"(ن?می‌? ?|ب|ن)([یا]فشون|پاشون|پرورون|پرون|پوسون|پوشون|پیچون|تابون|تازون|"+
        r"ترسون|ترکون|تکون|تون|جنبون|جوشون|چپون|چربون|چرخون|چرون|چسبون|چشون|چکون|"+
        r"چلون|خارون|خراشون|خشکون|خندون|خوابون|خورون|خون|خیسون|درخشون|د|دون|رسون|"+
        r"رقصون|ر|رنجون|رون|سابون|ستون|سوزون|ش|شورون|شین|غلتون|فهمون|کش|کوبون|"+
        r"گذرون|گردون|گریون|گزین|گسترون|گ|گنجون|لرزون|لغزون|لمبون|مالون|مون|ا?نداز|"+
        r"نشون|هراسون|وزون)(م|ی|ه|یم|ید|ن)",
    r"(ن?می‌? ?|ب|ن)([اآ]|چا|خا|خوا)(م|ی|د|یم|ید|ن)",
    r"(ن?می‌? ?|ب|ن)([یا]رز|[یا]فت|[یا]فراز|[یا]فروز|[یا]ندیش|[یا]نگیز|ایست|"+
        r"ی?[اآ]زار|ی?[اآ]فرین|ی?[اآ]مرز|ی?[اآ]میز|ی?[اآ]ور|ی?[اآ]ویز|بار|باز|"+
        r"باف|بال|بخش|بر|بلع|بند|بوس|بین|پاش|پذیر|پر|پراکن|پرداز|پرس|پرست|پرور|"+
        r"پز|پسند|پلک|پندار|پوس|پوش|پیچ|پیوند|تاب|تپ|تراش|ترس|ترش|ترک|جنب|جنگ|جه|"+
        r"جو|جوش|چاپ|چپ|چر|چرب|چرخ|چسب|چش|چک|چین|خار|خر|خز|خشک|خند|خواب|خور|دار|"+
        r"در|درخش|دزد|دم|دو|دوز|دوش|رس|رقص|رنج|ریز|رین|زار|زن|ساب|ساز|سپار|سنج|شاش|"+
        r"شکاف|شکف|شکن|شمر|شناس|شنو|شور|طپ|طلب|غر|غلت|فرست|فروش|فریب|فهم|قاپ|کار|"+
        r"کن|کوب|گذار|گذر|گرد|گری|گریز|گستر|گمار|گند|گوز|گیر|لرز|لغز|لنگ|لول|لیس|"+
        r"ماس|مال|مک|میر|ناز|نال|نگر|نواز|نورد|نویس|هراس|ورز|وز|یاب)(ه|ن)",
    r"(ن?می‌? ?|ب|ن)(پا|زا|کاه|گا)ن",
    #Slangy adverbs or words
    r"(ازش|انگار|اونه?ا|ایشون|اینجوری?|این[وه]|بازم|باهاش|براتون|برام|برای[مت]ا?ن?|"+
        r"به[مش]|بی‌خیال|تموم|چ?جوری|چیه|دیگه|کدوم|مونده|ول)",
    #Salutation words
    r"(ارادتمندم?|ببخشید|بفرما|جناب|خدمت[تم][وا]?ن?|خوبی|خودت[وا]ن|خودم[وا]ن|خوشحالم|"+
        r"خوشم|درود|دوستدار|سپاسگزارم|سلام|شرمنده|شماست|فلانی|مبارک|متشکرم|محترمت[وا]ن|"+
        r"مخالفم|مرسی|ممنونم?|منظورت[وا]ن|موافقم|نظر[تم][وا]?ن?|نظرم|یادت[وا]ن)",
    #wikipedia words
    r"(بحث\:|بحثم|کاربر\:|میان‌ویکی|ویکی‌? ?فا\b)",
    ])


BAD_REGEXES  = set([
    #Fingilish bad words 
    r"(madar|nanae|zan|khahar)\s*?(ghahbeh|ghahveh|ghabe|jendeh?|be khata)",
    r"khar madar",r"khar kos deh",
    r"([qkc]+o+s+|[qkc]+o+n+|[qkc]+i+r+|m+e+g+h+a+d)\s*?((va|o)\s*?[qkc]oon|"+
        r"lis|pareh?|k+h+a+r+|[qkc]esh|nane|nanat|babat|khah?a?r|abjit|mi ?dad"+
        r"|mi ?dah[iy]|[qkc]on|deh|khor|goshad|gondeh|[qkc]oloft|[qkc]esh|mashang"+
        r"|khol|baz|shenas|nag[uo]o?|maghz|sh[ae]r)",
    r"\bmameh?",r"sho+[mn]bo+l",r"\brazl",r"gaei?d[ia]m",r"\bk+i+r+i+",r"\bk+o+s+o+",
    r"\bk+o+n+i+",r"j+e+n+d+e+h?",r"[qkc]iram",r"(pedar|baba|naneh?|tokhme?) sag",
    r"pedasag",r"bi (sho+r|shour|sharaf|namo+s)",    r"madareto?",r"\bamato?",
    r"da[iy]o+s",r"goh? ?nakhor",r"\bashghal",r"\bavazi",
    #Persian bad words 
    r"کیرم", r"کونی", r"برووتو", r"لعنت", r"کاکاسیاه", r"آشغال", r"گائیدم", r"گوزیده",
    r"مشنگ", r"ننتو", r"بخواب",r"خار مادر",r"خوار کس ده",r"شو?مبول",r"\bممه\b",
    r"\b((ما\.?در|ننه|زن|خو?اه?ر) ?(خرابه|ق\.?[حه]\.?ب\.?ه|قحبه|قبه|ج\.?ن\.?د\.?ه|به خطا)",
    r"\b([کك]+س+|[کك]+و+ن+|[کك]+[یي]+ر+|مقعد|عضو ?تحتانی|ما?تحت)\s*(و کون|لیسی?|پاره|خر|"+
        r"[کك]ش|نن[هت]\b|بابات|خو?اه?ر|آبجیت|هم ?شیره|می ?داد|می ?ده?ی|می ?کنی?|کن|خور)",
    r"\b[کك]+(و+ن|س)\s*(خر|گشاد|گنده|کش|مشنگ|پاره|ننت|ننه\b|خل|باز|خور\b|شناس|نگو|مغز|"+
        r"ه؟ ؟شعر|و ?شعر|مادر|خو?اه?ر|آبجیت|هم ?شیره|داد)",
    r"ر[زذ]ل\b",r"[کك]+[یي]+ر+\s*م?(ی|خر|(ب|)خور|تو[ی ]|مو |دهن)",
    r"گا[يئی]ید[میي]",r"گاهييد[نه]",r"بگامت\b",r"(پدر|ننه|مادر|بابا|تخم)\s*سگ",
    r"بی ?(شعور|شرف|ناموس)[یي]", r"\پريودى\؟",r"مادرت گا",
    r"تنت میخاره", r"به کیرم",r"به گا ميدم",r"\bبگای?د",
    r"برای مادرت",r"دیو[سث]\b",r"\bننتو",r"گوزید[نه]?",r"\bگه نخور",r"انگشت به كون",
    r"\bچاکت\b",r"\bجنده",r"گه اضاف[يی] خورد[هیي]",r"خاک تو سرت",
    r"[کك][یي]رم\b",r"ر[یي]د[همی]\b",r"[کك]ون ?ده",r"[کك]س ?ده",
    r"گا[یي]ش",r"ب[کك]ن ب[کك]ن",r"([کك]+[یي]+ر+)ی+\b",
    r"(به پشت|دمر|دمرو) بخواب",r"خایه لیس",r"حسن کلیدساز",r"\bکره خر",
    r"آشغال ع+و+ض+ی+",r"پدسگ",r"سا[کك] زد",r"فاک (‌فنا|یو\b)",r"برو (گ+م+ش+و\b|ب+م+ی+ر+\b)",
    r"\bگوه خورد",r"\bشاش اضافه",r"آب [کك][یي]رو?\b",r"[کك]و?س [کك]ردن?\b",r"[کك][یي]ر [کك]لفت",
    r"کیونده",r"جر دادن?",r"مردک\b")]

BAD_REGEX = re.compile("|".join(BAD_REGEXES))
INFORMAL_REGEX = re.compile("|".join(INFORMAL_REGEXES))


def is_badword_process():
    def is_badword(word):
        return bool(BAD_REGEX.match(word.lower()))
    return is_badword
is_badword = LanguageUtility("is_badword", is_badword_process, depends_on=[])


def is_informal_word_process():
    def is_informal_word(word):
        return bool(INFORMAL_REGEX.match(word.lower()))
    return is_informal_word
is_informal_word = LanguageUtility("is_informal_word",is_informal_word_process, depends_on=[])

def is_misspelled_process():
    def is_misspelled(word):
        return not DICTIONARY.check(word)
    return is_misspelled

is_misspelled = LanguageUtility("is_misspelled", is_misspelled_process, depends_on=[])


sys.modules[__name__] = Language(__name__, [is_badword, is_misspelled,is_informalword])
"""
Implements :class:`~revscoring.languages.language.Language` for Persian/Farsi.
:data:`~revscoring.languages.language.is_badword` and
:data:`~revscoring.languages.language.is_informalword` and
:data:`~revscoring.languages.language.is_misspelled` are provided.
"""
