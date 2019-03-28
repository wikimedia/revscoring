from pytest import raises

from revscoring.dependencies.dependent import Dependent
from revscoring.dependencies.functions import (dig, draw, expand,
                                               normalize_context, solve)
from revscoring.errors import DependencyError, DependencyLoop


def test_solve():
    # Simple functions
    assert solve(lambda: "foo") == "foo"
    assert list(solve([lambda: "foo", lambda: "bar"])) == ["foo", "bar"]

    # Dependents
    foo = Dependent("foo", lambda: "foo")
    bar = Dependent("bar", lambda: "bar")
    foobar = Dependent("foobar", lambda foo, bar: foo + bar,
                       depends_on=[foo, bar])
    assert solve(foobar) == "foobar"
    assert list(solve([foo, bar, foobar])) == ["foo", "bar", "foobar"]

    # Cache
    assert solve(foobar, cache={foobar: "foobaz"}) == "foobaz"
    assert solve(foobar, cache={bar: "baz"}) == "foobaz"
    assert solve(foobar, cache={"dependent.bar": "baz"}) == "foobaz"

    # Context
    mybar = Dependent("bar", lambda: "baz")
    assert solve(foobar, context={mybar}) == "foobaz"
    assert solve(foobar, context={mybar: mybar}) == "foobaz"
    assert solve(foobar, context={bar: mybar}) == "foobaz"
    assert solve(foobar, context={bar: lambda: "baz"}) == "foobaz"

    solving_profile = {}
    solve(foobar, profile=solving_profile)
    # print(solving_profile)
    assert set(solving_profile.keys()) == {foo, bar, foobar}

    list(solve([foo, bar, foobar], profile=solving_profile))
    # print(solving_profile)
    assert len(solving_profile[foobar]) == 2


def test_unsolveable():
    with raises(RuntimeError):
        solve(5)


def test_dependency_loop():
    with raises(DependencyLoop):
        foo = Dependent("foo")
        bar = Dependent("bar", depends_on=[foo])
        my_foo = Dependent("foo", depends_on=[bar])

        solve(bar, context={my_foo})


def test_dependency_error():
    with raises(DependencyError):
        def derror():
            raise DependencyError()
        raises_error = Dependent("foo", derror)

        solve(raises_error)


def test_cache_preservation():
    foo = Dependent("foo")
    bar = Dependent("bar", depends_on=[foo], process=lambda foo: foo + "bar")
    fooz = Dependent("foo", process=lambda: "fooz")

    cache = {foo: "foo"}
    values = list(solve([foo, bar], cache=cache))
    assert values == ["foo", "foobar"]
    assert cache[bar] == "foobar"

    cache = {}
    values = list(solve([foo, bar], context={fooz}, cache=cache))
    assert values == ["fooz", "foozbar"]
    assert cache[bar] == "foozbar"


def test_expand():
    foo = Dependent("foo", lambda: "foo")
    bar = Dependent("bar", lambda: "bar")
    foobar = Dependent("foobar", lambda foo, bar: foo + bar,
                       depends_on=[foo, bar])

    derp = Dependent("derp", lambda: "derp")
    fooderp = Dependent("fooderp", lambda foo, derp: foo + derp,
                        depends_on=[foo, derp])

    dependents = list(expand(foobar))
    assert len(dependents) == 3
    assert set(dependents) == {foo, bar, foobar}

    dependents = list(expand([fooderp, foobar]))
    assert len(dependents) == 5
    assert set(dependents) == {derp, fooderp, foo, bar, foobar}


def test_dig():
    foo = Dependent("foo", lambda: "foo")
    bar = Dependent("bar", lambda: "bar")
    foobar = Dependent("foobar", lambda foo, bar: foo + bar,
                       depends_on=[foo, bar])
    foobar_foobar = Dependent("foobar_foobar",
                              lambda foobar1, foobar2: foobar1 + "_" + foobar2,
                              depends_on=[foobar, foobar])

    roots = list(dig(foobar_foobar))
    assert len(roots) == 2
    assert set(roots) == {foo, bar}

    roots = list(dig([foobar, foo, bar]))
    assert len(roots) == 2
    assert set(roots) == {foo, bar}

    roots = list(dig(foobar_foobar, cache={foo}))
    assert len(roots) == 1
    assert set(roots) == {bar}

    myfoobar = Dependent("foobar", lambda foo1, foo2: foo1 + foo2,
                         depends_on=[foo, foo])
    roots = list(dig(foobar_foobar, context={myfoobar}))
    assert len(roots) == 1
    assert set(roots) == {foo}

    def get_5():
        return 5

    myfoobar = Dependent("foobar", lambda my_5: 5 ** 2,
                         depends_on=[get_5])
    roots = list(dig(foobar_foobar, context={myfoobar}))
    assert len(roots) == 1
    assert set(roots) == {get_5}


def test_draw():
    foo = Dependent("foo", lambda: "foo")
    bar = Dependent("bar", lambda foo: foo + "bar", dependencies=[foo])

    draw(bar)  # Does not throw an error
    draw(bar, cache={foo: "CACHED"})  # Does not throw an error


def test_not_implemented_error():
    with raises(DependencyError):
        foo = Dependent("foo")
        solve(foo)


def test_normalize_context_fail():
    with raises(TypeError):
        normalize_context(15)
