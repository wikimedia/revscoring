from collections import namedtuple

from ..is_anon import is_anon


def test_is_section_comment():
    FakeRevisionMeta = namedtuple("FakeRevisionMeta", ['user_id'])
    
    revision_meta = FakeRevisionMeta(0)
    assert is_anon(revision_meta)
    
    revision_meta = FakeRevisionMeta(1)
    assert not is_anon(revision_meta)
