import pickle

import mwapi

from revscoring.datasources import revision_oriented as ro
from revscoring.extractors.api.datasources import (LastUserRevDoc,
                                                   PageCreationRevDoc,
                                                   PropertySuggestionDoc,
                                                   RevDocById, UserInfoDoc)
from revscoring.extractors.api.extractor import Extractor


def test_rev_doc_by_id():
    extractor = Extractor(mwapi.Session("foobar"))
    rev_doc_by_id = RevDocById(ro.revision, extractor)

    hash(rev_doc_by_id)
    assert pickle.loads(pickle.dumps(rev_doc_by_id)) == rev_doc_by_id


def test_page_creation_rev_doc():
    extractor = Extractor(mwapi.Session("foobar"))
    page_creation_rev_doc = PageCreationRevDoc(ro.revision.page, extractor)

    hash(page_creation_rev_doc)
    assert (pickle.loads(pickle.dumps(page_creation_rev_doc)) ==
            page_creation_rev_doc)


def test_property_suggestion_doc():
    extractor = Extractor(mwapi.Session("foobar"))
    property_suggestion_doc = PropertySuggestionDoc(ro.revision.page, extractor)

    hash(property_suggestion_doc)
    assert (pickle.loads(pickle.dumps(property_suggestion_doc)) ==
            property_suggestion_doc)


def test_user_info_doc():
    extractor = Extractor(mwapi.Session("foobar"))
    user_info_doc = UserInfoDoc(ro.revision.user, extractor)

    hash(user_info_doc)
    assert (pickle.loads(pickle.dumps(user_info_doc)) ==
            user_info_doc)


def test_last_user_rev_doc():
    extractor = Extractor(mwapi.Session("foobar"))
    last_user_rev_doc = LastUserRevDoc(ro.revision, extractor)

    hash(last_user_rev_doc)
    assert (pickle.loads(pickle.dumps(last_user_rev_doc)) ==
            last_user_rev_doc)
