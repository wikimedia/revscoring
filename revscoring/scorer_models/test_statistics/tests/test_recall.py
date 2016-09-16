from nose.tools import eq_

from ..recall import recall


def test_boolean():
    test_statistic = recall()
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
    eq_(stats, {False: 1.0, True: 1.0})

    stats = test_statistic.score(half_right, labels)
    eq_(stats, {False: 0.0, True: 1.0})

    eq_(test_statistic.format(stats),
        "Recall:\n" +
        "\t-----  -\n" +
        "\tFalse  0\n" +
        "\tTrue   1\n" +
        "\t-----  -\n")
    eq_(test_statistic.format(stats, format="json"),
        {False: 0.0, True: 1.0})


def test_multiclass():
    test_statistic = recall()
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
        {'b': 1.0, 'c': 1.0, 'a': 1.0})

    stats = test_statistic.score(sometimes_right, labels)
    eq_(test_statistic.format(stats, format="json"),
        {'b': 0.167, 'a': 1.0, 'c': 0.167})

    assert len(test_statistic.format(stats)) > 5

    merged_stats = test_statistic.merge(
        [test_statistic.score(all_right, labels),
         test_statistic.score(sometimes_right, labels)])
    eq_(test_statistic.format(merged_stats, format="json"),
        {'a': 1.0, 'b': 0.583, 'c': 0.583})
