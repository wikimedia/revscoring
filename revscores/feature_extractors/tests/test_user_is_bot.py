from collections import namedtuple

from ..user_is_bot import user_is_bot


def test_user_is_bot():
    FakeUserInfo = namedtuple("UserInfo", ['groups'])
    
    
    user_info = FakeUserInfo(["foo", "bar", "bot"])
    assert user_is_bot(user_info)
    
    user_info = FakeUserInfo(["foo", "bar"])
    assert not user_is_bot(user_info)
