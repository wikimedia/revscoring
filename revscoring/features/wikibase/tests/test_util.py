from nose.tools import eq_

from ..util import diff_dicts


def test_diff_dicts():

    diff = diff_dicts(None, {'a': 1, 'b': 2})
    eq_(diff.added, {'a', 'b'})
    eq_(diff.removed, set())
    eq_(diff.intersection, set())
    eq_(diff.changed, set())
    eq_(diff.unchanged, set())

    diff = diff_dicts({'a': 1, 'b': 2, 'c': 3}, {'a': 1, 'b': 3, 'd': 10})
    eq_(diff.added, {'d'})
    eq_(diff.removed, {'c'})
    eq_(diff.intersection, {'a', 'b'})
    eq_(diff.changed, {'b'})
    eq_(diff.unchanged, {'a'})
