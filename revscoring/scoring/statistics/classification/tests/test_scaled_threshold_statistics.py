import json

from nose.tools import eq_
from numpy import linspace

from ..scaled_threshold_statistics import ScaledThresholdStatistics


def test_sts():
    y_trues = [True] * 50 + [False] * 1950
    y_decisions = list(linspace(.45, 1, 50)) + list(linspace(0, .55, 1950))

    sts = ScaledThresholdStatistics(y_decisions, y_trues)
    print(sts.format_str({}, threshold_ndigits=1))
    print("...")
    print(sts.format_str({'maximum recall @ precision >= 0.9': {}}))
    print(json.dumps(sts.format_json(
        {'maximum recall @ precision >= 0.9': {},
         'maximum filter_rate @ recall >= 0.9': {}})))
