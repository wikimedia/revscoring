import pickle

from nose.tools import eq_

from .. import estonian
from ...datasources import revision
from ...dependencies import solve
from .util import compare_extraction

BAD = [
    "homo", "homod", "jobu", "junn", "junni", "kaka", "lits", "loll",
    "lollakas", "lollid", "munn", "munni", "munnid", "neeger", "nigga",
    "noku", "pask", "pede", "peded", "pedekas", "pederast", "pederastid",
    "perse", "perses", "persse", "pihku", "putsi", "sitane", "sitt", "sitta",
    "tsmir", "türa", "tšmir", "vittu", "vitupea"
]

INFORMAL = [
    "haha", "hahaha", "jou", "noob", "raisk", "räme", "sakib", "suht",
    "tegelt", "tere", "tsau"
]

OTHER = [
    """
    Friedrich Wilhelm Rembert von Berg sündis Beļava ja Sangaste mõisniku
    Friedrich Georg von Bergi ja Gerdruta Wilhelmine von Ermesi vanima pojana.
    Tal olid nooremad vennad Gustav, Magnus ja Alexander. Friedrich Wilhelmi ja
    tema vendade koduõpetaja oli hilisem tuntud astronoom Wilhelm Struve.
    """
]


def test_badwords():
    compare_extraction(estonian.revision.badwords_list, BAD, OTHER)


def test_informals():
    compare_extraction(estonian.revision.informals_list, INFORMAL, OTHER)


def test_revision():
    # Words
    cache = {revision.text: "Tal olid nooremad m80, vennad Gustav."}
    eq_(solve(estonian.revision.words_list, cache=cache),
        ["Tal", "olid", "nooremad", "m80", "vennad", "Gustav"])

    # Misspellings
    cache = {revision.text: "Tal olid nooremad, vennad, worngly. <td>"}
    eq_(solve(estonian.revision.misspellings_list, cache=cache), ["worngly"])


def test_pickling():

    eq_(estonian, pickle.loads(pickle.dumps(estonian)))
