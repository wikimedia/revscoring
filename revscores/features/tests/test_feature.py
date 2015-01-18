import pickle

from nose.tools import eq_, raises

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

def test_feature():
    
    foobar = Feature("foobar", return_foo,
                     returns=int, depends_on=["foo"])
    
    foobar_plus_one = foobar + 1
    
    eq_(foobar_plus_one(5), 6)
