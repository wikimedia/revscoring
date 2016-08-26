from nose.tools import eq_
import pickle

import mwapi

from ....datasources import revision_oriented as ro
from ..datasources import (RevDocById, PageCreationRevDoc, UserInfoDoc,
                           LastUserRevDoc)
from ..extractor import Extractor


def test_rev_doc_by_id():
    extractor = Extractor(mwapi.Session("foobar"))
    rev_doc_by_id = RevDocById(ro.revision, extractor)

    hash(rev_doc_by_id)
    eq_(pickle.loads(pickle.dumps(rev_doc_by_id)), rev_doc_by_id)


def test_page_creation_rev_doc():
    extractor = Extractor(mwapi.Session("foobar"))
    page_creation_rev_doc = PageCreationRevDoc(ro.revision.page, extractor)

    hash(page_creation_rev_doc)
    eq_(pickle.loads(pickle.dumps(page_creation_rev_doc)),
        page_creation_rev_doc)


def test_user_info_doc():
    extractor = Extractor(mwapi.Session("foobar"))
    user_info_doc = UserInfoDoc(ro.revision.user, extractor)

    hash(user_info_doc)
    eq_(pickle.loads(pickle.dumps(user_info_doc)),
        user_info_doc)


def test_last_user_rev_doc():
    extractor = Extractor(mwapi.Session("foobar"))
    last_user_rev_doc = LastUserRevDoc(ro.revision, extractor)

    hash(last_user_rev_doc)
    eq_(pickle.loads(pickle.dumps(last_user_rev_doc)),
        last_user_rev_doc)
