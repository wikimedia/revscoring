from nose.tools import eq_

from ..table import table


def test_boolean():
    test_statistic = table()
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
    eq_(stats, {False: {False: 5}, True: {True: 5}})

    stats = test_statistic.score(half_right, labels)
    eq_(stats, {False: {True: 5}, True: {True: 5}})

    assert len(test_statistic.format(stats)) > 5


def test_multiclass():
    test_statistic = table()
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
        {'c': {'c': 6}, 'b': {'b': 6}, 'a': {'a': 6}})

    stats = test_statistic.score(sometimes_right, labels)
    eq_(test_statistic.format(stats, format="json"),
        {'a': {'a': 6},
         'b': {'a': 5, 'b': 1},
         'c': {'a': 5, 'c': 1}})

    print(test_statistic.format(stats))
    eq_(len(test_statistic.format(stats).split("\n")), 7)
