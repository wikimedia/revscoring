from collections import namedtuple

from mw import Timestamp
from nose.tools import eq_

from ..hour_of_day_in_utc import hour_of_day_in_utc


def test_hour_of_day_in_utc():
    
    FakeRevisionMeta = namedtuple("RevisionMeta", ['timestamp'])
    
    rm = FakeRevisionMeta(Timestamp('2014-09-07T19:55:00Z'))
    
    eq_(hour_of_day_in_utc(rm), 19)
