import pickle
from math import log as math_log

from nose.tools import eq_, raises

from .. import modifiers
from ...dependent import solve
from ..feature import Feature

five = Feature("five", lambda: 5, returns=int, depends_on=[])

def identity_process(value): return value
int_identity = Feature("int_identity", identity_process,
                                       returns=int, depends_on=["value"])

def test_feature():
    
    eq_(int_identity(5), 5)
    
    eq_(pickle.loads(pickle.dumps(int_identity))(5), 5)

@raises(ValueError)
def test_feature_type():
    
    int_identity(11)
    
    int_identity("not int")

def test_add_sub():
    
    five_plus_one = five + 1
    five_minus_one = five - 1
    five_plus_five = five + five
    five_minus_five = five - five
    
    eq_(five_plus_one.returns, int)
    eq_(solve(five_plus_one), 6)
    eq_(solve(five_minus_one), 4)
    eq_(solve(five_plus_five), 10)
    eq_(solve(five_minus_five), 0)

def test_mul_div():
    
    five_times_two = five * 2
    five_divide_two = five / 2
    five_times_five = five * five
    five_divide_five = five / five
    
    eq_(five_times_two.returns, int)
    eq_(solve(five_times_two), 10)
    eq_(solve(five_divide_two), 2.5)
    eq_(solve(five_times_five), 25)
    eq_(solve(five_divide_five), 1)

def test_log():
    
    five = Feature("five", lambda: 5, returns=int, depends_on=[])
    
    log_five_plus_one = modifiers.log(five + 1)
    
    eq_(log_five_plus_one.returns, float)
    eq_(solve(log_five_plus_one), math_log(5+1))
