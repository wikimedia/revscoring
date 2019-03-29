import pickle

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.languages import icelandic

from .util import compare_extraction

BAD = [
    "adc",
    "böllinn",
    "böllur",
    "hommi",
    "idiot",
    "typpi",
    "typpið",
    "andskotans",
    "andskotinn",
    "djöfulsins",
    "djöfullinn",
    "helvítis",
    "helvíti",
    "hóra",
    "freta",
    "fretaði",
    "kúkar",
    "kúkaði",
    "faggi",
    "fábjáni",
    "fitabolla",
    "grenjuskjóða",
    "suckar",
    "suck",
    "sjúgðu",
    "saug",
    "væluskjóða",
    "fæðingarhálviti",
    "mannfjandi",
    "drulludeli",
    "drullukunta",
    "raggeit",
    "brundþró",
    "trunta",
    "prumpa",
    "prumpaði",
    "píka",
    "píku",
    "hálfviti",
    "hommadjöfull",
    "drullusokkur",
    "fáviti",
    "aumingi",
    "mannfýla",
    "negri",
    "negrar",
    "hlandbrenndu",
    "náriðill",
    "vesalingur",
    "ónytjungur",
    "fitubelgur",
    "lúði",
    "lúðablesi",
    "kvikindi",
    "kvikindið",
    "klikkhaus",
    "mella",
    "skítseiði",
    "kill",
    "drepa",
    "fjandinn",
    "fjandans",
    "fokka",
    "fokkaði",
    "nauðga",
    "nauðgaði"
]

INFORMAL = [
    "awesome",
    "del",
    "face",
    "mockbuster",
    "sick",
    "stupid",
    "bla", "blaa", "blaaa",
    "bæ",
    "bless",
    "hæ",
    "halló",
    "haha", "hahaa", "hahaaaa",
    "bull",
    "kveðja",
    "pampered",
    "lol",
    "auli",
    "aulast",
    "aulablesi",
    "fífl",
    "skúrkur",
    "flón",
    "skoffín",
    "garmur",
    "jullur",
    "mellufær",
    "dræsur",
    "brjóst"
]

OTHER = [
    """
    Albert 1. var þriðji konungur Belgíu frá árinu 1909 til dauðadags.
    Þetta var viðburðaríkt tímabil í sögu Belgíu því í fyrri
    heimsstyrjöldinni (1914 – 1918) var mikill meirihluti landsins hernuminn
    af Þjóðverjum.
    """
]

r_text = revision_oriented.revision.text


def test_badwords():
    compare_extraction(icelandic.badwords.revision.datasources.matches,
                       BAD, OTHER)

    assert icelandic.badwords == pickle.loads(pickle.dumps(icelandic.badwords))


def test_informals():
    compare_extraction(icelandic.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    assert icelandic.informals == pickle.loads(
        pickle.dumps(icelandic.informals))


def test_dictionary():
    cache = {r_text: 'belgíska konungsríkisins auk worngly. <td>'}
    assert (solve(icelandic.dictionary.revision.datasources.dict_words,
                  cache=cache) ==
            ["belgíska", "konungsríkisins", "auk"])
    assert (solve(icelandic.dictionary.revision.datasources.non_dict_words,
                  cache=cache) ==
            ["worngly"])

    assert icelandic.dictionary == pickle.loads(
        pickle.dumps(icelandic.dictionary))


def test_stopwords():
    cache = {revision_oriented.revision.text:
             "belgíska konungsríkisins auk verndarsvæði honum hann"}
    assert (
        solve(
            icelandic.stopwords.revision.datasources.stopwords,
            cache=cache) == [
            "auk",
            "honum",
            "hann"])
    assert (solve(icelandic.stopwords.revision.datasources.non_stopwords,
                  cache=cache) ==
            ["belgíska", "konungsríkisins", "verndarsvæði"])

    assert icelandic.stopwords == pickle.loads(
        pickle.dumps(icelandic.stopwords))
