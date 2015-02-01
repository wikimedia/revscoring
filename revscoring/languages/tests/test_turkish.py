from nose.tools import eq_

from ..turkish import turkish


def test_language():
    
    assert turkish.is_badword("mal")
    assert turkish.is_badword("shitty")
    assert not turkish.is_badword("hat")
    
    assert turkish.is_misspelled("wjwkjb")
    assert not turkish.is_misspelled("waffles")
    
    eq_(list(turkish.badwords(["good", "slut", "bad", "ugly", "fucker"])),
        ["slut", "fucker"])
    
    eq_(list(turkish.misspellings(["waffles", "oof", "dog", "blarg"])),
        ["oof", "blarg"])
