from nose.tools import eq_

from ..model_info import ModelInfo


def test_model_info():
    mi = ModelInfo(default_fields={'bar', 'foo'})
    mi['foo'] = 1
    mi['bar'] = 2
    mi['baz'] = 3

    assert 'foo' in mi.format([''], formatting="json")

    eq_(list(mi.keys()), ['foo', 'bar', 'baz'])
    eq_(list(mi.format_json({}).keys()), ['foo', 'bar'])
