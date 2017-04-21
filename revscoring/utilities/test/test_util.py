from nose.tools import eq_

from .. import util


def test_parse_statistic_path_string():
    eq_(util.parse_statistic_path_string("roc_auc.micro"),
        ["roc_auc", "micro"])
