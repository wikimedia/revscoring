import pickle

from pytest import raises

from revscoring.datasources import Datasource
from revscoring.dependencies import solve
from revscoring.dependencies.util import or_none
from revscoring.extractors.api.util import _lookup_keys, key, key_exists


def test_lookup_keys():

    assert _lookup_keys("foo", {'foo': 1}) == 1
    assert _lookup_keys(["foo", "bar"], {'foo': {'bar': 1}}) == 1


def test_key():
    my_dict = Datasource("my_dict")
    foo = key('foo', my_dict)
    assert solve(foo, cache={my_dict: {'foo': "bar"}}) == 'bar'
    assert repr(foo) == "<datasource.my_dict['foo']>"

    bar = key('bar', my_dict, apply=or_none(int))
    assert solve(bar, cache={my_dict: {'bar': None}}) is None
    assert solve(bar, cache={my_dict: {'bar': "1"}}) == 1

    foobar = key(['foo', 'bar'], my_dict)
    assert solve(foobar, cache={my_dict: {'bar': 1}}) is None
    assert solve(foobar, cache={my_dict: {'foo': {'bar': 1}}}) == 1
    assert repr(foobar) == "<datasource.my_dict[['foo', 'bar']]>"

    assert pickle.loads(pickle.dumps(foo)) == foo
    assert pickle.loads(pickle.dumps(bar)) == bar
    assert pickle.loads(pickle.dumps(foobar)) == foobar


def test_missing_key():
    with raises(RuntimeError):
        my_dict = Datasource("my_dict")
        foobar = key(['foo', 'bar'], my_dict,
                     if_missing=(RuntimeError))
        assert solve(foobar, cache={my_dict: {'bar': 1}}) is None


def test_key_exists():
    my_dict = Datasource("my_dict")
    foo_exists = key_exists('foo', my_dict)
    assert solve(foo_exists, cache={my_dict: {'foo': "bar"}}) is True
    assert solve(foo_exists, cache={my_dict: {'baz': "bar"}}) is False
    assert pickle.loads(pickle.dumps(foo_exists)) == foo_exists
