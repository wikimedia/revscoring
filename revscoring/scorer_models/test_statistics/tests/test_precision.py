from nose.tools import eq_

from ..precision import precision


def test_boolean():
    test_statistic = precision()
    score_labels = [
        ({'prediction': True}, {'prediction': True}, True),
        ({'prediction': False}, {'prediction': True}, False),
        ({'prediction': True}, {'prediction': False}, True),
        ({'prediction': False}, {'prediction': True}, False),
        ({'prediction': True}, {'prediction': True}, True),
        ({'prediction': False}, {'prediction': True}, False),
        ({'prediction': True}, {'prediction': True}, True),
        ({'prediction': False}, {'prediction': True}, False),
        ({'prediction': True}, {'prediction': True}, True),
        ({'prediction': False}, {'prediction': True}, False)
    ]
    all_right, half_right, labels = zip(*score_labels)

    stat = test_statistic.score(all_right, labels)
    eq_(stat, {False: 1.0, True: 1.0})

    stat = test_statistic.score(half_right, labels)
    eq_(stat, {False: 0.0, True: 0.44444444444444442})

    eq_(test_statistic.format(stat),
        "Precision:\n" +
        "\t-----  -----\n" +
        "\tFalse  0\n" +
        "\tTrue   0.444\n" +
        "\t-----  -----\n")
    eq_(test_statistic.format(stat, format="json"),
        {False: 0.0, True: 0.444})


def test_multiclass():
    test_statistic = precision()
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

    stat = test_statistic.score(all_right, labels)
    eq_(test_statistic.format(stat, format="json"),
        {'b': 1.0, 'c': 1.0, 'a': 1.0})

    stat = test_statistic.score(sometimes_right, labels)
    eq_(test_statistic.format(stat, format="json"),
        {'b': 1.0, 'c': 1.0, 'a': 0.375})

    assert len(test_statistic.format(stat)) > 5

    merged_stat = test_statistic.merge(
        [test_statistic.score(all_right, labels),
         test_statistic.score(sometimes_right, labels)])
    eq_(test_statistic.format(merged_stat, format="json"),
        {'b': 1.0, 'c': 1.0, 'a': 0.68799999999999994})
