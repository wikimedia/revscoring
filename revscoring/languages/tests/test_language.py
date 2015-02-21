import pickle
from io import BytesIO

from nose.tools import eq_

from ..language import Language


def is_badword(word): return word == "bad"
def is_misspelled(word): return word not in {"foo", "bar", "baz"}

def test_language():
    
    l = Language(
        "Test Language",
        is_badword,
        is_misspelled
    )
    
    assert l.is_badword("bad")
    assert not l.is_badword("good")
    
    assert l.is_misspelled("oof")
    assert not l.is_misspelled("foo")
    
    eq_(list(l.badwords(["good", "bad", "ugly", "bad"])),
        ["bad", "bad"])
    
    eq_(list(l.misspellings(["foo", "oof", "baz", "oof"])),
        ["oof", "oof"])

def test_pickle_hash():
    
    l = Language(
        "Test Language",
        is_badword,
        is_misspelled
    )
    
    f = BytesIO()
    
    pickle.dump(l, f)
    
    f.seek(0)
    
    l2 = pickle.load(f)
    
    eq_(l, l2)
