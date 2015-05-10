from nose.tools import eq_

from ..dependent import Dependent, expand, expand_many, solve, solve_many


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

def test_expand():
    foo = Dependent("foo", lambda: "foo")
    bar = Dependent("bar", lambda foo: foo + "bar", dependencies=[foo])

    cache = expand(bar)

    assert foo in cache

def test_expand_many():
    foo = Dependent("foo", lambda: "foo")
    bar = Dependent("bar", lambda foo: foo + "bar", dependencies=[foo])
    baz = Dependent("baz", lambda baz: foo + "baz", dependencies=[foo])

    dependents = [bar, baz]

    cache = expand_many(dependents)

    assert foo in cache
