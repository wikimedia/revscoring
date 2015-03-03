from nose.tools import eq_

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
            "blockreason": "{{uw-softerblock}} <!-- Promotional username, soft block -->",
            "blockexpiry": "infinity",
            "gender": "unknown"
        }
    }
    
    info = solve(user.info, cache=cache)
    
    eq_(info.name, "Hoardablehotsauce")
    eq_(info.implicitgroups, ['*', "user"])
