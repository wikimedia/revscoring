from nose.tools import eq_

from ..turkish import turkish


def test_language():

    assert turkish.is_badword("mal")
    assert turkish.is_badword("orospu çocuğu")
    assert not turkish.is_badword("resim")

    #assert turkish.is_misspelled("wjwkjb")
    assert not turkish.is_misspelled("sinema")

    eq_(list(turkish.badwords(["komedi", "pezevenk", "kedi", "güzergah", "ibne"])),
        ["pezevenk", "ibne"])

    #eq_(list(turkish.misspellings(["sinema", "oof", "köpek", "blarg"])),
    #    ["oof", "blarg"])
