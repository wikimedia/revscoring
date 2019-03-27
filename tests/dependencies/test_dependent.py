import pickle

from pytest import raises

from revscoring.dependencies.dependent import Dependent, DependentSet


def test_dependent():

    foobar1 = Dependent("foobar", lambda: "foobar1")
    foobar2 = Dependent("foobar", lambda: "foobar2")

    assert foobar1 == foobar2
    assert foobar1 != "foo"

    assert hash(foobar1) == hash(foobar2)

    assert foobar1 in {foobar2}


def test_name_type():
    with raises(TypeError):
        Dependent(5)  # Name can't be number


def test_format_name():
    foobar1 = Dependent("foobar")
    assert foobar1._format_name(None, []) == "Dependent()"


def test_dependent_set():
    my_dependents = DependentSet("my_dependents")
    c = Dependent('c')
    d = Dependent('d')
    e = Dependent('e')
    my_dependents.c = c

    assert my_dependents == my_dependents
    assert my_dependents != "foo"
    assert len(my_dependents) == 1
    assert set(my_dependents) == {c}

    assert c in my_dependents
    assert d not in my_dependents, set(my_dependents)

    my_dependents.d = d

    assert my_dependents & {d} == {d}
    assert my_dependents & {e} == set()
    assert my_dependents | {e} == {c, d, e}
    assert my_dependents - {c} == {d}

    my_sub_dependents = DependentSet("my_sub_dependents")
    f = Dependent('f')
    my_sub_dependents.f = f
    my_dependents.sub = my_sub_dependents

    assert my_sub_dependents.f in my_dependents

    assert set(my_dependents) == {c, d, f}
    assert my_dependents & {d} == {d}
    assert my_dependents & {f} == {f}
    assert my_dependents | {e} == {c, d, e, f}
    assert my_dependents - {f} == {c, d}

    assert pickle.loads(pickle.dumps(my_dependents)) == my_dependents


def test_duplicate_feature_warning():
    my_dependents = DependentSet("my_dependents")
    my_dependents.c = Dependent('c')  # Same!
    my_dependents.d = Dependent('d')
    my_dependents.e = Dependent('c')  # Same!
