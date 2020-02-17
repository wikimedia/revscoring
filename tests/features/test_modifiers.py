import pickle
from math import log as math_log

from revscoring.dependencies import solve
from revscoring.features import modifiers


def add_three(arg1, arg2, arg3):
    return arg1 + arg2 + arg3


def reverse_div_(left, right):
    return right / left


def test_function_applier():
    @modifiers.function_applier
    def three_way_sum(arg1, arg2, arg3, name, returns):
        return add_three, name, returns

    four = three_way_sum(0, 1, 3)
    assert solve(four) == 4
    assert solve(pickle.loads(pickle.dumps(four))) == 4
    assert repr(four) == "<feature.add_three(0, 1, 3)>"

    vector_of_four = three_way_sum([1, 2, 3], [3, 2, 1], [0, 0, 0])
    assert solve(vector_of_four) == [4, 4, 4]
    assert solve(pickle.loads(pickle.dumps(vector_of_four))) == [4, 4, 4]
    assert repr(vector_of_four) == "<feature_vector.add_three([1, 2, 3], [3, 2, 1], [0, 0, 0])>"


def test_binary_operator():
    @modifiers.binary_operator
    def reverse_div(left, right, returns):
        return reverse_div_, "\\", returns or float

    four = reverse_div(2, 8)
    assert solve(four) == 4
    assert solve(pickle.loads(pickle.dumps(four))) == 4
    assert repr(four) == "<feature.(2 \ 8)>"

    vector_of_four = reverse_div([1, 2, 3], [4, 8, 12])
    assert solve(vector_of_four) == [4, 4, 4]
    assert solve(pickle.loads(pickle.dumps(vector_of_four))) == [4, 4, 4]
    assert repr(vector_of_four) == "<feature_vector.([1, 2, 3] \ [4, 8, 12])>"


def test_log():
    log_five = modifiers.log(5)

    assert solve(log_five) == math_log(5)

    assert solve(pickle.loads(pickle.dumps(log_five))) == math_log(5)

    assert repr(log_five) == "<feature.log(5)>"


def test_max():

    max_five_six_seven = modifiers.max(5, 6, 7)

    assert solve(max_five_six_seven) == 7

    assert solve(pickle.loads(pickle.dumps(max_five_six_seven))) == 7

    assert repr(max_five_six_seven) == "<feature.max(5, 6, 7)>"


def test_min():

    min_five_six_seven = modifiers.min(5, 6, 7)

    assert solve(min_five_six_seven) == 5

    assert pickle.loads(pickle.dumps(min_five_six_seven)) == min_five_six_seven

    assert repr(min_five_six_seven) == "<feature.min(5, 6, 7)>"
