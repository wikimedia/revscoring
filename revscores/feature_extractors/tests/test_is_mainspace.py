from collections import namedtuple

from nose.tools import eq_

from ..is_mainspace import is_mainspace


def test_is_mainspace():
    FakeRevisionMeta = namedtuple("FakeRevisionMeta", ['page_namespace'])
    
    rm = FakeRevisionMeta(0)
    assert is_mainspace(rm)
    
    
    rm = FakeRevisionMeta(2)
    assert not is_mainspace(rm)
