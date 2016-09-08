from nose.tools import eq_

from ..roc import roc


def test_boolean():
    test_statistic = roc()
    score_labels = [
        ({'probability': {True: 0.89, False: 0.11}},
         {'probability': {True: 0.83, False: 0.17}}, True),
        ({'probability': {True: 0.09, False: 0.91}},
         {'probability': {True: 0.63, False: 0.37}}, False),
        ({'probability': {True: 0.83, False: 0.17}},
         {'probability': {True: 0.75, False: 0.25}}, True),
        ({'probability': {True: 0.07, False: 0.93}},
         {'probability': {True: 0.53, False: 0.47}}, False),
        ({'probability': {True: 0.97, False: 0.03}},
         {'probability': {True: 0.94, False: 0.06}}, True),
        ({'probability': {True: 0.15, False: 0.85}},
         {'probability': {True: 0.56, False: 0.44}}, False),
        ({'probability': {True: 0.99, False: 0.01}},
         {'probability': {True: 0.79, False: 0.21}}, True),
        ({'probability': {True: 0.05, False: 0.95}},
         {'probability': {True: 0.63, False: 0.37}}, False),
        ({'probability': {True: 0.75, False: 0.25}},
         {'probability': {True: 0.51, False: 0.49}}, True),
        ({'probability': {True: 0.18, False: 0.82}},
         {'probability': {True: 0.86, False: 0.24}}, False)
    ]
    all_right, half_right, labels = zip(*score_labels)

    stats = test_statistic.score(all_right, labels)
    eq_(test_statistic.format(stats, format="json"),
        {True: {'auc': 1.0},
         False: {'auc': 1.0}})

    stats = test_statistic.score(half_right, labels)
    eq_(test_statistic.format(stats, format="json"),
        {False: {'auc': 0.76000000000000001},
         True: {'auc': 0.68000000000000005}})

    eq_(test_statistic.format(stats),
        "ROC-AUC:\n" +
        "\t-----  ----\n" +
        "\tFalse  0.76\n" +
        "\tTrue   0.68\n" +
        "\t-----  ----\n")


def test_multiclass():
    test_statistic = roc()
    score_labels = [
        ({'probability': {"a": 0.92, "b": 0.03, "c": 0.05}},
         {'probability': {"a": 0.50, "b": 0.15, "c": 0.35}}, "a"),
        ({'probability': {"a": 0.12, "b": 0.82, "c": 0.10}},
         {'probability': {"a": 0.19, "b": 0.60, "c": 0.21}}, "b"),
        ({'probability': {"a": 0.05, "b": 0.10, "c": 0.85}},
         {'probability': {"a": 0.32, "b": 0.36, "c": 0.32}}, "c"),
        ({'probability': {"a": 0.92, "b": 0.03, "c": 0.05}},
         {'probability': {"a": 0.50, "b": 0.15, "c": 0.35}}, "a"),
        ({'probability': {"a": 0.12, "b": 0.82, "c": 0.10}},
         {'probability': {"a": 0.19, "b": 0.60, "c": 0.21}}, "b"),
        ({'probability': {"a": 0.05, "b": 0.10, "c": 0.85}},
         {'probability': {"a": 0.32, "b": 0.36, "c": 0.32}}, "c"),
        ({'probability': {"a": 0.92, "b": 0.03, "c": 0.05}},
         {'probability': {"a": 0.50, "b": 0.15, "c": 0.35}}, "a"),
        ({'probability': {"a": 0.12, "b": 0.82, "c": 0.10}},
         {'probability': {"a": 0.19, "b": 0.60, "c": 0.21}}, "b"),
        ({'probability': {"a": 0.05, "b": 0.10, "c": 0.85}},
         {'probability': {"a": 0.32, "b": 0.36, "c": 0.32}}, "c"),
        ({'probability': {"a": 0.92, "b": 0.03, "c": 0.05}},
         {'probability': {"a": 0.50, "b": 0.15, "c": 0.35}}, "a"),
        ({'probability': {"a": 0.12, "b": 0.82, "c": 0.10}},
         {'probability': {"a": 0.19, "b": 0.60, "c": 0.21}}, "b"),
        ({'probability': {"a": 0.05, "b": 0.10, "c": 0.85}},
         {'probability': {"a": 0.32, "b": 0.36, "c": 0.32}}, "c"),
        ({'probability': {"a": 0.92, "b": 0.03, "c": 0.05}},
         {'probability': {"a": 0.50, "b": 0.15, "c": 0.35}}, "a"),
        ({'probability': {"a": 0.12, "b": 0.82, "c": 0.10}},
         {'probability': {"a": 0.19, "b": 0.60, "c": 0.21}}, "b"),
        ({'probability': {"a": 0.05, "b": 0.10, "c": 0.85}},
         {'probability': {"a": 0.32, "b": 0.36, "c": 0.32}}, "c"),
        ({'probability': {"a": 0.92, "b": 0.03, "c": 0.05}},
         {'probability': {"a": 0.50, "b": 0.15, "c": 0.35}}, "a"),
        ({'probability': {"a": 0.12, "b": 0.82, "c": 0.10}},
         {'probability': {"a": 0.19, "b": 0.60, "c": 0.21}}, "b"),
        ({'probability': {"a": 0.05, "b": 0.10, "c": 0.85}},
         {'probability': {"a": 0.32, "b": 0.36, "c": 0.32}}, "c")
    ]
    all_right, sometimes_right, labels = zip(*score_labels)

    stats = test_statistic.score(all_right, labels)
    eq_(test_statistic.format(stats, format="json"),
        {'a': {'auc': 1.0}, 'c': {'auc': 1.0}, 'b': {'auc': 1.0}})

    stats = test_statistic.score(sometimes_right, labels)
    eq_(test_statistic.format(stats, format="json"),
        {'b': {'auc': 1.0}, 'a': {'auc': 1.0}, 'c': {'auc': 0.5}})

    assert len(test_statistic.format(stats)) > 5

    merged_stats = test_statistic.merge(
        [test_statistic.score(all_right, labels),
         test_statistic.score(sometimes_right, labels)])
    eq_(test_statistic.format(merged_stats, format="json"),
        {'a': {'auc': 0.995}, 'b': {'auc': 0.995}, 'c': {'auc': 0.753}})
