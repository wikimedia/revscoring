from collections import namedtuple

from mwtypes import Timestamp
from nose.tools import eq_

from ...datasources import page_creation, revision, site
from ...dependencies import solve
from ..page import age, is_content_namespace, is_mainspace


def test_is_content_namespace():
    FakeNamespace = namedtuple("FakeNamespace", ['content'])
    FakeRevisionMetadata = namedtuple("FakeRevisionMetadata",
                                      ['page_namespace'])
    cache = {
        site.namespace_map: {0: FakeNamespace(True), 1: FakeNamespace(False)},
        revision.metadata: FakeRevisionMetadata(1)
    }
    eq_(solve(is_content_namespace, cache=cache), False)
    cache = {
        site.namespace_map: {0: FakeNamespace(True), 1: FakeNamespace(False)},
        revision.metadata: FakeRevisionMetadata(0)
    }
    eq_(solve(is_content_namespace, cache=cache), True)


def test_is_mainspace():
    FakeRevisionMetadata = namedtuple("FakeRevisionMetadata",
                                      ['page_namespace'])
    cache = {
        revision.metadata: FakeRevisionMetadata(1)
    }
    eq_(solve(is_mainspace, cache=cache), False)
    cache = {
        revision.metadata: FakeRevisionMetadata(0)
    }
    eq_(solve(is_mainspace, cache=cache), True)


def test_age():
    FakeRevisionMetadata = namedtuple("FakeRevisionMetadata",
                                      ['timestamp'])

    cache = {
        revision.metadata: FakeRevisionMetadata(Timestamp(10)),
        page_creation.metadata: FakeRevisionMetadata(Timestamp(0))
    }
    eq_(solve(age, cache=cache), 10)
