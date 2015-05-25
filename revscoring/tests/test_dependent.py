from nose.tools import eq_, raises

from ..dependent import (DependencyError, DependencyLoop, Dependent, draw,
                         expand, expand_many, solve, solve_many)


def test_solve():
    # Simple function
    eq_(solve(lambda: "foo"), "foo")

    # Actual dependencies
    foo = Dependent("foo", lambda: "foo")
    bar = Dependent("bar", lambda foo: foo + "bar", dependencies=[foo])
    eq_(solve(bar), "foobar")

def test_solve_many():

    foo = Dependent("foo", lambda: "foo")
    bar = Dependent("bar", lambda foo: foo + "bar", dependencies=[foo])

    eq_(list(solve_many([bar, foo, bar])), ["foobar", "foo", "foobar"])
    eq_(foo.calls, 1)
    eq_(bar.calls, 1)

def test_cache():

    foobar = Dependent("foobar", lambda foo: foo + "bar", depends_on=["foo"])

    eq_(solve(foobar, cache={"foo": "foo"}), "foobar")

def test_context():

    foo = Dependent("foo")
    my_foo = Dependent("foo", lambda: "foo")
    foobar = Dependent("foobar", lambda foo: foo + "bar", depends_on=[foo])

    # A function with no arguements
    eq_(solve(foobar, context={foo: lambda: "foo"}), "foobar")

    # A set of Dependent
    eq_(solve(foobar, context={my_foo}), "foobar")

    # A dict of Dependent
    eq_(solve(foobar, context={foo: my_foo}), "foobar")
    eq_(solve(foobar, context={my_foo: my_foo}), "foobar")

@raises(RuntimeError)
def test_unsolveable():
    solve("string")

@raises(DependencyLoop)
def test_loop():
    foo = Dependent("foo")
    bar = Dependent("bar", depends_on=[foo])
    my_foo = Dependent("foo", depends_on=[bar])

    solve(bar, context={my_foo})

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

def test_draw():
    foo = Dependent("foo", lambda: "foo")
    bar = Dependent("bar", lambda foo: foo + "bar", dependencies=[foo])

    draw(bar) # Does not throw an error
    draw(bar, cache={foo: "CACHED"}) # Does not throw an error

@raises(DependencyError)
def test_not_implemented_error():
    foo = Dependent("foo")
    solve(foo)
