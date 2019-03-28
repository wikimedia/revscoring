import pickle

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.languages import turkish

from .util import compare_extraction

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

r_text = revision_oriented.revision.text


def test_badwords():
    compare_extraction(turkish.badwords.revision.datasources.matches,
                       BAD, OTHER)

    assert turkish.badwords == pickle.loads(pickle.dumps(turkish.badwords))


def test_informals():
    compare_extraction(turkish.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    assert turkish.informals == pickle.loads(pickle.dumps(turkish.informals))


def test_stopwords():
    cache = {r_text: 'Türkiye\'deki en üst seviye futbol ligi.'}
    assert (solve(turkish.stopwords.revision.datasources.stopwords, cache=cache) ==
            ["en"])
    assert (solve(turkish.stopwords.revision.datasources.non_stopwords,
                  cache=cache) ==
            ["Türkiye'deki", 'üst', 'seviye', 'futbol', 'ligi'])

    assert turkish.stopwords == pickle.loads(pickle.dumps(turkish.stopwords))
