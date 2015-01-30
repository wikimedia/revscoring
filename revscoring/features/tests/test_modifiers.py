import pickle
from math import log as math_log

from nose.tools import eq_

from .. import modifiers
from ...dependent import solve
from ..feature import Feature


def return_five(): return 5

def test_log():
    
    five = Feature("five", return_five, returns=int, depends_on=[])
    
    log_five = modifiers.log(five)
    
    eq_(solve(log_five), math_log(5))


def test_sum_sub():
    
    five = Feature("five", return_five, returns=int, depends_on=[])
    
    five_plus_one = modifiers.add(five, 1)
    
    eq_(solve(five_plus_one), 6)
    
    five_minus_one = modifiers.sub(five, 1)
    
    print(five_minus_one)
    eq_(solve(five_minus_one), 4)
    
def test_pickling():
    
    five = Feature("five", return_five, returns=int, depends_on=[])
    
    five_plus_one = modifiers.add(five, 1)
    
    eq_(solve(pickle.loads(pickle.dumps(five_plus_one))), 6)
    
    log_five = modifiers.log(five)
    
    eq_(solve(pickle.loads(pickle.dumps(log_five))), math_log(5))

def test_str_and_repr():
    
    five = Feature("five", return_five, returns=int, depends_on=[])
    
    log_five_plus_one = modifiers.log(five + 1)
    
    eq_(str(log_five_plus_one), "<log(five + 1)>")
    eq_(repr(log_five_plus_one), "<log(five + 1)>")
