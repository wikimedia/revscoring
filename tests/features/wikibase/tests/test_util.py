
from revscoring.features.wikibase.util import diff_dicts


def test_diff_dicts():

    diff = diff_dicts(None, {'a': 1, 'b': 2})
    assert diff.added == {'a', 'b'}
    assert diff.removed == set()
    assert diff.intersection == set()
    assert diff.changed == set()
    assert diff.unchanged == set()

    diff = diff_dicts({'a': 1, 'b': 2, 'c': 3}, {'a': 1, 'b': 3, 'd': 10})
    assert diff.added == {'d'}
    assert diff.removed == {'c'}
    assert diff.intersection == {'a', 'b'}
    assert diff.changed == {'b'}
    assert diff.unchanged == {'a'}
