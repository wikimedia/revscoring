from nose.tools import eq_

from ..english import english


def test_language():
    
    assert english.is_badword("shit")
    assert english.is_badword("shitty")
    assert not english.is_badword("hat")
    
    assert english.is_misspelled("wjwkjb")
    assert not english.is_misspelled("waffles")
    
    eq_(list(english.badwords(["good", "slut", "bad", "ugly", "fucker"])),
        ["slut", "fucker"])
    
    eq_(list(english.misspellings(["waffles", "oof", "dog", "blarg"])),
        ["oof", "blarg"])
