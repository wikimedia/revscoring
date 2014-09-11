from collections import namedtuple

from nose.tools import eq_

from ..is_section_comment import is_section_comment


def test_is_section_comment():
    FakeRevisionMeta = namedtuple("FakeRevisionMeta", ['comment'])
    
    rm = FakeRevisionMeta("/* Foobar */ I did some stuff!")
    assert is_section_comment(rm)
    
    
    rm = FakeRevisionMeta("Derp some stuff!")
    assert not is_section_comment(rm)
