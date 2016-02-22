from nose.tools import eq_

from ..accuracy import accuracy


def test_boolean():
    test_statistic = accuracy()
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
    eq_(stats, 0.5)

    eq_(test_statistic.format(stats), "Accuracy: 0.5")
    eq_(test_statistic.format(stats, format="json"), 0.5)


def test_multiclass():
    test_statistic = accuracy()
    score_labels = [
        ({'prediction': "a"}, {'prediction': "a"}, "a"),
        ({'prediction': "b"}, {'prediction': "a"}, "b"),
        ({'prediction': "c"}, {'prediction': "a"}, "c"),
        ({'prediction': "a"}, {'prediction': "a"}, "a"),
        ({'prediction': "b"}, {'prediction': "a"}, "b"),
        ({'prediction': "c"}, {'prediction': "a"}, "c"),
        ({'prediction': "a"}, {'prediction': "a"}, "a"),
        ({'prediction': "b"}, {'prediction': "a"}, "b"),
        ({'prediction': "c"}, {'prediction': "a"}, "c")
    ]
    all_right, third_right, labels = zip(*score_labels)

    stats = test_statistic.score(all_right, labels)
    eq_(stats, 1.0)

    stats = test_statistic.score(third_right, labels)
    eq_(round(stats, 3), 0.333)

    eq_(test_statistic.format(stats), "Accuracy: 0.333")
    eq_(test_statistic.format(stats, format="json"), 0.333)
