from nose.tools import eq_

from ..f1 import f1


def test_boolean():
    test_statistic = f1()
    score_labels = [
        ({'prediction': True}, {'prediction': True}, True),
        ({'prediction': False}, {'prediction': True}, False),
        ({'prediction': True}, {'prediction': True}, True),
        ({'prediction': False}, {'prediction': True}, False),
        ({'prediction': True}, {'prediction': True}, True),
        ({'prediction': False}, {'prediction': True}, False),
        ({'prediction': True}, {'prediction': True}, True),
        ({'prediction': False}, {'prediction': True}, False),
        ({'prediction': True}, {'prediction': True}, True),
        ({'prediction': False}, {'prediction': True}, False)
    ]
    all_right, half_right, labels = zip(*score_labels)

    stats = test_statistic.score(all_right, labels)
    eq_(stats, 1.0)

    stats = test_statistic.score(half_right, labels)
    eq_(round(stats, 3), 0.667)

    eq_(test_statistic.format(stats), "F1: 0.667")
    eq_(test_statistic.format(stats, format="json"), 0.667)


def test_multiclass():
    test_statistic = f1()
    score_labels = [
        ({'prediction': "a"}, {'prediction': "a"}, "a"),
        ({'prediction': "b"}, {'prediction': "a"}, "b"),
        ({'prediction': "c"}, {'prediction': "a"}, "c"),
        ({'prediction': "a"}, {'prediction': "a"}, "a"),
        ({'prediction': "b"}, {'prediction': "a"}, "b"),
        ({'prediction': "c"}, {'prediction': "a"}, "c"),
        ({'prediction': "a"}, {'prediction': "a"}, "a"),
        ({'prediction': "b"}, {'prediction': "a"}, "b"),
        ({'prediction': "c"}, {'prediction': "a"}, "c"),
        ({'prediction': "a"}, {'prediction': "a"}, "a"),
        ({'prediction': "b"}, {'prediction': "a"}, "b"),
        ({'prediction': "c"}, {'prediction': "a"}, "c"),
        ({'prediction': "a"}, {'prediction': "a"}, "a"),
        ({'prediction': "b"}, {'prediction': "a"}, "b"),
        ({'prediction': "c"}, {'prediction': "a"}, "c"),
        ({'prediction': "a"}, {'prediction': "a"}, "a"),
        ({'prediction': "b"}, {'prediction': "b"}, "b"),
        ({'prediction': "c"}, {'prediction': "c"}, "c")
    ]
    all_right, sometimes_right, labels = zip(*score_labels)

    stats = test_statistic.score(all_right, labels)
    eq_(test_statistic.format(stats, format="json"),
        {'a': 1.0, 'b': 1.0, 'c': 1.0})

    stats = test_statistic.score(sometimes_right, labels)
    eq_(test_statistic.format(stats, format="json"),
        {'a': 0.545, 'b': 0.286, 'c': 0.286})

    assert len(test_statistic.format(stats)) > 5
