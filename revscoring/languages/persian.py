from .features import Dictionary, RegexMatches, Stopwords

name = "persian"

try:
    import enchant
    dictionary = enchant.Dict("fa")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'fa'.  " +
                      "Consider installing 'myspell-fa'.")

dictionary = Dictionary(name + ".dictionary", dictionary.check)
"""
:class:`~revscoring.languages.features.Dictionary` features via
`enchant.Dict <https://github.com/rfk/pyenchant>`_ "fa".  Provided by `myspell-fa`
"""

stopwords = set([
    "آثار", "آری", "آغاز", "آمریکا",
    "آنها", "اثر", "اساس", "است", "استان",
    "استفاده", "اسلام", "اسلامی", "اشاره",
    "اصلی", "اطلاعات", "افراد", "اما",
    "امکان", "انبار", "انجام", "اندازه",
    "انگلیسی", "اهالی", "اهل", "اول",
    "اولین", "اين", "اگر", "ایالات", "ایران",
    "ایرانی", "این", "بار", "بازیابی",
    "باشد", "بانی", "باید", "بخش", "بدون",
    "برای", "برخی", "بزرگ", "بسیار",
    "بسیاری", "بعد", "بنا", "بناهای",
    "بود", "بودند", "بوده",
    "بیرون", "بیش", "بیشتر", "بین",
    "تاریخ", "تاریخی", "ترتیب",
    "تشکیل", "تصویر", "تغییر",
    "تلفن", "تمام", "تنها",
    "تهران", "توجه", "توسط",
    "جعبه", "جلالی", "جمله",
    "جنگ", "جهان", "جهانی", "حال",
    "حدود", "حذف", "حروف", "خرد", "خود",
    "داد", "داده", "دارای", "دارد", "دارند",
    "داشت", "داشته", "دانشگاه",
    "درباره", "درگذشتگان", "دست", "دلیل",
    "دهد", "دور", "دوران", "دوره",
    "دوم", "دیرینگی", "دیگر", "دیگری",
    "راه", "رده", "رسمی", "روز", "روی",
    "زادگان", "زبان", "زمان", "زمانی",
    "زمینه", "زنده", "زندگی", "زیادی",
    "زیر", "ساخت", "ساخته", "سازمان",
    "سال", "سال‌های", "سده", "سرعت",
    "سپتامبر", "سیاسی", "شامل", "شدن",
    "شدند", "شده", "شده‌است", "شرکت",
    "شهر", "شهرستان", "شود", "صفحه",
    "صورت", "علی", "عنوان", "غیر",
    "فارسی", "فعالیت", "فعلی", "فهرست",
    "فوریه", "قبل", "قدیمی", "قرار",
    "مالک", "مانند", "ماه", "متحده", "محل",
    "محلی", "محمد", "مختلف",
    "مدرک", "مردم", "مرمت", "مرکز",
    "مرکزی", "مرگ", "مسکونی",
    "مسیر", "معروف", "مقاله", "مقاله‌های",
    "ملی", "منابع", "مناطق", "منبع",
    "منطقه", "مورد", "میان",
    "میلادی", "می‌باشد", "می‌توان",
    "می‌دهد", "می‌شود", "می‌شوند", "می‌کند",
    "می‌کنند", "نادرست", "ناشر",
    "نام", "نام‌های", "نشان", "نشانی", "نشریه",
    "نظر", "نفر", "نوع", "نویسنده",
    "نیز", "نیست", "های", "هزار", "هستند",
    "همان", "همراه", "همه", "همچنین",
    "همین", "وابسته", "واقع", "وبگاه", "وب‌گاه",
    "وجود", "ولی", "ویکی",
    "پانویس", "پایان", "پایه", "پرونده",
    "پیش", "پیوند", "چند", "چون", "ژورنال",
    "کار", "کاربری", "کتاب", "کرد",
    "کردن", "کردند", "کرده", "کشور",
    "کشورهای", "کند", "کنند", "کنونی",
    "گرفت", "گرفته", "گروه", "گفته",
    "یافت", "یونسکو", "یکی"
])

stopwords = Stopwords(name + ".stopwords", stopwords)
"""
:class:`~revscoring.languages.features.Stopwords` features copied from
"common words" in https://meta.wikimedia.org/wiki/?oldid=13044766
"""

