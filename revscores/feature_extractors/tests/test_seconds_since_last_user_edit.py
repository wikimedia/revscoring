from collections import namedtuple

from mw import Timestamp
from nose.tools import eq_

from ..seconds_since_last_page_edit import seconds_since_last_page_edit


def test_seconds_since_last_page_edit():
    
    FakeRevisionMetadata = namedtuple("RevisionMetadata", ['timestamp'])
    
    previous_user_revision_metadata = \
            FakeRevisionMetadata(Timestamp(1234567890))
    
    revision_metadata = FakeRevisionMetadata(Timestamp(1234567890) + 1000)
    
    eq_(seconds_since_last_page_edit(previous_user_revision_metadata,
                                     revision_metadata),
        1000)
