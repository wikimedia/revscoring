import pickle

from nose.tools import eq_

from .. import albanian
from ...datasources import revision_oriented
from ...dependencies import solve
from .util import compare_extraction

BAD = [
    r"albaniancorner",
    r"alexeev",
    r"aliens",
    r"amazingdusseldorf",
    r"amerikanjizor",
    r"anal",
    r"anus",
    r"atp",
    r"bacon",
    r"baloncesto",
    r"bande",
    r"banya",
    r"baseballe",
    r"basketball",
    r"basketballnationalmannschaft",
    r"basketbalteam",
    r"bastard",
    r"bator",
    r"baturina",
    r"beker",
    r"ber",
]

INFORMAL = [
    r"ahah",
    r"ahahah",
    r"ahahaha",
    r"ahahahah",
    r"alarmues",
    r"and",
    r"awesome",
    r"btw",
    r"category",
    r"cdo",
    r"cool",
    r"dreq",
    r"eshte",
    r"ftw",
    r"haha",
    r"hahah",
]

OTHER = [
    """
    Kirenea (greqishtja e lashtë: Κυρήνη Kyrēnē) ka qenë një qytet antik grek dhe
    romak pranë qytetit të sotëm Shahhat, Libi. Ai ishte qyteti më i vjetër dhe më
    i rëndësishëm nga pesë qytetet greke në rajon. Ai i dha Libisë lindore emrin 
    klasik Cyrenaica që ajo ka ruajtur deri në kohët moderne.
    """
]

r_text = revision_oriented.revision.text


def test_badwords():
    compare_extraction(albanian.badwords.revision.datasources.matches,
                       BAD, OTHER)

    eq_(albanian.badwords, pickle.loads(pickle.dumps(albanian.badwords)))


def test_informals():
    compare_extraction(albanian.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    eq_(albanian.informals, pickle.loads(pickle.dumps(albanian.informals)))
