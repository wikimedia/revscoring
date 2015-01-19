from collections import namedtuple

from nose.tools import eq_

from ..is_content_namespace import is_content_namespace


def test_is_mainspace():
    FakeRevisionMeta = namedtuple("FakeRevisionMeta", ['page_namespace'])
    FakeNamespace = namedtuple("Namespace", ['id', 'content'])
    
    rm = FakeRevisionMeta(0)
    nses = {0: FakeNamespace(0, True)}
    assert is_content_namespace(rm, nses)
    
    
    rm = FakeRevisionMeta(2)
    nses = {0: FakeNamespace(0, True)}
    assert not is_content_namespace(rm, nses)
