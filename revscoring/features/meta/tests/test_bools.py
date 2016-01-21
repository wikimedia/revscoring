import pickle
import re

from nose.tools import eq_

from .. import bools
from ....datasources import Datasource
from ....dependencies import solve

my_item = Datasource("my_item")

my_set = Datasource("my_set")

my_string = Datasource("my_string")


def test_regex_match():
    starts_with_t = bools.regex_match(r"^t", my_string)

    eq_(solve(starts_with_t, cache={my_string: "Foo"}),
        False)
    eq_(solve(starts_with_t, cache={my_string: "too"}),
        True)
    eq_(solve(starts_with_t, cache={my_string: "Too"}),
        True)

    eq_(pickle.loads(pickle.dumps(starts_with_t)), starts_with_t)

    starts_with_lower_t = bools.regex_match(re.compile(r"^t"), my_string)

    eq_(solve(starts_with_lower_t, cache={my_string: "Foo"}),
        False)
    eq_(solve(starts_with_lower_t, cache={my_string: "too"}),
        True)
    eq_(solve(starts_with_lower_t, cache={my_string: "Too"}),
        False)

    eq_(pickle.loads(pickle.dumps(starts_with_lower_t)), starts_with_lower_t)


def test_item_in_set():
    is_a_sysop = bools.item_in_set('sysop', my_set)

    eq_(solve(is_a_sysop, cache={my_set: {'foo', 'bar'}}), False)
    eq_(solve(is_a_sysop, cache={my_set: {'foo', 'sysop'}}), True)
    eq_(solve(is_a_sysop, cache={my_set: None}), False)

    eq_(pickle.loads(pickle.dumps(is_a_sysop)), is_a_sysop)


def test_set_contains_item():
    is_me = bools.set_contains_item({6877667}, my_item)

    eq_(solve(is_me, cache={my_item: 999}), False)
    eq_(solve(is_me, cache={my_item: 6877667}), True)
    eq_(solve(is_me, cache={my_item: None}), False)

    eq_(pickle.loads(pickle.dumps(is_me)), is_me)


def test_sets_intersect():
    has_small_odd = bools.sets_intersect({1, 2, 3, 5, 7, 9, 11, 13}, my_set)

    eq_(solve(has_small_odd, cache={my_set: {4, 18, 10}}), False)
    eq_(solve(has_small_odd, cache={my_set: {20, 10, 3, 5, 1}}), True)
    eq_(solve(has_small_odd, cache={my_set: None}), False)

    eq_(pickle.loads(pickle.dumps(has_small_odd)), has_small_odd)
