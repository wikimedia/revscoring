import pickle

from pytest import mark

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.languages import bengali

from .util import compare_extraction

BAD = [
    "magi",
    "মাগী",
    "বাল",
    "পর্নো",
    "পর্ণো",
    "বেশ্যা",
    "নষ্টা",
    "মগা",
    "আবাল",
    "পেনিস",
    "নিগ্রো",
    "পায়খান",
    "সেক্সি",
    "সেক্স",
    "চটি",
]

INFORMAL = [
    "কর",
    "করবি",
    "থাম",
    "হাহা",
    "হাহাহা",
    "হাহাহাহা",
    "lol",
    "লোল",
    "লুল",
    "ইউজার",
    "ইউজ",
    "ব্লা",
    "ব্লাব্লা",
    "জান",
    "বিশ্রী",
    "প্লিজ",
    "পেত্নী",
]

OTHER = [
    """
    সত্যজিৎ রায় একজন ভারতীয় চলচ্চিত্র নির্মাতা ও বিংশ শতাব্দীর অন্যতম শ্রেষ্ঠ
    চলচ্চিত্র পরিচালক। কলকাতা শহরে সাহিত্য ও শিল্পের জগতে খ্যাতনামা এক বাঙালি
    পরিবারে তাঁর জন্ম হয়। তিনি কলকাতার প্রেসিডেন্সি কলেজ ও শান্তিনিকেতনে
    রবীন্দ্রনাথ ঠাকুরের প্রতিষ্ঠিত বিশ্বভারতী বিশ্ববিদ্যালয়ে পড়াশোনা করেন।
    সত্যজিতের কর্মজীবন একজন বাণিজ্যিক চিত্রকর হিসেবে শুরু হলেও প্রথমে কলকাতায়
    ফরাসী চলচ্চিত্র নির্মাতা জঁ রনোয়ারের সাথে সাক্ষাৎ ও পরে লন্ডন শহরে সফররত
    অবস্থায় ইতালীয় নব্য বাস্তবতাবাদী ছবি লাদ্রি দি বিচিক্লেত্তে.
    """
]

r_text = revision_oriented.revision.text


@mark.nottravis
def test_badwords():
    compare_extraction(bengali.badwords.revision.datasources.matches,
                       BAD, OTHER)

    assert bengali.badwords == pickle.loads(pickle.dumps(bengali.badwords))


@mark.nottravis
def test_informals():
    compare_extraction(bengali.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    assert bengali.informals == pickle.loads(pickle.dumps(bengali.informals))


'''
def test_dictionary():
    cache = {r_text: "দেখার পর তিনি worngly."}
    assert_equal(solve(bengali.dictionary.revision.datasources.dict_words,
              cache=cache),
        ['দেখার', 'পর', 'তিনি'])
    assert_equal(solve(bengali.dictionary.revision.datasources.non_dict_words,
        cache=cache),
        ["worngly"])

    assert_equal(bengali.dictionary, pickle.loads(pickle.dumps(bengali.dictionary)))
'''


@mark.nottravis
def test_stopwords():
    cache = {r_text: "আন চলচ্চিত্র."}
    assert (solve(bengali.stopwords.revision.datasources.stopwords, cache=cache) ==
            ["আন"])
    assert (solve(bengali.stopwords.revision.datasources.non_stopwords,
                  cache=cache) ==
            ['চলচ্চিত্র'])

    assert bengali.stopwords == pickle.loads(pickle.dumps(bengali.stopwords))
