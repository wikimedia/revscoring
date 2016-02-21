from nose.tools import eq_

from ..filter_rate_at_recall import filter_rate_at_recall


def test_boolean():
    test_statistic = filter_rate_at_recall(0.75)
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
    eq_(stats['threshold'], 0.83)
    eq_(stats['filter_rate'], 0.6)

    stats = test_statistic.score(half_right, labels)
    eq_(stats['threshold'], 0.75)
    eq_(stats['filter_rate'], 0.5)

    eq_(test_statistic.format(stats),
        "Filter rate @ 0.75 recall: threshold=0.75, filter_rate=0.5, " +
        "recall=0.8")
    eq_(test_statistic.format(stats, format="json"),
        {'threshold': 0.75, 'recall': 0.8, 'filter_rate': 0.5})


def test_multiclass():
    test_statistic = filter_rate_at_recall(0.75)
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
        {'a': {'filter_rate': 0.667, 'recall': 1.0, 'threshold': 0.92},
         'b': {'filter_rate': 0.667, 'recall': 1.0, 'threshold': 0.82},
         'c': {'filter_rate': 0.667, 'recall': 1.0, 'threshold': 0.85}})

    stats = test_statistic.score(sometimes_right, labels)
    eq_(test_statistic.format(stats, format="json"),
        {'a': {'threshold': 0.5, 'recall': 1.0, 'filter_rate': 0.667},
         'b': {'threshold': 0.6, 'recall': 1.0, 'filter_rate': 0.667},
         'c': {'threshold': 0.32, 'recall': 1.0, 'filter_rate': 0.333}})

    assert len(test_statistic.format(stats)) > 5
