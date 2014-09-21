from collections import namedtuple

from ..user_is_anon import user_is_anon


def test_user_is_anon():
    FakeRevisionMeta = namedtuple("FakeRevisionMeta", ['user_id'])
    
    revision_meta = FakeRevisionMeta(0)
    assert user_is_anon(revision_meta)
    
    revision_meta = FakeRevisionMeta(1)
    assert not user_is_anon(revision_meta)
