import pickle
from math import log as math_log

from nose.tools import eq_, raises

from .. import modifiers
from ...dependent import solve
from ..feature import Feature


def return_foo(foo):
    return foo

def test_feature():
    
    foobar = Feature("foobar", return_foo,
                     returns=int, depends_on=["foo"])
    
    eq_(foobar(5), 5)
    
    eq_(pickle.loads(pickle.dumps(foobar))(5), 5)

@raises(ValueError)
def test_feature_type():
    
    foobar = Feature("foobar", return_foo, returns=int, depends_on=["foo"])
    
    foobar(11)
    
    foobar("not int")

def test_add_sub():
    
    five = Feature("five", lambda: 5, returns=int, depends_on=[])
    
    five_plus_one = five + 1
    
    eq_(five_plus_one.returns, int)
    eq_(solve(five_plus_one), 6)

def test_log():
    
    five = Feature("five", lambda: 5, returns=int, depends_on=[])
    
    log_five_plus_one = modifiers.log(five + 1)
    
    eq_(log_five_plus_one.returns, float)
    eq_(solve(log_five_plus_one), math_log(5+1))

def test_solve():
    
    five = Feature("five", lambda: 5, returns=int, depends_on=[])
    
    five_plus_one = Feature("five_plus_one", lambda five: five+1,
                            returns=int, depends_on=[five])
    
    modified_five_plus_one = five + 1
    
    eq_(solve(five_plus_one), 6)
    eq_(solve(modified_five_plus_one), 6)
