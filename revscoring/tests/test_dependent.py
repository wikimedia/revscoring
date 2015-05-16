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

def test_inject():

    foo = Dependent("foo", lambda: NotImplemented)
    bar1 = Dependent("bar1", lambda foo: foo + "bar1", dependencies=[foo])
    bar2 = Dependent("bar2", lambda foo: foo + "bar2", dependencies=[foo])
    injected_foo = Dependent("foo", lambda: "foo")

    eq_(list(solve_many([bar1, bar2], context={injected_foo: injected_foo})),
        ['foobar1', 'foobar2'])

    eq_(injected_foo.calls, 1)
