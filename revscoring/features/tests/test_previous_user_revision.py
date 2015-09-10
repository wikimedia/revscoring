from collections import namedtuple

from mwtypes import Timestamp
from nose.tools import eq_

from ...datasources import previous_user_revision, revision
from ...dependencies import solve
from ..previous_user_revision import seconds_since


def test_seconds_since():
    FakeRevisionMetadata = namedtuple("FakeRevisionMetadata",
                                      ['timestamp'])

    cache = {
        revision.metadata: FakeRevisionMetadata(Timestamp(10)),
        previous_user_revision.metadata: FakeRevisionMetadata(Timestamp(1))
    }
    eq_(solve(seconds_since, cache=cache), 9)

    # Makes sure we don't crash when there was no previous user revision
    cache = {
        revision.metadata: FakeRevisionMetadata(Timestamp(10)),
        previous_user_revision.metadata: None
    }
    eq_(solve(seconds_since, cache=cache), 0)