badword_regexes = [
    r"(madar|nanae|zan|khahar)\s*?(ghahbeh|ghahveh|ghabe|jendeh?|be khata)",
    r"khar madar",  # Sister and mother (only used in swears)
    r"khar kos deh",  # Sister is whore
    # Pussy|ass|penis|anus (open so I (suck|tear|fuck)|sister|pimp|your mother
    # |your father|sister|was fucked|is fucked|male prostitute|sucker|big|big
    # |thick|dumb|dumb|fucker|expert!|don't say|nonsense)
    r"(?:[qkc]+o+s+|[qkc]+o+n+|[qkc]+i+r+|m+e+g+h+a+d)\s*?((?:va|o)" +
    r"\s*?[qkc]oon|lis|pareh?|k+?h+?a+?r+?|[qkc]esh|nane|nanat|babat" +
    r"|khah?a?r|abjit|mi ?dad|mi ?dah[iy]|[qkc]on|deh" +
    r"|khor|goshad|gondeh|[qkc]oloft|[qkc]esh|mashang" +
    r"|khol|baz|shenas|nag[uo]o?|maghz|sh[ae]r)",
    r"mameh?",  # boob
    r"sho+[mn]bo+l",  # dick in childern language
    r"razl",  # asshole
    r"gaei?d[ia]m",  # I fucked
    r"k+?i+?r+?i+?",  # dick
    r"k+?o+?s+?o+?",  # pussy
    r"k+?o+?n+?i+?",  # male prostitue
    r"j+?e+?n+?d+?e+?h?",  # female prostitue
    r"[qkc]iram",  # my dick
    r"(?:pedar|baba|naneh?|tokhme?) sag",  # your (father|dad|mother) is dog
    r"pedasag",  # your father is dog
    r"bi (?:sho+?r|shour|sharaf|namo+?s)",  # asshole
    r"madareto?",  # your mother
    r"amato?",  # your aunt
    r"da[iy]o+?s",  # pimp
    r"goh? ?nakhor",  # literally: don't eat shit
    r"ashghal",  # garbage
    r"avazi",  # jerk
    r"کیرم",  # my dick
    r"کونی",  # male prostitute
    r"برووتو",  # go inside (dick in something)
    r"لعنت",  # damn
    r"کاکاسیاه",  # nigger
    r"آشغال",  # garbage
    r"گائیدم",  # I fucked
    r"گوزیده",  # farted
    r"مشنگ",  # dumb
    r"ننتو",  # your mother
    r"بخواب",  # lie down
    r"خار مادر",  # mother and sister
    r"خوار کس ده",  # sister is prostitute
    r"شو?مبول",  # dick in childern language, used to call someone's dick to
    # imply it's as small as childern dick
    r"جنده",  # female prostitue
    r"کاکاسیاه",  # nigger
    r"آشغال",  # garbage
    r"آله",  # and his family (used in prayers for religous figures)
    r"ایتالیک",  # italic
    r"بخواب",  # lie down
    r"برووتو",  # go inside
    r"جمهورمحترم",  # dear president
    r"فرمود",  # said (used for religous figures)
    r"فرمودند",  # ibid
    r"فرموده",  # ibid
    r"لعنت",  # damn
    r"مشنگ",  # dumb
    r"ننتو",  # your mother
    r"کون",  # ass
    r"کونی",  # male prostitute
    r"کیر",  # dick
    r"گائیدم",  # I fucked
    r"گوزیده",  # farted
    r"کیرم",  # my dick
    r"ممه",  # boob
    # your (mother|sister|wife) is prostitute|whore
    r"(?:ما+?در|ننه|زن|خو?اه?ر) ?(?:خرابه|ق+?[حه]+?ب+?ه|قحبه|قبه|" +
    r"ج+?ن+?د+?ه|به خطا)",
    # (pussy|ass|dick|anus|bottom organism)
    # (and ass|sucker|torn|ass|mother|father|sister|
    # was fucked|is fucked|fucks|fucker|sucker)
    r"(?:[کك]+?س+?|[کك]+?و+?ن+?|[کك]+?[یي]+?ر+?|مقعد|عضو " +
    r"?تحتانی|ما?تحت)\s*(?:و کون|لیسی?|پاره|خر|[کك]ش|نن[هت]\b|بابات|خو?اه?ر|" +
    r"آبجیت|هم ?شیره|می ?داد|می ?ده?ی|می ?کنی?|کن|خور)",
    # (Ass|Pussy) (donkey|open|big|pimp|torn|your mother|mother|dumb|expert
    # dont't say|dumb|nonsense|mother|sister|your sister|sister|was fucked)
    r"[کك]+(و+ن|س)\s*(?:خر|گشاد|گنده|کش|مشنگ|پاره|ننت|ننه\b|خل|" +
    r"باز|خور|شناس|نگو|مغز|ه؟ ؟شعر|و ?شعر|مادر|خو?اه?ر|آبجیت|هم ?شیره|داد)",
    r"ر[زذ]ل",  # jerk
    # (ass|suck|fuck|mouth) (my)? dick
    r"[کك]+?[یي]+?ر+?\s*م?(ی|خر|(ب|)خور|تو[ی ]|مو |دهن)",
    r"گا[يئی]ید[میي]",  # fucked
    r"گاهييد[نه]",  # fucking
    r"بگامت",  # I fuck you
    r"بی ?(شعور|شرف|ناموس)[یي]",  # dumb|jerk|
    r"(پدر|ننه|مادر|بابا|تخم)\s*سگ",  # son of dog
    r"پريودى\؟",  # you are having period
    r"مادرت گا",  # your mother fuck
    r"تنت میخاره",  # you like to fight
    r"به کیرم",  # To my dick (means I don't give a shit)
    r"به گا ميدم",  # I fuck
    r"بگای?د",  # fuck
    r"انگشت به كون",  # fingering
    r"برای مادرت",  # To your mother
    r"دیو[سث]",  # pimp
    r"ننتو",  # Your mother
    r"گوزید[نه]?",  # Fart
    r"گه نخور",  # Don't eat shit
    r"چاکت",  # your pussy
    r"جنده",  # slut
    r"گه اضاف[يی] خورد[هیي]",  # eating extra shit
    r"خاک تو سرت",  # soli on your head
    r"[کك][یي]رم",  # dick
    r"ر[یي]د[همی]",  # (I|you|he|she|they) pooped
    r"[کك]ون ?ده",  # male prostitute
    r"[کك]س ?ده",  # female prostitute
    r"گا[یي]ش",  # To fuck
    r"ب[کك]ن ب[کك]ن",  # fuck fuck
    r"(?:[کك]+?[یي]+?ر+?)ی+",  # dick
    r"(?:به پشت|دمر|دمرو) بخواب",  # lie down
    r"خایه لیس",  # balls sucker
    r"حسن کلیدساز",  # Hasan locksmith (a swaer targeting Rouhani)
    r"کره خر",  # Son of donkey
    r"آشغال ع+?و+?ض+?ی+?",  # Jerk
    r"پدسگ",  # short form of "son of dog"
    r"سا[کك] زد",  # sucked (dick)
    r"فاک (‌?:فنا|یو)",  # "fuck"
    r"برو (?:گ+?م+?ش+?و|ب+?م+?ی+?ر+?)",  # go away
    r"گوه خورد",  # ate shit
    r"شاش اضافه",  # extra piss
    r"آب [کك][یي]رو?",  # semen
    r"[کك]و?س [کك]ردن?",  # to fuck pussy
    r"[کك][یي]ر [کك]لفت",  # big dick
    r"کیونده",  # Afghan varient of male prostitute
    r"جر دادن?",  # tearing (informal)
    r"مردک"  # man (very informal)
]

badwords = RegexMatches(name + ".badwords", badword_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
    r"آله", r"فرموده?", r"فرمودند", r"السلام", r"حضرت", r"\([سعص]\)",
    r"\(ره\)",
    r"\(قس\)",
    r"\(عج\)", r"امام", r"فرمودند", r"روحی?‌? ?ا?ل?فدا",
    r"شَ?هید", r"آزادهٔ? سرا?فراز",
    r"شادروان", r"جهانخوار", r"مستکبر", r"ملحد", r"ملعون",
    r"(?:لعن[تة]|رحمت|صلی|صلوات|سلام)‌? ?اللہ", r"دام‌? ?(?:ظلّ?ه|برکات)",
    r"قدس‌? ?سره‌? ?شریف", r"عل[يی]ه‌? ?السلام",
    r"اسقف محترم", r"خدا[یش]? بیامرز", r"دار فانی", r"به هلاکت",
    r"سَقط شد", r"ا?علیا?‌? ?حضرت",
    r"خادم خادمان", r"مقام معظّ?م", r"(?:حرم|مرقد) مطهر", r"مرحوم",
    r"شهادت", r"شاهنشاه",
    r"علیها", r"مد ?ظله"
]

informals = RegexMatches(name + ".informals", informal_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
