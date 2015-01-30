from collections import namedtuple

from mw import Timestamp
from nose.tools import eq_

from ..user_age_in_seconds import user_age_in_seconds


def test_user_age_in_seconds():
    
    FakeRevisionMetadata = namedtuple("RevisionMetadata", ['timestamp'])
    FakeUserInfo = namedtuple("UserInfo", ['id', 'registration'])
    
    user_info = FakeUserInfo(10, Timestamp(1234567890))
    
    revision_metadata = FakeRevisionMetadata(Timestamp(1234567890) + 1000)
    
    eq_(user_age_in_seconds(user_info, revision_metadata), 1000)
    
    anon_user_info = FakeUserInfo(None, None)
    
    eq_(user_age_in_seconds(anon_user_info, revision_metadata), 0)
