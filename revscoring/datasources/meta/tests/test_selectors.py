import io

from nose.tools import eq_

from .. import frequencies, selectors
from ....dependencies import solve
from ...datasource import Datasource

my_tokens = Datasource("my_tokens")
my_table = frequencies.table(my_tokens)
my_tfidf_table = selectors.tfidf(my_table, max_terms=3)
my_boolean_tfidf_table = selectors.tfidf(
    my_table, boolean=True, weight=False, max_terms=3)

my_filtered_keys = selectors.filter_keys(my_table, keys={"true", "false"})


def test_tfidf():
    my_tfidf_table.fit([
        ([{"one": 1, "maybe": 1, "true": 1, "four": 1}], True),
        ([{"one": 1, "true": 1}], True),
        ([{"one": 1, "true": 1, "four": 1}], True),
        ([{"one": 1, "four": 1, "three": 1}], True),
        ([{"maybe": 1, "true": 2}], True),
        ([{"one": 1, "four": 1, "false": 1}], False),
        ([{"one": 1, "maybe": -1, "four": 1, "false": 1}], False),
        ([{"one": 1, "false": 2, "three": 1}], False),
        ([{"false": 3}], False)
    ])

    cache = {my_tokens: ["one", "maybe", "true", "four", "false"]}
    tfidf_table = solve(my_tfidf_table, cache=cache)

    eq_(set(my_tfidf_table.keys()), {'true', 'false', 'maybe'})
    eq_(set(tfidf_table.keys()), {'true', 'false', 'maybe'})
    assert tfidf_table['true'] > tfidf_table['false']
    assert tfidf_table['maybe'] > 0

    f = io.BytesIO()
    my_tfidf_table.dump(f)
    f.seek(0)
    loaded_my_tfidf_table = Datasource.load(f)
    eq_(solve(my_tfidf_table, cache=cache),
        solve(loaded_my_tfidf_table, cache=cache))

    cache = {my_table: {'maybe': -1}}
    tfidf_table = solve(my_tfidf_table, cache=cache)
    assert tfidf_table['maybe'] < 0


def test_boolean_tfidf():
    my_boolean_tfidf_table.fit([
        ([{"one": 1, "maybe": 1, "true": 1, "four": 1}], True),
        ([{"one": 1, "true": 1}], True),
        ([{"one": 1, "true": 1, "four": 1}], True),
        ([{"one": 1, "four": 1, "three": 1}], True),
        ([{"maybe": 1, "true": 2}], True),
        ([{"one": 1, "four": 1, "false": 1}], False),
        ([{"one": 1, "maybe": -1, "four": 1, "false": 1}], False),
        ([{"one": 1, "false": 2, "three": 1}], False),
        ([{"false": 3}], False)
    ])

    cache = {my_tokens: ["one", "one", "maybe", "true", "four", "false"]}
    tfidf_table = solve(my_boolean_tfidf_table, cache=cache)

    eq_(set(tfidf_table.keys()), {'true', 'false', 'maybe'})


def test_filter_keys():
    cache = {my_tokens: ["one", "maybe", "true", "four", "false"]}
    filtered_keys = solve(my_filtered_keys, cache=cache)

    eq_(set(filtered_keys.keys()), {'true', 'false'})
