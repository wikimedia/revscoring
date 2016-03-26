import pickle

from nose.tools import eq_, raises

from ...dependencies import solve
from ..feature import Feature
from ..modifiers import not_


def return_five():
    return 5

five = Feature("five", return_five, returns=int, depends_on=[])


def return_true():
    return True

true = Feature("true", return_true, returns=bool, depends_on=[])


def identity_process(value):
    return value
int_identity = Feature("int_identity", identity_process,
                       returns=int, depends_on=["value"])


def check_feature(feature, expected):

    eq_(feature.returns, type(expected))

    eq_(hash(pickle.loads(pickle.dumps(feature))), hash(feature))

    eq_(solve(feature), expected)
    eq_(solve(pickle.loads(pickle.dumps(feature))), expected)


def test_feature():
    f = Feature("f")

    eq_(pickle.loads(pickle.dumps(f)), f)
    eq_(solve(f, cache={f: 5}), 5)
    eq_(solve(f, cache={"feature.f": 5}), 5)

    check_feature(five, 5)


def test_minimal_constructor():
    myfive = Feature("five")

    eq_(myfive, five)


@raises(ValueError)
def test_feature_type():

    int_identity(11)

    int_identity("not int")


def test_add():
    five_plus_one = five + 1
    check_feature(five_plus_one, 6)

    five_plus_five = five + five
    check_feature(five_plus_five, 10)


def test_sub():
    five_minus_one = five - 1
    check_feature(five_minus_one, 4)

    five_minus_five = five - five
    check_feature(five_minus_five, 0)


def test_mul():
    five_times_two = five * 2
    check_feature(five_times_two, 10)

    five_times_five = five * five
    check_feature(five_times_five, 25)


def test_div():
    five_divide_two = five / 2
    check_feature(five_divide_two, 2.5)

    five_divide_five = five / five
    check_feature(five_divide_five, 1.0)


def test_gt():
    five_gt_one = five > 1
    check_feature(five_gt_one, True)

    five_gt_five = five > five
    check_feature(five_gt_five, False)


def test_lt():
    five_lt_one = five < 1
    check_feature(five_lt_one, False)

    five_lt_five = five < five
    check_feature(five_lt_five, False)


def test_ge():
    five_ge_one = five >= 1
    check_feature(five_ge_one, True)

    five_ge_five = five >= five
    check_feature(five_ge_five, True)


def test_le():
    five_le_one = five <= 1
    check_feature(five_le_one, False)

    five_le_five = five <= five
    check_feature(five_le_five, True)


def test_eq():
    five_eq_one = five == 1
    check_feature(five_eq_one, False)

    five_eq_five = five == five
    check_feature(five_eq_five, True)


def test_ne():
    five_ne_one = five != 1
    check_feature(five_ne_one, True)

    five_ne_five = five != five
    check_feature(five_ne_five, False)


def test_and():
    true_and_true = true.and_(true)
    check_feature(true_and_true, True)

    true_and_not_true = true.and_(not_(true))
    check_feature(true_and_not_true, False)


def test_or():
    true_or_true = true.or_(true)
    check_feature(true_or_true, True)

    true_or_not_true = true.or_(not_(true))
    check_feature(true_or_not_true, True)


def test_not():
    not_true = not_(true)
    check_feature(not_true, False)

    not_true = true.not_()
    check_feature(not_true, False)


def test_complex():
    five_plus_five_times_two_is_fifteen = five + five * 2 == 15
    check_feature(five_plus_five_times_two_is_fifteen, True)

    grouped_five_plus_five_times_two_is_twenty = (five + five) * 2 == 20
    check_feature(grouped_five_plus_five_times_two_is_twenty, True)
