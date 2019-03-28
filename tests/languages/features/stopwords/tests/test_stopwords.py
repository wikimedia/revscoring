import pickle

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.languages.features.stopwords.stopwords import Stopwords

stopwords_set = {'my', 'is', 'the', 'of', 'and'}


my_stops = Stopwords("my_language", stopwords_set)

r_text = revision_oriented.revision.text
p_text = revision_oriented.revision.parent.text


def test_stopwords():
    cache = {p_text: "My hat is the king of France.",
             r_text: "My waffle is the king of Normandy and the king of York."}

    assert (solve(my_stops.revision.datasources.stopwords, cache=cache) ==
            ['My', 'is', 'the', 'of', 'and', 'the', 'of'])
    assert (solve(my_stops.revision.parent.datasources.stopwords, cache=cache) ==
            ['My', 'is', 'the', 'of'])

    assert (solve(my_stops.revision.datasources.non_stopwords, cache=cache) ==
            ['waffle', 'king', 'Normandy', 'king', 'York'])
    assert (solve(my_stops.revision.parent.datasources.non_stopwords, cache=cache) ==
            ['hat', 'king', 'France'])

    assert (solve(my_stops.revision.datasources.stopword_frequency, cache=cache) ==
            {'my': 1, 'is': 1, 'the': 2, 'and': 1, 'of': 2})
    assert (solve(my_stops.revision.datasources.non_stopword_frequency,
                  cache=cache) ==
            {'waffle': 1, 'king': 2, 'normandy': 1, 'york': 1})
    assert (solve(my_stops.revision.parent.datasources.stopword_frequency,
                  cache=cache) ==
            {'my': 1, 'is': 1, 'the': 1, 'of': 1})
    assert (solve(my_stops.revision.parent.datasources.non_stopword_frequency,
                  cache=cache) ==
            {'hat': 1, 'king': 1, 'france': 1})

    diff = my_stops.revision.diff
    assert (solve(diff.datasources.stopword_delta, cache=cache) ==
            {'of': 1, 'the': 1, 'and': 1})
    pd = solve(diff.datasources.stopword_prop_delta, cache=cache)
    assert pd.keys() == {'of', 'the', 'and'}
    assert round(pd['of'], 2) == 0.50
    assert round(pd['the'], 2) == 0.50
    assert round(pd['and'], 2) == 1

    assert (solve(diff.datasources.non_stopword_delta, cache=cache) ==
            {'hat': -1, 'waffle': 1, 'king': 1, 'normandy': 1, 'york': 1,
             'france': -1})
    pd = solve(diff.datasources.non_stopword_prop_delta, cache=cache)
    assert pd.keys() == {'hat', 'waffle', 'king', 'normandy', 'york', 'france'}
    assert round(pd['hat'], 2) == -1
    assert round(pd['waffle'], 2) == 1
    assert round(pd['king'], 2) == 0.50
    assert round(pd['normandy'], 2) == 1
    assert round(pd['york'], 2) == 1

    assert solve(my_stops.revision.stopwords, cache=cache) == 7
    assert solve(my_stops.revision.parent.stopwords, cache=cache) == 4
    assert solve(my_stops.revision.non_stopwords, cache=cache) == 5
    assert solve(my_stops.revision.parent.non_stopwords, cache=cache) == 3

    assert solve(diff.stopword_delta_sum, cache=cache) == 3
    assert solve(diff.stopword_delta_increase, cache=cache) == 3
    assert solve(diff.stopword_delta_decrease, cache=cache) == 0
    assert solve(diff.non_stopword_delta_sum, cache=cache) == 2
    assert solve(diff.non_stopword_delta_increase, cache=cache) == 4
    assert solve(diff.non_stopword_delta_decrease, cache=cache) == -2

    assert round(solve(diff.stopword_prop_delta_sum, cache=cache), 2) == 2
    assert round(solve(diff.stopword_prop_delta_increase, cache=cache), 2) == 2
    assert round(solve(diff.stopword_prop_delta_decrease, cache=cache), 2) == 0
    assert round(
        solve(
            diff.non_stopword_prop_delta_sum,
            cache=cache),
        2) == 1.5
    assert (round(solve(diff.non_stopword_prop_delta_increase, cache=cache), 2) ==
            3.5)
    assert (round(solve(diff.non_stopword_prop_delta_decrease, cache=cache), 2) ==
            -2)


def test_pickling():
    assert (pickle.loads(pickle.dumps(my_stops.revision.stopwords)) ==
            my_stops.revision.stopwords)
    assert (pickle.loads(pickle.dumps(my_stops.revision.parent.stopwords)) ==
            my_stops.revision.parent.stopwords)
    assert (pickle.loads(pickle.dumps(my_stops.revision.non_stopwords)) ==
            my_stops.revision.non_stopwords)
    assert (pickle.loads(pickle.dumps(my_stops.revision.parent.non_stopwords)) ==
            my_stops.revision.parent.non_stopwords)

    diff = my_stops.revision.diff
    assert (pickle.loads(pickle.dumps(diff.stopword_delta_sum)) ==
            diff.stopword_delta_sum)
    assert (pickle.loads(pickle.dumps(diff.stopword_delta_increase)) ==
            diff.stopword_delta_increase)
    assert (pickle.loads(pickle.dumps(diff.stopword_delta_decrease)) ==
            diff.stopword_delta_decrease)
    assert (pickle.loads(pickle.dumps(diff.non_stopword_delta_sum)) ==
            diff.non_stopword_delta_sum)
    assert (pickle.loads(pickle.dumps(diff.non_stopword_delta_increase)) ==
            diff.non_stopword_delta_increase)
    assert (pickle.loads(pickle.dumps(diff.non_stopword_delta_decrease)) ==
            diff.non_stopword_delta_decrease)

    assert (pickle.loads(pickle.dumps(diff.stopword_prop_delta_sum)) ==
            diff.stopword_prop_delta_sum)
    assert (pickle.loads(pickle.dumps(diff.stopword_prop_delta_increase)) ==
            diff.stopword_prop_delta_increase)
    assert (pickle.loads(pickle.dumps(diff.stopword_prop_delta_decrease)) ==
            diff.stopword_prop_delta_decrease)
    assert (pickle.loads(pickle.dumps(diff.non_stopword_prop_delta_sum)) ==
            diff.non_stopword_prop_delta_sum)
    assert (pickle.loads(pickle.dumps(
            diff.non_stopword_prop_delta_increase
        )) ==  # noqa
        diff.non_stopword_prop_delta_increase)
    assert (pickle.loads(pickle.dumps(
            diff.non_stopword_prop_delta_decrease
        )) ==  # noqa
        diff.non_stopword_prop_delta_decrease)
