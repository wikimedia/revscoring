import pickle

from nose.tools import eq_

from .. import hebrew
from ...datasources import revision
from ...dependencies import solve
from .util import compare_extraction

BAD = [
    "שרמוטה"
]

INFORMAL = [
    "בגללך"  # Because of you
]

OTHER = [
    "בגלל", "חתול"
]


def test_badwords():
    compare_extraction(hebrew.revision.badwords_list, BAD, OTHER)


def test_informals():
    compare_extraction(hebrew.revision.informals_list, INFORMAL, OTHER)


def test_revision():
    # Words
    cache = {revision.text: "סוויפט גדלה בוויומיסינג, פנסילבניה, לנאשוויל"}
    eq_(solve(hebrew.revision.words_list, cache=cache),
        ["סוויפט", "גדלה", "בוויומיסינג", "פנסילבניה", "לנאשוויל"])

    # Misspellings
    cache = {revision.text: 'בגלל חטול <td>'}
    eq_(solve(hebrew.revision.misspellings_list, cache=cache), ["חטול"])


def test_pickling():

    eq_(hebrew, pickle.loads(pickle.dumps(hebrew)))
