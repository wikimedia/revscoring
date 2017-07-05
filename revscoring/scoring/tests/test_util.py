from nose.tools import eq_

from .. import util


def test_pattern():
    eq_(util.parse_pattern("'maximum filter_rate @ recall >= 0.9'.labels.true"),  # noqa
        ["maximum filter_rate @ recall >= 0.9", "labels", "true"])
