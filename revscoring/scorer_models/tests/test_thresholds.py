from statistics import mean

from nose.tools import eq_

from ..thresholds import Thresholds

pool = \
    [({'probability': {True: i / 100, False: 1 - (i / 100)}},
      (False if (i < 50 and i % 10 != 3) or i % 10 == 5 else True))
     for i in range(0, 101)] + \
    [({'probability': {True: i / 100, False: 1 - (i / 100)}}, False)
     for i in range(0, 51)] * 39

score_labels = \
    [(s, l) for (s, l) in pool if l][:51] + \
    [(s, l) for (s, l) in pool if not l][:2000]

balanced_score_labels = \
    ([(s, l) for (s, l) in pool if l] * 20)[:1000] + \
    [(s, l) for (s, l) in pool if not l][:1000]


def test_thresholds():
    natural_thresholds = Thresholds(
        score_labels,
        label_rates={True: 2, False: 2}, max_thresholds=10)
    print(sum(1 for s, l in score_labels if l),
          sum(1 for s, l in score_labels if not l))
    print(natural_thresholds)

    scaled_thresholds = Thresholds(
        balanced_score_labels,
        label_rates={True: 40, False: 1}, max_thresholds=10)
    print(sum(1 for s, l in balanced_score_labels if l),
          sum(1 for s, l in balanced_score_labels if not l))
    print(scaled_thresholds)

    count = 0
    squared_error = 0
    error = 0
    for label in natural_thresholds:
        nl_thresholds = natural_thresholds[label]
        sl_thresholds = scaled_thresholds[label]
        for n_stats, s_stats in zip(nl_thresholds, sl_thresholds):
            for stat_name in n_stats:
                count += 1
                diff = n_stats[stat_name] - s_stats[stat_name]
                squared_error += diff**2
                error += diff

    rmse = (squared_error / count)**0.5
    print("RMSE", rmse)
    assert rmse < 0.05
