
from revscoring.dependencies.context import Context
from revscoring.dependencies.dependent import Dependent


def test_context():
    # No context
    context = Context()
    foo = Dependent("foo", lambda: "foo")
    bar = Dependent("bar", lambda: "bar")
    foobar = Dependent("foobar", lambda foo, bar: foo + bar,
                       depends_on=[foo, bar])
    assert context.solve(foobar) == "foobar"
    assert list(context.solve([foo, bar, foobar])) == ["foo", "bar", "foobar"]

    # Cache context
    context = Context(cache={bar: "baz"})
    assert context.solve(foobar) == "foobaz"

    # Context context
    mybar = Dependent("bar", lambda: "baz")

    context = Context(context={mybar})
    assert context.solve(foobar) == "foobaz"

    context = Context(context={mybar: mybar})
    assert context.solve(foobar) == "foobaz"

    context = Context(context={bar: mybar})
    assert context.solve(foobar) == "foobaz"

    context = Context(context={bar: lambda: "baz"})
    assert context.solve(foobar) == "foobaz"
    context.update(context={bar: lambda: "buzz"})
    assert context.solve(foobar) == "foobuzz"

    assert set(context.expand([foobar])) == {foo, bar, foobar}

    context.update(context={bar: bar})
    assert set(context.dig([foobar])) == {foo, bar}

    assert (context.draw(foobar) == " - <dependent.foobar>\n" +
            "\t - <dependent.foo>\n" +
            "\t - <dependent.bar>\n")
