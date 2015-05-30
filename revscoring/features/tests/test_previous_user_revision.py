from collections import namedtuple

from mw import Timestamp
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
