import json
import random

from numpy import linspace
import numpy as np
from revscoring.scoring.statistics.classification.scaled_threshold_statistics import \
    ScaledThresholdStatistics # noqa

np.random.seed(42)
# Build up the observations.
PROBAS = list(linspace(0, 1, 4000))
LABELS = [True if proba > 0.8 or
          proba > 0.5 and (int(proba * 100) % 10) != 5 or
          proba > 0.2 and proba <= 0.5 and
          (int(proba * 100) % 10) == 5 else False
          for proba in PROBAS]
OBS = list(zip(PROBAS, LABELS))

# Build two sets of observations, one skewed so that the target class is less
# common and the other is balanced.
SKEWED = random.sample([(p, l) for p, l in OBS if l], 500) + \
    random.sample([(p, l) for p, l in OBS if not l], 1500)
BALANCED = random.sample([(p, l) for p, l in OBS if l], 1000) + \
    random.sample([(p, l) for p, l in OBS if not l], 1000)


def test_sts():
    # Build threshold statistics with the same population rate for both
    # skewed and balanced datasets
    skewed_sts = ScaledThresholdStatistics(
        *zip(*SKEWED), population_rate=0.05)
    balanced_sts = ScaledThresholdStatistics(
        *zip(*BALANCED), population_rate=0.05)

    # Make sure we can format the statistics tables.  This will print out
    # if the test fails and that's good for debugging.
    print(skewed_sts.format_str({}, threshold_ndigits=3))
    print(balanced_sts.format_str({}, threshold_ndigits=3))
    print(skewed_sts.format_str({'maximum recall @ precision >= 0.9': {}}))
    print(skewed_sts.format_str({'maximum recall @ precision >= 1.1': {}}))
    print(json.dumps(skewed_sts.format_json(
        {'maximum recall @ precision >= 0.9': {},
         'maximum filter_rate @ recall >= 0.9': {}})))
    json.dumps(skewed_sts.format_json({}))

    # Build mappings between thresholds and statistics so that we can match and
    # compare threshold statistics for near-identical thresholds
    s_threshold_stats = {}
    b_threshold_stats = {}
    for s_stats, b_stats in zip(skewed_sts, balanced_sts):
        s_rounded_threshold = round(s_stats[0], 3)
        s_threshold_stats[s_rounded_threshold] = s_stats[1]

        b_rounded_threshold = round(b_stats[0], 3)
        b_threshold_stats[b_rounded_threshold] = b_stats[1]

    # Compare nearly identical threshold's statistics and accumulate error
    # metrics
    count = 0
    squared_error = 0
    error = 0
    for threshold, s_stats in s_threshold_stats.items():
        if threshold not in b_threshold_stats:
            continue
        b_stats = b_threshold_stats[threshold]
        for stat_name in s_stats:
            if s_stats[stat_name] and b_stats[stat_name]:
                diff = s_stats[stat_name] - b_stats[stat_name]
                squared_error += diff**2
                error += diff
                count += 1

    rmse = (squared_error / count)**0.5
    me = error / count
    print("RMSE", rmse)
    print("Error", me)
    # Make sure that the RMSE between the two tables is below 0.05
    assert rmse < 0.05, rmse
    # Make sure we actually found a substantial amount of overlap by checking
    # that the count is non-trivial
    assert count > 1000

    # Make sure that our overall statistics (roc, pr) are similar too
    assert abs(balanced_sts.roc_auc() - skewed_sts.roc_auc()) < 0.05, \
        abs(balanced_sts.roc_auc() - skewed_sts.roc_auc())
    assert abs(balanced_sts.pr_auc() - skewed_sts.pr_auc()) < 0.05, \
        abs(balanced_sts.pr_auc() - skewed_sts.pr_auc())

    limited_skewed_sts = ScaledThresholdStatistics(
        *zip(*SKEWED), population_rate=0.05, threshold_ndigits=1)
    assert len(limited_skewed_sts) <= 11, len(limited_skewed_sts)
