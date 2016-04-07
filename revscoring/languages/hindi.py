from .features import Dictionary, RegexMatches, Stopwords

name = "hindi"

try:
    import enchant
    dictionary = enchant.Dict("hi")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'hi'.  " +
                      "Consider installing 'aspell-hi'.")

dictionary = Dictionary(name + ".dictionary", dictionary.check)
"""
:class:`~revscoring.languages.features.Dictionary` features via
:class:`enchant.Dict` "hi".  Provided by `aspell-hi`
"""

badword_regexes = [
    "मादरचोद ",
    "मग्गी ",
    "मई चोद ",
    "रंडी ",
    "टट्टी ",
    "चोदा",
    "गांड ",
    "मुंह में ले ",
    "चूत",
    "भोसडीके",
    "भोसरी ",
    "भोसड़ा ",
    "ठरकी",
    "त्यागी",
    "चुटिया ",
    "चूतिया ",
    "भाड़ ",
    "भड़वा ",
    "भड़वे ",
    "लौड़े ",
    "भोसड्",
    "भुँडी ",
    "भोसड़ी के ",
    "बर्र ",
    "बरसूँगा ",
    "कमीना ",
    "दिल्ली ",
    "बहन चोदा",
    "गांडू",
    "हरामी ",
    "हराम ",
    "लोडु ",
    "रांड ",
    "साला ",
    "तगद ",
    "भोसड़ा ",
    "गधा ",
    "भड़वा ",
    "चुन्नी ",
    "गांडफाट",
    "झाट",
    "बकलंड ",
    "घस्ति ",
    "छिनार",
    "मुट्ठ ",
    "पागल ",
    "हरामखोर ",
]

badwords = RegexMatches(name + ".badwords", badword_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
    "फ़ुद्दी ",
    "ढीला ",
    "अंट",
    "संट",
    "बकचोदी क",
    "बकचोद",
    "भसड",
    "भैंस की ",
    "झंड",
    "झण्डूरा ",
    "झंडू ",
    "झाटु",
    "चक्कर",
    "चाटु",
    "चम्चा",
    "चिरकुट",
    "चालू",
    "दबाना",
    "ढक्कन",
    "दिनचक् ",
    "फंडा",
    "घपला",
    "गोली देना ",
    "ज्ञान ",
    "ज्ञान बा",
    "मजाक ",
    "गप",
    "गप मारना",
    "हटके",
    "झाड़ना ",
    "जुगाड़ ",
    "कांड ",
    "कबाब में हड्डी",
    "कट ले",
    "खिचड़ी",
    "कोई ना",
    "लेट लतीफ़",
    "मजनूँ ",
    "मस्त मोला",
    "माल",
    "पॉटी ",
    "पेशाब ",
    "उल्लू ",
    "लौंडिया ",
    "माल ",
    "छोड़ा ",
    "लोडू ",
    "हुग ",
    "हगना",
    "झंड ",
    "झंडू ",
    "हिजड़ा ",
    "हिंजडा ",
    "हीहीही ",
    "हहहा ",
    "हुदंग",
    "हुल्लड़",
    "कुत्ते ",
    "कुत्ता "
]

informals = RegexMatches(name + ".informals", informal_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
