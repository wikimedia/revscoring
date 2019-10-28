import pickle

from mwtypes import Timestamp
from revscoring.datasources import session_oriented
from revscoring.dependencies import solve
from revscoring.features.temporal.revision_oriented import \
    MW_REGISTRATION_EPOCH
from revscoring.features.temporal.session_oriented import session


def test_session_revisions():
    cache = {session_oriented.session.revisions.timestamp: [Timestamp(0)]}
    assert solve(session.revisions.day_of_week, cache=cache) == [3]  # Thursday, Jan 1 1970
    assert solve(session.revisions.hour_of_day, cache=cache) == [0]  # Midnight

    assert pickle.loads(pickle.dumps(session.revisions.day_of_week)
                        ) == session.revisions.day_of_week
    assert pickle.loads(pickle.dumps(session.revisions.hour_of_day)
                        ) == session.revisions.hour_of_day


def test_session_revisions_string_timestamp():
    cache = {session_oriented.session.revisions.timestamp_str: ["1970-01-01T00:00:00Z"]}
    assert solve(session.revisions.day_of_week, cache=cache) == [3]  # Thursday, Jan 1 1970
    assert solve(session.revisions.hour_of_day, cache=cache) == [0]  # Midnight

    assert pickle.loads(pickle.dumps(session.revisions.day_of_week)) == \
           session.revisions.day_of_week
    assert pickle.loads(pickle.dumps(session.revisions.hour_of_day)) == \
           session.revisions.hour_of_day


def test_session_page_creation():
    cache = {
        session_oriented.session.revisions.timestamp: [Timestamp(10)],
        session_oriented.session.revisions.page.creation.timestamp: [Timestamp(0)]
    }
    assert solve(session.revisions.page.creation.seconds_since, cache=cache) == [10]

    assert (pickle.loads(pickle.dumps(session.revisions.page.creation.seconds_since)) ==
            session.revisions.page.creation.seconds_since)


def test_session_user_registration():
    cache = {
        session_oriented.session.revisions.timestamp: [Timestamp(10)],
        session_oriented.session.user.id: 10,
        session_oriented.session.user.info.registration: Timestamp(0)
    }
    assert solve(session.user.seconds_since_registration, cache=cache) == 10

    # Anon (no registration)
    cache = {
        session_oriented.session.revisions.timestamp: [Timestamp(10)],
        session_oriented.session.user.id: 0,
        session_oriented.session.user.info.registration: None
    }
    assert solve(session.user.seconds_since_registration, cache=cache) == 0

    # Old user (no registration)
    cache = {
        session_oriented.session.revisions.timestamp: [MW_REGISTRATION_EPOCH + 10],
        session_oriented.session.user.id: 10,
        session_oriented.session.user.info.registration: None
    }
    assert solve(session.user.seconds_since_registration, cache=cache) == 10

    # Old user (broken registration date)
    cache = {
        session_oriented.session.revisions.timestamp: [Timestamp(0)],
        session_oriented.session.user.id: 10,
        session_oriented.session.user.info.registration: Timestamp(10)
    }
    assert (solve(session.user.seconds_since_registration, cache=cache) ==
            60 * 60 * 24 * 365)  # one year

    assert (pickle.loads(pickle.dumps(session.user.seconds_since_registration)) ==
            session.user.seconds_since_registration)


def test_last_user_revision():
    cache = {
        session_oriented.session.revisions.timestamp: [Timestamp(10)],
        session_oriented.session.user.last_revision.timestamp: Timestamp(0)
    }
    assert solve(session.user.last_revision.seconds_since, cache=cache) == 10

    cache = {
        session_oriented.session.revisions.timestamp: [Timestamp(10)],
        session_oriented.session.user.last_revision.timestamp: None
    }
    assert solve(session.user.last_revision.seconds_since, cache=cache) == 0


def test_parent_revision():
    cache = {
        session_oriented.session.revisions.timestamp: [Timestamp(10)],
        session_oriented.session.revisions.parent.timestamp: [Timestamp(0)]
    }
    assert solve(session.revisions.parent.seconds_since, cache=cache) == [10]

    assert (pickle.loads(pickle.dumps(session.revisions.parent.seconds_since)) ==
            session.revisions.parent.seconds_since)
