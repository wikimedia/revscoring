from .features import Dictionary, RegexMatches

name = "tamil"

try:
    import enchant
    dictionary = enchant.Dict("ta")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'ta'.  " +
                      "Consider installing 'aspell-ta'.")

dictionary = Dictionary(name + ".dictionary", dictionary.check)
"""
:class:`~revscoring.languages.features.Dictionary` features via
:class:`enchant.Dict` "ta". Provided by `aspell-ta`.
"""

badword_regexes = [
    r"பூ(ல்|லு)",
    r"கூதி",
    r"தே(வ|வு)டியா(ள்)",
    r"ஓத்தா?",
    r"சுன்னி",
    r"சுண்ணி",
    r"ஓ(ல்|ழ்|லு|ழு|ழி)",
    r"ஒம்மால",
    r"சூத்து",
    r"முண்(டை|ட)",
    r"புண்(ட|டை)",
    r"தாயோளி",
    r"ஓ(ல்|ழ்)மாரி",
    r"புழுத்தி"
]

badwords = RegexMatches(name + ".badwords", badword_regexes,
                        wrapping=(r"^|[^\w\u0b80-\u0bff]",
                                  r"$|[^\w\u0b80-\u0bff]"))
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
    r"பொட்டை"
]

informals = RegexMatches(name + ".informals", informal_regexes,
                         wrapping=(r"^|[^\w\u0b80-\u0bff]",
                                   r"$|[^\w\u0b80-\u0bff]"))
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
