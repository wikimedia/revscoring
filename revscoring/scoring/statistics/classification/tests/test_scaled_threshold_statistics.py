import json
import random

from numpy import linspace

from ..scaled_threshold_statistics import ScaledThresholdStatistics

PROBAS = list(linspace(0, 1, 4000))
LABELS = [True if proba > 0.8 or
                  proba > 0.5 and (int(proba * 100) % 10) != 5 or
                  proba > 0.2 and proba <= 0.5 and
                    (int(proba * 100) % 10) == 5 else False
          for proba in PROBAS]
OBS = list(zip(PROBAS, LABELS))

SKEWED = random.sample([(p, l) for p, l in OBS if l], 500) + \
         random.sample([(p, l) for p, l in OBS if not l], 1500)
BALANCED = random.sample([(p, l) for p, l in OBS if l], 1000) + \
           random.sample([(p, l) for p, l in OBS if not l], 1000)


def test_sts():
    skewed_sts = ScaledThresholdStatistics(
        *zip(*SKEWED), population_rate=0.05)
    balanced_sts = ScaledThresholdStatistics(
        *zip(*BALANCED), population_rate=0.05)
    print(skewed_sts.format_str({}, threshold_ndigits=3))
    print(balanced_sts.format_str({}, threshold_ndigits=3))
    print(skewed_sts.format_str({'maximum recall @ precision >= 0.9': {}}))
    print(json.dumps(skewed_sts.format_json(
        {'maximum recall @ precision >= 0.9': {},
         'maximum filter_rate @ recall >= 0.9': {}})))
    json.dumps(skewed_sts.format_json({}))

    s_threshold_stats = {}
    b_threshold_stats = {}
    for s_stats, b_stats in zip(skewed_sts, balanced_sts):
        squared_error = 0
        error = 0

        s_rounded_threshold = round(s_stats[0], 3)
        s_threshold_stats[s_rounded_threshold] = s_stats[1]

        b_rounded_threshold = round(b_stats[0], 3)
        b_threshold_stats[b_rounded_threshold] = b_stats[1]

    count = 0
    for threshold, s_stats in s_threshold_stats.items():
        if threshold not in b_threshold_stats:
            continue
        b_stats = b_threshold_stats[threshold]
        for stat_name in s_stats:
            if s_stats[stat_name] is not None:
                diff = (s_stats[stat_name] or 0) - (b_stats[stat_name] or 0)
                squared_error += diff**2
                error += diff
                count += 1

    rmse = (squared_error / count)**0.5
    me = error / count
    print("RMSE", rmse)
    print("Error", me)
    assert rmse < 0.05, rmse
    assert count > 1000
