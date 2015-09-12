from collections import namedtuple

from mwtypes import Timestamp
from nose.tools import eq_

from ...datasources import revision, user
from ...dependencies import solve
from ..user import age, is_anon, is_bot


def test_age():
    FakeRevisionMetadata = namedtuple("FakeRevisionMetadata",
                                      ['user_id', 'timestamp'])
    FakeUserInfo = namedtuple("FakeUserInfo", ['registration'])

    cache = {
        revision.metadata: FakeRevisionMetadata(10, Timestamp(10)),
        user.info: FakeUserInfo(Timestamp(0))
    }
    eq_(solve(age, cache=cache), 10)

    cache = {
        revision.metadata: FakeRevisionMetadata(None, Timestamp(10)),
        user.info: FakeUserInfo(Timestamp(0))
    }
    eq_(solve(age, cache=cache), 0)

    cache = {
        revision.metadata: FakeRevisionMetadata(10,
                                                Timestamp("20140101010101")),
        user.info: FakeUserInfo(None)
    }
    # Makes sure that old users with no registration are counted appropriately.
    assert solve(age, cache=cache) > 0

    cache = {
        revision.metadata: FakeRevisionMetadata(10, Timestamp(0)),
        user.info: FakeUserInfo(Timestamp(1))
    }
    # Makes sure that imports (revisions made before registration) don't return
    # negative values.
    eq_(solve(age, cache=cache), 0)

    cache = {
        revision.metadata: FakeRevisionMetadata(10, Timestamp(0)),
        user.info: None
    }
    eq_(solve(age, cache=cache), 0)


def test_is_anon():
    FakeRevisionMetadata = namedtuple("FakeRevisionMetadata",
                                      ['user_id'])
    cache = {
        revision.metadata: FakeRevisionMetadata(10)
    }
    assert not solve(is_anon, cache=cache)

    cache = {
        revision.metadata: FakeRevisionMetadata(None)
    }
    assert solve(is_anon, cache=cache)

    cache = {
        revision.metadata: FakeRevisionMetadata(0)
    }
    assert solve(is_anon, cache=cache)


def test_is_bot():
    FakeUserInfo = namedtuple("UserInfo", ['groups'])

    cache = {
        user.info: FakeUserInfo(["foo", "bar", "bot"])
    }
    assert solve(is_bot, cache=cache)

    cache = {
        user.info: FakeUserInfo(["foo", "bar"])
    }
    assert not solve(is_bot, cache=cache)

    cache = {
        user.info: None
    }
    assert not solve(is_bot, cache=cache)
