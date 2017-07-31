from nose.tools import eq_

from .. import util


def test_pattern():
    eq_(util.parse_pattern("'maximum filter_rate @ recall >= 0.9'.labels.true"),  # noqa
        ["maximum filter_rate @ recall >= 0.9", "labels", "true"])
    eq_(util.parse_pattern("'maximum filter_rate @ recall >= 0.9'.'labels'.true"),  # noqa
        ["maximum filter_rate @ recall >= 0.9", "labels", "true"])
    eq_(util.parse_pattern("'foo\"bar\"'.buz"),  # noqa
        ["foo\"bar\"", "buz"])


def test_treeify():
    paths = (util.parse_pattern(p)
             for p in ['foo.bar.baz', 'foo.bar.buz', 'foo.bar', 'bum'])
    eq_(util.treeify(paths),
        {'foo': {'bar': {'baz': {}, 'buz': {}}}, 'bum': {}})


def test_dict_lookup():
    r = util.dict_lookup({'foo': {'bar': {'baz': 1}}, 'bum': {'derp': 2}},
                         {'foo': {'bar': {}}})
    eq_(r, {'foo': {'bar': {'baz': 1}}})
