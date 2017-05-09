from .features import Dictionary, RegexMatches, Stopwords

name = "bengali"

try:
    import enchant
    dictionary = enchant.Dict("bn")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'bn'.  " +
                      "Consider installing 'aspell-bn'.")

dictionary = Dictionary(name + ".dictionary", dictionary.check)
"""
:class:`~revscoring.languages.features.Dictionary` features via
:class:`enchant.Dict` "bn".  Provided by `aspell-bn`
"""

stopwords = [
    r"অক",
    r"অঞ",
    r"অন",
    r"অনেক",
    r"অব",
    r"অবস",
    r"অর",
    r"অসম",
    r"আছে",
    r"আন",
    r"আর",
    r"আরও",
    r"ইংরেজি",
    r"ইতিহাস",
    r"ইন",
    r"উত",
    r"উদ",
    r"উল",
    r"এই",
    r"এক",
    r"একটি",
    r"এছাড",
    r"এটি",
    r"এবং",
    r"এর",
    r"ওয",
    r"কর",
    r"করতে",
    r"করা",
    r"করার",
    r"করে",
    r"করেন",
    r"কাজ",
    r"কার",
    r"কিছু",
    r"কিন",
    r"কে",
    r"কেন",
    r"চল",
    r"চিত",
    r"ছিল",
    r"ছিলেন",
    r"জন",
    r"জাতীয",
    r"টার",
    r"ঠিত",
    r"তথ",
    r"তন",
    r"তবে",
    r"তমান",
    r"তর",
    r"তাদের",
    r"তার",
    r"তালিকা",
    r"তিনি",
    r"থাকে",
    r"থান",
    r"থেকে",
    r"দক",
    r"দিয",
    r"দেখুন",
    r"দেয",
    r"দেশ",
    r"নয",
    r"নাম",
    r"নামে",
    r"নিয",
    r"নির",
    r"পড",
    r"পর",
    r"পরবর",
    r"পার",
    r"পুনর",
    r"পূর",
    r"বছর",
    r"বন",
    r"বয",
    r"বর",
    r"বলে",
    r"বহিঃসংযোগ",
    r"বাংলাদেশ",
    r"বার",
    r"বাস",
    r"বিভিন",
    r"বিশ",
    r"বিষয",
    r"বে",
    r"বের",
    r"ভারত",
    r"ভারতীয",
    r"ভাষা",
    r"মধ",
    r"মাধ",
    r"মার",
    r"যক",
    r"যন",
    r"যসূত",
    r"যান",
    r"যায",
    r"যার",
    r"যুক",
    r"যের",
    r"রতিষ",
    r"রথম",
    r"রধান",
    r"রয",
    r"রহণ",
    r"রান",
    r"রায",
    r"রিয",
    r"রে",
    r"রেণী",
    r"রের",
    r"শিক",
    r"শুরু",
    r"সংখ",
    r"সংস",
    r"সঙ",
    r"সম",
    r"সময",
    r"সর",
    r"সাথে",
    r"সালে",
    r"সালের",
    r"সূত",
    r"হতে",
    r"হন",
    r"হয",
    r"হিসেবে",
]

stopwords = Stopwords(name + ".stopwords", stopwords)
"""
:class:`~revscoring.languages.features.Stopwords` features copied from
"common words" in https://meta.wikimedia.org/wiki/?oldid=16626444
"""

badword_regexes = [
    r"মাগি",
    r"magi",
    r"মাগী",
    r"বাল",
    r"পর্নো",
    r"পর্ণো",
    r"বেশ্যা",
    r"নষ্টা",
    r"মগা",
    r"আবাল",
    r"পেনিস",
    r"নিগ্রো",
    r"পায়খান",
    r"সেক্সি",
    r"সেক্স",
    r"চটি",
    r"(চুত|চুদ)মারা(নি|নী)",
    r"(ছু|চু)+(ধা|দা)(ছু|চু)(ধি|দি)",
    r"চু(দি|দী)",
]

badwords = RegexMatches(name + ".badwords", badword_regexes,
                        wrapping=(r'^|[^\w\u0980-\u09FF]',
                                  r'$|[^\w\u0980-\u09FF]'))
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
    r"কর",
    r"করবি",
    r"থাম",
    r"হাহা",
    r"হাহাহা",
    r"হাহাহাহা",
    r"lol",
    r"লোল",
    r"লুল",
    r"ইউজার",
    r"ইউজ",
    r"ব্লা",
    r"ব্লাব্লা",
    r"জান",
    r"বিশ্রী",
    r"প্লিজ",
    r"পেত্নী",
]

informals = RegexMatches(name + ".informals", informal_regexes,
                         wrapping=(r'^|[^\w\u0980-\u09FF]',
                                   r'$|[^\w\u0980-\u09FF]'))
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
