from nose.tools import eq_

from ..statistics import parse_pattern


def test_parse_pattern():
    eq_(parse_pattern("roc_auc.micro"),
        ["roc_auc", "micro"])
