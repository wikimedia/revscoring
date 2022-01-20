import pickle

from pytest import mark

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve

from .util import compare_extraction

try:
    from revscoring.languages import hindi
except ImportError:
    # Can't install the enchant dictionary, skip
    pytestmark = mark.nottravis

# Word list provided by
BAD = [
    "मादरचोद",
    "मग्गी",
    "मई चोद",
    "रंडी",
    "टट्टी",
    "चोदा",
    "गांड",
    "मुंह में ले",
    "चूत",
    "भोसडीके",
    "भोसरी",
    "भोसड़ा",
    "ठरकी",
    "त्यागी",
    "चुटिया",
    "चूतिया",
    "भाड़",
    "भड़वा",
    "भड़वे",
    "लौड़े",
    "भोसड्",
    "भुँडी",
    "भोसड़ी के",
    "बर्र",
    "बरसूँगा",
    "कमीना",
    "दिल्ली",
    "बहन चोदा",
    "गांडू",
    "हरामी",
    "हराम",
    "लोडु",
    "रांड",
    "साला",
    "तगद",
    "भोसड़ा",
    "गधा",
    "भड़वा",
    "चुन्नी",
    "गांडफाट",
    "झाट",
    "बकलंड",
    "घस्ति",
    "छिनार",
    "मुट्ठ",
    "पागल",
    "हरामखोर",
    "बहनचोद",
    "गांडू",
    "सूअर",
    "हरामी",
    "हराम जादा",
    "लंड",
    "कुतिया",
    "कमीना",
    "कमीनी",
    "गधा",
    "हिजड़ा",
    "हिज्र",
    "साली",
]
INFORMAL = [
    "फ़ुद्दी",
    "ढीला",
    "अंट",
    "संट",
    "बकचोदी क",
    "बकचोद",
    "भसड",
    "भैंस की",
    "झंड",
    "झण्डूरा",
    "झंडू",
    "झाटु",
    "चक्कर",
    "चाटु",
    "चम्चा",
    "चिरकुट",
    "चालू",
    "दबाना",
    "ढक्कन",
    "दिनचक्",
    "फंडा",
    "घपला",
    "गोली देना",
    "ज्ञान",
    "ज्ञान बा",
    "मजाक",
    "गप",
    "गप मारना",
    "हटके",
    "झाड़ना",
    "जुगाड़",
    "कांड",
    "कबाब में हड्डी",
    "कट ले",
    "खिचड़ी",
    "कोई ना",
    "लेट लतीफ़",
    "मजनूँ",
    "मस्त मोला",
    "माल",
    "पॉटी",
    "पेशाब",
    "उल्लू",
    "लौंडिया",
    "माल",
    "छोड़ा",
    "लोडू",
    "हुग",
    "हगना",
    "झंड",
    "झंडू",
    "हिजड़ा",
    "हिंजडा",
    "हीहीही",
    "हहहा",
    "हुदंग",
    "हुल्लड़",
    "कुत्ते",
    "कुत्ता",
    "अच्छा",
    "वाह",
    "वाह वाह",
    "शाबाश",
    "हैं",
    "सुनो",
    "सुनो ना",
    "और फिर",
    "हां बोलो",
    "सच में",
    "फुद्दू",
    "मूत",
    "चुप कर",
]

OTHER = [
    """नालापत बालमणि अम्मा (എൻ. ബാലാമണിയമ്മ) भारत से मलयालम भाषा की प्रतिभावान
    कवयित्रियों में से एक थीं। वे हिन्दी साहित्य की लेखिका और कवयित्री
    महादेवी वर्मा की समकालीन
    थीं। उनके साहित्य और जीवन पर गांधी जी के विचारों और आदर्शों
    का स्पष्ट प्रभाव रहा।
    उन्होंने मलयालम कविता में उस कोमल शब्दावली का विकास किया जो अभी
    तक केवल संस्कृत
    में ही संभव मानी जाती थी। इसके लिए उन्होंने अपने समय
    के अनुकूल संस्कृत के कोमल
    शब्दों को चुनकर मलयालम का जामा पहनाया। उनकी कविताओं
    का नाद-सौंदर्य और पैनी उ
    क्तियों की व्यंजना शैली अन्यत्र दुर्लभ है। वे प्रतिभावान
    कवयित्री के साथ-साथ बाल
    कथा लेखिका और सृजनात्मक अनुवादक भी थीं। अपने पति वी॰एम॰ नायर के साथ
    मिलकर उन्होने अपनी कई कृतियों का अन्य भाषाओं में अनुवाद किया। अंग्रेजी भाषा
    की भारतीय लेखिका कमला दास उनकी सुपुत्री थीं,
    जिनके लेखन पर उनका खासा असर पड़ा था।
    """
]


@mark.nottravis
def test_badwords():
    compare_extraction(hindi.badwords.revision.datasources.matches, BAD,
                       OTHER)

    assert hindi.badwords == pickle.loads(pickle.dumps(hindi.badwords))


@mark.nottravis
def test_informals():
    compare_extraction(hindi.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    assert hindi.informals == pickle.loads(pickle.dumps(hindi.informals))


@mark.nottravis
def test_dictionary():
    cache = {revision_oriented.revision.text: 'पहनाया उनकी कविताओं worngly.'}
    assert (solve(hindi.dictionary.revision.datasources.dict_words, cache=cache) ==
            ["पहनाया", "उनकी"])
    assert (solve(hindi.dictionary.revision.datasources.non_dict_words,
                  cache=cache) ==
            ["कविताओं", "worngly"])

    assert hindi.dictionary == pickle.loads(pickle.dumps(hindi.dictionary))
