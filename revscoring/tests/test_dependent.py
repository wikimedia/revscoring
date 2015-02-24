from nose.tools import eq_

from ..dependent import Dependent, solve, solve_many


def test_solve():
    
    foo = Dependent("foo", lambda: "foo")
    bar = Dependent("bar", lambda foo: foo + "bar", dependencies=[foo])
    
    eq_(solve(bar), "foobar")
    
def test_solve_many():
    
    foo = Dependent("foo", lambda: "foo")
    bar = Dependent("bar", lambda foo: foo + "bar", dependencies=[foo])
    
    eq_(list(solve_many([bar, foo, bar])), ["foobar", "foo", "foobar"])
    eq_(foo.calls, 1)
    eq_(bar.calls, 1)
