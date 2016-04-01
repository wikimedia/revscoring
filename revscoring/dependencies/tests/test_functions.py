from nose.tools import eq_, raises

from ...errors import DependencyError, DependencyLoop
from ..dependent import Dependent
from ..functions import dig, draw, expand, normalize_context, solve


def test_solve():
    # Simple functions
    eq_(solve(lambda: "foo"), "foo")
    eq_(list(solve([lambda: "foo", lambda: "bar"])), ["foo", "bar"])

    # Dependents
    foo = Dependent("foo", lambda: "foo")
    bar = Dependent("bar", lambda: "bar")
    foobar = Dependent("foobar", lambda foo, bar: foo + bar,
                       depends_on=[foo, bar])
    eq_(solve(foobar), "foobar")
    eq_(list(solve([foo, bar, foobar])), ["foo", "bar", "foobar"])

    # Cache
    eq_(solve(foobar, cache={foobar: "foobaz"}), "foobaz")
    eq_(solve(foobar, cache={bar: "baz"}), "foobaz")
    eq_(solve(foobar, cache={"dependent.bar": "baz"}), "foobaz")

    # Context
    mybar = Dependent("bar", lambda: "baz")
    eq_(solve(foobar, context={mybar}), "foobaz")
    eq_(solve(foobar, context={mybar: mybar}), "foobaz")
    eq_(solve(foobar, context={bar: mybar}), "foobaz")
    eq_(solve(foobar, context={bar: lambda: "baz"}), "foobaz")

    solving_profile = {}
    solve(foobar, profile=solving_profile)
    # print(solving_profile)
    eq_(set(solving_profile.keys()), {foo, bar, foobar})

    list(solve([foo, bar, foobar], profile=solving_profile))
    # print(solving_profile)
    eq_(len(solving_profile[foobar]), 2)


@raises(RuntimeError)
def test_unsolveable():
    solve(5)


@raises(DependencyLoop)
def test_dependency_loop():
    foo = Dependent("foo")
    bar = Dependent("bar", depends_on=[foo])
    my_foo = Dependent("foo", depends_on=[bar])

    solve(bar, context={my_foo})


@raises(DependencyError)
def test_dependency_error():
    def derror():
        raise DependencyError()
    raises_error = Dependent("foo", derror)

    solve(raises_error)


def test_expand():
    foo = Dependent("foo", lambda: "foo")
    bar = Dependent("bar", lambda: "bar")
    foobar = Dependent("foobar", lambda foo, bar: foo + bar,
                       depends_on=[foo, bar])

    derp = Dependent("derp", lambda: "derp")
    fooderp = Dependent("fooderp", lambda foo, derp: foo + derp,
                        depends_on=[foo, derp])

    dependents = list(expand(foobar))
    eq_(len(dependents), 3)
    eq_(set(dependents), {foo, bar, foobar})

    dependents = list(expand([fooderp, foobar]))
    eq_(len(dependents), 5)
    eq_(set(dependents), {derp, fooderp, foo, bar, foobar})


def test_dig():
    foo = Dependent("foo", lambda: "foo")
    bar = Dependent("bar", lambda: "bar")
    foobar = Dependent("foobar", lambda foo, bar: foo + bar,
                       depends_on=[foo, bar])
    foobar_foobar = Dependent("foobar_foobar",
                              lambda foobar1, foobar2: foobar1 + "_" + foobar2,
                              depends_on=[foobar, foobar])

    roots = list(dig(foobar_foobar))
    eq_(len(roots), 2)
    eq_(set(roots), {foo, bar})

    roots = list(dig([foobar, foo, bar]))
    eq_(len(roots), 2)
    eq_(set(roots), {foo, bar})

    roots = list(dig(foobar_foobar, cache={foo}))
    eq_(len(roots), 1)
    eq_(set(roots), {bar})

    myfoobar = Dependent("foobar", lambda foo1, foo2: foo1 + foo2,
                         depends_on=[foo, foo])
    roots = list(dig(foobar_foobar, context={myfoobar}))
    eq_(len(roots), 1)
    eq_(set(roots), {foo})

    def get_5():
        return 5

    myfoobar = Dependent("foobar", lambda my_5: 5 ** 2,
                         depends_on=[get_5])
    roots = list(dig(foobar_foobar, context={myfoobar}))
    eq_(len(roots), 1)
    eq_(set(roots), {get_5})


def test_draw():
    foo = Dependent("foo", lambda: "foo")
    bar = Dependent("bar", lambda foo: foo + "bar", dependencies=[foo])

    draw(bar)  # Does not throw an error
    draw(bar, cache={foo: "CACHED"})  # Does not throw an error


@raises(DependencyError)
def test_not_implemented_error():
    foo = Dependent("foo")
    solve(foo)


@raises(TypeError)
def test_normalize_context_fail():
    normalize_context(15)
