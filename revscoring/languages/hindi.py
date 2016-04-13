from .features import Dictionary, RegexMatches

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
    r"मादरचोद",
    r"मग्गी",
    r"मई चोद",
    r"रंडी",
    r"टट्टी",
    r"चोदा",
    r"गांड",
    r"मुंह में ले",
    r"चूत",
    r"भोसडीके",
    r"भोसरी",
    r"भोसड़ा",
    r"ठरकी",
    r"त्यागी",
    r"चुटिया",
    r"चूतिया",
    r"भाड़",
    r"भड़वा",
    r"भड़वे",
    r"लौड़े",
    r"भोसड्",
    r"भुँडी",
    r"भोसड़ी के",
    r"बर्र",
    r"बरसूँगा",
    r"कमीना",
    r"दिल्ली",
    r"बहन चोदा",
    r"गांडू",
    r"हरामी",
    r"हराम",
    r"लोडु",
    r"रांड",
    r"साला",
    r"तगद",
    r"भोसड़ा",
    r"गधा",
    r"भड़वा",
    r"चुन्नी",
    r"गांडफाट",
    r"झाट",
    r"बकलंड",
    r"घस्ति",
    r"छिनार",
    r"मुट्ठ",
    r"पागल",
    r"हरामखोर"
]

badwords = RegexMatches(name + ".badwords", badword_regexes,
                        wrapping=(r'^|[^\w\u0901-\u0963]',
                                  r'$|[^\w\u0901-\u0963]'))
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
    r"फ़ुद्दी",
    r"ढीला",
    r"अंट",
    r"संट",
    r"बकचोदी क",
    r"बकचोद",
    r"भसड",
    r"भैंस की",
    r"झंड",
    r"झण्डूरा",
    r"झंडू",
    r"झाटु",
    r"चक्कर",
    r"चाटु",
    r"चम्चा",
    r"चिरकुट",
    r"चालू",
    r"दबाना",
    r"ढक्कन",
    r"दिनचक्",
    r"फंडा",
    r"घपला",
    r"गोली देना",
    r"ज्ञान( बा)?",
    r"मजाक",
    r"गप( मारना)?",
    r"हटके",
    r"झाड़ना",
    r"जुगाड़",
    r"कांड",
    r"कबाब में हड्डी",
    r"कट ले",
    r"खिचड़ी",
    r"कोई ना",
    r"लेट लतीफ़",
    r"मजनूँ",
    r"मस्त मोला",
    r"माल",
    r"पॉटी",
    r"पेशाब",
    r"उल्लू",
    r"लौंडिया",
    r"माल",
    r"छोड़ा",
    r"लोडू",
    r"हुग",
    r"हगना",
    r"झंड",
    r"झंडू",
    r"हिजड़ा",
    r"हिंजडा",
    r"हीहीही",
    r"हहहा",
    r"हुदंग",
    r"हुल्लड़",
    r"कुत्ते",
    r"कुत्ता"
]

informals = RegexMatches(name + ".informals", informal_regexes,
                         wrapping=(r'^|[^\w\u0901-\u0963]',
                                   r'$|[^\w\u0901-\u0963]'))
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
