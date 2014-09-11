from collections import namedtuple

from ..is_previous_user_same import is_previous_user_same


def test_is_previous_user_same():
    FakeRevisionMeta = namedtuple("FakeRevisionMeta", ['user_id', 'user_text'])
    
    previous_revision_meta = FakeRevisionMeta(10, "Foobar")
    revision_meta = FakeRevisionMeta(10, "Foobar")
    assert is_previous_user_same(previous_revision_meta, revision_meta)
    
    previous_revision_meta = FakeRevisionMeta(0, "127.0.0.1")
    revision_meta = FakeRevisionMeta(10, "Foobar")
    assert not is_previous_user_same(previous_revision_meta, revision_meta)
    
    previous_revision_meta = FakeRevisionMeta(11, "Foobar2")
    revision_meta = FakeRevisionMeta(10, "Foobar")
    assert not is_previous_user_same(previous_revision_meta, revision_meta)
