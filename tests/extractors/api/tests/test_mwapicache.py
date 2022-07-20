from revscoring.extractors.api.extractor import MWAPICache

import pytest


@pytest.fixture
def mwapicache():
    '''Returns an empty MWAPICache.'''
    return MWAPICache()

def test_init(mwapicache):
    cache = {
        "revisions": {},
        "pageid": {},
        "users": {},
        "wbsgetsuggestions": {},
        "usercontribs": {}
    }
    assert cache == mwapicache._cache

def test_get_non_existent_entries(mwapicache):
    assert None == mwapicache.get_revisions_batch_doc([123456])
    assert None == mwapicache.get_pageid_doc(123443)
    assert None == mwapicache.get_users_batch_doc(["Test1"])
    assert None == mwapicache.get_usercontribs_doc("Test1")
    assert None == mwapicache.get_wbsgetsuggestions_doc("Q12345")


def test_add_get_revisions_batch_doc(mwapicache):
    doc = {'batchcomplete': '', 'query': {'pages': {'64216': {'pageid': 64216, 'ns': 0, 'title': 'Basic training', 'revisions': [{'revid': 123456, 'parentid': 123443, 'user': 'Fredbauder', 'userid': 744, 'timestamp': '2002-07-25T05:02:10Z', 'size': 621, 'slots': {'main': {'contentmodel': 'wikitext', 'contentformat': 'text/x-wiki', '*': "'''Basic Training''' or bootcamp is a short intensive program for induction of recruits into an [[army]] or [[navy]]. In the [[United States]] a few military bases have special units devoted to basic training. [CUT]"}}, 'comment': ''}]}}}}

    mwapicache.add_revisions_batch_doc([123456], doc)
    assert mwapicache._cache["revisions"][(123456,)] == doc
    assert doc == mwapicache.get_revisions_batch_doc([123456])

def test_add_get_pageid_doc(mwapicache):
    doc = {'batchcomplete': '', 'query': {'pages': {'64216': {'pageid': 64216, 'ns': 0, 'title': 'Basic training', 'revisions': [{'revid': 123443, 'parentid': 0, 'user': 'Fredbauder', 'userid': 744, 'timestamp': '2002-07-25T05:00:59Z', 'size': 622, 'slots': {'main': {'contentmodel': 'wikitext', 'contentformat': 'text/x-wiki', '*': "'''Basic Training''' or bootcamp is a short intensive program for induction of recruits into an [[army]] or [[navy]]. In the [[United States]] a few military bases have special units devoted to basic training. The [[jargon]] of the service is introduced as well as the fundamentals of military discipline and the recruits are trained in the basic skills of their service. A great deal of emphasis is place upon proper wearing of the uniform, grooming, and drill.\r\n\r\nArmy recruits are often instructed in the firing and care of [[gun|guns]]; Navy recruits get a short introduction to [[fire fighting]].\r\n\r\nSee [[saltpetre]]"}}, 'comment': 'basic indeed'}]}}}}

    mwapicache.add_pageid_doc(123443, doc)
    assert mwapicache._cache["pageid"][123443] == doc
    assert doc == mwapicache.get_pageid_doc(123443)

def test_add_get_user_texts_batch_doc(mwapicache):
    doc = {'batchcomplete': '', 'query': {'users': [{'userid': 744, 'name': 'Test1', 'editcount': 2319, 'registration': '2002-02-28T06:13:53Z', 'groups': ['*', 'user', 'autoconfirmed'], 'gender': 'unknown'}]}}

    mwapicache.add_users_batch_doc(["Test1"], doc)
    assert mwapicache._cache["users"][("Test1",)] == doc
    assert doc == mwapicache.get_users_batch_doc(["Test1"])

def test_add_get_usercontribs_doc(mwapicache):
    doc = {"batchcomplete":"","continue":{"uccontinue":"20021112160010|453140","continue":"-||"},"query":{"usercontribs":[{"userid":744,"user":"Test1","pageid":111111,"revid":22222,"parentid":33333,"ns":0,"title":"Test","timestamp":"2002-11-15T20:52:13Z","minor":"","comment":"","size":3161}]}}

    mwapicache.add_usercontribs_doc("Test1", doc)
    assert mwapicache._cache["usercontribs"]["Test1"] == doc
    assert doc == mwapicache.get_usercontribs_doc("Test1")

def test_add_get_wbsgetsuggestions_doc(mwapicache):
    doc = {
        "search": [
            {
                "id": "P31",
                "url": "//www.wikidata.org/wiki/Property:P31",
                "rating": "0.38939021462979523",
                "label": "instance of",
                "description": "that class of which this subject is a particular example and member"
            },
            {
                "id": "P570",
                "url": "//www.wikidata.org/wiki/Property:P570",
                "rating": "0.0736081654448872",
                "label": "date of death",
                "description": "date on which the subject died"
            }
        ],
        "success": 1,
        "searchinfo": {
            "search": ""
        }
    }

    mwapicache.add_wbsgetsuggestions_doc("Q12345", doc)
    assert mwapicache._cache["wbsgetsuggestions"]["Q12345"] == doc
    assert doc == mwapicache.get_wbsgetsuggestions_doc("Q12345")
