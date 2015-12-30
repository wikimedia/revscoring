import pickle

from nose.tools import eq_, raises

from ..dependent import Dependent, DependentSet


def test_dependent():

    foobar1 = Dependent("foobar", lambda: "foobar1")
    foobar2 = Dependent("foobar", lambda: "foobar2")

    eq_(foobar1, foobar2)
    assert foobar1 != "foo"

    eq_(hash(foobar1), hash(foobar2))

    assert foobar1 in {foobar2}


@raises(TypeError)
def test_name_type():
    Dependent(5)  # Name can't be number


def test_format_name():
    foobar1 = Dependent("foobar")
    eq_(foobar1._format_name(None, []), "Dependent()")


def test_dependent_set():
    my_dependents = DependentSet("my_dependents")
    c = Dependent('c')
    d = Dependent('d')
    e = Dependent('e')
    my_dependents.c = c

    eq_(my_dependents, my_dependents)
    assert my_dependents != "foo"
    eq_(len(my_dependents), 1)
    eq_(set(my_dependents), {c})

    assert c in my_dependents
    assert d not in my_dependents, set(my_dependents)

    my_dependents.d = d

    eq_(my_dependents & {d}, {d})
    eq_(my_dependents & {e}, set())
    eq_(my_dependents | {e}, {c, d, e})
    eq_(my_dependents - {c}, {d})

    my_sub_dependents = DependentSet("my_sub_dependents")
    f = Dependent('f')
    my_sub_dependents.f = f
    my_dependents.sub = my_sub_dependents

    assert my_sub_dependents.f in my_dependents

    eq_(set(my_dependents), {c, d, f})
    eq_(my_dependents & {d}, {d})
    eq_(my_dependents & {f}, {f})
    eq_(my_dependents | {e}, {c, d, e, f})
    eq_(my_dependents - {f}, {c, d})

    eq_(pickle.loads(pickle.dumps(my_dependents)), my_dependents)


def test_duplicate_feature_warning():
    my_dependents = DependentSet("my_dependents")
    my_dependents.c = Dependent('c')  # Same!
    my_dependents.d = Dependent('d')
    my_dependents.e = Dependent('c')  # Same!
