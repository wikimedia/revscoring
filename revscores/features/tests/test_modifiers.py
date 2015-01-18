from math import log

from nose.tools import eq_

from .. import modifiers
from ...dependent import solve
from ..feature import Feature


def test_log():
    
    def process(): return 5
    
    five = Feature("five", process, returns=int, depends_on=[])
    
    log_five = modifiers.log(five)
    
    eq_(solve(log_five), log(5))


def test_sum_sub():
    
    def process(): return 5
    
    five = Feature("five", process, returns=int, depends_on=[])
    
    five_plus_one = modifiers.add(five, 1)
    
    eq_(solve(five_plus_one), 6)
    
    five_minus_one = modifiers.sub(five, 1)
    
    print(five_minus_one)
    eq_(solve(five_minus_one), 4)
