from .features import Dictionary, RegexMatches, Stopwords

name = "arabic"

try:
    import enchant
    dictionary = enchant.Dict("ar")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'ar'.  " +
                      "Consider installing 'aspell-ar'.")

dictionary = Dictionary(name + ".dictionary", dictionary.check)
"""
:class:`~revscoring.languages.features.Dictionary` features via
:class:`enchant.Dict` "ar".  Provided by `aspell-ar`
"""

stopwords = [
    r"ابن",  # son
    r"اسم",  # name
    r"الاسم",  # the name
    r"البلد",  # the land
    r"الت",
    r"التي",
    r"الثالث",  # third
    r"الثاني",  # second (2nd)
    r"الجديد",
    r"الحديث",
    r"الحيا",
    r"الخاص",
    r"الدول",
    r"الدولي",
    r"الدين",
    r"الذي",
    r"الذين",
    r"الر",
    r"الرسمي",
    r"السابق",
    r"السن",
    r"السياسي",  # political
    r"الصور",  # pictures
    r"العالم",  # the scientist
    r"العالمي",
    r"العام",
    r"العديد",
    r"العرب",  # the Arab
    r"العربي",  # the Arabic
    r"العمل",  # the action
    r"القديم",  # the old
    r"القرن",  # the century
    r"الكبير",  # the great
    r"الكثير",  # the plenty
    r"اللغ",
    r"الله",  # Allah
    r"الم",  # pain (?)
    r"المتحد",
    r"المحيط",
    r"المدين",
    r"المراجع",
    r"المصادر",
    r"المملك",
    r"المنطق",
    r"الموقع",
    r"الميلاد",  # born
    r"الوطني",
    r"الوفا",
    r"الوقت",
    r"الولايات",
    r"اليوم",
    r"انظر",
    r"باسم",
    r"بال",
    r"بداي",
    r"بذر",
    r"بريل",
    r"بسبب",
    r"بشكل",
    r"بعد",
    r"بعض",
    r"بما",
    r"بنا",
    r"بها",
    r"بهذه",
    r"بواب",
    r"بوابات",
    r"بين",
    r"تاريخ",  # date/history
    r"تحت",  # under
    r"تحديد",
    r"تحويل",
    r"تصغير",
    r"تصنيف",
    r"تعليق",
    r"تكون",
    r"تلك",
    r"توضيح",
    r"ثبت",  # record
    r"ثلاث",  # three
    r"ثنا",  # two
    r"جامع",  # comprehensive
    r"جدا",
    r"جديد",
    r"جغرافيا",  # geography
    r"جميع",
    r"جيد",
    r"حال",
    r"حداث",
    r"حسب",
    r"حسن",
    r"حمد",
    r"حول",
    r"حيا",
    r"حيث",
    r"خارجي",
    r"خاص",
    r"خلال",
    r"خير",  # good
    r"دار",
    r"دور",
    r"دول",
    r"دون",  # beneath
    r"ديسمبر",  # december
    r"ذات",
    r"ذلك",
    r"ربع",  # one forth
    r"سبتمبر",  # September
    r"سست",
    r"سلام",  # hello
    r"سلامي",
    r"سنوات",  # years
    r"شخاص",
    r"شريط",
    r"شهر",  # month
    r"صبح",
    r"صفح",  # pages
    r"صور",  # pcitures
    r"ضاف",
    r"طريق",
    r"عاد",
    r"عام",
    r"عبد",
    r"عبر",
    r"عدد",
    r"عربي",  # Arabic
    r"عرض",
    r"عشر",  # 1000
    r"عقد",
    r"علام",
    r"علم",
    r"علي",  # Ali
    r"عليه",
    r"عليها",
    r"عمال",
    r"عمل",  # action
    r"عند",
    r"عندما",
    r"عنه",
    r"عنوان",
    r"غسطس",
    r"غير",  # other
    r"فبراير",
    r"فتر",
    r"فضل",  # goodness
    r"فقد",  # lack
    r"فقط",
    r"فيما",
    r"فيه",  # in
    r"فيها",  # in
    r"قام",
    r"قبل",  # before
    r"قدم",
    r"قيد",
    r"كان",
    r"كانت",
    r"كانوا",
    r"كبر",
    r"كبير",  # great/big
    r"كتاب",  # book
    r"كتوبر",
    r"كثر",
    r"كثير",  # plenty
    r"كما",
    r"كومنز",
    r"لكن",  # but
    r"لها",
    r"ليس",
    r"مارس",  # March
    r"ماكن",
    r"مام",
    r"مايو",
    r"مثل",  # like
    r"مجموع",  # set
    r"محمد",  # Mohammad
    r"مختار",
    r"مختلف",  # different
    r"مدين",
    r"مراجع",
    r"مركز",  # center
    r"مريكي",
    r"مسدود",
    r"مصادر",
    r"مصدر",
    r"مصر",
    r"مصنف",
    r"معلومات",
    r"مقال",
    r"مكان",  # place
    r"ملف",
    r"مما",
    r"منذ",
    r"منطق",
    r"منه",
    r"منها",
    r"منهم",
    r"مواليد",
    r"موقع",
    r"نجليزي",
    r"نسب",
    r"نظر",
    r"نفس",
    r"نها",
    r"نهاي",
    r"نوع",
    r"نوفمبر",
    r"هذا",  # this
    r"هذه",  # this
    r"هناك",  # there
    r"هول",
    r"واحد",  # one
    r"وال",
    r"والتي",
    r"والذي",
    r"وبعد",
    r"وجود",
    r"وذلك",
    r"وسط",
    r"وصل",
    r"وصلات",
    r"وعل",
    r"وفي",  # die / dead
    r"وفيات",  # deathes
    r"وقد",
    r"وكان",
    r"وكانت",
    r"وكذلك",
    r"ولا",  # except
    r"ولد",  # parent
    r"ولكن",  # but
    r"ولم",
    r"وما",
    r"ومن",
    r"وهذا",
    r"وهو",
    r"وهي",
    r"ويكي",  # wiki
    r"يتم",
    r"يتيم",  # orphan
    r"يسي",
    r"يضا",
    r"يعتبر",
    r"يكون",
    r"يمكن",
    r"يناير",
    r"يوجد",
    r"يوليو",
    r"يوم",
    r"يونيو"
]

