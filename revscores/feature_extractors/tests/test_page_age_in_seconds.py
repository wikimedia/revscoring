from collections import namedtuple

from mw import Timestamp
from nose.tools import eq_

from ..page_age_in_seconds import page_age_in_seconds


def test_page_age_in_seconds():
    
    FakeRevisionMetadata = namedtuple("RevisionMetadata", ['timestamp'])
    
    first_revision_metadata = FakeRevisionMetadata(Timestamp(1234567890))
    revision_metadata = FakeRevisionMetadata(Timestamp(1234567890) + 1000)
    
    eq_(page_age_in_seconds(first_revision_metadata, revision_metadata), 1000)
