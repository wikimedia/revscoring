from collections import namedtuple

from nose.tools import eq_

from ..is_custom_comment import is_custom_comment


def test_is_custom_comment():
    FakeRevisionMeta = namedtuple("FakeRevisionMeta", ['comment'])
    
    rm = FakeRevisionMeta("/* Foobar */ I did some stuff!")
    assert is_custom_comment(rm)
    
    rm = FakeRevisionMeta("Derp some stuff!")
    assert is_custom_comment(rm)
    
    rm = FakeRevisionMeta("/* Foobar */")
    assert not is_custom_comment(rm)
    
    rm = FakeRevisionMeta("/* Foobar */ rv")
    assert is_custom_comment(rm)
