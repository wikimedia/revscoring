from math import log

from nose.tools import eq_

from .. import modifiers
from ..features import Feature


def test_log():
    
    def process(): return 5
    
    five = Feature("five", process, returns=int, depends_on=[])
    
    log_five = modifiers.log(five)
    
    eq_(log_five(), log(5))
