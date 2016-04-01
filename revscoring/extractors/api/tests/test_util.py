import pickle

from nose.tools import eq_, raises

from ....datasources import Datasource
from ....dependencies import solve
from ..util import _lookup_keys, key, key_exists, or_none


def test_lookup_keys():

    eq_(_lookup_keys("foo", {'foo': 1}), 1)
    eq_(_lookup_keys(["foo", "bar"], {'foo': {'bar': 1}}), 1)


def test_key():
    my_dict = Datasource("my_dict")
    foo = key('foo', my_dict)
    eq_(solve(foo, cache={my_dict: {'foo': "bar"}}), 'bar')
    eq_(repr(foo), "<datasource.my_dict['foo']>")

    bar = key('bar', my_dict, apply=or_none(int))
    eq_(solve(bar, cache={my_dict: {'bar': None}}), None)
    eq_(solve(bar, cache={my_dict: {'bar': "1"}}), 1)

    foobar = key(['foo', 'bar'], my_dict)
    eq_(solve(foobar, cache={my_dict: {'bar': 1}}), None)
    eq_(solve(foobar, cache={my_dict: {'foo': {'bar': 1}}}), 1)
    eq_(repr(foobar), "<datasource.my_dict[['foo', 'bar']]>")

    eq_(pickle.loads(pickle.dumps(foo)), foo)
    eq_(pickle.loads(pickle.dumps(bar)), bar)
    eq_(pickle.loads(pickle.dumps(foobar)), foobar)


@raises(RuntimeError)
def test_missing_key():
    my_dict = Datasource("my_dict")
    foobar = key(['foo', 'bar'], my_dict,
                 if_missing=(RuntimeError))
    eq_(solve(foobar, cache={my_dict: {'bar': 1}}), None)


def test_key_exists():
    my_dict = Datasource("my_dict")
    foo_exists = key_exists('foo', my_dict)
    eq_(solve(foo_exists, cache={my_dict: {'foo': "bar"}}), True)
    eq_(solve(foo_exists, cache={my_dict: {'baz': "bar"}}), False)
    eq_(pickle.loads(pickle.dumps(foo_exists)), foo_exists)
