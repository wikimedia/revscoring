import pickle
from math import log as math_log

from revscoring.dependencies import solve
from revscoring.features import modifiers


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
