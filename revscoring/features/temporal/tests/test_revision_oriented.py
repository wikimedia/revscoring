import pickle

from mwtypes import Timestamp
from nose.tools import eq_

from ....datasources import revision_oriented
from ....dependencies import solve
from ..revision_oriented import MW_REGISTRATION_EPOCH, revision


def test_revision():

    cache = {revision_oriented.revision.timestamp: Timestamp(0)}
    eq_(solve(revision.day_of_week, cache=cache), 3)  # Thursday, Jan 1 1970

    cache = {revision_oriented.revision.timestamp: Timestamp(0)}
    eq_(solve(revision.hour_of_day, cache=cache), 0)  # Midnight

    eq_(pickle.loads(pickle.dumps(revision.day_of_week)), revision.day_of_week)
    eq_(pickle.loads(pickle.dumps(revision.hour_of_day)), revision.hour_of_day)


def test_page_creation():

    cache = {
        revision_oriented.revision.timestamp: Timestamp(10),
        revision_oriented.revision.page.creation.timestamp: Timestamp(0)
    }
    eq_(solve(revision.page.creation.seconds_since, cache=cache), 10)

    eq_(pickle.loads(pickle.dumps(revision.page.creation.seconds_since)),
        revision.page.creation.seconds_since)


def test_user_registration():

    cache = {
        revision_oriented.revision.timestamp: Timestamp(10),
        revision_oriented.revision.user.id: 10,
        revision_oriented.revision.user.info.registration: Timestamp(0)
    }
    eq_(solve(revision.user.seconds_since_registration, cache=cache), 10)

    # Anon (no registration)
    cache = {
        revision_oriented.revision.timestamp: Timestamp(10),
        revision_oriented.revision.user.id: 0,
        revision_oriented.revision.user.info.registration: None
    }
    eq_(solve(revision.user.seconds_since_registration, cache=cache), 0)

    # Old user (no registration)
    cache = {
        revision_oriented.revision.timestamp: MW_REGISTRATION_EPOCH + 10,
        revision_oriented.revision.user.id: 10,
        revision_oriented.revision.user.info.registration: None
    }
    eq_(solve(revision.user.seconds_since_registration, cache=cache), 10)

    # Old user (broken registration date)
    cache = {
        revision_oriented.revision.timestamp: Timestamp(0),
        revision_oriented.revision.user.id: 10,
        revision_oriented.revision.user.info.registration: Timestamp(10)
    }
    eq_(solve(revision.user.seconds_since_registration, cache=cache),
        60 * 60 * 24 * 365)  # one year

    eq_(pickle.loads(pickle.dumps(revision.user.seconds_since_registration)),
        revision.user.seconds_since_registration)


def test_last_user_revision():

    cache = {
        revision_oriented.revision.timestamp: Timestamp(10),
        revision_oriented.revision.user.last_revision.timestamp: Timestamp(0)
    }
    eq_(solve(revision.user.last_revision.seconds_since, cache=cache), 10)

    cache = {
        revision_oriented.revision.timestamp: Timestamp(10),
        revision_oriented.revision.user.last_revision.timestamp: None
    }
    eq_(solve(revision.user.last_revision.seconds_since, cache=cache), 0)


def test_parent_revision():

    cache = {
        revision_oriented.revision.timestamp: Timestamp(10),
        revision_oriented.revision.parent.timestamp: Timestamp(0)
    }
    eq_(solve(revision.parent.seconds_since, cache=cache), 10)

    eq_(pickle.loads(pickle.dumps(revision.parent.seconds_since)),
        revision.parent.seconds_since)
