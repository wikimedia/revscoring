import pickle

from nose.tools import eq_

from .. import turkish
from ...datasources import revision
from ...dependencies import solve

BAD = [
    "adamın dib", "adamın dip",
    "ahlaksız",
    "ahmak",
    "allahsız",
    "am", "amcık",
    "amk", "amq",
    "amın oğlu",
    "amına", "amına koy", "amına koyayım", "amına koyyim",
    "amını",
    "ananı",
    "ananın am", "ananın dölü",
    "ananızın", "ananızın am",
    "anasını",
    "anasının am",
    "antisemitic",
    "aptal",
    "asdf",
    "ağzına sıçayım",
    "beyinsiz",
    "bi bok", "bok", "boktan", "bokça",
    "dedeler",
    "dinci", "dinsiz",
    "dönek",
    "dıcks",
    "embesil",
    "eshek",
    "gerizekalı",
    "gerzek",
    "godoş",
    "gotten",
    "göt", "göt deliği", "göt oğlanı", "götlek", "götoğlanı", "götveren",
    "götü", "götün",
    "haysiyetsiz",
    "heval", "hewal",
    "huur",
    "i.b.n.e", "ibne", "ibnedir", "ibneli k", "ibnelik",
    "inci",
    "israil köpektir",
    "it oğlu it",
    "kaltak",
    "kaşar",
    "kevaşe",
    "kıç",
    "liboş",
    "mal",
    "meme",
    "nesi kaşar",
    "nobrain",
    "o. çocuğ",
    "orospu", "orospu cocugu", "orospu çoc", "orospu çocuğu",
    "orospu çocuğudur", "orospudur", "orospunun", "orospunun evladı",
    "orospuçocuğu",
    "oğlan", "oğlancı",
    "pezeven", "pezeveng", "pezevengin evladı", "pezevenk",
    "pisliktir",
    "piç",
    "puşt", "puşttur",
    "pıgs",
    "reyiz",
    "sahip",
    "serkan",
    "salak",
    "sik", "sikem", "siken", "siker", "sikerim", "sikey", "sikici", "sikik",
    "sikil", "sikiş", "sikişme", "sikm", "sikseydin", "sikseyidin",
    "sikt", "siktim", "siktir", "siktir lan",
    "sokarım", "sokayım",
    "swicht şamandra",
    "tipini s.k", "tipinizi s.keyim",
    "veled", "weled",
    "woltağym",
    "woğtim",
    "wulftim",
    "yarrak", "yarrağ",
    "yavş", "yavşak",
    "yavşaktır",
    "zippo dünyanın en boktan çakmağıdır",
    "zortlamasi",
    "zıkkımım",
    "zıonısm",
    "çük",
    "ıbnelık",
    "ın tröst we trust",
    "şerefsiz",
]

INFORMAL = [
    "achtırma",
    "achıyorlardı",
    "arkadashlar",
    "arkadashım",
    "basharamıyor",
    "basharan",
    "basharıla",
    "bashka",
    "bashlangıc",
    "bashlıyor",
    "bashıma",
    "bashının",
    "beshinci",
    "beshtane",
    "chalıshmıshlar", "chalıshıldıgında", "chalıshılınırsa", "chalıshıyorlar",
    "chalıshıyorsun", "chalıshıyorum",
    "chamashırlar",
    "charpmadan",
    "charptı", "charpınca",
    "chevirsin", "chevırdım",
    "chimdirecem",
    "choluk",
    "chorusdan", "choruslar",
    "chıka", "chıkacak", "chıkmadı", "chıksa", "chıktı", "chıkıp", "chıkısh",
    "chıplak",
    "degishen", "degishiklik", "degishiyor",
    "dönüshü",
    "eastblacksea",
    "eshekoglu",
    "eshkıyanın",
    "gardash", "gardashlık", "gardaslık",
    "gecherken",
    "gechirdi", "gechirmeyeyeyim", "gechiyor", "gechti", "gechtim",
    "genish",
    "gerchegi",
    "ichimde", "ichimden", "ichin", "ichine", "ichini",
    "ichlerinde",
    "ishler",
    "kalmısh",
    "kardeshlerini", "kardeshlerinizde",
    "karshı",
    "keshke",
    "kishiler", "kishilerin", "kishinin", "kishiye", "kishiyle",
    "konushmalrını", "konushmuyor", "konushuldugunda", "konushur",
    "koshan", "koshtu", "koshuyor",
    "nıshanlı",
    "saatchide",
    "sachlı",
    "sanatchılarını",
    "shansin", "shansın",
    "shashırtma", "shashırtmaya",
    "sheytanlar",
    "takabeg",
    "theır",
    "uchakdan",
    "uzanmıshsın",
    "yaklashdıkdan",
    "yakıshıklı",
    "yaratılmısh",
    "yashamak", "yashatıyorsun", "yashta", "yashıyorsun",
    "yerleshtiriyorum",
    "yozgatfm",
    "üch",
    "ıchın",
    "ıshıksız"
]

OTHER = [
    """
    Türkiye'deki en üst seviye futbol ligi. Bir sezonda 18 takımın mücadele
    ettiği ligde, her takımın diğerleriyle ikişer maç yaptığı çift devreli lig
    usulü uygulanmaktadır. En üst sırada yer alan takım şampiyon olurken son üç
    sıradaki takım 1. Lig'e düşmekte, 1. Lig'deki üç takım ise ertesi sezon
    mücadele etmek üzere Süper Lig'e yükselmektedir.
    """
]


def compare_extraction(extractor, examples, counter_examples):

    for example in examples:
        eq_(extractor.process(example), [example])
        eq_(extractor.process("Sentence " + example + " sandwich."), [example])
        eq_(extractor.process("Sentence end " + example + "."), [example])
        eq_(extractor.process(example + " start of sentence."), [example])

    for example in counter_examples:
        eq_(extractor.process(example), [])
        eq_(extractor.process("Sentence " + example + " sandwich."), [])
        eq_(extractor.process("Sentence end " + example + "."), [])
        eq_(extractor.process(example + " start of sentence."), [])


def test_badwords():
    compare_extraction(turkish.revision.badwords_list, BAD, OTHER)


def test_informals():
    compare_extraction(turkish.revision.informals_list, INFORMAL, OTHER)


def test_revision():
    # Words
    cache = {revision.text: "Bir sezonda m18, takımın mücadele."}
    eq_(solve(turkish.revision.words_list, cache=cache),
        ["Bir", "sezonda", "m18", "takımın", "mücadele"])


def test_presence():
    assert hasattr(turkish.revision, "words")
    assert hasattr(turkish.revision, "content_words")
    assert hasattr(turkish.revision, "badwords")
    assert hasattr(turkish.revision, "informals")

    assert hasattr(turkish.parent_revision, "words")
    assert hasattr(turkish.parent_revision, "content_words")
    assert hasattr(turkish.parent_revision, "badwords")
    assert hasattr(turkish.parent_revision, "informals")

    assert hasattr(turkish.diff, "words_added")
    assert hasattr(turkish.diff, "badwords_added")
    assert hasattr(turkish.diff, "informals_added")
    assert hasattr(turkish.diff, "words_removed")
    assert hasattr(turkish.diff, "badwords_removed")
    assert hasattr(turkish.diff, "informals_removed")


def test_pickling():

    eq_(turkish, pickle.loads(pickle.dumps(turkish)))
