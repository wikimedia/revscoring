from nose.tools import eq_

from ..statistics import (TestStatistic, filter_rate_at_recall, pr,
                          recall_at_fpr, roc)

test_score_labels = [
    ({'probability': {True: 0.00, False: 1.00}}, False),
    ({'probability': {True: 0.05, False: 0.95}}, False),
    ({'probability': {True: 0.10, False: 0.90}}, False),
    ({'probability': {True: 0.10, False: 0.90}}, False),
    ({'probability': {True: 0.21, False: 0.79}}, False),
    ({'probability': {True: 0.32, False: 0.68}}, False),
    ({'probability': {True: 0.48, False: 0.52}}, True),
    ({'probability': {True: 0.57, False: 0.43}}, False),
    ({'probability': {True: 0.62, False: 0.48}}, True),
    ({'probability': {True: 0.70, False: 0.30}}, False),
    ({'probability': {True: 0.75, False: 0.25}}, True),
    ({'probability': {True: 0.81, False: 0.19}}, True),
    ({'probability': {True: 0.83, False: 0.17}}, False),
    ({'probability': {True: 0.94, False: 0.06}}, True),
    ({'probability': {True: 0.95, False: 0.05}}, False),
    ({'probability': {True: 0.97, False: 0.03}}, True),
    ({'probability': {True: 0.97, False: 0.03}}, True),
    ({'probability': {True: 0.98, False: 0.98}}, True),
    ({'probability': {True: 0.99, False: 0.99}}, False)
]
test_scores, test_labels = zip(*test_score_labels)


def test_recall_at_fpr():
    stats = recall_at_fpr(0.5).score(test_scores, test_labels)
    eq_(stats['threshold'], 0.21)
    eq_(round(stats['recall'], 2), 1.00)
    eq_(round(stats['fpr'], 2), 0.47)

    stats = recall_at_fpr(0.25).score(test_scores, test_labels)
    eq_(stats['threshold'], 0.97)
    eq_(round(stats['recall'], 2), 0.38)
    eq_(round(stats['fpr'], 2), 0.25)

    stats = recall_at_fpr(0.1).score(test_scores, test_labels)
    eq_(stats['threshold'], None)
    eq_(stats['recall'], None)
    eq_(stats['fpr'], None)

    statistic = \
        TestStatistic.from_stat_str("recall_at_fpr(max_fpr=0.25)")
    stats = statistic.score(test_scores, test_labels)
    eq_(stats['threshold'], 0.97)
    eq_(round(stats['recall'], 2), 0.38)
    eq_(round(stats['fpr'], 2), 0.25)

    eq_(statistic.format(stats),
        "Recall @ 0.25 false-positive rate: " +
        "threshold=0.97, recall=0.375, fpr=0.25")

    eq_(str(recall_at_fpr(0.05)), "recall_at_fpr(max_fpr=0.05)")

    assert recall_at_fpr(0.05).format(stats) is not None


def test_filter_rate_at_recall():
    stats = filter_rate_at_recall(0.5).score(test_scores, test_labels)
    eq_(stats['threshold'], 0.94)
    eq_(round(stats['filter_rate'], 2), 0.68)
    eq_(round(stats['recall'], 2), 0.50)

    stats = filter_rate_at_recall(0.75).score(test_scores, test_labels)
    eq_(stats['threshold'], 0.75)
    eq_(round(stats['filter_rate'], 2), 0.53)
    eq_(round(stats['recall'], 2), 0.75)

    stats = filter_rate_at_recall(0.95).score(test_scores, test_labels)
    eq_(stats['threshold'], 0.48)
    eq_(round(stats['filter_rate'], 2), 0.32)
    eq_(round(stats['recall'], 2), 1.00)

    statistic = \
        TestStatistic.from_stat_str("filter_rate_at_recall(min_recall=0.95)")
    stats = statistic.score(test_scores, test_labels)
    eq_(stats['threshold'], 0.48)
    eq_(round(stats['filter_rate'], 2), 0.32)
    eq_(round(stats['recall'], 2), 1.00)

    eq_(statistic.format(stats),
        "Filter rate @ 0.95 recall: " +
        "threshold=0.48, filter_rate=0.316, recall=1.0")

    eq_(str(filter_rate_at_recall(0.95)),
        "filter_rate_at_recall(min_recall=0.95)")

    assert filter_rate_at_recall(0.95).format(stats) is not None


def test_roc():
    stats = roc().score(test_scores, test_labels)
    eq_(round(stats['auc'], 2), 0.77)

    statistic = TestStatistic.from_stat_str("roc")
    stats = statistic.score(test_scores, test_labels)
    eq_(round(stats['auc'], 2), 0.77)

    eq_(statistic.format(stats), "ROC-AUC: 0.773")

    eq_(str(roc()), "roc")

    assert roc().format(stats) is not None


def test_pr():
    stats = pr().score(test_scores, test_labels)
    eq_(round(stats['auc'], 2), 0.57)

    statistic = TestStatistic.from_stat_str("pr")
    stats = statistic.score(test_scores, test_labels)
    eq_(round(stats['auc'], 2), 0.57)

    eq_(statistic.format(stats), "PR-AUC: 0.574")

    eq_(str(pr()), "pr")

    assert pr().format(stats) is not None
