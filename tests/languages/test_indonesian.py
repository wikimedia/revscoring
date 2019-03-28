import pickle

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.languages import indonesian

from .util import compare_extraction

BAD = [
    "anjing",
    "bajingan",
    "bangsat",
    "bispak",
    "bloon", "blo'on",
    "brengsek", "brengsex",
    "bencong",
    "babi",
    "cibai",
    "coley",
    "diselama",
    "escoduro",
    "fredrike",
    "fogh",
    "gauguin",
    "goblok",
    "gestapo",
    "husseins",
    "indon",
    "jambut",
    "jellinek",
    "jellygamat",
    "keparat",
    "kontol",
    "lonte",
    "loked",
    "lvmh",
    "malingsia",
    "memek",
    "monyong",
    "netnapa",
    "ngentot",
    "nesbitt",
    "panadta",
    "palaji",
    "perek",
    "pukimak",
    "pedofil",
    "riyhad",
    "sempak",
    "sinting",
    "steinway",
    "sukhano",
    "taenjamras",
    "tetek",
    "titit",
    "toket",
    "tzcesar",
    "thailaland",
    "thaicia"
]

INFORMAL = [
    "hai",
    "halo",
    "jancok"
]

OTHER = [
    """
    Gita Gutawa adalah seorang penyanyi sopran, aktris, dan penulis lagu
    berkebangsaan Indonesia. Ia adalah putri dari komponis Erwin Gutawa.
    Meskipun pada awalnya sempat belajar piano, Gita kemudian beralih ke vokal.
    Bakatnya ditemukan pada tahun 2004 saat ia sedang berlatih vokal,
    kemudian diminta untuk berduet dengan ADA Band.
    """
]

r_text = revision_oriented.revision.text


def test_badwords():
    compare_extraction(indonesian.badwords.revision.datasources.matches,
                       BAD, OTHER)

    assert indonesian.badwords == pickle.loads(
        pickle.dumps(indonesian.badwords))


def test_informals():
    compare_extraction(indonesian.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    assert indonesian.informals == pickle.loads(
        pickle.dumps(indonesian.informals))


def test_dictionary():
    cache = {r_text: "Gita Gutawa adalah seorang m80 sopran, aktris."}
    assert (solve(indonesian.dictionary.revision.datasources.dict_words,
                  cache=cache) ==
            ['adalah', 'seorang', 'sopran', 'aktris'])
    assert (solve(indonesian.dictionary.revision.datasources.non_dict_words,
                  cache=cache) ==
            ['Gita', 'Gutawa', 'm80'])

    assert (indonesian.dictionary ==
            pickle.loads(pickle.dumps(indonesian.dictionary)))


def test_stopwords():
    cache = {r_text: "Gita Gutawa adalah seorang m80 sopran, aktris."}
    assert (solve(indonesian.stopwords.revision.datasources.stopwords,
                  cache=cache) ==
            ['adalah', 'seorang'])
    assert (solve(indonesian.stopwords.revision.datasources.non_stopwords,
                  cache=cache) ==
            ['Gita', 'Gutawa', 'm80', 'sopran', 'aktris'])

    assert indonesian.stopwords == pickle.loads(
        pickle.dumps(indonesian.stopwords))
