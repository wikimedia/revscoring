from nose.tools import eq_

from ..language import Language


def test_language():
    
    l = Language(
        lambda w: w == "bad",
        lambda w: w not in {"foo", "bar", "baz"}
    )
    
    assert l.is_badword("bad")
    assert not l.is_badword("good")
    
    assert l.is_misspelled("oof")
    assert not l.is_misspelled("foo")
    
    eq_(list(l.badwords(["good", "bad", "ugly", "bad"])),
        ["bad", "bad"])
    
    eq_(list(l.misspellings(["foo", "oof", "baz", "oof"])),
        ["oof", "oof"])
