import pickle

from nose.tools import eq_

from .. import estonian
from ...datasources import revision_oriented
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

r_text = revision_oriented.revision.text


def test_badwords():
    compare_extraction(estonian.badwords.revision.datasources.matches,
                       BAD, OTHER)

    eq_(estonian.badwords, pickle.loads(pickle.dumps(estonian.badwords)))


def test_informals():
    compare_extraction(estonian.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    eq_(estonian.informals, pickle.loads(pickle.dumps(estonian.informals)))


def test_dictionary():
    cache = {r_text: "Tal olid nooremad, vennad worngly. <td>"}
    eq_(solve(estonian.dictionary.revision.datasources.dict_words,
              cache=cache), ["Tal", "olid", "nooremad", "vennad"])
    eq_(solve(estonian.dictionary.revision.datasources.non_dict_words,
              cache=cache), ["worngly"])

    eq_(estonian.dictionary, pickle.loads(pickle.dumps(estonian.dictionary)))


def test_stopwords():
    cache = {revision_oriented.revision.text: "Bergi ja Gerdruta Wilhelmine " +
                                              "von Ermesi vanima pojana."}
    eq_(solve(estonian.stopwords.revision.datasources.stopwords, cache=cache),
        ["von"])
    eq_(solve(estonian.stopwords.revision.datasources.non_stopwords,
        cache=cache),
        ["Bergi", "ja", "Gerdruta", "Wilhelmine", "Ermesi", "vanima",
         "pojana"])

    eq_(estonian.stopwords, pickle.loads(pickle.dumps(estonian.stopwords)))
