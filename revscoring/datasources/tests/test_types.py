from mw import Timestamp
from nose.tools import eq_

from ..types import RevisionMetadata, UserInfo


def test_revision_metadata():
    doc = {
        "revid": 3456789,
        "parentid": 54678,
        "comment": "Wat?",
        "user": "EpochFail",
        "userid": 34567890,
        "timestamp": "2015-01-07T12:23:57Z",
        "page": {
            "pageid": 347,
            "title": "Hats",
            "ns": 0
        }
    }
    metadata = RevisionMetadata.from_doc(doc)

    eq_(metadata.rev_id, 3456789)
    eq_(metadata.parent_id, 54678)
    eq_(metadata.user_id, 34567890)
    eq_(metadata.user_text, "EpochFail")
    eq_(metadata.timestamp, Timestamp("2015-01-07T12:23:57Z"))
    eq_(metadata.comment,  "Wat?")
    eq_(metadata.page_id, 347)
    eq_(metadata.page_namespace, 0)
    eq_(metadata.page_title, "Hats")

    doc = {}
    metadata = RevisionMetadata.from_doc(doc)

    eq_(metadata.timestamp, None)


def test_user_info():
    doc = {
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
    user_info = UserInfo.from_doc(doc)

    eq_(user_info.id, doc['userid'])
    eq_(user_info.name, doc['name'])
    eq_(user_info.editcount, doc['editcount'])
    eq_(user_info.registration, Timestamp(doc['registration']))
    eq_(user_info.groups, doc['groups'])
    eq_(user_info.implicitgroups, doc['implicitgroups'])
    eq_(user_info.gender, doc['gender'])
    eq_(user_info.blocked_by, doc['blockedby'])
    eq_(user_info.blocked_by_id, int(doc['blockedbyid']))
    eq_(user_info.blocked_timestamp, Timestamp(doc['blockedtimestamp']))
    eq_(user_info.block_reason, doc['blockreason'])
    eq_(user_info.block_expiry, doc['blockexpiry'])

    doc = {
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
        ]
    }
    user_info = UserInfo.from_doc(doc)
    eq_(user_info.registration, None)
    eq_(user_info.blocked_timestamp, None)