stopwords = Stopwords(name + ".stopwords", stopwords)
"""
:class:`~revscoring.languages.features.Stopwords` features copied from
"common words" in https://meta.wikimedia.org/wiki/?oldid=15258449
"""

badword_regexes = [
    r"احا",
    r"عاهرا",
    r"زندقتهما",
    r"حمار",  # Donkey
    r"لعن",  # Damn
    r"يلعن",  # Damned
    r"لعنه",  # Damn him/her
    r"امك",  # Your mother
    r"لعنتهما",  # Damn you
    r"فلعنهما",  # So damn you
    r"اعزبوا",
    r"عزبوا",
    r"لدحي",
    r"زبي",
    r"كلب",  # Dog
    r"كافر",  # Kafir
    r"والله",  # Swear to god
    r"الحمار",  # The donkey
    r"الزنا",
    r"النيك",
    r"كلابي",
    r"الكلب",  # The dog
    r"منو",
    r"نجس",
    r"والعياذ",
    r"يتبرز",
    r"الكافر",  # The Kaffir
    r"تتزر",
    r"منكاحا",
    r"وينكح",
    r"منافق",  # Monafigh
    r"الشيطان",  # Satan
]

badwords = RegexMatches(name + ".badwords", badword_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
    r"كالامازوه",
    r"فغانيون",
    r"ومراف",
    r"زوه",
    r"رلا",
    r"بلوجاتي",
    r"كتمتمان",
    r"سراريه",
    r"اجك",
    r"الجيدي",
    r"مناخرهم",
    r"الجيرل",
    r"وخلاخيل",
    r"اكشفي",
    r"ومحاسنه",
    r"يبزقن",
    r"اجهن",
    r"اطهن",
    r"ستنفض",
    r"خطبهن",
    r"اخدون",
    r"غمزني",
    r"فطلقني",
    r"فحكه",
    r"خرق",
    r"وهل",
    r"اللي",
    r"تحرموا",
    r"الزن",
    r"بالنعلين",
    r"وغلامك",
    r"عليلك",
    r"فتحدثها",
    r"اتمن",
    r"الشنبا",
    r"وروراو",
    r"والفاج",
    r"صوردون",
    r"ورجلاي",
    r"وضاحا",
    r"مختار",
    r"نسب",
    r"شيخ",  # Shikh
]

informals = RegexMatches(name + ".informals", informal_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
