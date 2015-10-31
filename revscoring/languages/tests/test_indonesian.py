import pickle

from nose.tools import eq_

from .. import indonesian
from ...datasources import revision
from ...dependencies import solve
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


def test_badwords():
    compare_extraction(indonesian.revision.badwords_list, BAD, OTHER)


def test_informals():
    compare_extraction(indonesian.revision.informals_list, INFORMAL, OTHER)


def test_revision():
    # Words
    cache = {revision.text: "Gita Gutawa adalah seorang m80 sopran, aktris."}
    eq_(solve(indonesian.revision.words_list, cache=cache),
        ["Gita", "Gutawa", "adalah", "seorang", "m80", "sopran", "aktris"])

    # Misspellings
    cache = {revision.text: 'Setelah merilis album duet worngly. <td>'}
    eq_(solve(indonesian.revision.misspellings_list, cache=cache), ["worngly"])


def test_pickling():

    eq_(indonesian, pickle.loads(pickle.dumps(indonesian)))
