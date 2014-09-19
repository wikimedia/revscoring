from collections import namedtuple

from mw import Timestamp
from nose.tools import eq_

from ..day_of_week_in_utc import day_of_week_in_utc


def test_day_of_week_in_utc():
    
    FakeRevisionMeta = namedtuple("RevisionMeta", ['timestamp'])
    
    rm = FakeRevisionMeta(Timestamp('2014-09-07T19:55:00Z'))
    
    eq_(day_of_week_in_utc(rm), 6)
