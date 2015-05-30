from nose.tools import eq_

from ..context import Context
from ..dependent import Dependent


def test_context():
    # No context
    context = Context()
    foo = Dependent("foo", lambda: "foo")
    bar = Dependent("bar", lambda: "bar")
    foobar = Dependent("foobar", lambda foo, bar: foo + bar,
                       depends_on=[foo, bar])
    eq_(context.solve(foobar), "foobar")
    eq_(list(context.solve([foo, bar, foobar])), ["foo", "bar", "foobar"])

    # Cache context
    context = Context(cache={bar: "baz"})
    eq_(context.solve(foobar), "foobaz")

    # Context context
    mybar = Dependent("bar", lambda: "baz")

    context = Context(context={mybar})
    eq_(context.solve(foobar), "foobaz")

    context = Context(context={mybar: mybar})
    eq_(context.solve(foobar), "foobaz")

    context = Context(context={bar: mybar})
    eq_(context.solve(foobar), "foobaz")

    context = Context(context={bar: lambda: "baz"})
    eq_(context.solve(foobar), "foobaz")
