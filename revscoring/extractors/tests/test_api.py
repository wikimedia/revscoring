from mwtypes import Timestamp
from nose.tools import eq_

from .. import api


def test_user_info_from_doc():

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

    info = api.APIExtractor.user_info_from_doc(doc)

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
        ],
        "gender": "unknown"
    }

    info = api.APIExtractor.user_info_from_doc(doc)
    eq_(info.registration, None)
    eq_(info.blocked_timestamp, None)

    doc = None
    info = api.APIExtractor.user_info_from_doc(doc)
    eq_(info, None)


def test_revision_metadata_from_doc():
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

    metadata = api.APIExtractor.revision_metadata_from_doc(doc)

    eq_(metadata.rev_id, 3456789)
    eq_(metadata.parent_id, 54678)
    eq_(metadata.user_id, 34567890)
    eq_(metadata.user_text, "EpochFail")
    eq_(metadata.timestamp, Timestamp("2015-01-07T12:23:57Z"))
    eq_(metadata.comment,  "Wat?")
    eq_(metadata.page_id, 347)
    eq_(metadata.page_namespace, 0)
    eq_(metadata.page_title, "Hats")


def test_namespace_map_from_doc():
    doc = {
        "namespaces": {
            "0": {
                "id": 0,
                "case": "first-letter",
                "*": "",
                "content": ""
            },
            "1": {
                "id": 1,
                "case": "first-letter",
                "*": "Discuss\u00e3o",
                "subpages": "",
                "canonical": "Talk"
            },
            "2": {
                "id": 2,
                "case": "first-letter",
                "*": "Usu\u00e1rio(a)",
                "subpages": "",
                "canonical": "User"
            }
        },
        "namespacealiases": [
            {
                "id": 1,
                "*": "WAFFLES"
            }
        ]
    }

    namespace_map = api.APIExtractor.namespace_map_from_doc(doc)

    eq_(len(namespace_map), 3)
    eq_(sum(ns.content for ns in namespace_map.values()), 1)


def test_from_config():
    config = {
        'extractors': {
            'enwiki': {
                'host': "https://en.wikipedia.org",
                'api_path': "/w/api.php",
                'timeout': 20,
                'user_agent': "revscoring tests"
            }
        }
    }

    api.APIExtractor.from_config(config, 'enwiki')  # Doesn't error
