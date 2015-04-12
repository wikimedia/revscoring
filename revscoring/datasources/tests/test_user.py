from nose.tools import eq_

from mw import Timestamp

from .. import user
from ...dependent import solve


def test_info():

    cache = {
        user.doc: {
            "userid": 24278012,
            "name": "Hoardablehotsauce",
            "editcount": 5,
            "registration": "2015-02-28T22:25:37Z",
            "groups": [
                "*",
                "user"
            ],
            "implicitgroups": [
                "*",
                "user"
            ],
            "blockid": "5752570",
            "blockedby": "Cryptic",
            "blockedbyid": "295294",
            "blockedtimestamp": "2015-02-28T22:43:23Z",
            "blockreason": "{{uw-softerblock}} <!-- Promotional username, "
                           "soft block -->",
            "blockexpiry": "infinity",
            "gender": "unknown"
        }
    }

    info = solve(user.info, cache=cache)

    eq_(info.name, "Hoardablehotsauce")
    eq_(info.groups, ['*', "user"])
    eq_(info.implicitgroups, ['*', "user"])
    eq_(info.registration, Timestamp("2015-02-28T22:25:37Z"))
    eq_(info.block_id, 5752570)
    eq_(info.blocked_by, "Cryptic")
    eq_(info.blocked_by_id, 295294)
    eq_(info.blocked_timestamp, Timestamp("2015-02-28T22:43:23Z"))
    eq_(info.block_reason,
        "{{uw-softerblock}} <!-- Promotional username, soft block -->")
    eq_(info.block_expiry, "infinity")
    eq_(info.gender, "unknown")

    cache = {
        user.doc: {
            "userid": 24278012,
            "name": "Hoardablehotsauce",
            "editcount": 5,
            "groups": [
                "*",
                "user"
            ],
            "implicitgroups": [
                "*",
                "user"
            ],
            "gender": "unknown"
        }
    }
    info = solve(user.info, cache=cache)
    eq_(info.registration, None)
    eq_(info.blocked_timestamp, None)

    cache = {
        user.doc: None
    }
    info = solve(user.info, cache=cache)
    eq_(info, None)
