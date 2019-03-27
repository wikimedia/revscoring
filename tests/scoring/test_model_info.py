from pytest import raises

from revscoring.errors import ModelInfoLookupError
from revscoring.scoring.model_info import ModelInfo


def test_model_info():
    mi = ModelInfo(default_fields={'bar', 'foo'})
    mi['foo'] = 1
    mi['bar'] = 2
    mi['baz'] = 3
    mi[True] = 1

    assert 'bar' in mi.format([''], formatting="json")
    assert 'baz' not in mi.format([''], formatting="json")
    mi.format(['true'], formatting="json")

    assert list(mi.keys()) == ['foo', 'bar', 'baz', True]
    assert list(mi.format_json({}).keys()) == ['foo', 'bar']


def test_model_info_error():
    with raises(ModelInfoLookupError) as e:
        mi = ModelInfo()
        mi['baz'] = 3
        mi[True] = 1

        mi.format(['false'])
    assert e.value.args[0] == 'false'
