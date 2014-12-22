from collections import namedtuple

from nose.tools import eq_

from ..bytes_changed import bytes_changed


def test_is_section_comment():
    FakeRevisionMeta = namedtuple("FakeRevisionMeta", ['bytes'])
    
    previous_revision_meta = FakeRevisionMeta(245)
    revision_meta = FakeRevisionMeta(200)
    eq_(bytes_changed(previous_revision_meta, revision_meta), -45)
    
    
    previous_revision_meta = FakeRevisionMeta(300)
    revision_meta = FakeRevisionMeta(320)
    eq_(bytes_changed(previous_revision_meta, revision_meta), 20)
    
    
    previous_revision_meta = FakeRevisionMeta(420)
    revision_meta = FakeRevisionMeta(420)
    eq_(bytes_changed(previous_revision_meta, revision_meta), 0)
