from nose.tools import eq_

from ..portuguese import portuguese


def test_language():
    
    assert portuguese.is_badword("merda")
    assert portuguese.is_badword("merdar")
    assert not portuguese.is_badword("arvere")
    
    assert portuguese.is_misspelled("wjwkjb")
    assert not portuguese.is_misspelled("Esta")
    
    eq_(list(portuguese.badwords(["Esta", "porra", "parece", "merda"])),
        ["porra", "merda"])
    
    eq_(list(portuguese.misspellings(["O", "urso", "abraca", "a", "arvere"])),
        ["abraca", "arvere"])
