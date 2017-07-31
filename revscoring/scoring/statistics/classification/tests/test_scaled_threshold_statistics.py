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

    count = 0
    squared_error = 0
    error = 0
    for s_stats, b_stats in zip(skewed_sts, balanced_sts):
        for stat_name in s_stats[1]:
            if s_stats[1][stat_name] is not None:
                count += 1
                diff = s_stats[1][stat_name] - b_stats[1][stat_name]
                squared_error += diff**2
                error += diff

    rmse = (squared_error / count)**0.5
    me = error / count
    print("RMSE", rmse)
    print("Error", me)
    assert rmse < 0.20, rmse

    assert abs(balanced_sts.roc_auc() - skewed_sts.roc_auc()) < 0.10, \
           abs(balanced_sts.roc_auc() - skewed_sts.roc_auc())

    assert abs(balanced_sts.pr_auc() - skewed_sts.pr_auc()) < 0.10, \
           abs(balanced_sts.pr_auc() - skewed_sts.pr_auc())
