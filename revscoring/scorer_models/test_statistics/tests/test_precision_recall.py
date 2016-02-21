from nose.tools import eq_

from ..precision_recall import precision_recall


def test_boolean():
    test_statistic = precision_recall()
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
        {'auc': 1.0})

    stats = test_statistic.score(half_right, labels)
    eq_(test_statistic.format(stats, format="json"),
        {'auc': 0.708})

    eq_(test_statistic.format(stats),
        "PR-AUC: 0.708")


def test_multiclass():
    test_statistic = precision_recall()
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
        {'a': 1.0, 'c': 1.0, 'b': 1.0})

    stats = test_statistic.score(sometimes_right, labels)
    eq_(test_statistic.format(stats, format="json"),
        {'a': 1.0, 'b': 1.0, 'c': 0.25})

    assert len(test_statistic.format(stats)) > 5
